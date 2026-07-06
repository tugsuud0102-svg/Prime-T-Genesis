import MetaTrader5 as mt5

from core.data_loader import get_candles
from core.order_manager import place_order
from core.logger import write_log
from core.position_manager import can_open_new_position
from core.trend_filter import h1_trend
from core.risk_manager import calculate_lot_size

from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr


SYMBOL = "GOLD"
RISK_PERCENT = 1.0

BUY_RSI_LEVEL = 60
SELL_RSI_LEVEL = 40


def get_account_balance():
    if not mt5.initialize():
        print("MT5 initialize failed:", mt5.last_error())
        return None

    account = mt5.account_info()
    mt5.shutdown()

    if account is None:
        return None

    return account.balance


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
    trend = h1_trend(SYMBOL)

    print("=" * 50)
    print("Prime T Genesis v1.9 - DEMO LIVE")
    print(f"Symbol  : {SYMBOL}")
    print(f"Close   : {last['close']:.2f}")
    print(f"EMA20   : {last['EMA20']:.2f}")
    print(f"EMA50   : {last['EMA50']:.2f}")
    print(f"EMA200  : {last['EMA200']:.2f}")
    print(f"RSI     : {last['RSI']:.2f}")
    print(f"ATR     : {last['ATR']:.2f}")
    print(f"H1 Trend: {trend}")
    print("=" * 50)

    buy_signal = (
        last["close"] > last["EMA20"] > last["EMA50"] > last["EMA200"]
        and last["RSI"] >= BUY_RSI_LEVEL
    )

    sell_signal = (
        last["close"] < last["EMA20"] < last["EMA50"] < last["EMA200"]
        and last["RSI"] <= SELL_RSI_LEVEL
    )

    if buy_signal and trend == "BULLISH":
        print("SIGNAL: STRONG BUY")

        if not can_open_new_position(SYMBOL, max_positions=2):
            write_log("BUY BLOCKED - MAX POSITIONS REACHED")
            return

        sl = entry - (atr * 2)
        tp = entry + (atr * 3)

        balance = get_account_balance()
        if balance is None:
            print("Could not get account balance")
            return

        volume = calculate_lot_size(balance, RISK_PERCENT, entry, sl)
        print(f"Dynamic Volume: {volume}")

        place_order("BUY", entry, sl, tp, volume=volume)
        write_log(
            f"BUY | Volume={volume} | Entry={entry:.2f} | SL={sl:.2f} | TP={tp:.2f}"
        )

    elif sell_signal and trend == "BEARISH":
        print("SIGNAL: STRONG SELL")

        if not can_open_new_position(SYMBOL, max_positions=2):
            write_log("SELL BLOCKED - MAX POSITIONS REACHED")
            return

        sl = entry + (atr * 2)
        tp = entry - (atr * 3)

        balance = get_account_balance()
        if balance is None:
            print("Could not get account balance")
            return

        volume = calculate_lot_size(balance, RISK_PERCENT, entry, sl)
        print(f"Dynamic Volume: {volume}")

        place_order("SELL", entry, sl, tp, volume=volume)
        write_log(
            f"SELL | Volume={volume} | Entry={entry:.2f} | SL={sl:.2f} | TP={tp:.2f}"
        )

    else:
        reasons = []

        if buy_signal and trend != "BULLISH":
            reasons.append("BUY blocked because H1 trend is not bullish")

        if sell_signal and trend != "BEARISH":
            reasons.append("SELL blocked because H1 trend is not bearish")

        if not buy_signal and not sell_signal:
            if not (last["close"] > last["EMA20"]):
                reasons.append("Close is not above EMA20")

            if not (last["EMA20"] > last["EMA50"]):
                reasons.append("EMA20 is not above EMA50")

            if not (last["EMA50"] > last["EMA200"]):
                reasons.append("EMA50 is not above EMA200")

            if not (last["RSI"] >= BUY_RSI_LEVEL):
                reasons.append(f"RSI is below {BUY_RSI_LEVEL}")

        print("SIGNAL: NO TRADE")
        print("Reasons:")
        for reason in reasons:
            print("-", reason)

        write_log("NO TRADE | " + ", ".join(reasons))


if __name__ == "__main__":
    main()