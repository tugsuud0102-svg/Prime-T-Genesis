from core.data_loader import get_candles
from core.order_manager import place_order

from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr


SYMBOL = "GOLD"


def main():
    df = get_candles(SYMBOL, count=200)

    df["EMA20"] = calculate_ema(df, 20)
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)
    df["RSI"] = calculate_rsi(df)
    df["ATR"] = calculate_atr(df)

    last = df.iloc[-1]

    entry = last["close"]
    atr = last["ATR"]

    print("=" * 50)
    print("Prime T Genesis v1.1 - DRY RUN")
    print(f"Symbol: {SYMBOL}")
    print(f"Close : {last['close']:.2f}")
    print(f"EMA20 : {last['EMA20']:.2f}")
    print(f"EMA50 : {last['EMA50']:.2f}")
    print(f"EMA200: {last['EMA200']:.2f}")
    print(f"RSI   : {last['RSI']:.2f}")
    print(f"ATR   : {last['ATR']:.2f}")
    print("=" * 50)

    buy_signal = (
        last["close"] > last["EMA20"] > last["EMA50"] > last["EMA200"]
        and last["RSI"] >= 55
    )

    sell_signal = (
        last["close"] < last["EMA20"] < last["EMA50"] < last["EMA200"]
        and last["RSI"] <= 45
    )

    if buy_signal:
        print("SIGNAL: STRONG BUY")

        place_order(
            signal="BUY",
            entry=entry,
            sl=entry - (atr * 2),
            tp=entry + (atr * 3),
            volume=0.01,
        )

    elif sell_signal:
        print("SIGNAL: STRONG SELL")

        place_order(
            signal="SELL",
            entry=entry,
            sl=entry + (atr * 2),
            tp=entry - (atr * 3),
            volume=0.01,
        )

    else:
        print("SIGNAL: NO TRADE")


if __name__ == "__main__":
    main()