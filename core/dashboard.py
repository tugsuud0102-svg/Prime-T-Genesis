from datetime import datetime, time, timedelta
from pathlib import Path

import MetaTrader5 as mt5

from config.settings import BOT_MAGIC, SYMBOL, TELEGRAM_REPORT_FILE
from core.daily_target import DAILY_TARGET, get_start_balance
from core.news_filter import load_news_events
from core.telegram_alert import send_telegram


MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


def _today_history():
    now = datetime.now()
    start = datetime.combine(now.date(), time.min)
    deals = mt5.history_deals_get(start, now)

    if deals is None:
        return 0, 0, 0.0

    wins = 0
    losses = 0
    profit = 0.0

    for deal in deals:
        if (
            deal.symbol == SYMBOL
            and deal.magic == BOT_MAGIC
            and deal.entry == mt5.DEAL_ENTRY_OUT
        ):
            value = deal.profit + deal.commission + deal.swap
            profit += value
            if value > 0:
                wins += 1
            elif value < 0:
                losses += 1

    return wins, losses, profit


def _next_news():
    now = datetime.now().astimezone()
    future = [event for event in load_news_events() if event["time"] >= now]
    future.sort(key=lambda event: event["time"])

    if not future:
        return "None"

    event = future[0]
    return (
        f"{event['time'].strftime('%Y-%m-%d %H:%M')} "
        f"{event['currency']} {event['impact']} {event['title']}"
    )


def build_dashboard_message():
    if not mt5.initialize(path=MT5_PATH):
        return f"Prime T Genesis\nMT5 error: {mt5.last_error()}"

    account = mt5.account_info()
    positions = mt5.positions_get(symbol=SYMBOL)
    wins, losses, history_profit = _today_history()
    start_balance = get_start_balance()

    if account is None:
        mt5.shutdown()
        return "Prime T Genesis\nAccount info unavailable"

    open_count = 0 if positions is None else len(positions)
    open_profit = sum(pos.profit for pos in positions or [])
    daily_profit = account.equity - start_balance if start_balance else history_profit
    total = wins + losses
    win_rate = (wins / total) * 100 if total else 0.0

    mt5.shutdown()

    return (
        "PRIME T GENESIS DASHBOARD\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Symbol: {SYMBOL}\n"
        f"Balance: ${account.balance:.2f}\n"
        f"Equity: ${account.equity:.2f}\n"
        f"Daily P/L: ${daily_profit:.2f} / ${DAILY_TARGET:.2f}\n"
        f"Open positions: {open_count}\n"
        f"Open P/L: ${open_profit:.2f}\n"
        f"Today W/L: {wins}/{losses} ({win_rate:.1f}%)\n"
        f"Next news: {_next_news()}"
    )


def send_dashboard():
    send_telegram(build_dashboard_message())


def send_daily_dashboard_if_due(now=None):
    from config.settings import (
        TELEGRAM_DAILY_REPORT_ENABLED,
        TELEGRAM_DAILY_REPORT_HOUR,
        TELEGRAM_DAILY_REPORT_MINUTE,
    )

    if not TELEGRAM_DAILY_REPORT_ENABLED:
        return False

    now = now or datetime.now()
    scheduled = now.replace(
        hour=TELEGRAM_DAILY_REPORT_HOUR,
        minute=TELEGRAM_DAILY_REPORT_MINUTE,
        second=0,
        microsecond=0,
    )

    if not scheduled <= now < scheduled + timedelta(minutes=20):
        return False

    path = Path(TELEGRAM_REPORT_FILE)
    path.parent.mkdir(exist_ok=True)
    today = now.date().isoformat()

    if path.exists() and path.read_text(encoding="utf-8").strip() == today:
        return False

    send_dashboard()
    path.write_text(today, encoding="utf-8")
    return True
