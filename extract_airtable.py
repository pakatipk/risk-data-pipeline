import requests
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import json

# Google Sheets API Credentials from GitHub Secrets
google_creds_json = os.getenv('GOOGLE_SHEET_CREDENTIALS_JSON')
google_creds = json.loads(google_creds_json)

# Airtable API configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Risks"  # Your Airtable Table Name
SHEET_NAME = "airtable_extract"  # Replace with your target Google Sheet name

# Airtable API URL
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# Assignee to Email mapping
assignee_mapping = {
    "recjfz1K9NP4Q4jb2": "airi.matsumoto@example.com",
    "recilmZDQRUcmQxfS": "alice.nakamura@example.com",
    "receIs96XJzIFFrcJ": "rina.fujimoto@example.com",
    "recSCBQpmJ1sdhzZh": "sota.fujikawa@example.com",
    "recY0l9J5WX3BKDNv": "ryota.inoue@example.com",
    "recDAq25uW1g2l6i5": "yuki.tanaka@example.com",
    "recBTc0H0V1U5JL34": "takuya.mori@example.com",
    "rec5Ylj0a3LyVuKmy": "daichi.aoyama@example.com",
    "recS3EHkkFpzuN7Dr": "erika.watanabe@example.com",
    "rec1v8TMErooKX8cc": "naomi.ishikawa@example.com",
    "recetYeyEmYOI6UMa": "hiroki.yamashita@example.com",
    "recQaVoKwTEQUe9OB": "haruto.sato@example.com",
    "reck0LGK3YVkrhU43": "takumi.nishida@example.com",
    "rec5a0QYVUOHkHN7D": "aya.kitamura@example.com",
    "recIwVwAziJhEkz9Y": "kenji.takahashi@example.com",
    "rechYNXa94V7gqbFg": "daiki.kobayashi@example.com"
}

# Reporter to Email mapping
reporter_mapping = {
    "reccYkK2ecMXypT2v": "haruka.kobayashi@example.com",
    "recKsG4OSdRitBxt0": "shohei.suzuki@example.com",
    "recIS2ofjfWlTWEAY": "mei.kuroda@example.com"
}

# Component to Name mapping
component_mapping = {
    "rec6g5lRpyO4OYbO7": "Finance App",
    "recH6388UYaP8Jz1d": "System A",
    "recgArQRyYSEAgi7g": "API Gateway",
    "rec8KfRQva3R67hJT": "Cloud Service X",
    "recRT44NeRFSIjmEw": "Customer DB",
    "recswaUvQCm7J8EnU": "System B",
    "recXNPTHBMa4zDQAZ": "HR Portal",
    "reck9EfC2gdNwMAKU": "Admin Console",
    "recOJvXQyWnVKwti0": "Mobile App Gateway",
    "rectvCL64TS2Y1CXP": "Data Integration Hub",
    "recL9IQb7RoUAsNT8": "Data Warehouse"
}

# Function to fetch all data from Airtable with pagination
def fetch_airtable_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    # List to store all records
    all_records = []

    # Initial params with no offset
    params = {}

    while True:
        # Fetch data from Airtable API
        response = requests.get(AIRTABLE_URL, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])
            all_records.extend(records)  # Add fetched records to all_records list

            # If there's more data, update params with the offset for pagination
            if "offset" in data:
                params["offset"] = data["offset"]
            else:
                break  # No more records to fetch, exit the loop
        else:
            print(f"Error fetching data: {response.status_code}")
            break  # Exit if there is an error

    return all_records

# Function to map Assignee ID to Email
def map_assignee_ids_to_email(record, field_name):
    assignee_ids = record.get(field_name)
    if isinstance(assignee_ids, list):  # Check if the field is a list of IDs
        assignee_ids = assignee_ids[0]  # Extract the first ID (if there's only one)
    
    if assignee_ids and assignee_ids in assignee_mapping:
        return assignee_mapping[assignee_ids]  # Replace ID with email
    return assignee_ids  # If no mapping found, return the ID as is

# Function to map Reporter ID to Email
def map_reporter_ids_to_email(record, field_name):
    reporter_ids = record.get(field_name)
    if isinstance(reporter_ids, list):  # Check if the field is a list of IDs
        reporter_ids = reporter_ids[0]  # Extract the first ID (if there's only one)
    
    if reporter_ids and reporter_ids in reporter_mapping:
        return reporter_mapping[reporter_ids]  # Replace ID with email
    return reporter_ids  # If no mapping found, return the ID as is

# Function to map Component ID to Name
def map_component_ids_to_name(record, field_name):
    component_ids = record.get(field_name)
    if isinstance(component_ids, list):  # Check if the field is a list of IDs
        component_ids = component_ids[0]  # Extract the first ID (if there's only one)
    
    if component_ids and component_ids in component_mapping:
        return component_mapping[component_ids]  # Replace ID with name
    return component_ids  # If no mapping found, return the ID as is

# Convert the fetched records into a pandas DataFrame, including the 'id' field
records = fetch_airtable_data()

# Apply the mappings to replace IDs with emails/names
for record in records:
    record["fields"]["Assignee"] = map_assignee_ids_to_email(record["fields"], "Assignee")
    record["fields"]["Reporter"] = map_reporter_ids_to_email(record["fields"], "Reporter")
    record["fields"]["Component"] = map_component_ids_to_name(record["fields"], "Component")

df = pd.DataFrame([{
    **record["fields"],  # Include all fields
    "Record ID": record["id"]  # Add the Record ID as a separate column
} for record in records])

# Convert all values to string type
df = df.astype(str)

# Clean up NaN and infinite values (if necessary)
df = df.replace([float('nan'), float('inf'), float('-inf')], "")

# Function to authorize and get Google Sheets client
def authorize_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEET_CREDENTIALS_JSON, scope)
    client = gspread.authorize(creds)
    return client

# Function to upload data to Google Sheets
def upload_to_google_sheets(df):
    # Authorize and open the Google Sheet
    client = authorize_google_sheets()
    sheet = client.open(SHEET_NAME).sheet1  # Open the first sheet of the Google Sheet
    
    # Convert DataFrame to a list of lists (the format Google Sheets API expects)
    data = [df.columns.values.tolist()] + df.values.tolist()
    
    # Upload the data to the sheet
    sheet.update(data)

# Now upload the cleaned data to Google Sheets
upload_to_google_sheets(df)

#print(records[0]["fields"])  # Print the fields of the first record'
#print(df['Assignee'])
