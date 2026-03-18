import logging

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, KEYWORDS, UK_FILTER_TERMS
from scrapers.greenhouse import fetch_greenhouse_jobs
from scrapers.ashby import fetch_ashby_jobs
from scrapers.workday import fetch_workday_jobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def location_filter(location):
    if not location:
        return False
    location_lower = location.lower()
    return any(term in location_lower for term in UK_FILTER_TERMS)


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
        except Exception as e:
            logger.error(f"Greenhouse scraper failed for {company}: {e}")

    for company in ASHBY_COMPANIES:
        try:
            all_jobs += fetch_ashby_jobs(company)
        except Exception as e:
            logger.error(f"Ashby scraper failed for {company}: {e}")

    for source in WORKDAY_SOURCES:
        try:
            all_jobs += fetch_workday_jobs(
                source["url"],
                source["label"],
                source["country"]
            )
        except Exception as e:
            logger.error(f"Workday scraper failed for {source['label']}: {e}")

    for job in all_jobs:
        matches = keyword_filter(job["title"])
        if not matches:
            continue

        if not location_filter(job.get("location")):
            continue

        job["keyword_match"] = matches

        key = (job["external_id"], job["company"])

        if key not in existing_ids:
            new_jobs.append(job)

        store_job(job)

    logger.info(f"Processed {len(all_jobs)} jobs, {len(new_jobs)} new matches")
    return new_jobs


if __name__ == "__main__":
    new = run()
    print(f"New jobs found: {len(new)}")
