import requests
import pandas as pd
import os
from requests.auth import HTTPBasicAuth

# Jira credentials and project info
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"

# Load the CSV
df = pd.read_csv("jira_issues_original.csv")  # or whatever the current file is

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


# Create a Jira issue from a row
def create_jira_issue(row):
    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": row["Summary"],  # Summary is correct in your CSV
        "description": to_adf(row.get("Description", "")),  # Description is 'Description' in your CSV
        "issuetype": {"name": row.get("issuetype", "Task")},  # Check if 'issuetype' is in your CSV
    }

    # Priority
    if pd.notna(row.get("Priority")):
        fields["priority"] = {"name": row["Priority"]}

    # Components (optional and only if added to screen)
    if pd.notna(row.get("Component")):
        fields["components"] = [{"name": row["Component"]}]

    # Due Date
    if pd.notna(row.get("Due date")):
        fields["duedate"] = row["Due date"]

    if pd.notna(row.get("Resolved date")):
        fields["customfield_10050"] = row["Resolved date"]

    # Custom fields
    if pd.notna(row.get("Risk type")):
        fields["customfield_10046"] = {"value": row["Risk type"]}
    
    if pd.notna(row.get("Assignee (S)")):
        fields["customfield_10047"] = {"value": row["Assignee (S)"]}

    if pd.notna(row.get("Reporter (S)")):
        fields["customfield_10048"] = {"value": row["Reporter (S)"]}

    if pd.notna(row.get("Resolution type")):
        fields["customfield_10049"] = {"value": row["Resolution type"]}


    

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