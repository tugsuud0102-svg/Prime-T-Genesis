"""Canonical MetaTrader 5 portable-mode connection for Prime T Genesis."""
import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
MT5_TIMEOUT_MS = 120_000

def initialize_mt5():
    return mt5.initialize(path=MT5_PATH, portable=True, timeout=MT5_TIMEOUT_MS)
