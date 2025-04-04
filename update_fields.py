import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Credentials
EMAIL = "kasai.pakatip@gmail.com"
API_TOKEN = "ATATT3xFfGF0cZD4YD1Sj2QMZY2pFezGnNcpv2m3PvmT6doI3VQcgB86i0LquCQeiuT2MYHdmBaTQFG1tEsIhutyZjktshkxtvG94vxMjxgEOBG_x9XUAqCTHkR7bqxUIGlAaL8PhTWCkAmPBQxIHhpjditF3rXhdN7QpkspTd4l5Of0TWZjDz8=FA446BB4"
JIRA_URL = "https://pkasai.atlassian.net"
FIELD_ID = "customfield_10046"

# CSV file path (update if different)
csv_path = "jira_issues_original.csv"

# Load the CSV
df = pd.read_csv(csv_path)

# Filter valid rows
valid_rows = df[df["Custom field (Risk type)"].notna() & df["Issue key"].notna()]

# Auth and headers
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Update each issue
for _, row in valid_rows.iterrows():
    issue_key = row["Issue key"]
    risk_type = row["Custom field (Risk type)"]

    payload = {
        "fields": {
            FIELD_ID: { "value": risk_type }
        }
    }

    response = requests.put(
        f"{JIRA_URL}/rest/api/3/issue/{issue_key}",
        headers=headers,
        auth=auth,
        json=payload
    )

    if response.status_code == 204:
        print(f"✅ Updated {issue_key} → {risk_type}")
    else:
        print(f"❌ Failed to update {issue_key} → {risk_type}: {response.status_code}")
        print(response.text)
