import requests
from requests.auth import HTTPBasicAuth

EMAIL = "kasai.pakatip@gmail.com"
API_TOKEN = "ATATT3xFfGF0cZD4YD1Sj2QMZY2pFezGnNcpv2m3PvmT6doI3VQcgB86i0LquCQeiuT2MYHdmBaTQFG1tEsIhutyZjktshkxtvG94vxMjxgEOBG_x9XUAqCTHkR7bqxUIGlAaL8PhTWCkAmPBQxIHhpjditF3rXhdN7QpkspTd4l5Of0TWZjDz8=FA446BB4"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = { "Accept": "application/json" }

# URL to get context/options for your custom dropdown field
url = "https://pkasai.atlassian.net/rest/api/3/field/customfield_10046/context"

response = requests.get(url, headers=headers, auth=auth)
print(response.status_code)
print(response.json())