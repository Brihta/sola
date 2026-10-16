-- Brihta — Šola: ponovni poskus pri manj kot 50 %
--
-- Če ima učenec ob oddaji manj kot polovico točk, se oddaja NE shrani.
-- Strežnik vrne ponovi = true, stran mu pokaže »Poskusi znova« in kviz
-- lahko reši še enkrat. Pri 50 % ali več velja oddaja kot doslej (en poskus).
--
-- Zaženi PO supabase_kvizi.sql v Supabase → SQL Editor (celo datoteko naenkrat).

-- Spremeni se vrsta, ki jo funkcija vrne (nov stolpec ponovi), zato drop.
drop function if exists public.sola_kviz_oddaj(uuid, text, jsonb);

create function public.sola_kviz_oddaj(p_student uuid, p_kviz text, p_odgovori jsonb)
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

  -- Manj kot 50 %: poskus se ne šteje, učenec reši znova.
  if t * 2 < v then
    return query select t, v, true, true;
    return;
  end if;

  insert into sola_oddaje (kviz_id, student_id, odgovori, pravilni, tocke, vseh)
  values (p_kviz, p_student, p_odgovori, pr, t, v)
  on conflict do nothing;
  return query select t, v, true, false;
end; $$;

grant execute on function public.sola_kviz_oddaj(uuid, text, jsonb) to anon;

-- NEOBVEZNO: že shranjene oddaje pod 50 % izbriši, da lahko ti učenci kviz
-- rešijo znova. Odstrani »--« pred naslednjo vrstico, če to želiš.
-- delete from sola_oddaje where tocke * 2 < vseh;
