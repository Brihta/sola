-- Brihta — Šola: samoocena (vpis rezultata brez pravila 50 %)
--
-- Kvizi, katerih datoteka se začne s »Samoocena« (id vsebuje »/samoocena-«), so
-- vpis rezultata, ne preverjanje znanja: učenec pri vsaki nalogi označi, ali jo je
-- rešil pravilno. Tu se oddaja shrani VEDNO, tudi pod 50 %, sicer bi slabši
-- učenci dobili »Poskusi znova« in bi jih to sililo v lažen vpis.
-- Vsi ostali kvizi delujejo kot doslej (pod 50 % poskusi znova).
--
-- Zaženi PO supabase_kvizi_ponovni_poskus.sql v Supabase → SQL Editor (celo datoteko naenkrat).

create or replace function public.sola_kviz_oddaj(p_student uuid, p_kviz text, p_odgovori jsonb)
returns table(tocke int, vseh int, novo boolean, ponovi boolean)
language plpgsql security definer set search_path = public as $$
declare k record; pr jsonb; t int; v int;
begin
  if not exists (select 1 from students s where s.id = p_student) then return; end if;
  select * into k from sola_kvizi where sola_kvizi.id = p_kviz and not skrit;
  if not found then return; end if;
  if jsonb_typeof(p_odgovori) <> 'array' or length(p_odgovori::text) > 50000 then return; end if;

  return query select o.tocke, o.vseh, false, false from sola_oddaje o
                where o.kviz_id = p_kviz and o.student_id = p_student;
  if found then return; end if;

  pr := public._sola_oceni(k.kljuc, p_odgovori);
  v  := jsonb_array_length(k.kljuc);
  select count(*) into t from jsonb_array_elements(pr) x where x = 'true'::jsonb;

  -- Manj kot 50 %: poskus se ne šteje, učenec reši znova (razen pri samooceni).
  if t * 2 < v and position('/samoocena-' in p_kviz) = 0 then
    return query select t, v, true, true;
    return;
  end if;

  insert into sola_oddaje (kviz_id, student_id, odgovori, pravilni, tocke, vseh)
  values (p_kviz, p_student, p_odgovori, pr, t, v)
  on conflict do nothing;
  return query select t, v, true, false;
end; $$;

grant execute on function public.sola_kviz_oddaj(uuid, text, jsonb) to anon;
