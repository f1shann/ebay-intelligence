import os 
import base64
import requests
import statistics
from dotenv import load_dotenv
load_dotenv()
app_id=os.getenv("APP_ID")
cert_id=os.getenv("CERT_ID")
credentials=app_id + ":" + cert_id
encoded=base64.b64encode(credentials.encode()).decode()
headers = {"Authorization": "Basic " + encoded}
body = {"grant_type": "client_credentials", "scope":
        "https://api.ebay.com/oauth/api_scope"}
url="https://api.ebay.com/identity/v1/oauth2/token"
response=requests.post(url, headers=headers, data=body)
data=response.json()
access_token=data["access_token"]
search_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
search_headers= {"Authorization": "Bearer " + access_token, "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB"}
search_params = {"q": "iphone 13"}
search_response= requests.get(search_url, headers=search_headers, params=search_params)
results=search_response.json()
prices=[]
for item in results.get("itemSummaries",[]):
    prices.append(float(item["price"]["value"]))
print(statistics.median(prices))

