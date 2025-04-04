import pandas as pd
import requests
import os
from requests.auth import HTTPBasicAuth

# Credentials
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"
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
