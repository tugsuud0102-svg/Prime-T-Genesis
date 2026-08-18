def detect_ema_slope(df, column="EMA20", periods=3):
    slope=float(df[column].iloc[-1]-df[column].iloc[-1-periods]) if len(df)>periods else 0.0
    return {"slope":slope,"direction":"BULLISH" if slope>0 else "BEARISH" if slope<0 else "FLAT","detected":slope!=0}
