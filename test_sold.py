import json
from evaluation import filter_variantsnew, median, listprices
with open("sold_data.json") as f:
    sold_list=json.load(f)
print(median(listprices(sold_list)))
print(len(sold_list["itemSummaries"]))
data=filter_variantsnew(sold_list)
print(median(listprices(data)))
print(len(data["itemSummaries"]))
print("")