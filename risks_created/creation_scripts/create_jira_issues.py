import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Jira credentials and project info
JIRA_DOMAIN = "https://pkasai.atlassian.net"
PROJECT_KEY = "DGRC"
EMAIL = "kasai.pakatip@gmail.com"
API_TOKEN = "ATATT3xFfGF04ZB_sBngfQEtujo-YObOeVbvaeqQZhQRXVaTlQiVzlbZ633V5VS01m7HpT9OyM5itj4fMxfTHxkrBUA9iUE4RMuHR9cdwX4v0zNxlCVUveEvsvPmASgeO30fQZKmW98sEMqtguF1t_g5hAHIW2f3JGnEvmOM34aojxOHt7dR1LY=8408BABE"  # 🔐 Replace with your actual API token safely!

# Load the CSV file
df = pd.read_csv("jira_issues.csv")

# Auth and headers
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Convert text to Atlassian Document Format (ADF)
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
                        "text": str(text)
                    }
                ]
            }
        ]
    }

# Function to create a Jira issue
def create_jira_issue(row):
    fields = {
        "project": { "key": PROJECT_KEY },
        "summary": row["Summary"],
        "description": to_adf(row["Description"]),
        "issuetype": { "name": "Task" },
        "priority": { "name": row["Priority"] },

        # Custom fields using correct format
        "customfield_10015": row["Start Date"],                         # Start Date
        "customfield_10038": { "value": row["Risk Type"] },            # Risk Type
        "customfield_10042": { "value": row["Assignee"] },             # Simulated Assignee
        "customfield_10041": { "value": row["Reporter"] },             # Simulated Reporter
        "customfield_10043": { "value": row["Component"] },            # Component
    }

    # Optional fields
    if pd.notna(row["Resolution Type"]):
        fields["customfield_10040"] = { "value": row["Resolution Type"] }
    if pd.notna(row["Resolved Date"]):
        fields["customfield_10039"] = row["Resolved Date"]
    if pd.notna(row["Due Date"]):
        fields["duedate"] = row["Due Date"]

    # Make the API call
    response = requests.post(
        f"{JIRA_DOMAIN}/rest/api/3/issue",
        json={"fields": fields},
        headers=headers,
        auth=auth
    )

    if response.status_code == 201:
        print(f"Issue created: {response.json()['key']}")
    else:
        print(f"Failed to create issue: {response.status_code} - {response.text}")

# Loop to create issues
for _, row in df.iterrows():
    create_jira_issue(row)
