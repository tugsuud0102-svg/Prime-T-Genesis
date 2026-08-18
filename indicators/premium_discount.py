from indicators.swing_points import detect_swing_points
def detect_premium_discount(df):
    s=detect_swing_points(df); hi=s["last_high"]["level"] if s["last_high"] else float(df["high"].max()); lo=s["last_low"]["level"] if s["last_low"] else float(df["low"].min()); p=float(df.iloc[-1]["close"]); size=max(hi-lo,1e-9); pos=(p-lo)/size*100
    zone="EQUILIBRIUM" if 45<=pos<=55 else "DISCOUNT" if pos<50 else "PREMIUM"
    return {"swing_high":hi,"swing_low":lo,"equilibrium":(hi+lo)/2,"current_price":p,"range_size":size,"position_percent":pos,"zone":zone}
