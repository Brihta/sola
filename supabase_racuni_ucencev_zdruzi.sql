-- Brihta — Šola: učitelj združi dva računa učenca
-- Dodatek k supabase_racuni_ucencev.sql (ta mora biti že zagnan).
--
-- ZAKAJ: otrok pozabi geslo in si naredi nov račun. Združitev prenese vse iz
-- starega računa (p_from) v račun, ki ga otrok obdrži (p_into), in stari
-- račun izbriše.
--
-- KAKO:
--   1. Šolski podatki (vse tabele sola_*, ki kažejo na students: oddani
--      kvizi, izdelki, besedila, presoje) se prestavijo na p_into. Če ima
--      p_into isto stvar že sam (npr. isti kviz), obdrži svojo, stara se
--      izbriše skupaj s starim računom.
--   2. Vadbo Brihta-MAT združi ista funkcija kot v Brihta-MAT (merge_students).
--   Če karkoli spodleti, se ne spremeni nič.
--
-- Zaženi v Supabase → SQL Editor. Varno za ponoven zagon.

-- Vrne OK, NI_UCENCA, ISTI, 'NAPAKA: …' ali NULL (seja ni veljavna).
create or replace function public.sola_ucenec_zdruzi(p_seja uuid, p_from text, p_into text)
returns text
language plpgsql security definer set search_path = public as $$
declare
  t uuid := public._sola_ucitelj(p_seja);
  v_from uuid; v_into uuid; fk record; vr record; r text;
begin
  if t is null then return null; end if;
  select id into v_from from students where lower(username) = lower(btrim(coalesce(p_from, '')));
  select id into v_into from students where lower(username) = lower(btrim(coalesce(p_into, '')));
  if v_from is null or v_into is null then return 'NI_UCENCA'; end if;
  if v_from = v_into then return 'ISTI'; end if;

  begin
    -- 1. Šolske tabele: vsak stolpec v tabeli sola_*, ki kaže na students(id).
    for fk in
      select c.conrelid::regclass as tabela, a.attname as stolpec
        from pg_constraint c
        join pg_attribute a on a.attrelid = c.conrelid and a.attnum = c.conkey[1]
       where c.contype = 'f' and c.confrelid = 'public.students'::regclass
         and array_length(c.conkey, 1) = 1
         and c.conrelid::regclass::text like 'sola\_%'
    loop
      for vr in execute format('select ctid from %s where %I = $1', fk.tabela, fk.stolpec) using v_from loop
        begin
          execute format('update %s set %I = $1 where ctid = $2', fk.tabela, fk.stolpec) using v_into, vr.ctid;
        exception when unique_violation then
          null;  -- p_into to že ima: obdrži svojo, stara gre z računom
        end;
      end loop;
    end loop;

    -- 2. Brihta-MAT (vadba, ime, razred) in brisanje starega računa.
    r := public.merge_students(t, p_from, p_into);
    if r is distinct from 'OK' then
      raise exception '%', coalesce(r, 'merge_students ni vrnil rezultata');
    end if;
  exception when others then
    return case when sqlerrm like 'NAPAKA%' then sqlerrm else 'NAPAKA: ' || sqlerrm end;
  end;
  return 'OK';
end; $$;

grant execute on function public.sola_ucenec_zdruzi(uuid, text, text) to anon, authenticated;
