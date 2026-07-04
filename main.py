from core.data_loader import get_candles
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr


def main():
    df = get_candles("GOLD")

    df["EMA20"] = calculate_ema(df, 20)
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)
    df["RSI"] = calculate_rsi(df)
    df["ATR"] = calculate_atr(df)

    last = df.iloc[-1]

    print("=" * 50)
    print("Prime T Genesis v1.0")
    print(f"Close : {last['close']:.2f}")
    print(f"EMA20 : {last['EMA20']:.2f}")
    print(f"EMA50 : {last['EMA50']:.2f}")
    print(f"EMA200: {last['EMA200']:.2f}")
    print(f"RSI   : {last['RSI']:.2f}")
    print(f"ATR   : {last['ATR']:.2f}")

    if last["close"] > last["EMA20"] > last["EMA50"] > last["EMA200"] and last["RSI"] >= 55:
        print("SIGNAL: STRONG BUY")
    elif last["close"] < last["EMA20"] < last["EMA50"] < last["EMA200"] and last["RSI"] <= 45:
        print("SIGNAL: STRONG SELL")
    else:
        print("SIGNAL: NO TRADE")

    print("=" * 50)


if __name__ == "__main__":
    main()