import os 
import json
from fetch_listings import get_token, search_listings
from evaluation import removeblacklists,median,listprices,remove_outliers,deviation,cv
def find_deals(query):
    if os.getenv("APP_ID"):
        token=get_token()
        data=search_listings(token,query)
    else:
        print("no keys found using sample data")
        with open("sample_data.json") as f:
            data=json.load(f)
    data=removeblacklists(data)
    prices=remove_outliers(listprices(data))
    if len(prices)==0:
        print("no listings left after filtering")
        return
    base=median(prices)
    print("baseline median:", base)
    print("cv:", round(cv(prices),1))
    for item in data["itemSummaries"]:
        price=float(item["price"]["value"])
        shipping=0
        if item.get("shippingOptions"):
            shipping=float(item["shippingOptions"][0]["shippingCost"]["value"])
        cost=price+shipping
        d=deviation(base,cost)
        if d>20:
            print(item["title"], cost, round(d,1),item["itemWebUrl"])
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
