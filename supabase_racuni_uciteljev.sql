-- Brihta — Šola: glavni skrbnik (admin) ureja tudi račune učiteljev
--
-- ZAKAJ: učitelji pozabijo geslo ali čakajo na potrditev računa. Doslej se je
-- to dalo urediti samo v SQL Editorju. Zdaj vidi skrbnik na strani »Računi
-- učencev« še skupino »👨‍🏫 Učitelji«.
--
-- Skrbnik je samo račun s teachers.admin = true (spodaj: Nino). Drugi učitelji
-- te skupine ne vidijo in funkcij ne morejo klicati.
--
-- Kaj lahko skrbnik:
--   • nastavi začasno geslo (najmanj 8 znakov); učitelj ga mora ob prvi
--     prijavi v Brihta-MAT zamenjati (must_change_password, kot pri novih računih);
--   • potrdi nov učiteljski račun ali ga onemogoči (ne briše; lahko ga znova
--     potrdi). Svojega računa ne more onemogočiti.
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat). Varno za ponoven zagon.

-- ── 1. Kdo je skrbnik ─────────────────────────────────────────────────────
alter table teachers add column if not exists admin boolean not null default false;

do $$
begin
  update teachers set admin = true where lower(email) = 'nino.kokalj@os-sempeter.si';
  if not found then
    raise exception 'Ni učiteljskega računa z e-naslovom nino.kokalj@os-sempeter.si';
  end if;
end $$;

-- Vrne skrbnika veljavne seje ali NULL.
create or replace function public._sola_admin(p_seja uuid)
returns uuid language sql stable security definer set search_path = public as $$
  select t.id from teachers t
   where t.id = public._sola_ucitelj(p_seja) and t.admin;
$$;
revoke execute on function public._sola_admin(uuid) from public, anon, authenticated;

-- ── 2. Seznam učiteljev (samo za skrbnika; drugim vrne prazen seznam) ─────
create or replace function public.sola_ucitelji_seznam(p_seja uuid)
returns table(username text, email text, approved boolean, must_change boolean, admin boolean, jaz boolean)
language plpgsql stable security definer set search_path = public as $$
declare a uuid := public._sola_admin(p_seja);
begin
  if a is null then return; end if;
  return query
    select t.username::text, t.email::text, t.approved, t.must_change_password, t.admin, t.id = a
      from teachers t
     order by t.approved, lower(t.email);
end; $$;

-- ── 3. Začasno geslo ──────────────────────────────────────────────────────
-- Vrne OK, KRATKO (manj kot 8 znakov), NI_UCITELJA ali NULL (ni skrbnik).
create or replace function public.sola_ucitelj_geslo(p_seja uuid, p_username text, p_geslo text)
returns text
language plpgsql security definer set search_path = public, extensions as $$
declare a uuid := public._sola_admin(p_seja);
begin
  if a is null then return null; end if;
  if length(coalesce(p_geslo, '')) < 8 then return 'KRATKO'; end if;
  update teachers
     set pin_hash = crypt(p_geslo, gen_salt('bf')),
         must_change_password = (id <> a)   -- svoje geslo si skrbnik nastavi brez menjave
   where username = btrim(coalesce(p_username, ''));
  if not found then return 'NI_UCITELJA'; end if;
  return 'OK';
end; $$;

-- ── 4. Potrdi ali onemogoči račun ─────────────────────────────────────────
-- Onemogočen učitelj se ne more prijaviti; njegove seje se pobrišejo.
-- Vrne OK, NI_UCITELJA, JAZ (svojega ne moreš onemogočiti) ali NULL.
create or replace function public.sola_ucitelj_potrdi(p_seja uuid, p_username text, p_potrjen boolean)
returns text
language plpgsql security definer set search_path = public as $$
declare a uuid := public._sola_admin(p_seja); v uuid;
begin
  if a is null then return null; end if;
  select id into v from teachers where username = btrim(coalesce(p_username, ''));
  if v is null then return 'NI_UCITELJA'; end if;
  if v = a and not coalesce(p_potrjen, false) then return 'JAZ'; end if;
  update teachers set approved = coalesce(p_potrjen, false) where id = v;
  if not coalesce(p_potrjen, false) then delete from sola_seje where teacher_id = v; end if;
  return 'OK';
end; $$;

grant execute on function public.sola_ucitelji_seznam(uuid) to anon, authenticated;
grant execute on function public.sola_ucitelj_geslo(uuid, text, text) to anon, authenticated;
grant execute on function public.sola_ucitelj_potrdi(uuid, text, boolean) to anon, authenticated;
