import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def show_positions():
    if not mt5.initialize(path=MT5_PATH):
        print(mt5.last_error())
        return

    positions = mt5.positions_get()

    if positions is None or len(positions) == 0:
        print("NO OPEN POSITIONS")
        mt5.shutdown()
        return

    print("\n===== OPEN POSITIONS =====")

    total_profit = 0

    for pos in positions:
        print(
            f"{pos.symbol} | "
            f"Ticket={pos.ticket} | "
            f"Volume={pos.volume} | "
            f"Profit={pos.profit:.2f}"
        )

        total_profit += pos.profit

    print("--------------------------")
    print(f"Total Profit: {total_profit:.2f}")
    print("==========================")

    mt5.shutdown()