-- Brihta — Šola: igra v živo (kviz na velikem zaslonu, učenci odgovarjajo na napravah)
--
-- ZAKAJ: učitelj pri kvizu v svojem predmetu klikne »Igraj v živo«. Na velikem
-- zaslonu so vprašanje, čas in lestvica; učenci njegovih razredov (prijavljeni)
-- dobijo na Brihti vabilo in odgovarjajo na tablicah. PIN ni potreben: igro vidijo
-- samo učenci razredov, ki jim je predmet dodeljen.
--
-- Točke: pravilen odgovor 500 do 1000 (hitreje = več), napačen 0. Ocenjuje strežnik
-- (_sola_oceni), pravilni odgovori gredo samo učitelju in šele po koncu vprašanja.
-- Igra se ne šteje v vadbo (sola_oddaje); rezultati ostanejo v sola_igra_*.
--
-- Stran vsako sekundo ali dve vpraša za stanje (brez Realtime).
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_predmeti_uciteljev.sql.
-- Varno za ponoven zagon.

-- ── 1. Tabele ─────────────────────────────────────────────────────────────
create table if not exists sola_igre (
  id         uuid primary key default gen_random_uuid(),
  kviz_id    text not null references sola_kvizi(id) on delete cascade,
  ucitelj    uuid not null references teachers(id) on delete cascade,
  razredi    text[] not null,
  stanje     text not null default 'cakanje' check (stanje in ('cakanje', 'vprasanje', 'rezultat', 'konec')),
  vprasanje  int  not null default -1,
  zacetek    timestamptz,                 -- začetek trenutnega vprašanja
  cas        int  not null default 20 check (cas between 5 and 120),
  ustvarjeno timestamptz not null default now(),
  posodobljeno timestamptz not null default now()
);
alter table sola_igre enable row level security;

create table if not exists sola_igra_igralci (
  igra_id    uuid not null references sola_igre(id) on delete cascade,
  student_id uuid not null references students(id) on delete cascade,
  tocke      int  not null default 0,
  pridruzen  timestamptz not null default now(),
  primary key (igra_id, student_id)
);
alter table sola_igra_igralci enable row level security;

create table if not exists sola_igra_odgovori (
  igra_id    uuid not null references sola_igre(id) on delete cascade,
  student_id uuid not null references students(id) on delete cascade,
  vprasanje  int  not null,
  odgovor    jsonb,
  pravilno   boolean not null,
  tocke      int  not null,
  oddano     timestamptz not null default now(),
  primary key (igra_id, student_id, vprasanje)
);
alter table sola_igra_odgovori enable row level security;

-- ── 2. Pomožne ────────────────────────────────────────────────────────────
-- Igra tega učitelja (vrne vrstico ali nič).
create or replace function public._sola_igra_moja(p_seja uuid, p_igra uuid)
returns sola_igre language sql stable security definer set search_path = public as $$
  select g.* from sola_igre g where g.id = p_igra and g.ucitelj = public._sola_ucitelj(p_seja);
$$;
revoke execute on function public._sola_igra_moja(uuid, uuid) from public, anon, authenticated;

-- Lestvica igre: [{id, ime, emoji, tocke, mesto}]
create or replace function public._sola_igra_lestvica(p_igra uuid)
returns jsonb language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(x order by x.tocke desc, x.ime), '[]'::jsonb) from (
    select s.id, coalesce(nullif(s.display_name, ''), s.username) as ime, s.emoji, i.tocke,
           rank() over (order by i.tocke desc) as mesto
      from sola_igra_igralci i join students s on s.id = i.student_id
     where i.igra_id = p_igra) x;
$$;
revoke execute on function public._sola_igra_lestvica(uuid) from public, anon, authenticated;

-- ── 3. Učitelj ────────────────────────────────────────────────────────────
-- Začne novo igro (prejšnje igre tega učitelja konča). Vrne id igre ali NULL.
create or replace function public.sola_igra_zacni(p_seja uuid, p_kviz text, p_cas int)
returns uuid
language plpgsql security definer set search_path = public as $$
declare u uuid := public._sola_ucitelj(p_seja); k record; r text[]; novi uuid;
begin
  if u is null then return null; end if;
  select * into k from sola_kvizi where id = p_kviz;
  if not found or not public._sola_tp_lastnik(p_seja, k.predmet) then return null; end if;
  select razredi into r from sola_tpredmeti where id = k.predmet;
  update sola_igre set stanje = 'konec', posodobljeno = now() where ucitelj = u and stanje <> 'konec';
  insert into sola_igre (kviz_id, ucitelj, razredi, cas)
  values (p_kviz, u, coalesce(r, '{}'), least(greatest(coalesce(p_cas, 20), 5), 120))
  returning id into novi;
  return novi;
end; $$;

-- Stanje za veliki zaslon.
create or replace function public.sola_igra_stanje_ucitelj(p_seja uuid, p_igra uuid)
returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare g sola_igre; k record; vseh int; odg int; izid jsonb;
begin
  g := public._sola_igra_moja(p_seja, p_igra);
  if g.id is null then return null; end if;
  select naslov, vprasanja, kljuc into k from sola_kvizi where id = g.kviz_id;
  vseh := jsonb_array_length(k.vprasanja);
  select count(*) into odg from sola_igra_odgovori where igra_id = g.id and vprasanje = g.vprasanje;
  izid := jsonb_build_object(
    'stanje', g.stanje, 'vprasanje', g.vprasanje, 'vseh', vseh, 'cas', g.cas, 'naslov', k.naslov,
    'kviz_id', g.kviz_id, 'razredi', to_jsonb(g.razredi),
    'preostalo_ms', case when g.stanje = 'vprasanje'
                         then greatest(0, (extract(epoch from (g.zacetek + make_interval(secs => g.cas) - now())) * 1000)::int) end,
    'odgovorov', odg,
    'igralci', public._sola_igra_lestvica(g.id));
  if g.vprasanje >= 0 and g.vprasanje < vseh then
    izid := izid || jsonb_build_object('q', k.vprasanja -> g.vprasanje);
  end if;
  if g.stanje = 'rezultat' and g.vprasanje >= 0 then
    izid := izid || jsonb_build_object(
      'kljuc', k.kljuc -> g.vprasanje,
      'pravilnih', (select count(*) from sola_igra_odgovori where igra_id = g.id and vprasanje = g.vprasanje and pravilno),
      'odgovori', (select coalesce(jsonb_agg(o.odgovor), '[]'::jsonb) from sola_igra_odgovori o
                    where o.igra_id = g.id and o.vprasanje = g.vprasanje));
  end if;
  return izid;
end; $$;

-- Naprej: čakanje → 1. vprašanje → rezultat → naslednje vprašanje … → konec.
create or replace function public.sola_igra_naprej(p_seja uuid, p_igra uuid, p_od int)
returns boolean
language plpgsql security definer set search_path = public as $$
declare g sola_igre; vseh int;
begin
  g := public._sola_igra_moja(p_seja, p_igra);
  if g.id is null or g.stanje = 'konec' then return false; end if;
  -- p_od = vprašanje, ki ga vidi zaslon; prepreči dvojni korak (dva klika, samodejni konec časa).
  if p_od is distinct from g.vprasanje then return false; end if;
  select jsonb_array_length(vprasanja) into vseh from sola_kvizi where id = g.kviz_id;
  if g.stanje = 'vprasanje' then
    update sola_igre set stanje = 'rezultat', posodobljeno = now() where id = g.id;
  elsif g.vprasanje + 1 >= vseh then
    update sola_igre set stanje = 'konec', posodobljeno = now() where id = g.id;
  else
    update sola_igre set stanje = 'vprasanje', vprasanje = g.vprasanje + 1, zacetek = now(), posodobljeno = now()
     where id = g.id;
  end if;
  return true;
end; $$;

create or replace function public.sola_igra_koncaj(p_seja uuid, p_igra uuid)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  update sola_igre set stanje = 'konec', posodobljeno = now()
   where id = p_igra and ucitelj = public._sola_ucitelj(p_seja) and stanje <> 'konec';
  return found;
end; $$;

-- ── 4. Učenec ─────────────────────────────────────────────────────────────
-- Igra v živo za razred tega učenca (začeta v zadnjih 3 urah, še ne končana).
create or replace function public.sola_igra_zame(p_student uuid)
returns table(id uuid, naslov text, stanje text, pridruzen boolean)
language sql stable security definer set search_path = public as $$
  select g.id, k.naslov, g.stanje,
         exists (select 1 from sola_igra_igralci i where i.igra_id = g.id and i.student_id = p_student)
    from sola_igre g join sola_kvizi k on k.id = g.kviz_id, students s
   where s.id = p_student and g.stanje <> 'konec' and g.ustvarjeno > now() - interval '3 hours'
     and public.razred_na_dan(s.letnik, s.oddelek, current_date) = any (g.razredi)
   order by g.ustvarjeno desc limit 1;
$$;

create or replace function public.sola_igra_pridruzi(p_student uuid, p_igra uuid)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from sola_igre g, students s
                  where g.id = p_igra and s.id = p_student and g.stanje <> 'konec'
                    and public.razred_na_dan(s.letnik, s.oddelek, current_date) = any (g.razredi)) then
    return false;
  end if;
  insert into sola_igra_igralci (igra_id, student_id) values (p_igra, p_student) on conflict do nothing;
  return true;
end; $$;

-- Stanje za učenčevo napravo (brez pravilnih odgovorov).
create or replace function public.sola_igra_stanje_ucenec(p_student uuid, p_igra uuid)
returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare g sola_igre; k record; jaz record; moj record; lest jsonb; izid jsonb;
begin
  select * into g from sola_igre where id = p_igra;
  if not found then return null; end if;
  select * into jaz from sola_igra_igralci where igra_id = g.id and student_id = p_student;
  if not found then return jsonb_build_object('stanje', g.stanje, 'igralec', false); end if;
  select naslov, vprasanja into k from sola_kvizi where id = g.kviz_id;
  select * into moj from sola_igra_odgovori where igra_id = g.id and student_id = p_student and vprasanje = g.vprasanje;
  lest := public._sola_igra_lestvica(g.id);
  izid := jsonb_build_object(
    'stanje', g.stanje, 'igralec', true, 'naslov', k.naslov, 'vprasanje', g.vprasanje, 'kviz_id', g.kviz_id,
    'vseh', jsonb_array_length(k.vprasanja), 'cas', g.cas,
    -- med vprašanjem točke brez tega odgovora (da učenec ne ve, ali je bil pravilen, preden je rezultat)
    'tocke', jaz.tocke - case when g.stanje = 'vprasanje' then coalesce(moj.tocke, 0) else 0 end,
    'igralcev', jsonb_array_length(lest),
    'mesto', (select (x->>'mesto')::int from jsonb_array_elements(lest) x where x->>'id' = p_student::text),
    'odgovoril', moj.student_id is not null);
  if g.stanje = 'vprasanje' then
    izid := izid || jsonb_build_object('q', k.vprasanja -> g.vprasanje,
      'preostalo_ms', greatest(0, (extract(epoch from (g.zacetek + make_interval(secs => g.cas) - now())) * 1000)::int));
  elsif g.stanje = 'rezultat' then
    izid := izid || jsonb_build_object('pravilno', coalesce(moj.pravilno, false), 'dobil', coalesce(moj.tocke, 0));
  end if;
  return izid;
end; $$;

-- Odgovor na trenutno vprašanje (en odgovor na vprašanje). Vrne true, če je sprejet.
create or replace function public.sola_igra_odgovori(p_student uuid, p_igra uuid, p_vprasanje int, p_odgovor jsonb)
returns boolean
language plpgsql security definer set search_path = public as $$
declare g sola_igre; kl jsonb; ok boolean; t int; pretece numeric;
begin
  select * into g from sola_igre where id = p_igra;
  if not found or g.stanje <> 'vprasanje' or g.vprasanje <> p_vprasanje then return false; end if;
  if not exists (select 1 from sola_igra_igralci where igra_id = g.id and student_id = p_student) then return false; end if;
  pretece := extract(epoch from (now() - g.zacetek));
  if pretece > g.cas + 1.5 then return false; end if;          -- 1,5 s za zamudo omrežja
  if length(coalesce(p_odgovor::text, '')) > 5000 then return false; end if;
  select kljuc -> g.vprasanje into kl from sola_kvizi where id = g.kviz_id;
  ok := coalesce((public._sola_oceni(jsonb_build_array(kl), jsonb_build_array(p_odgovor)) ->> 0)::boolean, false);
  t := case when ok then 500 + round(500 * greatest(0, 1 - pretece / g.cas))::int else 0 end;
  insert into sola_igra_odgovori (igra_id, student_id, vprasanje, odgovor, pravilno, tocke)
  values (g.id, p_student, g.vprasanje, p_odgovor, ok, t)
  on conflict do nothing;
  if not found then return false; end if;
  update sola_igra_igralci set tocke = tocke + t where igra_id = g.id and student_id = p_student;
  return true;
end; $$;

-- ── 5. Pravice ────────────────────────────────────────────────────────────
grant execute on function public.sola_igra_zacni(uuid, text, int) to anon, authenticated;
grant execute on function public.sola_igra_stanje_ucitelj(uuid, uuid) to anon, authenticated;
grant execute on function public.sola_igra_naprej(uuid, uuid, int) to anon, authenticated;
grant execute on function public.sola_igra_koncaj(uuid, uuid) to anon, authenticated;
grant execute on function public.sola_igra_zame(uuid) to anon, authenticated;
grant execute on function public.sola_igra_pridruzi(uuid, uuid) to anon, authenticated;
grant execute on function public.sola_igra_stanje_ucenec(uuid, uuid) to anon, authenticated;
grant execute on function public.sola_igra_odgovori(uuid, uuid, int, jsonb) to anon, authenticated;
