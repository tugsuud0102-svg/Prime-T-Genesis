import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if not mt5.initialize(path=MT5_PATH):
    print("MT5 initialize failed!")
    print(mt5.last_error())
    quit()

symbol = "GOLD"

info = mt5.symbol_info(symbol)

if info is None:
    print("Symbol not found!")
else:
    print("=" * 40)
    print("Symbol :", info.name)
    print("Bid    :", info.bid)
    print("Ask    :", info.ask)
    print("Spread :", info.spread)
    print("=" * 40)

mt5.shutdown()