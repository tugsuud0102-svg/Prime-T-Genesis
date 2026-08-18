def detect_supply_demand(df, atr):
    price=float(df.iloc[-1]["close"]); look=df.iloc[-30:-1] if len(df)>30 else df.iloc[:-1]
    if look.empty:return {"detected":False,"direction":"NONE","zone_type":"NONE","zone_bottom":None,"zone_top":None,"inside_zone":False,"distance":None}
    low,high=float(look["low"].min()),float(look["high"].max()); width=float(atr or (high-low)*.1)*.5
    zones=[("BULLISH","DEMAND",low,low+width),("BEARISH","SUPPLY",high-width,high)]
    z=min(zones,key=lambda x:0 if x[2]<=price<=x[3] else min(abs(price-x[2]),abs(price-x[3]))); d=0.0 if z[2]<=price<=z[3] else min(abs(price-z[2]),abs(price-z[3]))
    return {"detected":True,"direction":z[0],"zone_type":z[1],"zone_bottom":z[2],"zone_top":z[3],"inside_zone":d==0,"distance":d}
