import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

print("Starting...")

if not mt5.initialize(path=MT5_PATH):
    print("Initialize failed:", mt5.last_error())
    quit()

print("Connected!")

symbols = mt5.symbols_get()

if symbols is None:
    print("No symbols returned!")
else:
    print(f"Total symbols: {len(symbols)}")

    for symbol in symbols:
        if "XAU" in symbol.name.upper() or "GOLD" in symbol.name.upper():
            print(symbol.name)

mt5.shutdown()