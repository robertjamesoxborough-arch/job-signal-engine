import requests


def fetch_workday_jobs(base_url, company_label, country_facet=None):
    jobs = []
    offset = 0
    page_size = 50

    while True:
        payload = {
            "appliedFacets": {},
            "limit": page_size,
            "offset": offset,
            "searchText": ""
        }

        if country_facet:
            payload["appliedFacets"] = {
                "Country___Territory": [country_facet]
            }

        response = requests.post(base_url, json=payload)

        if response.status_code != 200:
            break

        data = response.json()
        listings = data.get("jobPostings", [])

        if not listings:
            break

        for job in listings:
            job_id = job.get("bulletFields", [""])[0]
            title = job.get("title")
            location = job.get("locationsText")
            external_path = job.get("externalPath")

            url = None
            if external_path:
                base = base_url.split("/wday/cxs")[0]
                url = base + external_path

            jobs.append({
                "external_id": str(job_id) + "_" + str(title),
                "company": company_label,
                "title": title,
                "location": location,
                "url": url
            })

        offset += page_size

    return jobs
