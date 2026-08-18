def detect_fvg(df, atr=None):
    price=float(df.iloc[-1]["close"]); zones=[]
    for i in range(2,len(df)):
        a,c=df.iloc[i-2],df.iloc[i]
        if c["low"]>a["high"]: zones.append(("BULLISH",float(a["high"]),float(c["low"])))
        if c["high"]<a["low"]: zones.append(("BEARISH",float(c["high"]),float(a["low"])))
    if not zones: return {"detected":False,"direction":"NONE","gap_bottom":None,"gap_top":None,"inside_zone":False,"distance":None}
    z=min(zones,key=lambda x:0 if x[1]<=price<=x[2] else min(abs(price-x[1]),abs(price-x[2])))
    distance=0.0 if z[1]<=price<=z[2] else min(abs(price-z[1]),abs(price-z[2]))
    return {"detected":True,"direction":z[0],"gap_bottom":z[1],"gap_top":z[2],"inside_zone":distance==0,"distance":distance}
