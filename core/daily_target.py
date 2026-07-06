import os
import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

DAILY_TARGET = 50.0
BALANCE_FILE = "data/daily_start_balance.txt"


def get_start_balance():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            return float(f.read())

    account = mt5.account_info()

    if account is None:
        return None

    start_balance = account.balance

    with open(BALANCE_FILE, "w") as f:
        f.write(str(start_balance))

    return start_balance


def daily_target_hit():
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return False

    account = mt5.account_info()

    if account is None:
        mt5.shutdown()
        return False

    start_balance = get_start_balance()

    if start_balance is None:
        mt5.shutdown()
        return False

    profit = account.balance - start_balance

    print(
        f"Daily Profit: ${profit:.2f} / ${DAILY_TARGET:.2f}"
    )

    mt5.shutdown()

    return profit >= DAILY_TARGET