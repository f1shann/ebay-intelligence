import os 
import base64
import requests
import statistics
from dotenv import load_dotenv
load_dotenv()
def get_token():
        app_id=os.getenv("APP_ID")
        cert_id=os.getenv("CERT_ID")
        credentials=app_id + ":" + cert_id
        encoded=base64.b64encode(credentials.encode()).decode()
        headers = {"Authorization": "Basic " + encoded}
        body = {"grant_type": "client_credentials", "scope":
                "https://api.ebay.com/oauth/api_scope"}
        url="https://api.ebay.com/identity/v1/oauth2/token"
        response=requests.post(url, headers=headers, data=body)
        if response.status_code != 200:
                print("Token request failed:", response.status_code, response.txt)
                return None
        data=response.json()
        return data["access_token"]
def searchlistings(token,query):
        search_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        search_headers= {"Authorization": "Bearer " + token, "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB"}
        search_params = {"q": query}
        search_response= requests.get(search_url, headers=search_headers, params=search_params)
        return search_response.json()
if __name__=="__main__":
        query=input("What is your search")
        token=get_token()
        searchlistings(token,query)        

