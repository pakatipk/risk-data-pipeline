import requests
import pandas as pd
import os
from requests.auth import HTTPBasicAuth

# Jira credentials and project info
JIRA_DOMAIN = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"
EMAIL = "kasai.pakatip@gmail.com"
API_TOKEN = "ATATT3xFfGF0cZD4YD1Sj2QMZY2pFezGnNcpv2m3PvmT6doI3VQcgB86i0LquCQeiuT2MYHdmBaTQFG1tEsIhutyZjktshkxtvG94vxMjxgEOBG_x9XUAqCTHkR7bqxUIGlAaL8PhTWCkAmPBQxIHhpjditF3rXhdN7QpkspTd4l5Of0TWZjDz8=FA446BB4"

# Load the CSV
df = pd.read_csv("jira_issues.csv")  # or whatever the current file is

# Auth and headers
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Convert text to Atlassian Document Format
def to_adf(text):
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": str(text) if pd.notna(text) else ""
                    }
                ]
            }
        ]
    }

custom_select_fields = [
    "customfield_10046",  # Risk Type
    "customfield_10047",  # Assignee (S)
    "customfield_10048",  # Reporter (S)
    "customfield_10049",  # Resolution Type
]

# Create a Jira issue from a row
def create_jira_issue(row):
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": row["summary"],
        "description": to_adf(row.get("description", "")),
        "issuetype": {"name": row.get("issuetype", "Task")},
    }

    # Priority
    if pd.notna(row.get("priority")):
        fields["priority"] = {"name": row["priority"]}

    # Components (optional and only if added to screen)
    if pd.notna(row.get("components")):
        fields["components"] = [{"name": row["components"]}]

    # Due Date
    if pd.notna(row.get("duedate")):
        fields["duedate"] = row["duedate"]

    # Select list custom fields
    for field in custom_select_fields:
        if field in row and pd.notna(row[field]):
            fields[field] = {"value": row[field]}

    # Remove None values to prevent 400 errors
    fields = {k: v for k, v in fields.items() if v is not None}

    # Send POST request to create issue
    response = requests.post(
        f"{JIRA_DOMAIN}/rest/api/3/issue",
        json={"fields": fields},
        headers=headers,
        auth=auth
    )

    if response.status_code == 201:
        print(f"Issue created: {response.json()['key']}")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

# Create issues
for _, row in df.iterrows():
    create_jira_issue(row)