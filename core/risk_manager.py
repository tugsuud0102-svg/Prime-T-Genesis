import MetaTrader5 as mt5
import pandas as pd

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if not mt5.initialize(path=MT5_PATH):
    print(mt5.last_error())
    quit()

symbol = "GOLD"

rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 200)

tick = mt5.symbol_info_tick(symbol)

mt5.shutdown()

df = pd.DataFrame(rates)

df["H-L"] = df["high"] - df["low"]
df["H-PC"] = abs(df["high"] - df["close"].shift())
df["L-PC"] = abs(df["low"] - df["close"].shift())

df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
df["ATR"] = df["TR"].rolling(14).mean()

atr = df.iloc[-1]["ATR"]

entry = tick.ask

sl = entry - atr * 2
tp = entry + atr * 3

print("=" * 40)
print(f"Entry : {entry:.2f}")
print(f"ATR   : {atr:.2f}")
print(f"SL    : {sl:.2f}")
print(f"TP    : {tp:.2f}")
print("=" * 40)