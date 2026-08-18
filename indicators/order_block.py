def detect_order_block(df, atr=None):
    price=float(df.iloc[-1]["close"]); zones=[]
    for i in range(1,len(df)-1):
        row,nxt=df.iloc[i],df.iloc[i+1]
        if row["close"]<row["open"] and nxt["close"]>row["high"]: zones.append(("BULLISH",float(row["low"]),float(row["high"])))
        if row["close"]>row["open"] and nxt["close"]<row["low"]: zones.append(("BEARISH",float(row["low"]),float(row["high"])))
    if not zones:return {"detected":False,"direction":"NONE","zone_bottom":None,"zone_top":None,"inside_zone":False,"distance":None}
    z=min(zones,key=lambda x:0 if x[1]<=price<=x[2] else min(abs(price-x[1]),abs(price-x[2]))); d=0.0 if z[1]<=price<=z[2] else min(abs(price-z[1]),abs(price-z[2]))
    return {"detected":True,"direction":z[0],"zone_bottom":z[1],"zone_top":z[2],"inside_zone":d==0,"distance":d}
