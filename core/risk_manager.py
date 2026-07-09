import MetaTrader5 as mt5

from config.settings import SYMBOL

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def calculate_lot_size(balance, risk_percent, entry, sl, symbol=SYMBOL):
    risk_amount = balance * (risk_percent / 100)
    stop_distance = abs(entry - sl)

    if stop_distance == 0:
        return 0.01

    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return 0.01

    info = mt5.symbol_info(symbol)
    mt5.shutdown()

    if info is None or info.trade_tick_size == 0 or info.trade_tick_value == 0:
        print("Symbol risk info missing, using fallback lot formula")
        lot = risk_amount / (stop_distance * 100)
        return max(round(lot, 2), 0.01)

    loss_per_lot = (stop_distance / info.trade_tick_size) * info.trade_tick_value

    if loss_per_lot <= 0:
        return info.volume_min

    lot = risk_amount / loss_per_lot

    step = info.volume_step or 0.01
    lot = round(lot / step) * step
    lot = max(lot, info.volume_min)
    lot = min(lot, info.volume_max)

    return round(lot, 2)
