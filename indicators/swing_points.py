"""Confirmed swing points without look-ahead use at the evaluation candle."""
def detect_swing_points(df, window=2):
    highs, lows = [], []
    if df is None or len(df) < window * 2 + 1:
        return {"highs": highs, "lows": lows, "last_high": None, "last_low": None}
    # A swing is usable only after `window` candles have closed to its right.
    for i in range(window, len(df) - window):
        row = df.iloc[i]
        high_slice = df.iloc[i-window:i+window+1]["high"]
        low_slice = df.iloc[i-window:i+window+1]["low"]
        if row["high"] >= high_slice.max():
            highs.append({"index": i, "level": float(row["high"]), "label": "HH" if highs and row["high"] > highs[-1]["level"] else "LH"})
        if row["low"] <= low_slice.min():
            lows.append({"index": i, "level": float(row["low"]), "label": "HL" if lows and row["low"] > lows[-1]["level"] else "LL"})
    return {"highs": highs, "lows": lows, "last_high": highs[-1] if highs else None, "last_low": lows[-1] if lows else None}
