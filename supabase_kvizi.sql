-- Brihta — Šola: spletni kvizi
--
-- Učenci se prijavijo z ISTIM računom kot v Brihta-MAT (tabela students),
-- zato ta datoteka doda samo kvize in oddaje. Nič obstoječega se ne spremeni.
--
-- ZAKAJ SE KVIZI OCENJUJEJO TUKAJ: repozitorij sola je javen, stran tudi.
-- Če bi bili pravilni odgovori v brskalniku, bi jih lahko vsak prebral.
-- Zato:
--   vprasanja  — javno: besedila vprašanj in ponudenih odgovorov (premešanih)
--   kljuc      — skrito: pravilni odgovori; bere ga samo sola_kviz_oddaj
-- Kvize pošlje v bazo skripta scripts/kvizi.py z učiteljevega računalnika.
-- Za to potrebuje skrivnost iz app_config (korak 6 spodaj).
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat).

-- ── 1. Kvizi ──────────────────────────────────────────────────────────────
create table if not exists sola_kvizi (
  id           text primary key,            -- 'racunalnistvo-5/scratch-ponovitev'
  predmet      text not null,               -- ime mape, npr. 'racunalnistvo-5'
  naslov       text not null,
  opis         text,
  vprasanja    jsonb not null,               -- javno, brez odgovorov
  kljuc        jsonb not null,               -- pravilni odgovori
  skrit        boolean not null default false,
  objavljeno   timestamptz not null default now(),
  posodobljeno timestamptz not null default now()
);
-- RLS brez politik = z javnim ključem ni neposrednega dostopa.
alter table sola_kvizi enable row level security;

-- ── 2. Oddaje ─────────────────────────────────────────────────────────────
-- En poskus na kviz (unique). Učitelj lahko poskus izbriše in učenec reši znova.
create table if not exists sola_oddaje (
  kviz_id    text not null references sola_kvizi(id) on delete cascade,
  student_id uuid not null references students(id) on delete cascade,
  odgovori   jsonb not null,
  pravilni   jsonb not null,                -- [true,false,...] po vprašanjih
  tocke      int  not null,
  vseh       int  not null,
  oddano     timestamptz not null default now(),
  primary key (kviz_id, student_id)
);
alter table sola_oddaje enable row level security;
create index if not exists sola_oddaje_student on sola_oddaje (student_id);

-- ── 3. Ocenjevanje ────────────────────────────────────────────────────────
-- Primerjava kratkih odgovorov: brez razlike med velikimi in malimi črkami,
-- odvečnimi presledki, piko na koncu ter decimalno vejico in piko.
create or replace function public._sola_norm(t text)
returns text language sql immutable as $$
  select regexp_replace(
           replace(lower(regexp_replace(btrim(coalesce(t, '')), '\s+', ' ', 'g')), ',', '.'),
           '[.!?]+$', '');
$$;

-- kljuc:    [{"t":"izbira","p":["5"]}, {"t":"vec","p":["pes","mačka"]},
--            {"t":"kratek","p":["Ljubljana"]}, {"t":"povezi","p":[["Francija","Pariz"]]},
--            {"t":"vrstni","p":["miška","mačka","slon"]}]
-- odgovori: ["5", ["mačka","pes"], "ljubljana", {"Francija":"Pariz"}, ["miška","mačka","slon"]]
-- Vrne [true,false,...]. Funkcija ne bere nobene tabele, zato je lahko javna.
create or replace function public._sola_oceni(p_kljuc jsonb, p_odgovori jsonb)
returns jsonb language plpgsql immutable as $$
declare
  k jsonb; a jsonb; ok boolean; i int := 0; izid jsonb := '[]'::jsonb;
begin
  for k in select value from jsonb_array_elements(p_kljuc) loop
    a := p_odgovori -> i;
    ok := false;
    if a is not null and jsonb_typeof(a) <> 'null' then
      case k->>'t'
        when 'izbira' then
          ok := jsonb_typeof(a) = 'string' and a #>> '{}' = k->'p'->>0;
        when 'vec' then
          ok := jsonb_typeof(a) = 'array'
            and (select coalesce(array_agg(distinct x order by x), '{}') from jsonb_array_elements_text(a) x)
              = (select coalesce(array_agg(distinct x order by x), '{}') from jsonb_array_elements_text(k->'p') x);
        when 'kratek' then
          ok := jsonb_typeof(a) = 'string'
            and public._sola_norm(a #>> '{}') <> ''
            and exists (select 1 from jsonb_array_elements_text(k->'p') x
                         where public._sola_norm(x) = public._sola_norm(a #>> '{}'));
        when 'povezi' then
          ok := jsonb_typeof(a) = 'object'
            and not exists (select 1 from jsonb_array_elements(k->'p') e
                             where coalesce(a->>(e->>0), '') <> e->>1);
        when 'vrstni' then
          ok := jsonb_typeof(a) = 'array' and a = k->'p';
        else ok := false;
      end case;
    end if;
    izid := izid || to_jsonb(ok);
    i := i + 1;
  end loop;
  return izid;
end; $$;

-- ── 4. Za učence ──────────────────────────────────────────────────────────
-- Seznam objavljenih kvizov (brez vprašanj — ta se naložijo ob odprtju).
create or replace function public.sola_kvizi_seznam()
returns table(id text, predmet text, naslov text, opis text, vprasanj int, objavljeno timestamptz)
language sql stable security definer set search_path = public as $$
  select k.id, k.predmet, k.naslov, k.opis, jsonb_array_length(k.vprasanja), k.objavljeno
    from sola_kvizi k where not k.skrit
   order by k.objavljeno desc;
$$;

create or replace function public.sola_kviz(p_id text)
returns table(id text, predmet text, naslov text, opis text, vprasanja jsonb, objavljeno timestamptz)
language sql stable security definer set search_path = public as $$
  select k.id, k.predmet, k.naslov, k.opis, k.vprasanja, k.objavljeno
    from sola_kvizi k where k.id = p_id and not k.skrit;
$$;

-- Oddaja. Če je učenec kviz že oddal, se nič ne spremeni in vrne prejšnji rezultat.
create or replace function public.sola_kviz_oddaj(p_student uuid, p_kviz text, p_odgovori jsonb)
returns table(tocke int, vseh int, novo boolean)
language plpgsql security definer set search_path = public as $$
declare k record; pr jsonb; t int; v int;
begin
  if not exists (select 1 from students s where s.id = p_student) then return; end if;
  select * into k from sola_kvizi where sola_kvizi.id = p_kviz and not skrit;
  if not found then return; end if;
  if jsonb_typeof(p_odgovori) <> 'array' or length(p_odgovori::text) > 50000 then return; end if;

  return query select o.tocke, o.vseh, false from sola_oddaje o
                where o.kviz_id = p_kviz and o.student_id = p_student;
  if found then return; end if;

  pr := public._sola_oceni(k.kljuc, p_odgovori);
  v  := jsonb_array_length(k.kljuc);
  select count(*) into t from jsonb_array_elements(pr) x where x = 'true'::jsonb;

  insert into sola_oddaje (kviz_id, student_id, odgovori, pravilni, tocke, vseh)
  values (p_kviz, p_student, p_odgovori, pr, t, v)
  on conflict do nothing;
  return query select t, v, true;
end; $$;

-- Kateri kvizi so že oddani (za oznake »Oddano 7/10« na strani).
create or replace function public.sola_kviz_moje(p_student uuid)
returns table(kviz_id text, tocke int, vseh int, oddano timestamptz)
language sql stable security definer set search_path = public as $$
  select o.kviz_id, o.tocke, o.vseh, o.oddano from sola_oddaje o where o.student_id = p_student;
$$;

-- ── 5. Za učitelje ────────────────────────────────────────────────────────
-- Enak vzorec kot v Brihta-MAT: odobren učiteljski račun (teachers.approved).
create or replace function public.sola_kviz_rezultati(p_teacher_id uuid, p_kviz text)
returns table(student_id uuid, username text, ime text, emoji text, razred text,
              tocke int, vseh int, pravilni jsonb, oddano timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not exists (select 1 from teachers t where t.id = p_teacher_id and t.approved) then return; end if;
  return query
    select s.id, s.username, coalesce(nullif(s.display_name, ''), s.username), s.emoji,
           public.razred_na_dan(s.letnik, s.oddelek, current_date),
           o.tocke, o.vseh, o.pravilni, o.oddano
      from sola_oddaje o join students s on s.id = o.student_id
     where o.kviz_id = p_kviz
     order by o.oddano;
end; $$;

-- Izbriše oddajo, da lahko učenec kviz reši znova.
create or replace function public.sola_kviz_ponastavi(p_teacher_id uuid, p_kviz text, p_student uuid)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from teachers t where t.id = p_teacher_id and t.approved) then return false; end if;
  delete from sola_oddaje where kviz_id = p_kviz and student_id = p_student;
  return found;
end; $$;

-- ── 6. Objava kvizov (skripta scripts/kvizi.py) ───────────────────────────
-- Skrivnost je v app_config. Nastavi jo z datoteko kvizi/NASTAVI_SKRIVNOST.sql,
-- ki jo je ustvarila skripta na tvojem računalniku (ni na GitHubu).
create table if not exists app_config (key text primary key, value text not null);
alter table app_config enable row level security;

-- p_kvizi: [{"id","predmet","naslov","opis","vprasanja","kljuc"}, ...] — VSI kvizi.
-- Kvizi, ki jih ni več v seznamu, se skrijejo (oddaje ostanejo).
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
    insert into sola_kvizi (id, predmet, naslov, opis, vprasanja, kljuc, skrit)
    values (e->>'id', e->>'predmet', e->>'naslov', nullif(e->>'opis', ''), e->'vprasanja', e->'kljuc', false)
    on conflict (id) do update
       set predmet = excluded.predmet, naslov = excluded.naslov, opis = excluded.opis,
           vprasanja = excluded.vprasanja, kljuc = excluded.kljuc, skrit = false,
           posodobljeno = case when sola_kvizi.vprasanja is distinct from excluded.vprasanja
                                 or sola_kvizi.kljuc is distinct from excluded.kljuc
                               then now() else sola_kvizi.posodobljeno end;
    n := n + 1;
  end loop;

  update sola_kvizi set skrit = true
   where not skrit
     and id not in (select value->>'id' from jsonb_array_elements(p_kvizi));
  return n;
end; $$;

-- ── 7. Dostop ─────────────────────────────────────────────────────────────
grant execute on function public._sola_oceni(jsonb, jsonb) to anon;
grant execute on function public.sola_kvizi_seznam() to anon;
grant execute on function public.sola_kviz(text) to anon;
grant execute on function public.sola_kviz_oddaj(uuid, text, jsonb) to anon;
grant execute on function public.sola_kviz_moje(uuid) to anon;
grant execute on function public.sola_kviz_rezultati(uuid, text) to anon;
grant execute on function public.sola_kviz_ponastavi(uuid, text, uuid) to anon;
grant execute on function public.sola_kviz_objavi(text, jsonb) to anon;

-- Opomba: merge_students in delete_student (Brihta-MAT) oddaj ne prenašata.
-- Ob izbrisu učenca se njegove oddaje izbrišejo (on delete cascade).
