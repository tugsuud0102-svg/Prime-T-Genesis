import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

mt5.initialize(path=MT5_PATH)

info = mt5.symbol_info("GOLD")

print(info)

mt5.shutdown()