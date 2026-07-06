import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

START_BALANCE = 10000.0
MAX_DAILY_LOSS_PERCENT = 10.0


def equity_protection():
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return False

    account = mt5.account_info()

    if account is None:
        mt5.shutdown()
        return False

    equity = account.equity

    drawdown_percent = (
        (START_BALANCE - equity) / START_BALANCE
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