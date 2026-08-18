from indicators.swing_points import detect_swing_points

def detect_bos(df):
    swings = detect_swing_points(df.iloc[:-1])
    price = float(df.iloc[-1]["close"])
    high, low = swings["last_high"], swings["last_low"]
    direction = "BULLISH" if high and price > high["level"] else "BEARISH" if low and price < low["level"] else "NONE"
    return {"detected": direction != "NONE", "direction": direction, "level": high["level"] if direction == "BULLISH" else low["level"] if direction == "BEARISH" else None}
