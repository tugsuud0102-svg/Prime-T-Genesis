import MetaTrader5 as mt5
import pandas as pd

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def get_candles(symbol: str = "GOLD", timeframe=mt5.TIMEFRAME_M15, count: int = 200):
    if not mt5.initialize(path=MT5_PATH):
        raise RuntimeError(mt5.last_error())

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    mt5.shutdown()

    if rates is None:
        raise RuntimeError("Candle data авч чадсангүй")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df