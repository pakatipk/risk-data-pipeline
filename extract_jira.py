import os
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://pkasai.atlassian.net/rest/api/3/project"

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

#EMAIL = "kasai.pakatip@gmail.com"
#API_TOKEN = "ATATT3xFfGF0cZD4YD1Sj2QMZY2pFezGnNcpv2m3PvmT6doI3VQcgB86i0LquCQeiuT2MYHdmBaTQFG1tEsIhutyZjktshkxtvG94vxMjxgEOBG_x9XUAqCTHkR7bqxUIGlAaL8PhTWCkAmPBQxIHhpjditF3rXhdN7QpkspTd4l5Of0TWZjDz8=FA446BB4"

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

response = requests.request("GET", url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
