import os
from datetime import date, datetime
import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5

from config.settings import DAILY_TARGET

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def balance_file():
    return f"data/daily_start_balance_{date.today().isoformat()}.txt"


def get_start_balance():
    filename = balance_file()
    os.makedirs("data", exist_ok=True)

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return float(f.read())

    account = mt5.account_info()

    if account is None:
        return None

    start_balance = account.balance

    with open(filename, "w") as f:
        f.write(str(start_balance))

    return start_balance


def daily_target_hit():
    if not initialize_mt5():
        print("MT5 initialize failed:", mt5.last_error())
        return False

    start = datetime.combine(date.today(), datetime.min.time())
    deals = mt5.history_deals_get(start, datetime.now()) or []
    exit_values = {getattr(mt5, "DEAL_ENTRY_OUT", 1), getattr(mt5, "DEAL_ENTRY_OUT_BY", 3)}
    from config.settings import BOT_MAGIC
    profit = sum(
        float(getattr(d, "profit", 0)) + float(getattr(d, "commission", 0)) + float(getattr(d, "swap", 0))
        for d in deals
        if getattr(d, "magic", None) == BOT_MAGIC and getattr(d, "entry", None) in exit_values
    )
    print(f"Daily Realized P/L: ${profit:.2f} / ${DAILY_TARGET:.2f}")

    mt5.shutdown()

    return profit >= DAILY_TARGET
