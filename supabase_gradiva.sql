-- Brihta — Šola: učitelj na strani skrije/objavi gradivo in nalaga datoteke.
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_kvizi_ucitelj.sql.
--
-- 1. Objava/skrivanje: tabela sola_gradiva_stanje hrani, kaj je učitelj ročno
--    objavil ali skril (ključ = pot gradiva iz gradiva.json ali id naložene datoteke).
--    Brez zapisa velja: gradivo z datumom v prihodnosti je skrito, ostalo je objavljeno.
--    Pozor: datoteke v repozitoriju so javne (GitHub), skrivanje jih samo umakne s strani.
-- 2. Nalaganje: datoteke gredo v javno shrambo »sola-gradiva«. Nalagati in brisati
--    sme samo, kdor ima od učiteljeve seje kratkotrajno dovolilnico za točno to pot.

-- ── 1. Objava in skrivanje ────────────────────────────────────────────────
create table if not exists sola_gradiva_stanje (
  kljuc        text primary key,
  objavljeno   boolean not null,
  posodobljeno timestamptz not null default now()
);
alter table sola_gradiva_stanje enable row level security;

create or replace function public.sola_gradiva_stanje()
returns table(kljuc text, objavljeno boolean)
language sql stable security definer set search_path = public as $$
  select s.kljuc, s.objavljeno from sola_gradiva_stanje s;
$$;

create or replace function public.sola_gradivo_objavi(p_seja uuid, p_kljuc text, p_objavljeno boolean)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  if p_kljuc is null or length(p_kljuc) > 500 or p_objavljeno is null then return false; end if;
  insert into sola_gradiva_stanje (kljuc, objavljeno) values (p_kljuc, p_objavljeno)
  on conflict (kljuc) do update set objavljeno = excluded.objavljeno, posodobljeno = now();
  return true;
end; $$;

-- ── 2. Naložena gradiva ───────────────────────────────────────────────────
create table if not exists sola_gradiva_dodana (
  id           uuid primary key default gen_random_uuid(),
  predmet      text not null,
  naslov       text not null,
  vrsta        text not null,              -- pdf | word | slika
  pot          text not null unique,       -- pot v shrambi: <predmet>/<uuid>.<končnica>
  ime_datoteke text,                       -- izvirno ime (za prenos)
  velikost     bigint,
  datum        timestamptz not null default now(),
  dodano       timestamptz not null default now()
);
alter table sola_gradiva_dodana enable row level security;

-- Dovolilnice za shrambo (pot + dejanje), veljajo 15 minut.
create table if not exists sola_nalaganja (
  pot     text not null,
  dejanje text not null check (dejanje in ('nalozi', 'izbrisi')),
  potece  timestamptz not null default now() + interval '15 minutes',
  primary key (pot, dejanje)
);
alter table sola_nalaganja enable row level security;

-- Seznam naloženih gradiv (javno; skrita filtrira stran po sola_gradiva_stanje).
create or replace function public.sola_gradiva_dodana()
returns table(id uuid, predmet text, naslov text, vrsta text, pot text, ime_datoteke text, velikost bigint, datum timestamptz)
language sql stable security definer set search_path = public as $$
  select d.id, d.predmet, d.naslov, d.vrsta, d.pot, d.ime_datoteke, d.velikost, d.datum
    from sola_gradiva_dodana d order by d.datum desc;
$$;

-- Korak 1 nalaganja: vrne pot, na katero sme stran v naslednjih 15 minutah naložiti datoteko.
create or replace function public.sola_nalaganje_zacni(p_seja uuid, p_predmet text, p_koncnica text)
returns text
language plpgsql security definer set search_path = public as $$
declare k text := lower(coalesce(p_koncnica, '')); p text;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if coalesce(p_predmet, '') !~ '^[a-z0-9-]{2,40}$' then return null; end if;
  if k not in ('pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png') then return null; end if;
  delete from sola_nalaganja where potece < now();
  p := p_predmet || '/' || gen_random_uuid()::text || '.' || k;
  insert into sola_nalaganja (pot, dejanje) values (p, 'nalozi');
  return p;
end; $$;

-- Korak 2 nalaganja: ko je datoteka v shrambi, jo vpiše med gradiva.
create or replace function public.sola_gradivo_dodaj(p_seja uuid, p_pot text, p_naslov text, p_vrsta text,
                                                     p_ime_datoteke text, p_velikost bigint, p_datum timestamptz,
                                                     p_objavljeno boolean)
returns uuid
language plpgsql security definer set search_path = public as $$
declare novi uuid;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if not exists (select 1 from sola_nalaganja where pot = p_pot and dejanje = 'nalozi') then return null; end if;
  if coalesce(trim(p_naslov), '') = '' or length(p_naslov) > 200 or p_vrsta not in ('pdf', 'word', 'slika') then return null; end if;
  delete from sola_nalaganja where pot = p_pot and dejanje = 'nalozi';
  insert into sola_gradiva_dodana (predmet, naslov, vrsta, pot, ime_datoteke, velikost, datum)
  values (split_part(p_pot, '/', 1), trim(p_naslov), p_vrsta, p_pot, left(p_ime_datoteke, 200), p_velikost, coalesce(p_datum, now()))
  returning id into novi;
  insert into sola_gradiva_stanje (kljuc, objavljeno) values ('dodano:' || novi, coalesce(p_objavljeno, true))
  on conflict (kljuc) do update set objavljeno = excluded.objavljeno, posodobljeno = now();
  return novi;
end; $$;

-- Izbris: odstrani vpis in vrne pot, ki jo sme stran nato izbrisati iz shrambe.
create or replace function public.sola_gradivo_izbrisi(p_seja uuid, p_id uuid)
returns text
language plpgsql security definer set search_path = public as $$
declare p text;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  delete from sola_gradiva_dodana where id = p_id returning pot into p;
  if p is null then return null; end if;
  delete from sola_gradiva_stanje where kljuc = 'dodano:' || p_id;
  insert into sola_nalaganja (pot, dejanje) values (p, 'izbrisi') on conflict do nothing;
  return p;
end; $$;

-- Uporabljajo pravila shrambe spodaj (kliče jih vloga anon).
create or replace function public.sola_nalaganje_dovoljeno(p_pot text, p_dejanje text)
returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from sola_nalaganja n where n.pot = p_pot and n.dejanje = p_dejanje and n.potece > now());
$$;
grant execute on function public.sola_nalaganje_dovoljeno(text, text) to anon, authenticated;

-- ── 3. Shramba ────────────────────────────────────────────────────────────
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('sola-gradiva', 'sola-gradiva', true, 26214400,
        array['application/pdf', 'application/msword',
              'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
              'image/jpeg', 'image/png'])
on conflict (id) do update set public = excluded.public, file_size_limit = excluded.file_size_limit,
                               allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "sola_gradiva_nalozi" on storage.objects;
drop policy if exists "sola_gradiva_izbrisi" on storage.objects;
drop policy if exists "sola_gradiva_beri_za_izbris" on storage.objects;

create policy "sola_gradiva_nalozi" on storage.objects for insert to anon, authenticated
  with check (bucket_id = 'sola-gradiva' and public.sola_nalaganje_dovoljeno(name, 'nalozi'));
create policy "sola_gradiva_izbrisi" on storage.objects for delete to anon, authenticated
  using (bucket_id = 'sola-gradiva' and public.sola_nalaganje_dovoljeno(name, 'izbrisi'));
-- Brisanje prek API-ja potrebuje tudi branje; dovoljeno samo za pot z dovolilnico (seznama datotek ni).
create policy "sola_gradiva_beri_za_izbris" on storage.objects for select to anon, authenticated
  using (bucket_id = 'sola-gradiva' and public.sola_nalaganje_dovoljeno(name, 'izbrisi'));
