import requests
from requests.auth import HTTPBasicAuth
import os

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
field_id = "customfield_10038"  # Risk Type field

url = f"https://pkasai.atlassian.net/rest/api/3/field/customfield_10041/context"

auth = HTTPBasicAuth(email, api_token)
headers = { "Accept": "application/json" }

response = requests.get(url, headers=headers, auth=auth)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
