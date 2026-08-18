import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def show_account_dashboard():
    if not initialize_mt5():
        print(mt5.last_error())
        return

    acc = mt5.account_info()

    print("=" * 50)
    print("PRIME T ACCOUNT DASHBOARD")
    print(f"Login        : {acc.login}")
    print(f"Balance      : ${acc.balance:.2f}")
    print(f"Equity       : ${acc.equity:.2f}")
    print(f"Profit       : ${acc.profit:.2f}")
    print(f"Margin Free  : ${acc.margin_free:.2f}")
    print(f"Leverage     : 1:{acc.leverage}")
    print("=" * 50)

    mt5.shutdown()


if __name__ == "__main__":
    show_account_dashboard()
