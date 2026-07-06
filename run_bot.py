print("=" * 50)
print("Prime T Genesis v1.5")
print("Mode: DEMO LIVE")
print("Timeframe: M15")
print("=" * 50)
import time

from main import main
from core.trailing_stop import move_sl_to_break_even
from core.equity_guard import equity_protection


print("=" * 50)
print("Prime T Genesis Live Bot Started")
print("Mode: DEMO LIVE")
print("=" * 50)

while True:
    try:
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

    print("\nSleeping 30 seconds...")
    time.sleep(900)