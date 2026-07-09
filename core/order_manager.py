import MetaTrader5 as mt5
from datetime import datetime
from pathlib import Path

from core.telegram_alert import send_telegram

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
SYMBOL = "GOLD"


def write_trade_log(message):
    Path("logs").mkdir(exist_ok=True)
    with open("logs/trades.log", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")


def place_order(signal, entry, sl, tp, volume=0.01):
    if not mt5.initialize(path=MT5_PATH):
        error = mt5.last_error()
        print("❌ MT5 initialize failed:", error)
        write_trade_log(f"MT5 INIT FAILED | {error}")
        return

    mt5.symbol_select(SYMBOL, True)
    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print("❌ Tick data not found")
        write_trade_log("TICK DATA NOT FOUND")
        mt5.shutdown()
        return

    if signal == "BUY":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
    elif signal == "SELL":
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        print("❌ Invalid signal")
        mt5.shutdown()
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 20260704,
        "comment": "Prime T Genesis demo order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    result = mt5.order_send(request)

    print("\n===== ORDER RESULT =====")

    if result is None:
        print("❌ ORDER FAILED: No result")
        write_trade_log("ORDER FAILED | No result")

    elif result.retcode == mt5.TRADE_RETCODE_DONE:
        print("✅ ORDER EXECUTED")
        print(f"Signal : {signal}")
        print(f"Deal   : {result.deal}")
        print(f"Order  : {result.order}")
        print(f"Volume : {result.volume}")
        print(f"Price  : {result.price}")
        print(f"SL     : {sl:.2f}")
        print(f"TP     : {tp:.2f}")

        write_trade_log(
            f"EXECUTED | {signal} | Deal={result.deal} | Order={result.order} | "
            f"Volume={result.volume} | Price={result.price} | SL={sl:.2f} | TP={tp:.2f}"
        )

        msg = (
            "🚀 PRIME T GENESIS\n\n"
            f"✅ ORDER EXECUTED\n"
            f"Signal: {signal}\n"
            f"Symbol: {SYMBOL}\n"
            f"Volume: {result.volume}\n"
            f"Price: {result.price:.2f}\n"
            f"SL: {sl:.2f}\n"
            f"TP: {tp:.2f}\n"
            f"Deal: {result.deal}\n"
            f"Order: {result.order}"
        )
        send_telegram(msg)

    else:
        print("❌ ORDER NOT EXECUTED")
        print(f"Retcode : {result.retcode}")
        print(f"Comment : {result.comment}")

        write_trade_log(
            f"FAILED | {signal} | Retcode={result.retcode} | Comment={result.comment}"
        )

        send_telegram(
            f"⚠️ PRIME T ORDER FAILED\n\n"
            f"Signal: {signal}\n"
            f"Retcode: {result.retcode}\n"
            f"Comment: {result.comment}"
        )

    print("========================\n")
    mt5.shutdown()
