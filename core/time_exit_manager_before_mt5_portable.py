import MetaTrader5 as mt5
from config.settings import TIME_EXIT_ENABLED,TIME_EXIT_MAX_HOURS,TIME_EXIT_MINIMUM_PROFIT
from core.mt5_actions import own_positions,close_position
from core.time_exit_engine import evaluate_time_exit
from core.telegram_alert import send_telegram
def manage_time_exits():
    if not TIME_EXIT_ENABLED or not mt5.initialize():return 0
    count=0
    for p in own_positions():
        d=evaluate_time_exit(p,TIME_EXIT_MAX_HOURS,TIME_EXIT_MINIMUM_PROFIT)
        if d["exit"] and close_position(p,comment="Prime T time exit"):count+=1; send_telegram(f"⏱ Time exit\n{p.symbol} #{p.ticket}\n{d['reason']}")
    mt5.shutdown(); return count
