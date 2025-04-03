import requests
from requests.auth import HTTPBasicAuth

email = "kasai.pakatip@gmail.com"       # Replace with your Atlassian email
api_token = "ATATT3xFfGF04ZB_sBngfQEtujo-YObOeVbvaeqQZhQRXVaTlQiVzlbZ633V5VS01m7HpT9OyM5itj4fMxfTHxkrBUA9iUE4RMuHR9cdwX4v0zNxlCVUveEvsvPmASgeO30fQZKmW98sEMqtguF1t_g5hAHIW2f3JGnEvmOM34aojxOHt7dR1LY=8408BABE"           # Replace with your Jira API token
url = "https://pkasai.atlassian.net/rest/api/3/field"

auth = HTTPBasicAuth(email, api_token)
headers = { "Accept": "application/json" }

response = requests.get(url, headers=headers, auth=auth)
fields = response.json()

for field in fields:
    print(f"{field['name']} - {field['id']}")
