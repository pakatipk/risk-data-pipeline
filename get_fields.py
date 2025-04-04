import os
import requests
from requests.auth import HTTPBasicAuth

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

url = "https://pkasai.atlassian.net/rest/api/3/field"

response = requests.get(url, headers=headers, auth=auth)
fields = response.json()

for field in fields:
    print(f"{field['name']} - {field['id']}")
