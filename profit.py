def buyerprotnum(item_price):
    temp=item_price
    separators=[[300,0.02],[20, 0.04],[0,0.07]]
    buyerprot=0.10
    for i in range(len(separators)):
        if temp>separators[i][0]:
            temp,difference=separators[i][0],temp-separators[i][0]
            buyerprot=buyerprot+difference*separators[i][1]
    return round(buyerprot,2)