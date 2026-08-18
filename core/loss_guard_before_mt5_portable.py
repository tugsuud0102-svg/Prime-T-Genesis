from datetime import datetime, time

import MetaTrader5 as mt5

from config.settings import (
    BOT_MAGIC,
    LOSS_STREAK_GUARD_ENABLED,
    MAX_CONSECUTIVE_LOSSES,
    SYMBOL,
)


MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def consecutive_losses_today():
    if not mt5.initialize(path=MT5_PATH):
        print("MT5 initialize failed:", mt5.last_error())
        return 0

    now = datetime.now()
    start = datetime.combine(now.date(), time.min)
    deals = mt5.history_deals_get(start, now)
    mt5.shutdown()

    if deals is None:
        return 0

    closed = [
        deal for deal in deals
        if deal.symbol == SYMBOL
        and deal.magic == BOT_MAGIC
        and deal.entry == mt5.DEAL_ENTRY_OUT
    ]
    closed.sort(key=lambda deal: deal.time)

    streak = 0
    for deal in reversed(closed):
        profit = deal.profit + deal.commission + deal.swap
        if profit < 0:
            streak += 1
            continue
        if profit > 0:
            break

    return streak


def loss_streak_block_reason():
    if not LOSS_STREAK_GUARD_ENABLED:
        return None

    streak = consecutive_losses_today()
    if streak >= MAX_CONSECUTIVE_LOSSES:
        return f"LOSS STREAK BLOCK: {streak} losses today"

    return None
