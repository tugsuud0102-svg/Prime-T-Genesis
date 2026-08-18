import MetaTrader5 as mt5
from core.mt5_connection import initialize_mt5
from config.settings import SMART_EXIT_ENABLED
from core.mt5_actions import own_positions,close_position
from core.market_engine import build_market_snapshot
from core.smart_exit_engine import evaluate_smart_exit
from core.telegram_alert import send_telegram
def manage_smart_exits():
    if not SMART_EXIT_ENABLED or not initialize_mt5():return 0
    count=0
    for p in own_positions():
        try:decision=evaluate_smart_exit(p,build_market_snapshot(p.symbol))
        except Exception as exc:print("Smart exit analysis skipped:",exc); continue
        if decision["exit"] and initialize_mt5() and close_position(p,comment="Prime T smart exit"):
            count+=1; send_telegram(f"🧠 Smart exit\n{p.symbol} #{p.ticket}\nReason: {', '.join(decision['reasons'])}")
    mt5.shutdown(); return count
