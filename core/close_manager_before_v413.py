import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def close_position(ticket):
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return

    positions = mt5.positions_get(ticket=ticket)

    if positions is None or len(positions) == 0:
        print(f"Position not found: {ticket}")
        mt5.shutdown()
        return

    position = positions[0]
    symbol = position.symbol
    volume = position.volume

    tick = mt5.symbol_info_tick(symbol)

    if position.type == mt5.POSITION_TYPE_BUY:
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 20,
        "magic": 20260704,
        "comment": "Prime T Genesis close position",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    result = mt5.order_send(request)

    print("\n===== CLOSE RESULT =====")
    print(result)
    print("========================\n")

    mt5.shutdown()