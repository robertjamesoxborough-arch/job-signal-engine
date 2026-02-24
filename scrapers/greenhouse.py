import requests


def fetch_greenhouse_jobs(company_slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    response = requests.get(url)
    data = response.json()

    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "external_id": str(job.get("id")),
            "company": company_slug,
            "title": job.get("title"),
            "location": job.get("location", {}).get("name"),
            "url": job.get("absolute_url")
        })

    return jobs
