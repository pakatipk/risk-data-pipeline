import requests  # Assuming you are using requests for API calls
import os
import pandas as pd
from requests.auth import HTTPBasicAuth

# Environment variables for sensitive information
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"

# Authentication setup
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

# Read data from the CSV file
df = pd.read_csv("jira_issues_original.csv")  # or whatever the current file is

# Define a function to get Jira fields

def get_jira_fields(JIRA_URL, auth):
    url = f"{JIRA_URL}/rest/api/3/field"
    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        fields = response.json()
        for field in fields:
            print(f"{field['name']} - {field['id']}")
        #return fields  # Return fields so you can use them elsewhere
    else:
        print(f"Error fetching fields: {response.status_code}")
        print(response.text)

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
                        "text": str(text) if pd.notna(text) else ""
                    }
                ]
            }
        ]
    }

# Function to create Jira issue
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
        f"{JIRA_URL}/rest/api/3/issue",
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


# Main function to demonstrate the functionality
def main():
    #Extract Jira fields
    get_jira_fields(JIRA_URL, auth)

    #Create Jira issues based on CSV data
    #for _, row in df.iterrows():
        #create_jira_issue(row)

if __name__ == "__main__":
    main()