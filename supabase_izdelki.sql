-- Brihta — Šola: izdelki učencev v samostojnih urah (npr. simetrija na mreži)
--
-- Stran ure po vsaki rešeni nalogi shrani, kaj je učenec naredil:
-- stanje (sam / z namigom / pogledal rešitev), število poskusov in njegovo mrežo.
-- Učitelj iz tega na strani natisne poročilo, eno stran na učenca.
--
-- Učenec je isti kot v kvizih (tabela students iz Brihta-MAT).
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_kvizi_ucitelj.sql.

create table if not exists sola_izdelki (
  ura          text not null,               -- 'racunalnistvo-3/2026-11-06-simetrija'
  student_id   uuid not null references students(id) on delete cascade,
  stopnja      text not null,               -- id naloge v uri, npr. 's03'
  zap          int  not null,               -- vrstni red naloge v uri
  podatki      jsonb not null,              -- {naslov, stanje, poskusi, namigi, w, h, os, dano, moje}
  posodobljeno timestamptz not null default now(),
  primary key (ura, student_id, stopnja)
);
-- RLS brez politik = z javnim ključem ni neposrednega dostopa.
alter table sola_izdelki enable row level security;

-- Shrani (ali posodobi) eno nalogo enega učenca.
create or replace function public.sola_izdelek_shrani(p_student uuid, p_ura text, p_stopnja text, p_zap int, p_podatki jsonb)
returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from students s where s.id = p_student) then return false; end if;
  if p_ura is null or length(p_ura) > 200 or p_stopnja is null or length(p_stopnja) > 60 then return false; end if;
  if jsonb_typeof(p_podatki) <> 'object' or length(p_podatki::text) > 20000 then return false; end if;
  insert into sola_izdelki (ura, student_id, stopnja, zap, podatki)
  values (p_ura, p_student, p_stopnja, coalesce(p_zap, 0), p_podatki)
  on conflict (ura, student_id, stopnja)
  do update set podatki = excluded.podatki, zap = excluded.zap, posodobljeno = now();
  return true;
end; $$;

-- Za učitelja (veljavna seja): vsi izdelki ene ure, z imenom in razredom učenca.
create or replace function public.sola_izdelki_porocilo(p_seja uuid, p_ura text)
returns table(student_id uuid, username text, ime text, emoji text, razred text,
              stopnja text, zap int, podatki jsonb, posodobljeno timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return; end if;
  return query
    select s.id, s.username, coalesce(nullif(s.display_name, ''), s.username), s.emoji,
           public.razred_na_dan(s.letnik, s.oddelek, current_date),
           i.stopnja, i.zap, i.podatki, i.posodobljeno
      from sola_izdelki i join students s on s.id = i.student_id
     where i.ura = p_ura
     order by 3, i.zap;
end; $$;

-- Za učitelja: izbriše izdelke ene ure (npr. ob koncu šolskega leta).
create or replace function public.sola_izdelki_izbrisi(p_seja uuid, p_ura text)
returns int
language plpgsql security definer set search_path = public as $$
declare n int;
begin
  if public._sola_ucitelj(p_seja) is null then return 0; end if;
  delete from sola_izdelki where ura = p_ura;
  get diagnostics n = row_count;
  return n;
end; $$;
