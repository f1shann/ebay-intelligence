import json
from fetch_listings import get_token, search_listings
token = get_token()
data = search_listings(token, "iphone 15 pro max")
data["itemSummaries"]=data["itemSummaries"][:20]
with open("sample_data.json","w") as f:
    json.dump(data,f,indent=2)
