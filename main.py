from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, KEYWORDS
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

ASHBY_COMPANIES = ["claylabs"]

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


def fetch_existing_ids():
    res = supabase.table("jobs").select("external_id,company").execute()
    return {(r["external_id"], r["company"]) for r in res.data}


def store_job(job):
    supabase.table("jobs") \
        .upsert(job, on_conflict="external_id,company") \
        .execute()


def run():
    existing_ids = fetch_existing_ids()
    new_jobs = []

    all_jobs = []

    for company in GREENHOUSE_COMPANIES:
        try:
            all_jobs += fetch_greenhouse_jobs(company)
        except:
            pass

    for company in ASHBY_COMPANIES:
        try:
            all_jobs += fetch_ashby_jobs(company)
        except:
            pass

    for source in WORKDAY_SOURCES:
        try:
            all_jobs += fetch_workday_jobs(
                source["url"],
                source["label"],
                source["country"]
            )
        except:
            pass

    for job in all_jobs:
        matches = keyword_filter(job["title"])
        if not matches:
            continue

        key = (job["external_id"], job["company"])

        if key not in existing_ids:
            new_jobs.append(job)

        store_job(job)

    return new_jobs


if __name__ == "__main__":
    new = run()
    print(f"New jobs found: {len(new)}")
