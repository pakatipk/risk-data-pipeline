import requests
from requests.auth import HTTPBasicAuth

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

# URL to get context/options for your custom dropdown field
url = "https://pkasai.atlassian.net/rest/api/3/field/customfield_10046/context"

response = requests.get(url, headers=headers, auth=auth)
print(response.status_code)
print(response.json())