import json 
from fetch_listings import get_token, search_listings
token=get_token()
if token is None:
    print("Check app id and cert id")
else:
    data=search_listings(token,"iphone 15 pro max")
    with open("sample_data.json","w") as f:
        json.dump(data,f,indent=2)