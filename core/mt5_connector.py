import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if initialize_mt5():
    print("✅ MT5 initialized")
    print("Version:", mt5.version())
    print("Terminal:", mt5.terminal_info())
    print("Account:", mt5.account_info())
else:
    print("❌ Initialization failed")
    print("Last error:", mt5.last_error())

mt5.shutdown()
