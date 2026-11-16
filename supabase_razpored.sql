-- Brihta — Šola: učitelj na strani predmeta doda naslove (podnaslove) in sam določi vrstni red.
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_kvizi_ucitelj.sql.
--
-- sola_naslovi:  naslovi, ki jih učitelj vpiše (samo besedilo, ni gradivo).
-- sola_razpored: vrstni red na strani predmeta, seznam ključev:
--                gradivo = pot ali url (kot ključ v naslovu strani), kviz = 'kviz:<id>', naslov = 'naslov:<id>'.

create table if not exists sola_naslovi (
  id        uuid primary key default gen_random_uuid(),
  predmet   text not null,
  besedilo  text not null,
  dodano    timestamptz not null default now()
);
alter table sola_naslovi enable row level security;

create table if not exists sola_razpored (
  predmet      text primary key,
  red          jsonb not null default '[]'::jsonb,
  posodobljeno timestamptz not null default now()
);
alter table sola_razpored enable row level security;

-- Javno branje (vse naenkrat; podatkov je malo).
create or replace function public.sola_razpored_vse()
returns jsonb
language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'naslovi', coalesce((select jsonb_agg(jsonb_build_object('id', n.id, 'predmet', n.predmet, 'besedilo', n.besedilo)
                                          order by n.dodano) from sola_naslovi n), '[]'::jsonb),
    'razpored', coalesce((select jsonb_object_agg(r.predmet, r.red) from sola_razpored r), '{}'::jsonb));
$$;

create or replace function public.sola_naslov_dodaj(p_seja uuid, p_predmet text, p_besedilo text)
returns uuid
language plpgsql security definer set search_path = public as $$
declare novi uuid;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if coalesce(p_predmet, '') !~ '^[a-z0-9-]{2,40}$' then return null; end if;
  if coalesce(trim(p_besedilo), '') = '' or length(p_besedilo) > 120 then return null; end if;
  insert into sola_naslovi (predmet, besedilo) values (p_predmet, trim(p_besedilo)) returning id into novi;
  return novi;
end; $$;

create or replace function public.sola_naslov_uredi(p_seja uuid, p_id uuid, p_besedilo text)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  if coalesce(trim(p_besedilo), '') = '' or length(p_besedilo) > 120 then return false; end if;
  update sola_naslovi set besedilo = trim(p_besedilo) where id = p_id;
  return found;
end; $$;

create or replace function public.sola_naslov_izbrisi(p_seja uuid, p_id uuid)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  delete from sola_naslovi where id = p_id;
  update sola_razpored set red = red - ('naslov:' || p_id::text), posodobljeno = now();
  return true;
end; $$;

create or replace function public.sola_razpored_shrani(p_seja uuid, p_predmet text, p_red jsonb)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  if coalesce(p_predmet, '') !~ '^[a-z0-9-]{2,40}$' then return false; end if;
  if jsonb_typeof(p_red) <> 'array' or jsonb_array_length(p_red) > 1000 then return false; end if;
  insert into sola_razpored (predmet, red) values (p_predmet, p_red)
  on conflict (predmet) do update set red = excluded.red, posodobljeno = now();
  return true;
end; $$;
