import time

from main import main
from core.break_even_engine import manage_break_even
from core.atr_trailing_engine import manage_atr_trailing
from core.partial_close import manage_partial_close
from core.smart_exit_manager import manage_smart_exits
from core.time_exit_manager import manage_time_exits
from core.equity_guard import equity_protection
from core.daily_target import daily_target_hit
from core.forexfactory import update_news_blackout
from core.dashboard import send_daily_dashboard_if_due
from core.telegram_commands import handle_telegram_commands
from trade_stats.closed_trade_sync import sync_closed_trades
from config.settings import LOOP_SECONDS, TRADING_MODE, TIMEFRAME_NAME


print("=" * 50)
print("Prime T Genesis v4.1.3")
print(f"Mode: {TRADING_MODE}")
print(f"Timeframe: {TIMEFRAME_NAME}")
print("=" * 50)

def _safe_call(name, function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except Exception as exc:
        print(f"{name} skipped: {exc}")
        return None

def run_forever():
 while True:
    try:
        print("\nUpdating ForexFactory news...")
        try:
            _safe_call("ForexFactory update", update_news_blackout)
        except Exception as e:
            print("ForexFactory update skipped:", e)

        print("\nChecking Telegram commands...")
        try:
            _safe_call("Telegram commands", handle_telegram_commands)
        except Exception as e:
            print("Telegram command check skipped:", e)

        print("\nChecking daily Telegram dashboard...")
        try:
            _safe_call("Telegram dashboard", send_daily_dashboard_if_due)
        except Exception as e:
            print("Telegram dashboard skipped:", e)

        print("\nChecking daily profit target...")
        _safe_call("Closed trade sync", sync_closed_trades)
        if _safe_call("Daily target", daily_target_hit):
            print("DAILY TARGET REACHED")
            print("BOT STOPPED")
            break

        print("\nChecking equity protection...")
        if _safe_call("Equity protection", equity_protection):
            print("BOT STOPPED - MAX LOSS REACHED")
            break

        print("\nChecking position management...")
        _safe_call("Smart exits", manage_smart_exits)
        _safe_call("Time exits", manage_time_exits)
        _safe_call("Partial close", manage_partial_close)
        _safe_call("Break-even", manage_break_even)
        _safe_call("ATR trailing", manage_atr_trailing)

        print("\nChecking market signal...")
        _safe_call("Signal cycle", main, True)

    except Exception as e:
        print("ERROR:", e)

    print(f"\nSleeping {LOOP_SECONDS} seconds...")
    time.sleep(LOOP_SECONDS)

if __name__ == "__main__":
    run_forever()
