-- Brihta — Šola: učitelj ureja račune učencev (razred, geslo)
--
-- ZAKAJ: na Šoli je učitelj lahko samo objavljal gradiva in kvize. Za premik
-- otroka v drug razred ali novo geslo je moral v Brihta-MAT. Zdaj ima v meniju
-- računa gumb »Računi učencev«.
--
-- Računi so isti kot v Brihta-MAT (tabela students). Brihta-MAT se ne spremeni.
-- Zaščita: veljavna učiteljska seja Šole (_sola_ucitelj, supabase_kvizi_ucitelj.sql).
-- Premik v razred kliče move_student_razred iz Brihta-MAT (supabase_obiskovalec.sql),
-- zato se razred shrani natanko tako kot tam.
--
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat). Varno za ponoven zagon.

-- ── 1. Seznam učencev ─────────────────────────────────────────────────────
-- razred: npr. '4A', 'OBISK' (obiskovalec) ali NULL (še ni izbral / končal šolo).
create or replace function public.sola_ucenci_seznam(p_seja uuid)
returns table(username text, display_name text, emoji text, razred text)
language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return; end if;
  return query
    select s.username::text, s.display_name::text, s.emoji::text,
           public.razred_ali_obisk(s.obiskovalec, s.letnik, s.oddelek, current_date)
      from students s
     order by s.username;
end; $$;

-- ── 2. Premik v razred ali med obiskovalce ────────────────────────────────
-- Vrne OK, NI_UCENCA, SLAB_RAZRED ali NULL (seja ni veljavna).
create or replace function public.sola_ucenec_razred(p_seja uuid, p_username text, p_razred text)
returns text
language plpgsql security definer set search_path = public as $$
declare t uuid := public._sola_ucitelj(p_seja);
begin
  if t is null then return null; end if;
  return public.move_student_razred(t, p_username, p_razred);
end; $$;

-- ── 3. Novo geslo (4 živali) ──────────────────────────────────────────────
-- Geslo: indeksi živali 0–11, ločeni z vejico (kot pri prijavi).
-- Pobriše tudi zaklep po napačnih poskusih, da se otrok takoj prijavi.
-- Vrne OK, NI_UCENCA, SLABO_GESLO ali NULL (seja ni veljavna).
create or replace function public.sola_ucenec_geslo(p_seja uuid, p_username text, p_pin text)
returns text
language plpgsql security definer set search_path = public, extensions as $$
declare
  v_u  text := lower(btrim(coalesce(p_username, '')));
  v_id uuid;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if coalesce(p_pin, '') !~ '^([0-9]|1[01]),([0-9]|1[01]),([0-9]|1[01]),([0-9]|1[01])$' then
    return 'SLABO_GESLO';
  end if;
  select id into v_id from students where lower(username) = v_u;
  if v_id is null then return 'NI_UCENCA'; end if;

  update students set pin_hash = crypt(p_pin, gen_salt('bf')) where id = v_id;
  -- Varovalka: z novim geslom se mora dati prijaviti, sicer vse prekliči.
  if not exists (select 1 from public.login_student_preveri(p_username, p_pin)) then
    raise exception 'Novo geslo se ne ujema s prijavo — nič ni spremenjeno.';
  end if;
  delete from login_attempts where uname = v_u;
  return 'OK';
end; $$;

grant execute on function public.sola_ucenci_seznam(uuid) to anon, authenticated;
grant execute on function public.sola_ucenec_razred(uuid, text, text) to anon, authenticated;
grant execute on function public.sola_ucenec_geslo(uuid, text, text) to anon, authenticated;
