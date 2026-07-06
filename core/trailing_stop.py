import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def move_sl_to_break_even(symbol="GOLD", min_profit=5.0):
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return

    positions = mt5.positions_get(symbol=symbol)

    if positions is None or len(positions) == 0:
        print("NO OPEN POSITIONS")
        mt5.shutdown()
        return

    for pos in positions:
        if pos.profit < min_profit:
            print(f"SKIP | Ticket={pos.ticket} | Profit={pos.profit:.2f}")
            continue

        new_sl = pos.price_open

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": pos.ticket,
            "symbol": pos.symbol,
            "sl": new_sl,
            "tp": pos.tp,
            "magic": 20260704,
            "comment": "Move SL to break even",
        }

        result = mt5.order_send(request)

        print("\n===== TRAILING STOP RESULT =====")
        print(f"Ticket : {pos.ticket}")
        print(f"Profit : {pos.profit:.2f}")
        print(f"New SL : {new_sl:.2f}")
        print(result)
        print("================================\n")

    mt5.shutdown()