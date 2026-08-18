import os
from datetime import date
import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

MAX_DAILY_LOSS_PERCENT = 10.0


def balance_file():
    return f"data/daily_start_balance_{date.today().isoformat()}.txt"


def get_start_balance():
    filename = balance_file()

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return float(f.read())

    return None


def equity_protection():
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

    equity = account.equity

    drawdown_percent = (
        (start_balance - equity)
        / start_balance
    ) * 100

    print(
        f"Equity: {equity:.2f} | "
        f"Drawdown: {drawdown_percent:.2f}%"
    )

    mt5.shutdown()

    if drawdown_percent >= MAX_DAILY_LOSS_PERCENT:
        print("EQUITY PROTECTION TRIGGERED")
        return True

    return False
