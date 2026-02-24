create extension if not exists "pgcrypto";

create table if not exists public.jobs (
    id uuid primary key default gen_random_uuid(),
    external_id text not null,
    company text not null,
    title text not null,
    location text,
    url text not null,
    keyword_match text[],
    first_seen timestamptz default now(),
    unique (external_id, company)
);

create index if not exists idx_jobs_company on public.jobs(company);
create index if not exists idx_jobs_title on public.jobs(title);
create index if not exists idx_jobs_first_seen on public.jobs(first_seen desc);
