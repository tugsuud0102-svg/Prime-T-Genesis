import MetaTrader5 as mt5
from datetime import datetime
from pathlib import Path

from core.telegram_alert import send_telegram
from config.settings import BOT_MAGIC, ORDER_DEVIATION, SYMBOL, TRADING_MODE

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def write_trade_log(message):
    Path("logs").mkdir(exist_ok=True)
    with open("logs/trades.log", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {message}\n")


def legacy_place_order(signal, entry, sl, tp, volume=0.01, context=None):
    if TRADING_MODE != "DEMO":
        print("Order blocked: TRADING_MODE must remain DEMO")
        return None
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
        "deviation": ORDER_DEVIATION,
        "magic": BOT_MAGIC,
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
    return result

def place_order(signal, entry, sl, tp, volume=0.01, context=None):
    """Execute a DEMO order and record the broker's real identifiers."""
    from trade_stats.recorder import insert_open_trade
    if TRADING_MODE != "DEMO":
        print("❌ Order blocked: TRADING_MODE must remain DEMO")
        return None
    if not mt5.initialize(path=MT5_PATH):
        print("❌ MT5 initialize failed:", mt5.last_error())
        return None
    try:
        mt5.symbol_select(SYMBOL, True)
        tick = mt5.symbol_info_tick(SYMBOL)
        if tick is None or signal not in ("BUY", "SELL"):
            print("❌ Invalid signal or missing tick")
            return None
        is_buy = signal == "BUY"
        request = {"action": mt5.TRADE_ACTION_DEAL, "symbol": SYMBOL, "volume": volume,
            "type": mt5.ORDER_TYPE_BUY if is_buy else mt5.ORDER_TYPE_SELL,
            "price": tick.ask if is_buy else tick.bid, "sl": sl, "tp": tp,
            "deviation": ORDER_DEVIATION, "magic": BOT_MAGIC,
            "comment": "Prime T Genesis demo order", "type_time": mt5.ORDER_TIME_GTC}
        result = None
        for filling in (mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_RETURN):
            request["type_filling"] = filling
            result = mt5.order_send(request)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                break
        if not result or result.retcode != mt5.TRADE_RETCODE_DONE:
            print("❌ ORDER NOT EXECUTED", getattr(result, "comment", "No result"))
            return result
        positions = [p for p in (mt5.positions_get(symbol=SYMBOL) or []) if p.magic == BOT_MAGIC]
        position = max(positions, key=lambda p: getattr(p, "time", 0)) if positions else None
        flags = context or {}
        try:
            insert_open_trade(ticket=getattr(position, "ticket", None), deal=result.deal,
                order_id=result.order, position_id=getattr(position, "ticket", None),
                symbol=SYMBOL, signal=signal, entry_price=result.price, volume=result.volume,
                sl=sl, tp=tp, score=flags.get("score"), rating=flags.get("rating"),
                **{k: int(bool(flags.get(k))) for k in ("bos","choch","mss","fvg","order_block","supply_demand","liquidity","mtf")},
                rsi=flags.get("rsi"), atr=flags.get("atr"), spread=flags.get("spread"))
        except Exception as exc:
            print("Statistics save warning (trade succeeded):", exc)
        write_trade_log(f"EXECUTED | {signal} | Deal={result.deal} | Order={result.order} | Volume={result.volume} | Price={result.price}")
        send_telegram(f"🚀 PRIME T GENESIS\n\n✅ ORDER EXECUTED\nSignal: {signal}\nSymbol: {SYMBOL}\nVolume: {result.volume}\nPrice: {result.price:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}\nDeal: {result.deal}\nOrder: {result.order}")
        return result
    finally:
        mt5.shutdown()
