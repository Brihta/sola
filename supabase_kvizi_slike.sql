-- Brihta — Šola: slike pri vprašanjih kviza
--
-- ZAKAJ: učitelj kviz naredi iz Excela (brez slik), nato na strani pri vprašanju
-- doda sliko. Slika je vezana na BESEDILO vprašanja (ne na številko), zato ostane,
-- ko učitelj naloži popravljen Excel ali premeša vprašanja. Če besedilo vprašanja
-- spremeni, se slika odklopi (učitelj jo doda znova).
--
-- Slike so v javni shrambi »sola-gradiva« pod kvizi/<uuid>.jpg (stran jih pred
-- nalaganjem pomanjša na največ 1200 px, JPG). Nalaganje in brisanje uporabljata
-- iste kratkotrajne dovolilnice kot gradiva (sola_nalaganja, supabase_gradiva.sql).
--
-- Slika iz iskanja (Openverse, proste licence) ima v »vir« avtorja, licenco in povezavo
-- (JSON {a, l, u}); stran jih izpiše pod sliko. Pri lastni sliki je vir prazen.
--
-- Kviz v predmetu učitelja (u-…) ureja samo njegov lastnik, ostale kvize vsak učitelj.
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_gradiva.sql
-- in supabase_predmeti_uciteljev.sql. Varno za ponoven zagon.

create table if not exists sola_kviz_slike (
  kviz_id   text not null references sola_kvizi(id) on delete cascade,
  besedilo  text not null,
  pot       text not null unique,
  dodano    timestamptz not null default now(),
  primary key (kviz_id, besedilo)
);
alter table sola_kviz_slike enable row level security;
alter table sola_kviz_slike add column if not exists vir text;
drop function if exists public.sola_kviz_slike(text);
drop function if exists public.sola_kviz_slika_shrani(uuid, text, text, text);

-- Ali sme ta seja urejati slike tega kviza.
create or replace function public._sola_kviz_urednik(p_seja uuid, p_kviz text)
returns boolean language sql stable security definer set search_path = public as $$
  select public._sola_ucitelj(p_seja) is not null
     and exists (select 1 from sola_kvizi k where k.id = p_kviz
                  and (k.predmet not like 'u-%' or public._sola_tp_lastnik(p_seja, k.predmet)));
$$;
revoke execute on function public._sola_kviz_urednik(uuid, text) from public, anon, authenticated;

-- Slike kviza (javno, kot slike same).
create or replace function public.sola_kviz_slike(p_kviz text)
returns table(besedilo text, pot text, vir text)
language sql stable security definer set search_path = public as $$
  select s.besedilo, s.pot, s.vir from sola_kviz_slike s where s.kviz_id = p_kviz;
$$;

-- Korak 1: vrne pot, na katero sme stran v 15 minutah naložiti sliko.
create or replace function public.sola_kviz_slika_zacni(p_seja uuid, p_kviz text)
returns text
language plpgsql security definer set search_path = public as $$
declare p text;
begin
  if not public._sola_kviz_urednik(p_seja, p_kviz) then return null; end if;
  delete from sola_nalaganja where potece < now();
  p := 'kvizi/' || gen_random_uuid()::text || '.jpg';
  insert into sola_nalaganja (pot, dejanje) values (p, 'nalozi');
  return p;
end; $$;

-- Korak 2: sliko pripne vprašanju. Vrne pot prejšnje slike (stran jo izbriše) ali ''.
create or replace function public.sola_kviz_slika_shrani(p_seja uuid, p_kviz text, p_besedilo text, p_pot text,
                                                         p_vir text default null)
returns text
language plpgsql security definer set search_path = public as $$
declare stara text;
begin
  if not public._sola_kviz_urednik(p_seja, p_kviz) then return null; end if;
  if coalesce(p_besedilo, '') = '' or length(p_besedilo) > 2000 then return null; end if;
  if not exists (select 1 from sola_nalaganja where pot = p_pot and dejanje = 'nalozi') then return null; end if;
  if length(coalesce(p_vir, '')) > 1000 then return null; end if;
  delete from sola_nalaganja where pot = p_pot and dejanje = 'nalozi';
  select pot into stara from sola_kviz_slike where kviz_id = p_kviz and besedilo = p_besedilo;
  insert into sola_kviz_slike (kviz_id, besedilo, pot, vir) values (p_kviz, p_besedilo, p_pot, nullif(p_vir, ''))
  on conflict (kviz_id, besedilo) do update set pot = excluded.pot, vir = excluded.vir, dodano = now();
  if stara is null then return ''; end if;
  insert into sola_nalaganja (pot, dejanje) values (stara, 'izbrisi') on conflict do nothing;
  return stara;
end; $$;

-- Odstrani sliko z vprašanja. Vrne pot, ki jo sme stran izbrisati iz shrambe.
create or replace function public.sola_kviz_slika_odstrani(p_seja uuid, p_kviz text, p_besedilo text)
returns text
language plpgsql security definer set search_path = public as $$
declare p text;
begin
  if not public._sola_kviz_urednik(p_seja, p_kviz) then return null; end if;
  delete from sola_kviz_slike where kviz_id = p_kviz and besedilo = p_besedilo returning pot into p;
  if p is null then return null; end if;
  insert into sola_nalaganja (pot, dejanje) values (p, 'izbrisi') on conflict do nothing;
  return p;
end; $$;

grant execute on function public.sola_kviz_slike(text) to anon, authenticated;
grant execute on function public.sola_kviz_slika_zacni(uuid, text) to anon, authenticated;
grant execute on function public.sola_kviz_slika_shrani(uuid, text, text, text, text) to anon, authenticated;
grant execute on function public.sola_kviz_slika_odstrani(uuid, text, text) to anon, authenticated;
