import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def close_all_positions():
    if not mt5.initialize(path=MT5_PATH):
        print(mt5.last_error())
        return

    positions = mt5.positions_get()

    if positions is None or len(positions) == 0:
        print("NO OPEN POSITIONS")
        mt5.shutdown()
        return

    for pos in positions:

        tick = mt5.symbol_info_tick(pos.symbol)

        if pos.type == mt5.POSITION_TYPE_BUY:
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": order_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 20,
            "magic": 20260704,
            "comment": "Close All",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)

        print(
            f"Closed Ticket={pos.ticket} "
            f"Profit={pos.profit:.2f}"
        )

    mt5.shutdown()