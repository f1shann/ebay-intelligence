import os 
import sys
import json
from fetch_listings import get_token, search_listings
from evaluation import removeblacklists,totalcost,median,listprices,deviation,remove_outliers,cv,filter_model,filter_variants
from profit import profit
weight=0.3
length=20.0
width=12.0
height=4.0
base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
def find_deals(query):
    if os.getenv("APP_ID"):
        token=get_token()
        data=search_listings(token,query)
        minprofit=40
    else:
        print("no keys found, using sample data (only covers 'iphone 15 pro max')")
        with open(os.path.join(base_dir, "sample_data.json")) as f:
            data = json.load(f)
        minprofit=20
    data=removeblacklists(data)
    data=filter_model(data,query)
    data=filter_variants(data)
    activeprices=remove_outliers(listprices(data))
    with open(os.path.join(base_dir,"sold_active.json")) as f:
        sold_list=json.load(f)
    sold_list=removeblacklists(sold_list)
    sold_list=filter_variants(sold_list)
    soldprices=remove_outliers(listprices(sold_list))
    if len(activeprices)==0:
        print("no listings left after filtering")
        return
    base=median(soldprices)
    print("baseline median(based on sold prices):", base)
    print("cv:", round(cv(soldprices),1))
    newitemSummaries=[]
    for item in data["itemSummaries"]:
        if totalcost(item) in activeprices:
            newitemSummaries.append(item)
    data["itemSummaries"]=newitemSummaries
    newitemSummaries=[]
    for item in sold_list["itemSummaries"]:
        if totalcost(item) in soldprices:
            newitemSummaries.append(item)
    sold_list["itemSummaries"]=newitemSummaries
    for item in data["itemSummaries"]:
        cost=totalcost(item)
        d=deviation(base,cost)
        p=profit(base,cost,weight,length,width,height)
        if p>minprofit:
            print(item["title"],",total cost(including shipping):", round(cost,2),",deviation:", round(d,1),",profit:",round(p,2),item["itemWebUrl"])
def main():
    print("Marketplace Intelligence started.")
    while True:
        command = input("> ").strip().lower()
        if command == "quit":
            break
        if command.startswith("find "):
            find_deals(command[5:])
            continue
        print(f"Unknown command: {command}")
if __name__ == "__main__":
    main()