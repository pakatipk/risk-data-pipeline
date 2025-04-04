import os
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Jira config
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

# Search Jira issues from RCM project
url = f"{JIRA_URL}/rest/api/3/search"
params = {
    "jql": f"project={PROJECT_KEY}",
    "maxResults": 100,
    "fields": "*all"
}

response = requests.get(url, headers=headers, auth=auth, params=params)

if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    exit()

issues_data = response.json().get("issues", [])
issues = []

for issue in issues_data:
    fields = issue["fields"]
    issues.append({
        "Key": issue["key"],
        "Summary": fields.get("summary"),
        "Status": fields.get("status", {}).get("name"),
        "Priority": fields.get("priority", {}).get("name"),
        "Risk Type": fields.get("customfield_10046"),
        "Due Date": fields.get("duedate"),
        "Resolved Date": fields.get("customfield_10050"),
        "Resolution Type": fields.get("customfield_10049"),
        "Component": fields.get("components"),
        "Assignee (S)": fields.get("customfield_10047"),
        "Reporter (S)": fields.get("customfield_10048"),
    })

# Save to CSV
df = pd.DataFrame(issues)
df.to_csv("jira_issues.csv", index=False)
print("✅ Issues saved to jira_issues.csv")
