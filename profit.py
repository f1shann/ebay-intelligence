def buyerprotnum(item_price):
    temp=item_price
    separators=[[300,0.02],[20, 0.04],[0,0.07]]
    buyerprot=0.10
    for i in range(len(separators)):
        if temp>separators[i][0]:
            temp,difference=separators[i][0],temp-separators[i][0]
            buyerprot=buyerprot+difference*separators[i][1]
    return round(buyerprot,2)
def shippingcost(weight,length,width,height):
    parcelsizes = [["Large letter", 1.0, 35.0, 25.0, 2.5, 2.70],["Small parcel", 1.0, 45.0, 35.0, 16.0, 2.94],["Small parcel", 2.0, 45.0, 35.0, 16.0, 3.38],["Medium parcel", 1.0, 61.0, 46.0, 46.0, 2.94],["Medium parcel", 2.0, 61.0, 46.0, 46.0, 3.71],["Medium parcel", 10.0, 61.0, 46.0, 46.0, 5.21],["Medium parcel", 20.0, 61.0, 46.0, 46.0, 7.19]]
    for name,max_kg, max_l,max_w,max_h,cost in parcelsizes:
        if weight <= max_kg and length <= max_l and width <=max_w and height<= max_h:
            return cost
def profit(median_price,item_price,weight,length,width,height):
    return median_price-item_price-buyerprotnum(item_price)-shippingcost(weight,length,width,height)
                    