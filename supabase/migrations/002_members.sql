-- urIQ: every new account waits for the site owner's approval.
-- A row is created automatically for each new user (approved = false). The owner gets an
-- e-mail (edge function signup-notify) with a link to approve.html, which calls the edge
-- function approve with the row's secret token.
create table if not exists public.members (
  user_id     uuid primary key references auth.users(id) on delete cascade,
  email       text,
  name        text,
  approved    boolean not null default false,
  token       uuid not null default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  notified_at timestamptz,
  approved_at timestamptz
);

alter table public.members enable row level security;
drop policy if exists "read own membership" on public.members;
create policy "read own membership" on public.members for select to authenticated using ((select auth.uid()) = user_id);

-- users may read only whether they are approved; the token never leaves the server
revoke all on public.members from anon, authenticated;
grant select (user_id, approved) on public.members to authenticated;

-- a members row for every new account
create or replace function public.on_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.members (user_id, email, name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', ''))
  on conflict (user_id) do nothing;
  return new;
end $$;
revoke execute on function public.on_new_user() from public, anon, authenticated;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.on_new_user();

-- everyone who signed up before this change is already approved
insert into public.members (user_id, email, name, approved, approved_at, notified_at)
select id, email, coalesce(raw_user_meta_data->>'full_name', raw_user_meta_data->>'name', ''), true, now(), now()
from auth.users
on conflict (user_id) do update set approved = true, approved_at = coalesce(public.members.approved_at, now());

-- progress is only for approved users
create or replace function public.is_approved() returns boolean
language sql stable security definer set search_path = '' as $$
  select coalesce((select approved from public.members where user_id = (select auth.uid())), false)
$$;
revoke execute on function public.is_approved() from public, anon;
grant execute on function public.is_approved() to authenticated;

drop policy if exists "read own progress"   on public.progress;
drop policy if exists "insert own progress" on public.progress;
drop policy if exists "update own progress" on public.progress;
create policy "read own progress"   on public.progress for select to authenticated using ((select auth.uid()) = user_id and (select public.is_approved()));
create policy "insert own progress" on public.progress for insert to authenticated with check ((select auth.uid()) = user_id and (select public.is_approved()));
create policy "update own progress" on public.progress for update to authenticated using ((select auth.uid()) = user_id and (select public.is_approved())) with check ((select auth.uid()) = user_id and (select public.is_approved()));
