-- Brihta — Šola: pisanje besedil (stran pisanje-besedil/)
--
-- Učitelj ustvari projekt (npr. »Moj najljubši dan«). Učenec v projektu napiše
-- svoje besedilo; stran ga shranjuje vsakih nekaj sekund. Učitelj vidi vsa
-- besedila, jih lahko popravi in napiše komentar. Učenec vidi samo svoje.
--
-- Vrstniška presoja (»dve zvezdi in želja«): učitelj jo vklopi z enim gumbom.
-- Besedila se naključno in enakomerno razdelijo med učence, ki so v projektu
-- kaj napisali: vsak dobi enako število tujih besedil in vsako besedilo enako
-- število ocenjevalcev. Nihče ne dobi svojega. Ocenjevalec ne vidi avtorja,
-- avtor ne vidi ocenjevalca; učitelj vidi oba.
--
-- Učenec je isti kot v kvizih (tabela students iz Brihta-MAT), učitelj pa
-- seja iz supabase_kvizi_ucitelj.sql (_sola_ucitelj).
-- Zaženi v Supabase → SQL Editor (celo datoteko naenkrat), PO supabase_kvizi_ucitelj.sql.

-- ── 1. Tabele ─────────────────────────────────────────────────────────────
create table if not exists sola_pis_projekti (
  id          uuid primary key default gen_random_uuid(),
  ime         text not null,
  opis        text,
  razred      text,                          -- '4' (vsi 4.), '4A' ali NULL (vsi)
  presoja     boolean not null default false, -- vrstniška presoja vklopljena
  presoja_n   int not null default 1,         -- koliko tujih besedil prebere vsak
  arhiviran   boolean not null default false, -- učenci ga ne vidijo več
  zaklenjen   boolean not null default false, -- učenci besedilo vidijo, a ga ne morejo spreminjati
  ustvarjeno  timestamptz not null default now()
);
alter table sola_pis_projekti add column if not exists zaklenjen boolean not null default false;
alter table sola_pis_projekti enable row level security;

create table if not exists sola_pis_besedila (
  id           uuid primary key default gen_random_uuid(),
  projekt_id   uuid not null references sola_pis_projekti(id) on delete cascade,
  student_id   uuid not null references students(id) on delete cascade,
  naslov       text not null default '',
  vsebina      jsonb not null default '{"ops":[{"insert":"\n"}]}', -- zapis urejevalnika (Quill delta)
  besedilo     text not null default '',      -- golo besedilo (za štetje besed)
  besed        int  not null default 0,
  verzija      int  not null default 1,       -- ob vsakem shranjevanju +1 (zaščita pred prepisom)
  urejal       text not null default 'ucenec', -- kdo je nazadnje spremenil: 'ucenec' / 'ucitelj'
  komentar     text,
  komentar_cas timestamptz,
  ustvarjeno   timestamptz not null default now(),
  posodobljeno timestamptz not null default now(),
  unique (projekt_id, student_id)
);
alter table sola_pis_besedila enable row level security;
create index if not exists sola_pis_besedila_student on sola_pis_besedila (student_id);

create table if not exists sola_pis_presoje (
  besedilo_id  uuid not null references sola_pis_besedila(id) on delete cascade,
  ocenjevalec  uuid not null references students(id) on delete cascade,
  zap          int  not null default 1,        -- vrstni red pri ocenjevalcu
  zvezda1      text,
  zvezda2      text,
  zelja        text,
  oddano       timestamptz,
  primary key (besedilo_id, ocenjevalec)
);
alter table sola_pis_presoje enable row level security;
create index if not exists sola_pis_presoje_ocenjevalec on sola_pis_presoje (ocenjevalec);

-- ── 2. Pomožne ────────────────────────────────────────────────────────────
-- Ali učenec vidi projekt (ni arhiviran in se ujema razred, če je določen).
create or replace function public._sola_pis_vidi(p_student uuid, p_projekt uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from sola_pis_projekti p, students s
     where p.id = p_projekt and s.id = p_student and not p.arhiviran
       and (p.razred is null or p.razred = ''
            or public.razred_na_dan(s.letnik, s.oddelek, current_date) is null
            or public.razred_na_dan(s.letnik, s.oddelek, current_date) like p.razred || '%'));
$$;
revoke execute on function public._sola_pis_vidi(uuid, uuid) from public, anon, authenticated;

-- Ime učenca, kot ga vidi učitelj.
create or replace function public._sola_pis_ime(p_student uuid)
returns jsonb language sql stable security definer set search_path = public as $$
  select jsonb_build_object('id', s.id, 'ime', coalesce(nullif(s.display_name, ''), s.username),
                            'username', s.username, 'emoji', s.emoji,
                            'razred', public.razred_na_dan(s.letnik, s.oddelek, current_date))
    from students s where s.id = p_student;
$$;
revoke execute on function public._sola_pis_ime(uuid) from public, anon, authenticated;

-- Skupno shranjevanje (učenec ali učitelj). Če je verzija drugačna od
-- pričakovane, je besedilo medtem spremenil nekdo drug: nič ne prepiše in
-- vrne trenutno stanje, da ga stran naloži.
create or replace function public._sola_pis_zapisi(p_id uuid, p_verzija int, p_naslov text,
                                                  p_vsebina jsonb, p_besedilo text, p_kdo text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v int; b record;
begin
  if jsonb_typeof(p_vsebina) <> 'object' or length(p_vsebina::text) > 400000
     or length(coalesce(p_besedilo, '')) > 100000 or length(coalesce(p_naslov, '')) > 200 then
    return jsonb_build_object('ok', false, 'napaka', 'PREVELIKO');
  end if;
  update sola_pis_besedila
     set naslov = coalesce(p_naslov, ''), vsebina = p_vsebina, besedilo = coalesce(p_besedilo, ''),
         besed = coalesce(array_length(regexp_split_to_array(btrim(coalesce(p_besedilo, '')), '\s+'), 1), 0)
                 * (btrim(coalesce(p_besedilo, '')) <> '')::int,
         verzija = verzija + 1, urejal = p_kdo, posodobljeno = now()
   where id = p_id and verzija = p_verzija
  returning verzija into v;
  if found then return jsonb_build_object('ok', true, 'verzija', v); end if;
  select naslov, vsebina, verzija, urejal into b from sola_pis_besedila where id = p_id;
  if not found then return jsonb_build_object('ok', false, 'napaka', 'NI'); end if;
  return jsonb_build_object('ok', false, 'napaka', 'KONFLIKT', 'naslov', b.naslov,
                            'vsebina', b.vsebina, 'verzija', b.verzija, 'urejal', b.urejal);
end; $$;
revoke execute on function public._sola_pis_zapisi(uuid, int, text, jsonb, text, text) from public, anon, authenticated;

-- ── 3. Za učence ──────────────────────────────────────────────────────────
-- Projekti, ki jih učenec vidi, z njegovim besedilom in nalogami presoje.
create or replace function public.sola_pis_moji(p_student uuid)
returns jsonb language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(jsonb_build_object(
           'id', p.id, 'ime', p.ime, 'opis', p.opis, 'presoja', p.presoja, 'zaklenjen', p.zaklenjen, 'ustvarjeno', p.ustvarjeno,
           'besedilo', (select jsonb_build_object('id', b.id, 'naslov', b.naslov, 'besed', b.besed,
                                                  'posodobljeno', b.posodobljeno, 'urejal', b.urejal,
                                                  'komentar', b.komentar is not null and b.komentar <> '',
                                                  'presoj', (select count(*) from sola_pis_presoje r
                                                              where r.besedilo_id = b.id and r.oddano is not null))
                          from sola_pis_besedila b where b.projekt_id = p.id and b.student_id = p_student),
           'naloge', case when p.presoja then
                       (select jsonb_build_object('vseh', count(*), 'oddanih', count(r.oddano))
                          from sola_pis_presoje r join sola_pis_besedila b on b.id = r.besedilo_id
                         where b.projekt_id = p.id and r.ocenjevalec = p_student) end
         ) order by p.ustvarjeno desc), '[]'::jsonb)
    from sola_pis_projekti p
   where exists (select 1 from students s where s.id = p_student)
     and public._sola_pis_vidi(p_student, p.id);
$$;

-- Odpre učenčevo besedilo v projektu (če ga še ni, ga ustvari).
create or replace function public.sola_pis_odpri(p_student uuid, p_projekt uuid)
returns jsonb language plpgsql security definer set search_path = public as $$
declare b record; p record;
begin
  if not public._sola_pis_vidi(p_student, p_projekt) then return null; end if;
  select * into p from sola_pis_projekti where id = p_projekt;
  insert into sola_pis_besedila (projekt_id, student_id) values (p_projekt, p_student)
  on conflict (projekt_id, student_id) do nothing;
  select * into b from sola_pis_besedila where projekt_id = p_projekt and student_id = p_student;
  return jsonb_build_object(
    'projekt', jsonb_build_object('id', p.id, 'ime', p.ime, 'opis', p.opis, 'presoja', p.presoja, 'zaklenjen', p.zaklenjen),
    'id', b.id, 'naslov', b.naslov, 'vsebina', b.vsebina, 'verzija', b.verzija, 'urejal', b.urejal,
    'komentar', b.komentar, 'komentar_cas', b.komentar_cas, 'posodobljeno', b.posodobljeno,
    'presoje', (select coalesce(jsonb_agg(jsonb_build_object('zvezda1', r.zvezda1, 'zvezda2', r.zvezda2,
                                                             'zelja', r.zelja, 'oddano', r.oddano) order by r.oddano), '[]'::jsonb)
                  from sola_pis_presoje r where r.besedilo_id = b.id and r.oddano is not null));
end; $$;

create or replace function public.sola_pis_shrani(p_student uuid, p_id uuid, p_verzija int,
                                                 p_naslov text, p_vsebina jsonb, p_besedilo text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare pid uuid;
begin
  select projekt_id into pid from sola_pis_besedila where id = p_id and student_id = p_student;
  if pid is null then return jsonb_build_object('ok', false, 'napaka', 'NI'); end if;
  if not public._sola_pis_vidi(p_student, pid)
     or (select zaklenjen from sola_pis_projekti where id = pid) then
    return jsonb_build_object('ok', false, 'napaka', 'ZAKLENJENO');
  end if;
  return public._sola_pis_zapisi(p_id, p_verzija, p_naslov, p_vsebina, p_besedilo, 'ucenec');
end; $$;

-- Besedila, ki jih mora učenec presoditi (samo, ko je presoja vklopljena). Brez imena avtorja.
create or replace function public.sola_pis_naloge(p_student uuid, p_projekt uuid)
returns jsonb language sql stable security definer set search_path = public as $$
  select coalesce(jsonb_agg(jsonb_build_object(
           'id', b.id, 'zap', r.zap, 'naslov', b.naslov, 'vsebina', b.vsebina,
           'zvezda1', r.zvezda1, 'zvezda2', r.zvezda2, 'zelja', r.zelja, 'oddano', r.oddano
         ) order by r.zap), '[]'::jsonb)
    from sola_pis_presoje r
    join sola_pis_besedila b on b.id = r.besedilo_id
    join sola_pis_projekti p on p.id = b.projekt_id
   where r.ocenjevalec = p_student and b.projekt_id = p_projekt and p.presoja
     and public._sola_pis_vidi(p_student, p_projekt);
$$;

create or replace function public.sola_pis_presoja_oddaj(p_student uuid, p_besedilo uuid,
                                                        p_zvezda1 text, p_zvezda2 text, p_zelja text)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if btrim(coalesce(p_zvezda1, '')) = '' or btrim(coalesce(p_zvezda2, '')) = '' or btrim(coalesce(p_zelja, '')) = ''
     or length(p_zvezda1) > 1000 or length(p_zvezda2) > 1000 or length(p_zelja) > 1000 then
    return false;
  end if;
  update sola_pis_presoje r
     set zvezda1 = btrim(p_zvezda1), zvezda2 = btrim(p_zvezda2), zelja = btrim(p_zelja), oddano = now()
    from sola_pis_besedila b, sola_pis_projekti p
   where r.besedilo_id = p_besedilo and r.ocenjevalec = p_student
     and b.id = r.besedilo_id and p.id = b.projekt_id and p.presoja
     and public._sola_pis_vidi(p_student, p.id);
  return found;
end; $$;

-- ── 4. Za učitelja (veljavna seja) ────────────────────────────────────────
create or replace function public.sola_pis_u_projekti(p_seja uuid)
returns jsonb language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  return (select coalesce(jsonb_agg(jsonb_build_object(
            'id', p.id, 'ime', p.ime, 'opis', p.opis, 'razred', p.razred, 'presoja', p.presoja,
            'presoja_n', p.presoja_n, 'arhiviran', p.arhiviran, 'zaklenjen', p.zaklenjen, 'ustvarjeno', p.ustvarjeno,
            'besedil', (select count(*) from sola_pis_besedila b where b.projekt_id = p.id and b.besed > 0),
            'posodobljeno', (select max(b.posodobljeno) from sola_pis_besedila b where b.projekt_id = p.id)
          ) order by p.arhiviran, p.ustvarjeno desc), '[]'::jsonb)
     from sola_pis_projekti p);
end; $$;

-- Nov projekt (p_id NULL) ali sprememba imena, opisa, razreda.
create or replace function public.sola_pis_u_projekt_shrani(p_seja uuid, p_id uuid, p_ime text, p_opis text, p_razred text)
returns uuid language plpgsql security definer set search_path = public as $$
declare i uuid;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if btrim(coalesce(p_ime, '')) = '' or length(p_ime) > 120 or length(coalesce(p_opis, '')) > 2000
     or length(coalesce(p_razred, '')) > 10 then return null; end if;
  if p_id is null then
    insert into sola_pis_projekti (ime, opis, razred)
    values (btrim(p_ime), nullif(btrim(coalesce(p_opis, '')), ''), nullif(upper(btrim(coalesce(p_razred, ''))), ''))
    returning id into i;
  else
    update sola_pis_projekti
       set ime = btrim(p_ime), opis = nullif(btrim(coalesce(p_opis, '')), ''),
           razred = nullif(upper(btrim(coalesce(p_razred, ''))), '')
     where id = p_id returning id into i;
  end if;
  return i;
end; $$;

create or replace function public.sola_pis_u_arhiviraj(p_seja uuid, p_id uuid, p_arhiviran boolean)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  update sola_pis_projekti set arhiviran = coalesce(p_arhiviran, true) where id = p_id;
  return found;
end; $$;

-- Zaklep: učenci besedilo še vidijo (in presojo), spreminjati ga ne morejo. Učitelj lahko.
create or replace function public.sola_pis_u_zakleni(p_seja uuid, p_id uuid, p_zaklenjen boolean)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  update sola_pis_projekti set zaklenjen = coalesce(p_zaklenjen, true) where id = p_id;
  return found;
end; $$;

create or replace function public.sola_pis_u_izbrisi_projekt(p_seja uuid, p_id uuid)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  delete from sola_pis_projekti where id = p_id;
  return found;
end; $$;

-- Projekt z vsemi besedili (brez vsebine) in stanjem presoje.
create or replace function public.sola_pis_u_projekt(p_seja uuid, p_id uuid)
returns jsonb language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  return (select jsonb_build_object(
            'id', p.id, 'ime', p.ime, 'opis', p.opis, 'razred', p.razred, 'presoja', p.presoja,
            'presoja_n', p.presoja_n, 'arhiviran', p.arhiviran, 'zaklenjen', p.zaklenjen,
            'razdeljeno', exists (select 1 from sola_pis_presoje r join sola_pis_besedila b on b.id = r.besedilo_id
                                   where b.projekt_id = p.id),
            'besedila', (select coalesce(jsonb_agg(jsonb_build_object(
                           'id', b.id, 'ucenec', public._sola_pis_ime(b.student_id), 'naslov', b.naslov,
                           'besed', b.besed, 'posodobljeno', b.posodobljeno, 'urejal', b.urejal,
                           'komentar', b.komentar is not null and b.komentar <> '',
                           'prejetih', (select count(r.oddano) from sola_pis_presoje r where r.besedilo_id = b.id),
                           'dodeljenih', (select count(*) from sola_pis_presoje r where r.besedilo_id = b.id),
                           'napisal', (select count(r.oddano) from sola_pis_presoje r join sola_pis_besedila x on x.id = r.besedilo_id
                                        where x.projekt_id = p.id and r.ocenjevalec = b.student_id),
                           'naj_napise', (select count(*) from sola_pis_presoje r join sola_pis_besedila x on x.id = r.besedilo_id
                                           where x.projekt_id = p.id and r.ocenjevalec = b.student_id)
                         )), '[]'::jsonb)
                         from sola_pis_besedila b where b.projekt_id = p.id))
     from sola_pis_projekti p where p.id = p_id);
end; $$;

-- Celotna besedila (enega ali več) z imeni, komentarjem in presojami — za ogled in izvoz.
create or replace function public.sola_pis_u_besedila(p_seja uuid, p_ids uuid[])
returns jsonb language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  return (select coalesce(jsonb_agg(jsonb_build_object(
            'id', b.id, 'projekt_id', b.projekt_id, 'ucenec', public._sola_pis_ime(b.student_id),
            'naslov', b.naslov, 'vsebina', b.vsebina, 'verzija', b.verzija, 'urejal', b.urejal,
            'besed', b.besed, 'komentar', b.komentar, 'komentar_cas', b.komentar_cas, 'posodobljeno', b.posodobljeno,
            'presoje', (select coalesce(jsonb_agg(jsonb_build_object(
                          'ocenjevalec', public._sola_pis_ime(r.ocenjevalec), 'zvezda1', r.zvezda1,
                          'zvezda2', r.zvezda2, 'zelja', r.zelja, 'oddano', r.oddano) order by r.oddano nulls last), '[]'::jsonb)
                        from sola_pis_presoje r where r.besedilo_id = b.id)
          )), '[]'::jsonb)
     from sola_pis_besedila b where b.id = any(p_ids));
end; $$;

create or replace function public.sola_pis_u_shrani(p_seja uuid, p_id uuid, p_verzija int,
                                                   p_naslov text, p_vsebina jsonb, p_besedilo text)
returns jsonb language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return jsonb_build_object('ok', false, 'napaka', 'SEJA'); end if;
  return public._sola_pis_zapisi(p_id, p_verzija, p_naslov, p_vsebina, p_besedilo, 'ucitelj');
end; $$;

create or replace function public.sola_pis_u_komentar(p_seja uuid, p_id uuid, p_komentar text)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null or length(coalesce(p_komentar, '')) > 5000 then return false; end if;
  update sola_pis_besedila
     set komentar = nullif(btrim(coalesce(p_komentar, '')), ''), komentar_cas = now()
   where id = p_id;
  return found;
end; $$;

-- Izbriše vsebino ene presoje (npr. neprimerna); ocenjevalec jo lahko napiše znova.
create or replace function public.sola_pis_u_presoja_pocisti(p_seja uuid, p_besedilo uuid, p_ocenjevalec uuid)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  update sola_pis_presoje set zvezda1 = null, zvezda2 = null, zelja = null, oddano = null
   where besedilo_id = p_besedilo and ocenjevalec = p_ocenjevalec;
  return found;
end; $$;

-- Vklop/izklop vrstniške presoje.
-- Ob vklopu se besedila razdelijo, če še niso bila (ali če p_na_novo: stare
-- presoje se izbrišejo). Sodelujejo samo besedila, ki niso prazna.
-- Razdelitev: avtorji v naključnem vrstnem redu 0..n-1; učenec na mestu i
-- presodi besedila na mestih i+1, i+2, … i+k (po modulu n). Tako vsak dobi
-- k besedil, vsako besedilo k ocenjevalcev in nihče svojega.
create or replace function public.sola_pis_u_presoja(p_seja uuid, p_id uuid, p_vklop boolean, p_n int, p_na_novo boolean)
returns jsonb language plpgsql security definer set search_path = public as $$
declare n int; k int; je boolean;
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  if not exists (select 1 from sola_pis_projekti where id = p_id) then return null; end if;
  if not coalesce(p_vklop, false) then
    update sola_pis_projekti set presoja = false where id = p_id;
    return jsonb_build_object('presoja', false);
  end if;

  if coalesce(p_na_novo, false) then
    delete from sola_pis_presoje r using sola_pis_besedila b where b.id = r.besedilo_id and b.projekt_id = p_id;
  end if;
  je := exists (select 1 from sola_pis_presoje r join sola_pis_besedila b on b.id = r.besedilo_id where b.projekt_id = p_id);
  select count(*) into n from sola_pis_besedila where projekt_id = p_id and besed > 0;

  if not je then
    k := least(greatest(coalesce(p_n, 1), 1), 5, n - 1);
    if k < 1 then return jsonb_build_object('presoja', false, 'napaka', 'PREMALO', 'besedil', n); end if;
    with a as materialized (
      select id, student_id, (row_number() over (order by random()) - 1)::int as i
        from sola_pis_besedila where projekt_id = p_id and besed > 0
    )
    insert into sola_pis_presoje (besedilo_id, ocenjevalec, zap)
    select t.id, r.student_id, j
      from a r cross join generate_series(1, k) j
      join a t on t.i = (r.i + j) % n;
    update sola_pis_projekti set presoja_n = k where id = p_id;
  end if;

  update sola_pis_projekti set presoja = true where id = p_id;
  return jsonb_build_object('presoja', true, 'besedil', n, 'n', (select presoja_n from sola_pis_projekti where id = p_id));
end; $$;

-- ── 5. Dostop ─────────────────────────────────────────────────────────────
grant execute on function public.sola_pis_moji(uuid) to anon;
grant execute on function public.sola_pis_odpri(uuid, uuid) to anon;
grant execute on function public.sola_pis_shrani(uuid, uuid, int, text, jsonb, text) to anon;
grant execute on function public.sola_pis_naloge(uuid, uuid) to anon;
grant execute on function public.sola_pis_presoja_oddaj(uuid, uuid, text, text, text) to anon;
grant execute on function public.sola_pis_u_projekti(uuid) to anon;
grant execute on function public.sola_pis_u_projekt_shrani(uuid, uuid, text, text, text) to anon;
grant execute on function public.sola_pis_u_arhiviraj(uuid, uuid, boolean) to anon;
grant execute on function public.sola_pis_u_zakleni(uuid, uuid, boolean) to anon;
grant execute on function public.sola_pis_u_izbrisi_projekt(uuid, uuid) to anon;
grant execute on function public.sola_pis_u_projekt(uuid, uuid) to anon;
grant execute on function public.sola_pis_u_besedila(uuid, uuid[]) to anon;
grant execute on function public.sola_pis_u_shrani(uuid, uuid, int, text, jsonb, text) to anon;
grant execute on function public.sola_pis_u_komentar(uuid, uuid, text) to anon;
grant execute on function public.sola_pis_u_presoja_pocisti(uuid, uuid, uuid) to anon;
grant execute on function public.sola_pis_u_presoja(uuid, uuid, boolean, int, boolean) to anon;
