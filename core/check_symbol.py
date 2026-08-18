import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

initialize_mt5()

info = mt5.symbol_info("GOLD")

print(info)

mt5.shutdown()
