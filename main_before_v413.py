import MetaTrader5 as mt5

from core.data_loader import get_candles
from core.order_manager import place_order
from core.logger import write_log
from core.position_manager import can_open_new_position
from core.trend_filter import h1_trend
from core.risk_manager import calculate_lot_size
from core.news_filter import news_blackout_reason
from core.bot_state import is_paused
from core.loss_guard import loss_streak_block_reason
from core.session_filter import session_block_reason
from core.trade_journal import record_signal
from config.settings import (
    BUY_RSI_MAX,
    BUY_RSI_MIN,
    MAX_ATR,
    MAX_POSITIONS,
    MAX_SPREAD,
    MIN_ATR,
    MIN_EMA_GAP_ATR,
    RISK_PERCENT,
    SELL_RSI_MAX,
    SELL_RSI_MIN,
    SL_ATR_MULTIPLIER,
    SYMBOL,
    TP_ATR_MULTIPLIER,
    TRADING_MODE,
)

from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr


def get_account_balance():
    if not mt5.initialize():
        print("MT5 initialize failed:", mt5.last_error())
        return None

    account = mt5.account_info()
    mt5.shutdown()

    if account is None:
        return None

    return account.balance


def get_symbol_spread(symbol):
    if not mt5.initialize():
        print("MT5 initialize failed:", mt5.last_error())
        return None

    tick = mt5.symbol_info_tick(symbol)
    mt5.shutdown()

    if tick is None:
        return None

    return abs(tick.ask - tick.bid)


def bullish_candle(candle):
    return candle["close"] > candle["open"]


def bearish_candle(candle):
    return candle["close"] < candle["open"]


def main():
    if is_paused():
        reason = "BOT PAUSED"
        print("SIGNAL: NO TRADE")
        print(reason)
        write_log(reason)
        record_signal(SYMBOL, "NO_TRADE", TRADING_MODE, reasons=[reason])
        return

    blocked_reason = session_block_reason()
    if blocked_reason:
        print("SIGNAL: NO TRADE")
        print(blocked_reason)
        write_log(blocked_reason)
        record_signal(SYMBOL, "NO_TRADE", TRADING_MODE, reasons=[blocked_reason])
        return

    news_reason = news_blackout_reason()
    if news_reason:
        print("SIGNAL: NO TRADE")
        print(news_reason)
        write_log(news_reason)
        record_signal(SYMBOL, "NO_TRADE", TRADING_MODE, reasons=[news_reason])
        return

    loss_reason = loss_streak_block_reason()
    if loss_reason:
        print("SIGNAL: NO TRADE")
        print(loss_reason)
        write_log(loss_reason)
        record_signal(SYMBOL, "NO_TRADE", TRADING_MODE, reasons=[loss_reason])
        return

    df = get_candles(SYMBOL, count=250)

    df["EMA20"] = calculate_ema(df, 20)
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)
    df["RSI"] = calculate_rsi(df)
    df["ATR"] = calculate_atr(df)

    last = df.iloc[-2]
    prev = df.iloc[-3]

    entry = last["close"]
    atr = last["ATR"]
    trend = h1_trend(SYMBOL)
    spread = get_symbol_spread(SYMBOL)

    print("=" * 50)
    print("Prime T Genesis v1.9 - DEMO LIVE")
    print(f"Symbol  : {SYMBOL}")
    print(f"Close   : {last['close']:.2f}")
    print(f"EMA20   : {last['EMA20']:.2f}")
    print(f"EMA50   : {last['EMA50']:.2f}")
    print(f"EMA200  : {last['EMA200']:.2f}")
    print(f"RSI     : {last['RSI']:.2f}")
    print(f"ATR     : {last['ATR']:.2f}")
    print(f"Spread  : {spread:.2f}" if spread is not None else "Spread  : N/A")
    print(f"H1 Trend: {trend}")
    print("=" * 50)

    ema_gap_ok = abs(last["EMA20"] - last["EMA50"]) >= (atr * MIN_EMA_GAP_ATR)
    atr_ok = MIN_ATR <= atr <= MAX_ATR
    spread_ok = spread is not None and spread <= MAX_SPREAD

    buy_signal = (
        last["close"] > last["EMA20"] > last["EMA50"] > last["EMA200"]
        and BUY_RSI_MIN <= last["RSI"] <= BUY_RSI_MAX
        and bullish_candle(last)
        and last["close"] > prev["high"]
        and ema_gap_ok
        and atr_ok
        and spread_ok
    )

    sell_signal = (
        last["close"] < last["EMA20"] < last["EMA50"] < last["EMA200"]
        and SELL_RSI_MIN <= last["RSI"] <= SELL_RSI_MAX
        and bearish_candle(last)
        and last["close"] < prev["low"]
        and ema_gap_ok
        and atr_ok
        and spread_ok
    )

    if buy_signal and trend == "BULLISH":
        print("SIGNAL: STRONG BUY")

        if not can_open_new_position(SYMBOL, max_positions=MAX_POSITIONS):
            write_log("BUY BLOCKED - MAX POSITIONS REACHED")
            return

        sl = entry - (atr * SL_ATR_MULTIPLIER)
        tp = entry + (atr * TP_ATR_MULTIPLIER)

        balance = get_account_balance()
        if balance is None:
            print("Could not get account balance")
            return

        volume = calculate_lot_size(balance, RISK_PERCENT, entry, sl, symbol=SYMBOL)
        print(f"Dynamic Volume: {volume}")

        record_signal(
            SYMBOL, "BUY", TRADING_MODE, entry, sl, tp, volume,
            last["RSI"], atr, spread, trend
        )

        if TRADING_MODE == "PAPER":
            print("PAPER MODE: BUY order not sent")
        else:
            place_order("BUY", entry, sl, tp, volume=volume)

        write_log(
            f"{TRADING_MODE} BUY | Volume={volume} | Entry={entry:.2f} | "
            f"SL={sl:.2f} | TP={tp:.2f}"
        )

    elif sell_signal and trend == "BEARISH":
        print("SIGNAL: STRONG SELL")

        if not can_open_new_position(SYMBOL, max_positions=MAX_POSITIONS):
            write_log("SELL BLOCKED - MAX POSITIONS REACHED")
            return

        sl = entry + (atr * SL_ATR_MULTIPLIER)
        tp = entry - (atr * TP_ATR_MULTIPLIER)

        balance = get_account_balance()
        if balance is None:
            print("Could not get account balance")
            return

        volume = calculate_lot_size(balance, RISK_PERCENT, entry, sl, symbol=SYMBOL)
        print(f"Dynamic Volume: {volume}")

        record_signal(
            SYMBOL, "SELL", TRADING_MODE, entry, sl, tp, volume,
            last["RSI"], atr, spread, trend
        )

        if TRADING_MODE == "PAPER":
            print("PAPER MODE: SELL order not sent")
        else:
            place_order("SELL", entry, sl, tp, volume=volume)

        write_log(
            f"{TRADING_MODE} SELL | Volume={volume} | Entry={entry:.2f} | "
            f"SL={sl:.2f} | TP={tp:.2f}"
        )

    else:
        reasons = []

        if buy_signal and trend != "BULLISH":
            reasons.append("BUY blocked because H1 trend is not bullish")

        if sell_signal and trend != "BEARISH":
            reasons.append("SELL blocked because H1 trend is not bearish")

        if not buy_signal and not sell_signal:
            if not (last["close"] > last["EMA20"]):
                reasons.append("BUY: Close is not above EMA20")

            if not (last["EMA20"] > last["EMA50"]):
                reasons.append("BUY: EMA20 is not above EMA50")

            if not (last["EMA50"] > last["EMA200"]):
                reasons.append("BUY: EMA50 is not above EMA200")

            if not (BUY_RSI_MIN <= last["RSI"] <= BUY_RSI_MAX):
                reasons.append(f"BUY: RSI is not between {BUY_RSI_MIN}-{BUY_RSI_MAX}")

            if not (last["close"] < last["EMA20"]):
                reasons.append("SELL: Close is not below EMA20")

            if not (last["EMA20"] < last["EMA50"]):
                reasons.append("SELL: EMA20 is not below EMA50")

            if not (last["EMA50"] < last["EMA200"]):
                reasons.append("SELL: EMA50 is not below EMA200")

            if not (SELL_RSI_MIN <= last["RSI"] <= SELL_RSI_MAX):
                reasons.append(f"SELL: RSI is not between {SELL_RSI_MIN}-{SELL_RSI_MAX}")

            if not ema_gap_ok:
                reasons.append("EMA gap is too small")

            if not atr_ok:
                reasons.append(f"ATR is outside {MIN_ATR}-{MAX_ATR}")

            if not spread_ok:
                reasons.append(f"Spread is above {MAX_SPREAD}")

        print("SIGNAL: NO TRADE")
        print("Reasons:")
        for reason in reasons:
            print("-", reason)

        record_signal(
            SYMBOL, "NO_TRADE", TRADING_MODE, entry=entry, rsi=last["RSI"],
            atr=atr, spread=spread, trend=trend, reasons=reasons
        )
        write_log("NO TRADE | " + ", ".join(reasons))


if __name__ == "__main__":
    main()
