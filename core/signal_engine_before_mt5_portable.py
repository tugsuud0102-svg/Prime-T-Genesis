import MetaTrader5 as mt5
import pandas as pd

from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
SYMBOL = "GOLD"

if not mt5.initialize(path=MT5_PATH):
    print(mt5.last_error())
    quit()

rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M15, 0, 200)
mt5.shutdown()

df = pd.DataFrame(rates)
df["time"] = pd.to_datetime(df["time"], unit="s")

df["EMA20"] = calculate_ema(df, 20)
df["EMA50"] = calculate_ema(df, 50)
df["EMA200"] = calculate_ema(df, 200)
df["RSI"] = calculate_rsi(df)
df["ATR"] = calculate_atr(df)

last = df.iloc[-1]

print("=" * 50)
print(f"Close : {last['close']:.2f}")
print(f"EMA20 : {last['EMA20']:.2f}")
print(f"EMA50 : {last['EMA50']:.2f}")
print(f"EMA200: {last['EMA200']:.2f}")
print(f"RSI   : {last['RSI']:.2f}")
print(f"ATR   : {last['ATR']:.2f}")
print("=" * 50)

if last["close"] > last["EMA20"] > last["EMA50"] > last["EMA200"] and last["RSI"] >= 55:
    print("🟢 STRONG BUY SIGNAL")
elif last["close"] < last["EMA20"] < last["EMA50"] < last["EMA200"] and last["RSI"] <= 45:
    print("🔴 STRONG SELL SIGNAL")
else:
    print("🟡 NO TRADE")