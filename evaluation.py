import statistics
def listprices(data):
    prices=[]
    for item in data["itemSummaries"]:
        prices.append(float(item["price"]["value"]))
    return prices.sort()
def median(prices):
    return statistics.median(prices)
def IQR(prices):
    return prices[round(3/4*(len(prices)+1))] - prices[round(1/4*(len(prices)+1))]

