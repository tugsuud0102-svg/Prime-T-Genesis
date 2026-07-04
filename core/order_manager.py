import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def place_order(signal, entry, sl, tp, volume=0.01):
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return

    symbol = "GOLD"
    mt5.symbol_select(symbol, True)

    tick = mt5.symbol_info_tick(symbol)

    if signal == "BUY":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
    elif signal == "SELL":
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        print("Invalid signal")
        mt5.shutdown()
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
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

    print("\n===== LIVE DEMO ORDER =====")
    print(result)
    print("===========================\n")

    mt5.shutdown()