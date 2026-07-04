import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if mt5.initialize(path=MT5_PATH):
    print("✅ MT5 initialized")
    print("Version:", mt5.version())
    print("Terminal:", mt5.terminal_info())
    print("Account:", mt5.account_info())
else:
    print("❌ Initialization failed")
    print("Last error:", mt5.last_error())

mt5.shutdown()