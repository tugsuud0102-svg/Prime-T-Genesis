import MetaTrader5 as mt5
from datetime import datetime, timedelta

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
BOT_MAGIC = 20260704
SYMBOL = "GOLD"


def show_history_stats(days=30):
    if not mt5.initialize(path=MT5_PATH):
        print(mt5.last_error())
        return

    date_to = datetime.now()
    date_from = date_to - timedelta(days=days)

    deals = mt5.history_deals_get(date_from, date_to)

    if deals is None:
        print("No history found")
        mt5.shutdown()
        return

    trade_deals = []

    for deal in deals:
        if (
            deal.symbol == SYMBOL
            and deal.magic == BOT_MAGIC
            and deal.entry == mt5.DEAL_ENTRY_OUT
        ):
            trade_deals.append(deal)

    wins = 0
    losses = 0
    total_profit = 0.0
    gross_win = 0.0
    gross_loss = 0.0

    for deal in trade_deals:
        profit = deal.profit + deal.commission + deal.swap
        total_profit += profit

        if profit > 0:
            wins += 1
            gross_win += profit
        elif profit < 0:
            losses += 1
            gross_loss += abs(profit)

    total = wins + losses

    print("=" * 50)
    print("PRIME T BOT HISTORY STATS")
    print(f"Closed Bot Trades : {total}")
    print(f"Wins              : {wins}")
    print(f"Losses            : {losses}")

    if total > 0:
        print(f"Win Rate          : {(wins / total) * 100:.2f}%")

    print(f"Net Profit        : ${total_profit:.2f}")

    if gross_loss > 0:
        print(f"Profit Factor     : {gross_win / gross_loss:.2f}")
    else:
        print("Profit Factor     : N/A")

    print("=" * 50)

    mt5.shutdown()


if __name__ == "__main__":
    show_history_stats()