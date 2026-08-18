import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def count_open_positions(symbol="GOLD"):
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return 0

    positions = mt5.positions_get(symbol=symbol)
    mt5.shutdown()

    if positions is None:
        return 0

    return len(positions)


def can_open_new_position(symbol="GOLD", max_positions=2):
    open_count = count_open_positions(symbol)

    if open_count >= max_positions:
        print(f"OPEN POSITION LIMIT REACHED: {open_count}/{max_positions}")
        return False

    print(f"OPEN POSITIONS: {open_count}/{max_positions}")
    return True