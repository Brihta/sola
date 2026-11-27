-- Brihta — Šola: razredi pri posameznem kvizu in modulu v predmetu učitelja
--
-- ZAKAJ: učitelj ima en predmet (npr. »Kvizko«), v njem pa kvize in module za različne
-- razrede. Pri kvizu ali modulu izbere razrede, ki ga vidijo. Kdo vidi kviz:
--   1. razredi kviza, če so izbrani;
--   2. sicer razredi modula, v katerem je kviz (če so izbrani);
--   3. sicer razredi predmeta (kot doslej).
-- Učenec vidi predmet, če je njegov razred med razredi predmeta ALI pri katerem koli
-- vidnem kvizu ali modulu v njem.
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_predmeti_uciteljev.sql,
-- supabase_razpored.sql in supabase_igra_v_zivo.sql. Varno za ponoven zagon.

-- ── 1. Stolpca ────────────────────────────────────────────────────────────
alter table sola_kvizi   add column if not exists razredi text[] not null default '{}';
alter table sola_naslovi add column if not exists razredi text[] not null default '{}';

-- ── 2. Učinkoviti razredi kviza (kviz → modul → predmet) ──────────────────
create or replace function public._sola_kviz_razredi(p_kviz text)
returns text[] language sql stable security definer set search_path = public as $$
  select coalesce(
    (select k.razredi from sola_kvizi k where k.id = p_kviz and cardinality(k.razredi) > 0),
    (select n.razredi
       from sola_kvizi k
       join sola_razpored r on r.predmet = k.predmet
       cross join lateral jsonb_array_elements(r.red) e
       join sola_naslovi n on n.id::text = e->>'m'
      where k.id = p_kviz and jsonb_typeof(e) = 'object'
        and (e->'v') ? ('kviz:' || k.id) and cardinality(n.razredi) > 0
      limit 1),
    (select t.razredi from sola_kvizi k join sola_tpredmeti t on t.id = k.predmet where k.id = p_kviz),
    '{}');
$$;
revoke execute on function public._sola_kviz_razredi(text) from public, anon, authenticated;

-- ── 3. Branje (javno; razredi niso skrivnost) ─────────────────────────────
-- Kvizi v predmetih učiteljev, ki imajo izbrane svoje razrede.
create or replace function public.sola_tp_kvizi_razredi()
returns table(id text, razredi text[])
language sql stable security definer set search_path = public as $$
  select k.id, k.razredi from sola_kvizi k where k.predmet like 'u-%' and cardinality(k.razredi) > 0;
$$;

-- Razred učenca danes (npr. '6A').
create or replace function public.sola_ucenec_moj_razred(p_student uuid)
returns text
language sql stable security definer set search_path = public as $$
  select public.razred_na_dan(s.letnik, s.oddelek, current_date) from students s where s.id = p_student;
$$;

-- Naslovi in moduli zdaj nosijo še razrede.
create or replace function public.sola_razpored_vse()
returns jsonb
language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'naslovi', coalesce((select jsonb_agg(jsonb_build_object('id', n.id, 'predmet', n.predmet, 'besedilo', n.besedilo,
                                                             'vrsta', n.vrsta, 'razredi', to_jsonb(n.razredi))
                                          order by n.dodano) from sola_naslovi n), '[]'::jsonb),
    'razpored', coalesce((select jsonb_object_agg(r.predmet, r.red) from sola_razpored r), '{}'::jsonb));
$$;

-- Učenec: predmeti, kjer je zanj kaj (razred predmeta, kviza ali modula).
create or replace function public.sola_tp_ucenec(p_student uuid)
returns table(id text, ime text, emoji text, barva int, razredi text[])
language sql stable security definer set search_path = public as $$
  with r as (select public.razred_na_dan(s.letnik, s.oddelek, current_date) as raz
               from students s where s.id = p_student)
  select t.id, t.ime, t.emoji, t.barva, t.razredi
    from sola_tpredmeti t, r
   where r.raz = any (t.razredi)
      or exists (select 1 from sola_kvizi k where k.predmet = t.id and not k.skrit and r.raz = any (k.razredi))
      or exists (select 1 from sola_naslovi n where n.predmet = t.id and n.vrsta = 'modul' and r.raz = any (n.razredi))
   order by t.ime;
$$;

-- ── 4. Učitelj nastavi razrede ────────────────────────────────────────────
-- Prazen seznam = kot modul oz. predmet.
create or replace function public.sola_tp_kviz_razredi(p_seja uuid, p_id text, p_razredi text[])
returns boolean
language plpgsql security definer set search_path = public as $$
declare pr text;
begin
  select predmet into pr from sola_kvizi where id = p_id;
  if pr is null or not public._sola_tp_lastnik(p_seja, pr) then return false; end if;
  if coalesce(array_length(p_razredi, 1), 0) > 20 then return false; end if;
  update sola_kvizi set razredi = coalesce(p_razredi, '{}') where id = p_id;
  return true;
end; $$;

create or replace function public.sola_tp_modul_razredi(p_seja uuid, p_id uuid, p_razredi text[])
returns boolean
language plpgsql security definer set search_path = public as $$
declare pr text;
begin
  select predmet into pr from sola_naslovi where id = p_id and vrsta = 'modul';
  if pr is null or not public._sola_tp_lastnik(p_seja, pr) then return false; end if;
  if coalesce(array_length(p_razredi, 1), 0) > 20 then return false; end if;
  update sola_naslovi set razredi = coalesce(p_razredi, '{}') where id = p_id;
  return true;
end; $$;

-- ── 5. Igra v živo: pasico dobijo razredi kviza (kviz → modul → predmet) ──
create or replace function public.sola_igra_zacni(p_seja uuid, p_kviz text, p_cas int)
returns uuid
language plpgsql security definer set search_path = public as $$
declare u uuid := public._sola_ucitelj(p_seja); k record; novi uuid;
begin
  if u is null then return null; end if;
  select * into k from sola_kvizi where id = p_kviz;
  if not found or not public._sola_tp_lastnik(p_seja, k.predmet) then return null; end if;
  update sola_igre set stanje = 'konec', posodobljeno = now() where ucitelj = u and stanje <> 'konec';
  insert into sola_igre (kviz_id, ucitelj, razredi, cas)
  values (p_kviz, u, public._sola_kviz_razredi(p_kviz), least(greatest(coalesce(p_cas, 20), 5), 120))
  returning id into novi;
  return novi;
end; $$;

-- ── 6. Pravice ────────────────────────────────────────────────────────────
grant execute on function public.sola_tp_kvizi_razredi() to anon, authenticated;
grant execute on function public.sola_ucenec_moj_razred(uuid) to anon, authenticated;
grant execute on function public.sola_tp_kviz_razredi(uuid, text, text[]) to anon, authenticated;
grant execute on function public.sola_tp_modul_razredi(uuid, uuid, text[]) to anon, authenticated;
