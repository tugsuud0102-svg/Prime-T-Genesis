import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def move_sl_to_break_even(symbol="GOLD", min_profit=5.0):
    from core.break_even_engine import manage_break_even
    return manage_break_even()
