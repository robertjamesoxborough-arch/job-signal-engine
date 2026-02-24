import requests
import os


def send_email(jobs):
    if not jobs:
        return

    api_key = os.getenv("RESEND_API_KEY")

    content = "<h2>New Job Matches</h2><ul>"
    for job in jobs:
        content += f'<li><a href="{job["url"]}">{job["company"]} – {job["title"]}</a></li>'
    content += "</ul>"

    requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "from": "Job Signal <onboarding@resend.dev>",
            "to": ["robertjamesoxborough@gmail.com"],
            "subject": f"{len(jobs)} New Job Matches Found",
            "html": content
        }
    )
