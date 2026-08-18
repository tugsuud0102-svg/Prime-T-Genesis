def detect_liquidity_sweep(df):
    if len(df) < 3: return {"detected": False, "direction": "NONE"}
    last, prior = df.iloc[-1], df.iloc[-2]
    bullish = last["low"] < prior["low"] and last["close"] > prior["low"]
    bearish = last["high"] > prior["high"] and last["close"] < prior["high"]
    direction = "BULLISH" if bullish else "BEARISH" if bearish else "NONE"
    return {"detected": direction != "NONE", "direction": direction}
