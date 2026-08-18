def detect_price_action(df):
    last,prev=df.iloc[-1],df.iloc[-2]; body=abs(last["close"]-last["open"]); rng=max(last["high"]-last["low"],1e-9)
    pin_dir="BULLISH" if min(last["open"],last["close"])-last["low"]>2*body else "BEARISH" if last["high"]-max(last["open"],last["close"])>2*body else "NONE"
    bull=last["close"]>last["open"] and prev["close"]<prev["open"] and last["open"]<=prev["close"] and last["close"]>=prev["open"]
    bear=last["close"]<last["open"] and prev["close"]>prev["open"] and last["open"]>=prev["close"] and last["close"]<=prev["open"]
    eng="BULLISH" if bull else "BEARISH" if bear else "NONE"
    return {"pin_bar":{"detected":pin_dir!="NONE" and body/rng<.4,"direction":pin_dir},"engulfing":{"detected":eng!="NONE","direction":eng},"inside_bar":{"detected":last["high"]<prev["high"] and last["low"]>prev["low"]}}
