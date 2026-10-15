-- Brihta — Šola: kvizi, objavljeni kar na strani (»Nov kviz«), in varna
-- učiteljska prijava. Zaženi PO supabase_kvizi.sql.
--
-- ZAKAJ SEJE: doslej je bila učiteljeva »prijava« na strani samo njegov ID
-- v brskalniku. Kdor bi ga dobil (npr. s pozabljeno prijavo na računalniku v
-- učilnici), bi za vedno lahko bral rezultate. Zdaj prijava ustvari sejo, ki
-- po 12 urah poteče in jo odjava izbriše. Ker lahko seja zdaj tudi objavlja
-- in briše kvize, je to nujno.
--
-- Brihta-MAT se ne spremeni (njegove funkcije ostanejo, kot so).
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat).

-- ── 1. Seje ───────────────────────────────────────────────────────────────
create table if not exists sola_seje (
  token      uuid primary key default gen_random_uuid(),
  teacher_id uuid not null references teachers(id) on delete cascade,
  potece     timestamptz not null default now() + interval '12 hours'
);
alter table sola_seje enable row level security;

-- Prijava: enako preverjanje gesla kot login_teacher_email v Brihta-MAT.
create or replace function public.sola_ucitelj_prijava(p_email text, p_password text)
returns table(seja uuid, username text, potece timestamptz, napaka text)
language plpgsql security definer set search_path = public, extensions as $$
declare r record; s record;
begin
  delete from sola_seje where sola_seje.potece < now();
  select t.id, t.username, t.approved, t.must_change_password, t.pin_hash into r
    from teachers t where lower(t.email) = lower(trim(coalesce(p_email, '')));
  if not found or r.pin_hash is null or r.pin_hash <> crypt(coalesce(p_password, ''), r.pin_hash) then
    return query select null::uuid, null::text, null::timestamptz, 'NAPACNO'; return;
  end if;
  if not r.approved then return query select null::uuid, null::text, null::timestamptz, 'NEPOTRJEN'; return; end if;
  if r.must_change_password then return query select null::uuid, null::text, null::timestamptz, 'ZAMENJAJ_GESLO'; return; end if;
  insert into sola_seje (teacher_id) values (r.id) returning sola_seje.token, sola_seje.potece into s;
  return query select s.token, r.username, s.potece, null::text;
end; $$;

create or replace function public.sola_ucitelj_odjava(p_seja uuid)
returns void language sql security definer set search_path = public as $$
  delete from sola_seje where token = p_seja;
$$;

-- Vrne učitelja veljavne seje ali NULL.
create or replace function public._sola_ucitelj(p_seja uuid)
returns uuid language sql stable security definer set search_path = public as $$
  select s.teacher_id from sola_seje s join teachers t on t.id = s.teacher_id
   where s.token = p_seja and s.potece > now() and t.approved;
$$;
revoke execute on function public._sola_ucitelj(uuid) from public, anon;

create or replace function public.sola_ucitelj_preveri(p_seja uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select public._sola_ucitelj(p_seja) is not null;
$$;

-- ── 2. Kvizi: vir in izvor ────────────────────────────────────────────────
-- vir   = besedilo kviza (s pravilnimi odgovori), da ga lahko učitelj uredi
-- izvor = 'splet' (Nov kviz na strani) ali 'datoteka' (scripts/kvizi.py)
alter table sola_kvizi add column if not exists vir text;
alter table sola_kvizi add column if not exists izvor text not null default 'datoteka';

-- Skripta odslej skrije samo SVOJE kvize, ki jih ni več v mapi — kvizov,
-- objavljenih na strani, se ne dotika.
create or replace function public.sola_kviz_objavi(p_skrivnost text, p_kvizi jsonb)
returns int
language plpgsql security definer set search_path = public as $$
declare s text; e jsonb; n int := 0;
begin
  select value into s from app_config where key = 'sola_kviz_skrivnost';
  if s is null or length(s) < 20 or p_skrivnost is distinct from s then
    raise exception 'NAPACNA_SKRIVNOST';
  end if;
  for e in select value from jsonb_array_elements(p_kvizi) loop
    insert into sola_kvizi (id, predmet, naslov, opis, vprasanja, kljuc, skrit, izvor)
    values (e->>'id', e->>'predmet', e->>'naslov', nullif(e->>'opis', ''), e->'vprasanja', e->'kljuc', false, 'datoteka')
    on conflict (id) do update
       set predmet = excluded.predmet, naslov = excluded.naslov, opis = excluded.opis,
           vprasanja = excluded.vprasanja, kljuc = excluded.kljuc, skrit = false, izvor = 'datoteka',
           posodobljeno = case when sola_kvizi.vprasanja is distinct from excluded.vprasanja
                                 or sola_kvizi.kljuc is distinct from excluded.kljuc
                               then now() else sola_kvizi.posodobljeno end;
    n := n + 1;
  end loop;
  update sola_kvizi set skrit = true
   where not skrit and izvor = 'datoteka'
     and id not in (select value->>'id' from jsonb_array_elements(p_kvizi));
  return n;
end; $$;

-- ── 3. Objava s strani ────────────────────────────────────────────────────
-- p_kviz: {"id","predmet","naslov","opis","vprasanja","kljuc"}; p_vir = besedilo.
-- Vrne 'NOV' ali 'POSODOBLJEN' (ali NULL, če seja ni veljavna).
create or replace function public.sola_kviz_shrani(p_seja uuid, p_kviz jsonb, p_vir text)
returns text
language plpgsql security definer set search_path = public as $$
declare obstaja boolean;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if coalesce(p_kviz->>'id', '') !~ '^[a-z0-9-]+/[a-z0-9-]+$'
     or jsonb_typeof(p_kviz->'vprasanja') <> 'array' or jsonb_typeof(p_kviz->'kljuc') <> 'array'
     or jsonb_array_length(p_kviz->'vprasanja') <> jsonb_array_length(p_kviz->'kljuc')
     or jsonb_array_length(p_kviz->'kljuc') = 0 or length(p_kviz::text) > 100000 then
    return 'NAPACEN_KVIZ';
  end if;
  select exists (select 1 from sola_kvizi where id = p_kviz->>'id') into obstaja;
  insert into sola_kvizi (id, predmet, naslov, opis, vprasanja, kljuc, skrit, izvor, vir)
  values (p_kviz->>'id', p_kviz->>'predmet', p_kviz->>'naslov', nullif(p_kviz->>'opis', ''),
          p_kviz->'vprasanja', p_kviz->'kljuc', false, 'splet', p_vir)
  on conflict (id) do update
     set predmet = excluded.predmet, naslov = excluded.naslov, opis = excluded.opis,
         vprasanja = excluded.vprasanja, kljuc = excluded.kljuc, skrit = false,
         izvor = 'splet', vir = excluded.vir, posodobljeno = now();
  return case when obstaja then 'POSODOBLJEN' else 'NOV' end;
end; $$;

create or replace function public.sola_kviz_skrij(p_seja uuid, p_id text)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  update sola_kvizi set skrit = true where id = p_id;
  return found;
end; $$;

-- Besedilo kviza za urejanje (vsebuje odgovore, zato samo za učitelja).
create or replace function public.sola_kviz_vir(p_seja uuid, p_id text)
returns table(id text, predmet text, naslov text, vir text, izvor text)
language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return; end if;
  return query select k.id, k.predmet, k.naslov, k.vir, k.izvor from sola_kvizi k where k.id = p_id;
end; $$;

-- ── 4. Rezultati in ponastavitev: odslej s sejo ───────────────────────────
drop function if exists public.sola_kviz_rezultati(uuid, text);
drop function if exists public.sola_kviz_ponastavi(uuid, text, uuid);

create or replace function public.sola_kviz_rezultati(p_seja uuid, p_kviz text)
returns table(student_id uuid, username text, ime text, emoji text, razred text,
              tocke int, vseh int, pravilni jsonb, oddano timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return; end if;
  return query
    select s.id, s.username, coalesce(nullif(s.display_name, ''), s.username), s.emoji,
           public.razred_na_dan(s.letnik, s.oddelek, current_date),
           o.tocke, o.vseh, o.pravilni, o.oddano
      from sola_oddaje o join students s on s.id = o.student_id
     where o.kviz_id = p_kviz
     order by o.oddano;
end; $$;

create or replace function public.sola_kviz_ponastavi(p_seja uuid, p_kviz text, p_student uuid)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  delete from sola_oddaje where kviz_id = p_kviz and student_id = p_student;
  return found;
end; $$;

-- ── 5. Dostop ─────────────────────────────────────────────────────────────
grant execute on function public.sola_ucitelj_prijava(text, text) to anon;
grant execute on function public.sola_ucitelj_odjava(uuid) to anon;
grant execute on function public.sola_ucitelj_preveri(uuid) to anon;
grant execute on function public.sola_kviz_objavi(text, jsonb) to anon;
grant execute on function public.sola_kviz_shrani(uuid, jsonb, text) to anon;
grant execute on function public.sola_kviz_skrij(uuid, text) to anon;
grant execute on function public.sola_kviz_vir(uuid, text) to anon;
grant execute on function public.sola_kviz_rezultati(uuid, text) to anon;
grant execute on function public.sola_kviz_ponastavi(uuid, text, uuid) to anon;
