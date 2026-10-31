import json
from fetch_listings import searchsoldlistings
data=searchsoldlistings("iphone 15 pro max ",)
with open("sold_active.json","w") as f:
    json.dump(data,f,indent=4)
