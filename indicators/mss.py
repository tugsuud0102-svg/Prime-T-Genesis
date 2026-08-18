from indicators.choch import detect_choch

def detect_mss(df, active_bias="NONE", atr=None):
    result = detect_choch(df, active_bias)
    price = float(df.iloc[-1]["close"])
    level = result.get("level")
    distance = abs(price-level) if level is not None else 0.0
    normalized = distance / float(atr or 1.0)
    strength = "STRONG" if normalized >= .5 else "MODERATE" if normalized >= .25 else "WEAK" if result["detected"] else "NONE"
    return {**result, "break_price": price, "break_distance": distance, "normalized_strength": normalized, "strength": strength}
