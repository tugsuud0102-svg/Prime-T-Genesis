def evaluate_smart_exit(position,snapshot):
    held="BULLISH" if position.type==0 else "BEARISH"; opposite="BEARISH" if held=="BULLISH" else "BULLISH"
    reasons=[]
    for name,item in (("opposite CHoCH",snapshot.choch),("opposite MSS",snapshot.mss),("opposite liquidity sweep",snapshot.liquidity_sweep)):
        if item.get("detected") and item.get("direction")==opposite:reasons.append(name)
    for name,item in (("opposite Pin Bar",snapshot.price_action["pin_bar"]),("opposite Engulfing",snapshot.price_action["engulfing"])):
        if item.get("detected") and item.get("direction")==opposite:reasons.append(name)
    if snapshot.mtf_confluence["blocked"]:reasons.append("MTF blocked")
    strong="opposite MSS" in reasons or ("opposite CHoCH" in reasons and "MTF blocked" in reasons)
    return {"exit":strong or len(reasons)>=2,"reasons":reasons}
