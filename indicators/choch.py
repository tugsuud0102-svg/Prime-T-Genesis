from indicators.bos import detect_bos
from indicators.swing_points import detect_swing_points

def detect_choch(df, active_bias="NONE"):
    bos = detect_bos(df)
    opposite = (active_bias == "BULLISH" and bos["direction"] == "BEARISH") or (active_bias == "BEARISH" and bos["direction"] == "BULLISH")
    swings = detect_swing_points(df.iloc[:-1])
    previous = swings["last_high"]["label"] if active_bias == "BEARISH" and swings["last_high"] else swings["last_low"]["label"] if swings["last_low"] else "NONE"
    return {"detected": bool(opposite), "direction": bos["direction"] if opposite else "NONE", "previous_structure": previous, "level": bos.get("level")}
