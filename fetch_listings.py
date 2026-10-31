import os 
import base64
import requests
from dotenv import load_dotenv
import json
from evaluation import conditionfix,generate_ebay_url
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
        print("Token request failed:", response.status_code, response.text)
        return None
    data=response.json()
    return data["access_token"]
def search_listings(token,query):
    search_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    search_headers= {"Authorization": "Bearer " + token, "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB"}
    search_params = {"q": query}
    search_response= requests.get(search_url, headers=search_headers, params=search_params)
    return search_response.json()
def searchsoldlistings(keyword,itemConditions,maxitems):
    apify_token=os.getenv("APIFY_API_TOKEN")
    url= f"https://api.apify.com/v2/acts/epicscrapers~ebay-sold-listings-api/run-sync-get-dataset-items?token={apify_token}"
    inputs={
        "startUrls": [
            {
                "url": generate_ebay_url(keyword,itemConditions)
            }
  		],      
	}
    try:
        response=requests.post(url,json=inputs,timeout=120)
        response.raise_for_status()
        response=response.json()
        removals=[]
        for i in range(len(response)):
            item=response[i]
            if item.get("totalPrice") is None:
                removals.append(i)
                continue
            cleaneditem={
                "title":item["title"],
                "price":{"value":str(item["totalPrice"])},
                "endedAt":item["soldAt"],
                "itemWebUrl":item["url"],
                "categoryId": item["categoryId"],
                "condition": conditionfix(item.get("condition")),
                "listingId":item["listingId"],
                "quantitySold":item["quantitySold"]
                }     
            if cleaneditem["condition"] is None:
                removals.append(i)
            else:
                response[i]=cleaneditem
        removals.reverse()
        print("removed (no totalPrice or condition):", len(removals), "of", len(response))
        for x in removals:
            response.pop(x)
        return {"itemSummaries":response}
    except requests.exceptions.RequestException as x:
        print(f"Apify Error: {x}")
        return{"itemSummaries":[]}
if __name__=="__main__":
    query=[input("What is your search")]
    results=searchsoldlistings(query)
    if results:
        with open("sold_data.json","w",encoding="utf-8") as f:
            json.dump(results,f,indent=4)
    else:
        print("No results")