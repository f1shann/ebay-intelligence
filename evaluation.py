import statistics
import re
def sold_to_active(sold_list):
    items=[]
    for item in sold_list:
        items.append({
            "title":item["title"],
            "price":{"value":str(item["totalPrice"])},
            "itemWebUrl":item["url"],
            "endedAt":item["endedAt"],
            "categoryId":item["categoryId"],
            "condition":item["condition"]
        })
    return {"itemSummaries":items}
def totalcost(item):
    price=float(item["price"]["value"])
    shipping=0
    if item.get("shippingOptions"):
        shipping=float(item["shippingOptions"][0]["shippingCost"]["value"])
    return price+shipping
def filter_model(data,query):
    numbers=[w for w in query.lower().split() if w.isdigit()]
    kept=[]
    for item in data["itemSummaries"]:
        title_words=[w.strip(".,()!?:;\"'") for w in item["title"].lower().split()]
        if all(n in title_words for n in numbers):
            kept.append(item)
    data["itemSummaries"]=kept
    return data
def listprices(data):
    prices=[]
    for item in data["itemSummaries"]:
        prices.append(totalcost(item))
    prices.sort()
    return prices
def has_phrase(words,phrase):
    for i in range(len(words)-len(phrase)+1):
        if words[i:i+len(phrase)]==phrase:
            return True
    return False
def median(prices):
    return statistics.median(prices)
def remove_outliers(prices):
    if len(prices)<4:
        return prices
    q1,_,q3=statistics.quantiles(prices,n=4)
    iqr=q3-q1
    lowerbound,upperbound=q1-(1.5*iqr),q3+(1.5*iqr)
    prices=[p for p in prices if lowerbound <=p<=upperbound]
    return prices
def removeblacklists(data):
    wordblacklist = ["faulty", "case", "broken", "cracked", "locked", "untested", "as-is", "asis", "defect", "defective", "damaged", "repair", "repairs", "spares", "scrap", "junk", "frp", "mdm", "bypass", "dummy", "replica", "clone", "fake", "counterfeit", "housing", "shell", "body", "digital", "download", "pdf", "poster", "print", "wanted", "demo"]
    phraseblacklist = [["box", "only"], ["empty", "box"], ["cover", "only"], ["body", "only"], ["screen", "protector"], ["charger", "only"], ["cable", "only"], ["for", "parts"], ["parts", "only"], ["spare", "parts"], ["spares", "or", "repair"], ["not", "working"], ["does", "not", "work"], ["needs", "repair"], ["not", "tested"], ["read", "description"], ["read", "desc"], ["read", "before", "buying"], ["icloud", "lock"], ["activation", "lock"], ["blacklisted", "imei"], ["digital", "delivery"], ["digital", "copy"], ["job", "lot"], ["bundle", "of"], ["display", "model"]]
    filteredlistings=[]
    for item in data["itemSummaries"]:
        words = [w.strip(".,()!?:;\"'") for w in item["title"].lower().split()]
        if any (word in words for word in wordblacklist):
            continue
        if any(has_phrase(words,p) for p in phraseblacklist):
            continue
        filteredlistings.append(item)
    data["itemSummaries"]=filteredlistings
    return data
def deviation(median,price):
    if median==0:
        return 0
    return 100*(median-price)/median
def cv(prices):
    if len(prices)<2:
        return 0
    return statistics.stdev(prices) / statistics.mean(prices)*100
def filter_variants(data):
    kept=[]
    for item in data["itemSummaries"]:
        if re.search(r"\d/\d", item["title"]) is None:
            kept.append(item)
    data["itemSummaries"]=kept
    return data
def filter_variantsnew(data):
    kept=[]
    for item in data["itemSummaries"]:
        if re.search(r"\d/\d|\d+\s?(?:gb|tb)\s*/", item["title"], re.I) is None:
            kept.append(item)
    data["itemSummaries"]=kept
    return data
def conditionfix(conditionId):
    if conditionId is None:
        return None
    if conditionId in (1000,1750):
        return "New"
    if conditionId==1500:
        return "Opened"
    if conditionId in (2750,2990,4000,3000):
        return "Used"
    if conditionId in (2000, 2010, 2020, 2030, 2500):
        return "Refurbished"
    if conditionId in (5000, 6000, 7000):
        return None
    return None