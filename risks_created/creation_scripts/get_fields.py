import requests
from requests.auth import HTTPBasicAuth
import os

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
url = "https://pkasai.atlassian.net/rest/api/3/field"

auth = HTTPBasicAuth(email, api_token)
headers = { "Accept": "application/json" }

response = requests.get(url, headers=headers, auth=auth)
fields = response.json()

for field in fields:
    print(f"{field['name']} - {field['id']}")
