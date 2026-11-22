-- Brihta: kljukice »Done in class« pri korakih ur v Teaching. Zaženi enkrat v Supabase → SQL Editor.
-- Piše samo prijavljen učitelj. Branje je javno (samo poti korakov in čas, brez osebnih podatkov),
-- da jih lahko prebere tedenski agent Max.
create table if not exists sola_ura_kljukice (
  kljuc        text primary key,
  opravljeno   boolean not null,
  posodobljeno timestamptz not null default now()
);
alter table sola_ura_kljukice enable row level security;

create or replace function public.sola_ura_kljukice()
returns table(kljuc text, opravljeno boolean, posodobljeno timestamptz)
language sql stable security definer set search_path = public as $$
  select k.kljuc, k.opravljeno, k.posodobljeno from sola_ura_kljukice k;
$$;

create or replace function public.sola_ura_kljukica(p_seja uuid, p_kljuc text, p_opravljeno boolean)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if public._sola_ucitelj(p_seja) is null then return false; end if;
  if p_kljuc is null or length(p_kljuc) > 500 or p_opravljeno is null then return false; end if;
  insert into sola_ura_kljukice (kljuc, opravljeno) values (p_kljuc, p_opravljeno)
  on conflict (kljuc) do update set opravljeno = excluded.opravljeno, posodobljeno = now();
  return true;
end; $$;

grant execute on function public.sola_ura_kljukice() to anon;
grant execute on function public.sola_ura_kljukica(uuid, text, boolean) to anon;
