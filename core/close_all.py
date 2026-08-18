import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5
from core.mt5_actions import own_positions, close_position

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def close_all_positions():
    if not initialize_mt5():
        print(mt5.last_error())
        return

    positions = own_positions()

    if positions is None or len(positions) == 0:
        print("NO OPEN POSITIONS")
        mt5.shutdown()
        return

    for pos in positions:
        result = close_position(pos, comment="Prime T close all")
        if result:
            print(f"Closed Ticket={pos.ticket} Profit={pos.profit:.2f}")

    mt5.shutdown()
