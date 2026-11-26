-- Brihta — Šola: predmeti učiteljev, kvizi iz Excela in vadba
--
-- ZAKAJ: vsak učitelj si na strani sam naredi predmete (kvadratki), v njih module
-- in kvize, ki jih naloži iz Excelove predloge (orodja/kviz-predloga/). Predmet
-- dodeli razredom; vidijo ga samo učenci teh razredov. Razred se računa iz
-- letnika (razred_na_dan), zato isti predmet za »4A« naslednje leto vidi nova 4A
-- in učitelju kvizov ni treba delati znova.
--
-- Kvizi v predmetih učiteljev so VADBA: učenec jih rešuje, kolikokrat želi.
-- Shrani se najboljši rezultat in število poskusov; pravila 50 % ni.
-- Obstoječi kvizi (Računalništvo, Fleksi) se ne spremenijo.
--
-- Id predmeta je 'u-' + 8 znakov (npr. u-k3x9p2ma). Kvizi, moduli in razpored
-- uporabljajo ta id kot »predmet«, zato delujejo obstoječe funkcije.
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_razpored.sql.
-- Varno za ponoven zagon.

-- ── 1. Predmeti ───────────────────────────────────────────────────────────
create table if not exists sola_tpredmeti (
  id        text primary key check (id ~ '^u-[a-z0-9]{8}$'),
  ucitelj   uuid not null references teachers(id) on delete cascade,
  ime       text not null check (length(ime) between 1 and 60),
  emoji     text not null default '📚',
  barva     int  not null default 0,
  razredi   text[] not null default '{}',
  ustvarjeno timestamptz not null default now()
);
alter table sola_tpredmeti enable row level security;

-- Vadba: število poskusov pri oddaji (najboljši rezultat je v tocke/pravilni).
alter table sola_oddaje add column if not exists poskusov int not null default 1;

-- Ali je predmet od tega učitelja.
create or replace function public._sola_tp_lastnik(p_seja uuid, p_predmet text)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from sola_tpredmeti t
                  where t.id = p_predmet and t.ucitelj = public._sola_ucitelj(p_seja));
$$;
revoke execute on function public._sola_tp_lastnik(uuid, text) from public, anon, authenticated;

-- ── 2. Seznami ────────────────────────────────────────────────────────────
-- Učitelj: svoji predmeti.
create or replace function public.sola_tp_moji(p_seja uuid)
returns table(id text, ime text, emoji text, barva int, razredi text[])
language sql stable security definer set search_path = public as $$
  select t.id, t.ime, t.emoji, t.barva, t.razredi from sola_tpredmeti t
   where t.ucitelj = public._sola_ucitelj(p_seja)
   order by t.ustvarjeno;
$$;

-- Učenec: predmeti njegovega razreda (današnjega).
create or replace function public.sola_tp_ucenec(p_student uuid)
returns table(id text, ime text, emoji text, barva int, razredi text[])
language sql stable security definer set search_path = public as $$
  select t.id, t.ime, t.emoji, t.barva, t.razredi
    from sola_tpredmeti t, students s
   where s.id = p_student
     and public.razred_na_dan(s.letnik, s.oddelek, current_date) = any (t.razredi)
   order by t.ime;
$$;

-- ── 3. Dodaj, uredi, izbriši ──────────────────────────────────────────────
-- p_id NULL = nov predmet. Vrne id ali NULL (ni prijave / ni lastnik / napačni podatki).
create or replace function public.sola_tp_shrani(p_seja uuid, p_id text, p_ime text, p_emoji text,
                                                 p_barva int, p_razredi text[])
returns text
language plpgsql security definer set search_path = public as $$
declare u uuid := public._sola_ucitelj(p_seja); novi text;
begin
  if u is null then return null; end if;
  if coalesce(btrim(p_ime), '') = '' or length(p_ime) > 60 then return null; end if;
  if length(coalesce(p_emoji, '')) > 16 or coalesce(array_length(p_razredi, 1), 0) > 20 then return null; end if;
  if p_id is null then
    loop
      novi := 'u-' || substr(md5(random()::text || clock_timestamp()::text), 1, 8);
      exit when not exists (select 1 from sola_tpredmeti where id = novi);
    end loop;
    insert into sola_tpredmeti (id, ucitelj, ime, emoji, barva, razredi)
    values (novi, u, btrim(p_ime), coalesce(nullif(p_emoji, ''), '📚'), coalesce(p_barva, 0), coalesce(p_razredi, '{}'));
    return novi;
  end if;
  update sola_tpredmeti
     set ime = btrim(p_ime), emoji = coalesce(nullif(p_emoji, ''), '📚'),
         barva = coalesce(p_barva, 0), razredi = coalesce(p_razredi, '{}')
   where id = p_id and ucitelj = u;
  return case when found then p_id else null end;
end; $$;

-- Izbriše predmet z vsemi kvizi (in oddajami), moduli in vrstnim redom.
create or replace function public.sola_tp_izbrisi(p_seja uuid, p_id text)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if not public._sola_tp_lastnik(p_seja, p_id) then return false; end if;
  delete from sola_kvizi where predmet = p_id;
  delete from sola_naslovi where predmet = p_id;
  delete from sola_razpored where predmet = p_id;
  delete from sola_tpredmeti where id = p_id;
  return true;
end; $$;

-- ── 4. Kvizi: skrij / pokaži ──────────────────────────────────────────────
-- Skrite kvize svojih predmetov vidi samo učitelj (da jih lahko znova pokaže).
create or replace function public.sola_tp_skriti_kvizi(p_seja uuid)
returns table(id text, predmet text, naslov text, opis text, vprasanj int, objavljeno timestamptz)
language sql stable security definer set search_path = public as $$
  select k.id, k.predmet, k.naslov, k.opis, jsonb_array_length(k.vprasanja), k.objavljeno
    from sola_kvizi k join sola_tpredmeti t on t.id = k.predmet
   where k.skrit and t.ucitelj = public._sola_ucitelj(p_seja);
$$;

create or replace function public.sola_tp_kviz_skrit(p_seja uuid, p_id text, p_skrit boolean)
returns boolean
language plpgsql security definer set search_path = public as $$
declare pr text;
begin
  select predmet into pr from sola_kvizi where id = p_id;
  if pr is null or not public._sola_tp_lastnik(p_seja, pr) then return false; end if;
  update sola_kvizi set skrit = p_skrit where id = p_id;
  return true;
end; $$;

-- Predogled vprašanj tudi za skrit kviz (samo lastnik).
create or replace function public.sola_tp_kviz(p_seja uuid, p_id text)
returns table(id text, predmet text, naslov text, opis text, vprasanja jsonb, objavljeno timestamptz)
language sql stable security definer set search_path = public as $$
  select k.id, k.predmet, k.naslov, k.opis, k.vprasanja, k.objavljeno
    from sola_kvizi k
   where k.id = p_id and public._sola_tp_lastnik(p_seja, k.predmet);
$$;

-- ── 5. Vadba: oddaja ──────────────────────────────────────────────────────
-- Vedno oceni in vrne, kaj je bilo pravilno (brez pravilnih odgovorov).
-- Shrani najboljši rezultat in prešteje poskuse.
create or replace function public.sola_vaja_oddaj(p_student uuid, p_kviz text, p_odgovori jsonb)
returns table(tocke int, vseh int, pravilni jsonb, najboljse int, poskusov int)
language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare k record; pr jsonb; t int; v int;
begin
  if not exists (select 1 from students s where s.id = p_student) then return; end if;
  select * into k from sola_kvizi
   where sola_kvizi.id = p_kviz and not skrit and predmet like 'u-%';
  if not found then return; end if;
  if jsonb_typeof(p_odgovori) <> 'array' or length(p_odgovori::text) > 50000 then return; end if;

  pr := public._sola_oceni(k.kljuc, p_odgovori);
  v  := jsonb_array_length(k.kljuc);
  select count(*) into t from jsonb_array_elements(pr) x where x = 'true'::jsonb;

  insert into sola_oddaje as o (kviz_id, student_id, odgovori, pravilni, tocke, vseh, poskusov)
  values (p_kviz, p_student, p_odgovori, pr, t, v, 1)
  on conflict (kviz_id, student_id) do update
     set poskusov = o.poskusov + 1,
         odgovori = case when excluded.tocke >= o.tocke then excluded.odgovori else o.odgovori end,
         pravilni = case when excluded.tocke >= o.tocke then excluded.pravilni else o.pravilni end,
         oddano   = case when excluded.tocke >= o.tocke then now() else o.oddano end,
         vseh     = excluded.vseh,
         tocke    = greatest(o.tocke, excluded.tocke);

  return query select t, v, pr, o.tocke, o.poskusov from sola_oddaje o
                where o.kviz_id = p_kviz and o.student_id = p_student;
end; $$;

-- ── 6. Pravice ────────────────────────────────────────────────────────────
grant execute on function public.sola_tp_moji(uuid) to anon, authenticated;
grant execute on function public.sola_tp_ucenec(uuid) to anon, authenticated;
grant execute on function public.sola_tp_shrani(uuid, text, text, text, int, text[]) to anon, authenticated;
grant execute on function public.sola_tp_izbrisi(uuid, text) to anon, authenticated;
grant execute on function public.sola_tp_skriti_kvizi(uuid) to anon, authenticated;
grant execute on function public.sola_tp_kviz_skrit(uuid, text, boolean) to anon, authenticated;
grant execute on function public.sola_tp_kviz(uuid, text) to anon, authenticated;
grant execute on function public.sola_vaja_oddaj(uuid, text, jsonb) to anon, authenticated;
