import MetaTrader5 as mt5

from core.data_loader import get_candles
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr
from config.settings import (
    BUY_RSI_MAX,
    BUY_RSI_MIN,
    RISK_PERCENT,
    SELL_RSI_MAX,
    SELL_RSI_MIN,
    SL_ATR_MULTIPLIER,
    SYMBOL,
    TP_ATR_MULTIPLIER,
)

START_BALANCE = 100.0

balance = START_BALANCE
peak_balance = START_BALANCE
max_drawdown = 0.0

wins = 0
losses = 0

df = get_candles(SYMBOL, timeframe=mt5.TIMEFRAME_M15, count=1000)
h1 = get_candles(SYMBOL, timeframe=mt5.TIMEFRAME_H1, count=300)

df["EMA20"] = calculate_ema(df, 20)
df["EMA50"] = calculate_ema(df, 50)
df["EMA200"] = calculate_ema(df, 200)
df["RSI"] = calculate_rsi(df)
df["ATR"] = calculate_atr(df)

h1["EMA50"] = calculate_ema(h1, 50)
h1["EMA200"] = calculate_ema(h1, 200)

h1_last = h1.iloc[-1]
h1_trend = "BULLISH" if h1_last["EMA50"] > h1_last["EMA200"] else "BEARISH"

print(f"H1 Trend Used: {h1_trend}")

for i in range(200, len(df) - 10):
    row = df.iloc[i]
    future = df.iloc[i + 1:i + 11]

    buy_signal = (
        row["close"] > row["EMA20"] > row["EMA50"] > row["EMA200"]
        and BUY_RSI_MIN <= row["RSI"] <= BUY_RSI_MAX
        and h1_trend == "BULLISH"
    )

    sell_signal = (
        row["close"] < row["EMA20"] < row["EMA50"] < row["EMA200"]
        and SELL_RSI_MIN <= row["RSI"] <= SELL_RSI_MAX
        and h1_trend == "BEARISH"
    )

    result = None

    if buy_signal:
        entry = row["close"]
        sl = entry - (row["ATR"] * SL_ATR_MULTIPLIER)
        tp = entry + (row["ATR"] * TP_ATR_MULTIPLIER)

        for _, candle in future.iterrows():
            if candle["low"] <= sl:
                result = "LOSS"
                break
            if candle["high"] >= tp:
                result = "WIN"
                break

    elif sell_signal:
        entry = row["close"]
        sl = entry + (row["ATR"] * SL_ATR_MULTIPLIER)
        tp = entry - (row["ATR"] * TP_ATR_MULTIPLIER)

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
