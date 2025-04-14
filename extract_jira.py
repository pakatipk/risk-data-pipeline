import os
import gspread
from google.auth.transport.requests import Request  # Corrected import syntax
from google.oauth2.service_account import Credentials  # Corrected import syntax
import json
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = "https://pkasai.atlassian.net"
PROJECT_KEY = "RCM"


# Google Sheets API Credentials from GitHub Secrets
google_creds_json = os.getenv('GOOGLE_SHEET_CREDENTIALS_JSON')
google_creds = json.loads(google_creds_json)

# Jira config
auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

# Search Jira issues from RCM project
url = f"{JIRA_URL}/rest/api/3/search"
params = {
    "jql": "project = RCM",  # This will fetch issues from the RCM project
    "maxResults": "100",      # Fetch up to 100 issues
    "fields": "*all"          # Fetch all fields
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

# Function to handle NoneType values
def get_field_value(field):
    return field if field is not None else ""

for issue in issues_data:
    fields = issue["fields"]
    issues.append({
        "Key": issue.get("key", ""),
        "Summary": fields.get("summary", ""),
        "Status": fields.get("status", {}).get("name", ""),
        "Priority": fields.get("priority", {}).get("name", ""),
        "Due Date": fields.get("duedate", ""),
        "Resolved Date": fields.get("customfield_10050", ""),
        
        # Ensure Resolution Type is safely handled
        "Resolution Type": fields.get("customfield_10049", {}).get("value", "") if fields.get("customfield_10049") else "",
        
        # Flatten Component field and safely handle if no components
        "Component": ', '.join([component['name'] for component in fields.get("components", [])]) if fields.get("components") else "",
        
        # Safely handle Assignee and Reporter fields
        "Assignee (S)": fields.get("customfield_10047", {}).get("value", "") if fields.get("customfield_10047") else "",
        "Reporter (S)": fields.get("customfield_10048", {}).get("value", "") if fields.get("customfield_10048") else "",
        
        # Flatten Risk Type field and safely handle NoneType
        "Risk Type": fields.get("customfield_10046", {}).get("value", "") if fields.get("customfield_10046") else ""
    })

# Convert the data to a DataFrame
df = pd.DataFrame(issues)

print("Data fetched from Jira:", df)

# Google Sheets API authorization
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Corrected code: passing scopes as a keyword argument
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
# Authorize gspread client
client = gspread.authorize(creds)



# Open the Google Sheet by name (replace with your Google Sheet name)
sheet = client.open('jira-extract').sheet1  # Replace 'jira-extract' with your sheet name

# Push the data to Google Sheets
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Jira issues pushed to Google Sheets!")

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

