from core.data_loader import get_candles
from core.order_manager import place_order
from core.logger import write_log
from core.position_manager import can_open_new_position

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
    print("Prime T Genesis v1.4 - DEMO LIVE")
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

        if not can_open_new_position(SYMBOL, max_positions=2):
            write_log("BUY BLOCKED - MAX POSITIONS REACHED")
            return

        sl = entry - (atr * 2)
        tp = entry + (atr * 3)

        place_order("BUY", entry, sl, tp, volume=0.01)
        write_log(f"BUY | Entry={entry:.2f} | SL={sl:.2f} | TP={tp:.2f}")

    elif sell_signal:
        print("SIGNAL: STRONG SELL")

        if not can_open_new_position(SYMBOL, max_positions=2):
            write_log("SELL BLOCKED - MAX POSITIONS REACHED")
            return

        sl = entry + (atr * 2)
        tp = entry - (atr * 3)

        place_order("SELL", entry, sl, tp, volume=0.01)
        write_log(f"SELL | Entry={entry:.2f} | SL={sl:.2f} | TP={tp:.2f}")

    else:
        reasons = []

        if not (last["close"] > last["EMA20"]):
            reasons.append("Close is not above EMA20")

        if not (last["EMA20"] > last["EMA50"]):
            reasons.append("EMA20 is not above EMA50")

        if not (last["EMA50"] > last["EMA200"]):
            reasons.append("EMA50 is not above EMA200")

        if not (last["RSI"] >= 55):
            reasons.append("RSI is below 55")

        print("SIGNAL: NO TRADE")
        print("Reasons:")
        for reason in reasons:
            print("-", reason)

        write_log("NO TRADE | " + ", ".join(reasons))


if __name__ == "__main__":
    main()