import os 
import sys
import json
from fetch_listings import get_token, search_listings, searchsoldlistings
from evaluation import removeblacklists,totalcost,median,listprices,deviation,remove_outliers,cv,filter_model,filter_variants,conditionfix,dedupe,withinwindow
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
    with open(os.path.join(base_dir,"sold_active.json")) as f:
        sold_list=json.load(f)
    conditionlist=["New","Opened","Refurbished","Used"]
    for i in range(2):
        conditionstoretry=[]
        for condition in conditionlist:
            activekept={"itemSummaries":[]}
            for item in data["itemSummaries"]:
                if conditionfix(item.get("condition"))==condition:
                    activekept["itemSummaries"].append(item)
            soldkept={"itemSummaries":[]}
            for item in sold_list["itemSummaries"]:
                if item.get("condition")==condition:
                    soldkept["itemSummaries"].append(item)
            print(condition,":")      
            activekept=removeblacklists(activekept)
            activekept=filter_model(activekept,query)
            activekept=filter_variants(activekept)
            activeprices=remove_outliers(listprices(activekept))
            soldkept=removeblacklists(soldkept)
            soldkept=filter_variants(soldkept)
            soldkept=withinwindow(soldkept)
            soldprices=remove_outliers(listprices(soldkept))
            if len(activeprices)==0:
                print("no listings left after filtering")
                continue
            if len(soldprices)<15:
                if i==0:
                    print("Unreliable Baseline(retrying for more sold listings)")
                    conditionstoretry.append(condition)
                else:
                    print("Still unreliable after retry")
                continue
            base=median(soldprices)
            print("baseline median(based on sold prices):", base)
            print("cv:", round(cv(soldprices),1))
            newitemSummaries=[]
            for item in activekept["itemSummaries"]:
                if round(totalcost(item),2) in activeprices:
                    newitemSummaries.append(item)
            activekept["itemSummaries"]=newitemSummaries
            newitemSummaries=[]
            # for item in soldkept["itemSummaries"]:
            #     if round(totalcost(item),2) in soldprices:
            #         newitemSummaries.append(item)
            # soldkept["itemSummaries"]=newitemSummaries
            for item in activekept["itemSummaries"]:
                cost=totalcost(item)
                d=deviation(base,cost)
                p=profit(base,cost,weight,length,width,height)
                if p>minprofit:
                    print(item["title"],",total cost(including shipping):", round(cost,2),",deviation:", round(d,1),",profit:",round(p,2),item["itemWebUrl"])
        if conditionstoretry!=[]:
            response=searchsoldlistings(query,conditionstoretry,25*len(conditionstoretry))
            with open(os.path.join(base_dir,"sold_active.json")) as f:
                sold_data=json.load(f)
            sold_data["itemSummaries"].extend(response["itemSummaries"])
            sold_data=withinwindow(dedupe(sold_data))
            with open(os.path.join(base_dir,"sold_active.json"),"w") as f:
                json.dump(sold_data,f,indent=4)
            sold_list=sold_data
            conditionlist=conditionstoretry
        else:
            break
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