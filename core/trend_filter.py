import MetaTrader5 as mt5

from core.data_loader import get_candles
from indicators.ema import calculate_ema


def h1_trend(symbol="GOLD"):
    df = get_candles(
        symbol,
        timeframe=mt5.TIMEFRAME_H1,
        count=300
    )

    df["EMA20"] = calculate_ema(df, 20)
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)

    last = df.iloc[-2]

    if last["close"] > last["EMA20"] > last["EMA50"] > last["EMA200"]:
        return "BULLISH"

    if last["close"] < last["EMA20"] < last["EMA50"] < last["EMA200"]:
        return "BEARISH"

    return "NEUTRAL"
