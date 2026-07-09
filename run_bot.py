import time

from main import main
from core.trailing_stop import move_sl_to_break_even
from core.equity_guard import equity_protection
from core.daily_target import daily_target_hit
from core.forexfactory import update_news_blackout
from core.dashboard import send_daily_dashboard_if_due
from core.telegram_commands import handle_telegram_commands


print("=" * 50)
print("Prime T Genesis v1.7")
print("Mode: DEMO LIVE")
print("Timeframe: M15")
print("=" * 50)

while True:
    try:
        print("\nUpdating ForexFactory news...")
        try:
            update_news_blackout()
        except Exception as e:
            print("ForexFactory update skipped:", e)

        print("\nChecking Telegram commands...")
        try:
            handle_telegram_commands()
        except Exception as e:
            print("Telegram command check skipped:", e)

        print("\nChecking daily Telegram dashboard...")
        try:
            send_daily_dashboard_if_due()
        except Exception as e:
            print("Telegram dashboard skipped:", e)

        print("\nChecking daily profit target...")
        if daily_target_hit():
            print("DAILY TARGET REACHED")
            print("BOT STOPPED")
            break

        print("\nChecking equity protection...")
        if equity_protection():
            print("BOT STOPPED - MAX LOSS REACHED")
            break

        print("\nChecking positions / trailing stop...")
        move_sl_to_break_even(min_profit=5.0)

        print("\nChecking market signal...")
        main()

    except Exception as e:
        print("ERROR:", e)

    print("\nSleeping 900 seconds...")
    time.sleep(900)
