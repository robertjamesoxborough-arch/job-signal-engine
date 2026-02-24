import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import run

def handler(request, context):
    run()
    return {
        "statusCode": 200,
        "body": "Job engine executed successfully"
    }
