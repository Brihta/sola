-- Brihta — Šola: učitelj preimenuje ali izbriše račun učenca
-- Dodatek k supabase_racuni_ucencev.sql (ta mora biti že zagnan).
--
-- Kliče isti funkciji kot Brihta-MAT (set_student_name, delete_student),
-- zato se ime in brisanje obnašata natanko tako kot tam. Šolske tabele
-- (sola_oddaje, sola_izdelki, sola_pis_*) imajo »on delete cascade«, zato se
-- ob brisanju pobrišejo same.
--
-- Zaženi v Supabase → SQL Editor. Varno za ponoven zagon.

-- Vrne OK, SLABO_IME, NI_UCENCA ali NULL (seja ni veljavna).
create or replace function public.sola_ucenec_ime(p_seja uuid, p_username text, p_ime text)
returns text
language plpgsql security definer set search_path = public as $$
declare t uuid := public._sola_ucitelj(p_seja);
begin
  if t is null then return null; end if;
  return public.set_student_name(t, p_username, p_ime);
end; $$;

-- Vrne OK, NI_UCENCA, 'NAPAKA: …' ali NULL (seja ni veljavna).
create or replace function public.sola_ucenec_izbrisi(p_seja uuid, p_username text)
returns text
language plpgsql security definer set search_path = public as $$
declare t uuid := public._sola_ucitelj(p_seja);
begin
  if t is null then return null; end if;
  return public.delete_student(t, p_username);
end; $$;

grant execute on function public.sola_ucenec_ime(uuid, text, text) to anon, authenticated;
grant execute on function public.sola_ucenec_izbrisi(uuid, text) to anon, authenticated;
