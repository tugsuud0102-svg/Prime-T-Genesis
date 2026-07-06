import MetaTrader5 as mt5

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def calculate_lot_size(balance, risk_percent, entry, sl):
    risk_amount = balance * (risk_percent / 100)
    stop_distance = abs(entry - sl)

    if stop_distance == 0:
        return 0.01

    lot = risk_amount / (stop_distance * 100)
    lot = round(lot, 2)

    if lot < 0.01:
        lot = 0.01

    return lot