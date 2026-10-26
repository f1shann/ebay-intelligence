import json
from evaluation import sold_to_active
with open("sold_data.json") as f:
    sold_list=json.load(f)
data=sold_to_active(sold_list)
with open("sold_active.json","w") as f:
    json.dump(data,f,indent=4)
