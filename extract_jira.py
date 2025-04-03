import os
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://pkasai.atlassian.net/rest/api/3/project"

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = "DGRC"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

response = requests.request("GET", url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_key=True, ident=4, separator=(",", ": ")))
