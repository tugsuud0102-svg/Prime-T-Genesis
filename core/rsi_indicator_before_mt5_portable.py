import MetaTrader5 as mt5
import pandas as pd

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if not mt5.initialize(path=MT5_PATH):
    print(mt5.last_error())
    quit()

symbol = "GOLD"

rates = mt5.copy_rates_from_pos(
    symbol,
    mt5.TIMEFRAME_M15,
    0,
    200
)

mt5.shutdown()

df = pd.DataFrame(rates)
df["time"] = pd.to_datetime(df["time"], unit="s")

# ===== RSI =====

delta = df["close"].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

df["RSI"] = 100 - (100 / (1 + rs))

print(df[["time", "close", "RSI"]].tail())