import requests


def fetch_ashby_jobs(company_slug):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{company_slug}"
    response = requests.get(url)
    data = response.json()

    jobs = []

    for job in data.get("jobs", []):
        job_id = str(job.get("id"))

        location = None

        if job.get("locationName"):
            location = job.get("locationName")
        elif job.get("offices"):
            offices = job.get("offices")
            if len(offices) > 0:
                location = offices[0].get("name")

        constructed_url = f"https://jobs.ashbyhq.com/{company_slug}/{job_id}"

        jobs.append({
            "external_id": job_id,
            "company": company_slug,
            "title": job.get("title"),
            "location": location,
            "url": constructed_url
        })

    return jobs
