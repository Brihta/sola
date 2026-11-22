-- Brihta: objava in skrivanje gradiva s skrivnostjo (brez prijave učitelja).
-- Zaženi enkrat v Supabase → SQL Editor, PO supabase_gradiva.sql.
-- Uporablja isto skrivnost kot kvizi (app_config.sola_kviz_skrivnost), ki je
-- samo na Ninovem Macu. Kliče jo scripts/objavi.py.

create or replace function public.sola_gradivo_objavi_skrivnost(p_skrivnost text, p_kljuc text, p_objavljeno boolean)
returns boolean
language plpgsql security definer set search_path = public as $$
declare s text;
begin
  select value into s from app_config where key = 'sola_kviz_skrivnost';
  if s is null or length(s) < 20 or p_skrivnost is distinct from s then
    raise exception 'NAPACNA_SKRIVNOST';
  end if;
  if p_kljuc is null or length(p_kljuc) > 500 or p_objavljeno is null then return false; end if;
  insert into sola_gradiva_stanje (kljuc, objavljeno) values (p_kljuc, p_objavljeno)
  on conflict (kljuc) do update set objavljeno = excluded.objavljeno, posodobljeno = now();
  return true;
end; $$;

revoke all on function public.sola_gradivo_objavi_skrivnost(text, text, boolean) from public;
grant execute on function public.sola_gradivo_objavi_skrivnost(text, text, boolean) to anon;
