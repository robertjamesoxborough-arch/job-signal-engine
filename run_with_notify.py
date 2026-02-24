from main import run
from notify import send_email

new_jobs = run()
send_email(new_jobs)

print(f"New jobs found: {len(new_jobs)}")
