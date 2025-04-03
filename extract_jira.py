import os
import requests
from requests.auth import HTTPBasicAuth

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "DGRC"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

params = {
    "jql": "project=DGRC ORDER BY created DESC",
    "maxResults": 10,
    "fields": "summary,status,priority,resolutiondate"
}


url = f"{JIRA_URL}/rest/api/3/search"
response = requests.get(url, headers=headers, auth=auth)


response = requests.get(url, headers=headers, auth=auth)

print(response.status_code)
print(response.json())
