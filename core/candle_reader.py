import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5
import pandas as pd

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if not initialize_mt5():
    print("MT5 initialize failed!")
    print(mt5.last_error())
    quit()

symbol = "GOLD"

rates = mt5.copy_rates_from_pos(
    symbol,
    mt5.TIMEFRAME_M15,
    0,
    100
)

mt5.shutdown()

if rates is None:
    print("❌ Candle data авч чадсангүй.")
else:
    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(df["time"], unit="s")

    print(df[["time", "open", "high", "low", "close"]].tail())
