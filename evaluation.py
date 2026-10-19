import statistics
def listprices(data):
    prices=[]
    for item in data["itemSummaries"]:
        prices.append(float(item["price"]["value"]))
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
    wordblacklist = ["faulty", "broken", "cracked", "locked", "untested", "as-is", "asis", "defect", "defective", "damaged", "repair", "repairs", "spares", "scrap", "junk", "frp", "mdm", "bypass", "dummy", "replica", "clone", "fake", "counterfeit", "housing", "shell", "body", "digital", "download", "pdf", "poster", "print", "wanted", "demo"]
    phraseblacklist = [["box", "only"], ["empty", "box"], ["case", "only"], ["cover", "only"], ["body", "only"], ["screen", "protector"], ["charger", "only"], ["cable", "only"], ["for", "parts"], ["parts", "only"], ["spare", "parts"], ["spares", "or", "repair"], ["not", "working"], ["does", "not", "work"], ["needs", "repair"], ["not", "tested"], ["read", "description"], ["read", "desc"], ["read", "before", "buying"], ["icloud", "lock"], ["activation", "lock"], ["blacklisted", "imei"], ["digital", "delivery"], ["digital", "copy"], ["job", "lot"], ["bundle", "of"], ["display", "model"]]
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