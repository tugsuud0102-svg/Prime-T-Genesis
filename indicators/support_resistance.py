from indicators.swing_points import detect_swing_points
def detect_support_resistance(df):
    s=detect_swing_points(df); p=float(df.iloc[-1]["close"]); sup=s["last_low"]["level"] if s["last_low"] else None; res=s["last_high"]["level"] if s["last_high"] else None
    return {"support":sup,"resistance":res,"support_distance":abs(p-sup) if sup else None,"resistance_distance":abs(res-p) if res else None}
