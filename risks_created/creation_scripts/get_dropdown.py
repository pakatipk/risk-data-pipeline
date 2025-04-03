import requests
from requests.auth import HTTPBasicAuth

email = "kasai.pakatip@gmail.com"
api_token = "ATATT3xFfGF04ZB_sBngfQEtujo-YObOeVbvaeqQZhQRXVaTlQiVzlbZ633V5VS01m7HpT9OyM5itj4fMxfTHxkrBUA9iUE4RMuHR9cdwX4v0zNxlCVUveEvsvPmASgeO30fQZKmW98sEMqtguF1t_g5hAHIW2f3JGnEvmOM34aojxOHt7dR1LY=8408BABE"
field_id = "customfield_10038"  # Risk Type field

url = f"https://pkasai.atlassian.net/rest/api/3/field/customfield_10041/context"

auth = HTTPBasicAuth(email, api_token)
headers = { "Accept": "application/json" }

response = requests.get(url, headers=headers, auth=auth)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
