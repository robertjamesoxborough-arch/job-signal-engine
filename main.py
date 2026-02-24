from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, KEYWORDS, UK_FILTER_TERMS
from scrapers.greenhouse import fetch_greenhouse_jobs
from scrapers.ashby import fetch_ashby_jobs
from scrapers.workday import fetch_workday_jobs

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

GREENHOUSE_COMPANIES = [
    "monzo",
    "tide",
    "spotify",
    "elastic",
    "canva",
    "github",
    "hubspot",
    "headspace",
    "shopify"
]

ASHBY_COMPANIES = [
    "claylabs"
]

WORKDAY_SOURCES = [
    {
        "url": "https://relx.wd3.myworkdayjobs.com/wday/cxs/relx/relx/jobs",
        "label": "relx",
        "country": "29247e57dbaf46fb855b224e03170bc7"
    }
]


def keyword_filter(title):
    title_lower = title.lower()
    return [k for k in KEYWORDS if k in title_lower]


def store_job(job):
    supabase.table("jobs") \
        .upsert(job, on_conflict="external_id,company") \
        .execute()


def run():
    all_jobs = []

    for company in GREENHOUSE_COMPANIES:
        try:
            jobs = fetch_greenhouse_jobs(company)
            all_jobs.extend(jobs)
        except Exception:
            continue

    for company in ASHBY_COMPANIES:
        try:
            jobs = fetch_ashby_jobs(company)
            all_jobs.extend(jobs)
        except Exception:
            continue

    for source in WORKDAY_SOURCES:
        try:
            jobs = fetch_workday_jobs(
                source["url"],
                source["label"],
                source.get("country")
            )
            all_jobs.extend(jobs)
        except Exception:
            continue

    for job in all_jobs:
        matches = keyword_filter(job["title"])
        if not matches:
            continue

        job["keyword_match"] = matches
        store_job(job)


if __name__ == "__main__":
    run()
