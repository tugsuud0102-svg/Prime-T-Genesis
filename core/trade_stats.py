from pathlib import Path

LOG_FILE = Path("logs/trades.log")


def show_trade_stats():
    if not LOG_FILE.exists():
        print("No trades.log found")
        return

    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()

    executed = [line for line in lines if "EXECUTED" in line]
    failed = [line for line in lines if "FAILED" in line]

    buy_count = sum(1 for line in executed if "| BUY |" in line)
    sell_count = sum(1 for line in executed if "| SELL |" in line)

    print("=" * 40)
    print("PRIME T TRADE STATS")
    print(f"Executed Trades : {len(executed)}")
    print(f"BUY Trades      : {buy_count}")
    print(f"SELL Trades     : {sell_count}")
    print(f"Failed Orders   : {len(failed)}")
    print("=" * 40)


if __name__ == "__main__":
    show_trade_stats()