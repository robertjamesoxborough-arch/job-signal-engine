import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import run
from notify import send_email


def handler(request):
    new_jobs = run()
    send_email(new_jobs)
    return {
        "statusCode": 200,
        "body": f"Job engine executed. {len(new_jobs)} new jobs found."
    }
