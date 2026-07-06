from core.data_loader import get_candles
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr

START_BALANCE = 100.0
RISK_PERCENT = 0.5

balance = START_BALANCE
peak_balance = START_BALANCE
max_drawdown = 0.0

wins = 0
losses = 0

df = get_candles("GOLD", count=1000)

df["EMA20"] = calculate_ema(df, 20)
df["EMA50"] = calculate_ema(df, 50)
df["EMA200"] = calculate_ema(df, 200)
df["RSI"] = calculate_rsi(df)
df["ATR"] = calculate_atr(df)

for i in range(200, len(df) - 10):
    row = df.iloc[i]
    future = df.iloc[i + 1:i + 11]

    buy_signal = (
        row["close"] > row["EMA20"] > row["EMA50"] > row["EMA200"]
        and row["RSI"] >= 60
    )

    sell_signal = (
        row["close"] < row["EMA20"] < row["EMA50"] < row["EMA200"]
        and row["RSI"] <= 40
    )

    result = None

    if buy_signal:
        entry = row["close"]
        sl = entry - (row["ATR"] * 2)
        tp = entry + (row["ATR"] * 3)

        for _, candle in future.iterrows():
            if candle["low"] <= sl:
                result = "LOSS"
                break
            if candle["high"] >= tp:
                result = "WIN"
                break

    elif sell_signal:
        entry = row["close"]
        sl = entry + (row["ATR"] * 2)
        tp = entry - (row["ATR"] * 3)

        for _, candle in future.iterrows():
            if candle["high"] >= sl:
                result = "LOSS"
                break
            if candle["low"] <= tp:
                result = "WIN"
                break

    if result == "WIN":
        wins += 1
        risk_amount = balance * (RISK_PERCENT / 100)
        balance += risk_amount * 1.5

    elif result == "LOSS":
        losses += 1
        risk_amount = balance * (RISK_PERCENT / 100)
        balance -= risk_amount

    if result in ["WIN", "LOSS"]:
        peak_balance = max(peak_balance, balance)
        drawdown = (peak_balance - balance) / peak_balance * 100
        max_drawdown = max(max_drawdown, drawdown)

total = wins + losses
net_r = (wins * 1.5) - losses

print("=" * 50)
print("PRIME T GENESIS BACKTEST")
print(f"Wins         : {wins}")
print(f"Losses       : {losses}")
print(f"Trades       : {total}")

if total > 0:
    print(f"Win Rate     : {(wins / total) * 100:.2f}%")

print(f"Net R        : {net_r:.2f}R")
print("-" * 50)
print("ACCOUNT SIMULATION")
print(f"Start Balance: ${START_BALANCE:.2f}")
print(f"End Balance  : ${balance:.2f}")
print(f"Profit       : ${balance - START_BALANCE:.2f}")
print(f"Return       : {((balance - START_BALANCE) / START_BALANCE) * 100:.2f}%")
print(f"Max Drawdown : {max_drawdown:.2f}%")
print("=" * 50)