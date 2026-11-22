-- Brihta: zasebno spremljanje (Assessment) za učitelja. Zaženi enkrat v Supabase → SQL Editor,
-- PO supabase_kvizi_ucitelj.sql. Imen in točk NI v repozitoriju (je javen): so samo v teh tabelah,
-- do njih pride le prijavljen učitelj (preverja _sola_ucitelj). Učence vpišeš z ločenim SQL ali na strani.

create table if not exists sola_ocene_ucenci (
  id         bigint generated always as identity primary key,
  skupina    text not null,                 -- npr. 'fleksi-5-3'
  ime        text not null,                 -- ime in začetnica priimka, če se ime ponovi
  vrstni_red int not null default 0,
  aktiven    boolean not null default true
);
alter table sola_ocene_ucenci enable row level security;

create table if not exists sola_ocene_spelling (
  ucenec_id    bigint not null references sola_ocene_ucenci(id) on delete cascade,
  teden        int not null check (teden between 1 and 60),
  tocke        int not null check (tocke between 0 and 50),
  posodobljeno timestamptz not null default now(),
  primary key (ucenec_id, teden)
);
alter table sola_ocene_spelling enable row level security;

create or replace function public.sola_ocene_preberi(p_seja uuid, p_skupina text)
returns jsonb language plpgsql stable security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return null; end if;
  return jsonb_build_object(
    'ucenci', coalesce((select jsonb_agg(jsonb_build_object('id', u.id, 'ime', u.ime) order by u.vrstni_red, u.ime)
                        from sola_ocene_ucenci u where u.skupina = p_skupina and u.aktiven), '[]'::jsonb),
    'spelling', coalesce((select jsonb_agg(jsonb_build_object('u', s.ucenec_id, 't', s.teden, 'p', s.tocke))
                          from sola_ocene_spelling s join sola_ocene_ucenci u on u.id = s.ucenec_id
                          where u.skupina = p_skupina), '[]'::jsonb));
end; $$;

-- p_tocke NULL = izbriši vnos (učenec testa ni pisal).
create or replace function public.sola_ocena_spelling(p_seja uuid, p_ucenec bigint, p_teden int, p_tocke int)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  if p_tocke is null then
    delete from sola_ocene_spelling where ucenec_id = p_ucenec and teden = p_teden;
  else
    insert into sola_ocene_spelling (ucenec_id, teden, tocke) values (p_ucenec, p_teden, p_tocke)
    on conflict (ucenec_id, teden) do update set tocke = excluded.tocke, posodobljeno = now();
  end if;
  return true;
end; $$;

create or replace function public.sola_ocene_ucenec_dodaj(p_seja uuid, p_skupina text, p_ime text)
returns bigint language plpgsql security definer set search_path = public as $$
declare n bigint;
begin
  if public._sola_ucitelj(p_seja) is null or length(trim(coalesce(p_ime, ''))) = 0 then return null; end if;
  insert into sola_ocene_ucenci (skupina, ime, vrstni_red)
  values (p_skupina, trim(p_ime), (select coalesce(max(vrstni_red), 0) + 1 from sola_ocene_ucenci where skupina = p_skupina))
  returning id into n;
  return n;
end; $$;

create or replace function public.sola_ocene_ucenec_odstrani(p_seja uuid, p_ucenec bigint)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  update sola_ocene_ucenci set aktiven = false where id = p_ucenec;   -- točke ostanejo
  return true;
end; $$;

revoke all on function public.sola_ocene_preberi(uuid, text), public.sola_ocena_spelling(uuid, bigint, int, int),
  public.sola_ocene_ucenec_dodaj(uuid, text, text), public.sola_ocene_ucenec_odstrani(uuid, bigint) from public;
grant execute on function public.sola_ocene_preberi(uuid, text), public.sola_ocena_spelling(uuid, bigint, int, int),
  public.sola_ocene_ucenec_dodaj(uuid, text, text), public.sola_ocene_ucenec_odstrani(uuid, bigint) to anon;
