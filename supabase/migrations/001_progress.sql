-- Uri Q: one progress document per signed-in user.
-- Row-level security guarantees a user can only read and write their own row.
create table if not exists public.progress (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  constraint progress_size check (pg_column_size(data) < 512000)
);

alter table public.progress enable row level security;

drop policy if exists "read own progress"   on public.progress;
drop policy if exists "insert own progress" on public.progress;
drop policy if exists "update own progress" on public.progress;

create policy "read own progress"   on public.progress for select to authenticated using ((select auth.uid()) = user_id);
create policy "insert own progress" on public.progress for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "update own progress" on public.progress for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);

revoke all on public.progress from anon;
grant select, insert, update on public.progress to authenticated;
