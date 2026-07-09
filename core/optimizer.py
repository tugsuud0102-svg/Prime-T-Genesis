import csv
from itertools import product
from pathlib import Path

import MetaTrader5 as mt5

from config.settings import OPTIMIZER_RESULTS_FILE, RISK_PERCENT, SYMBOL
from core.data_loader import get_candles
from indicators.atr import calculate_atr
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi


def _simulate(df, params):
    balance = 1000.0
    peak = balance
    max_drawdown = 0.0
    wins = 0
    losses = 0
    gross_win = 0.0
    gross_loss = 0.0

    for i in range(200, len(df) - 12):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        future = df.iloc[i + 1:i + 13]

        ema_gap_ok = abs(row["EMA20"] - row["EMA50"]) >= (
            row["ATR"] * params["min_ema_gap_atr"]
        )
        atr_ok = params["min_atr"] <= row["ATR"] <= params["max_atr"]

        buy_signal = (
            row["close"] > row["EMA20"] > row["EMA50"] > row["EMA200"]
            and params["buy_rsi_min"] <= row["RSI"] <= params["buy_rsi_max"]
            and row["close"] > row["open"]
            and row["close"] > prev["high"]
            and ema_gap_ok
            and atr_ok
        )

        sell_signal = (
            row["close"] < row["EMA20"] < row["EMA50"] < row["EMA200"]
            and params["sell_rsi_min"] <= row["RSI"] <= params["sell_rsi_max"]
            and row["close"] < row["open"]
            and row["close"] < prev["low"]
            and ema_gap_ok
            and atr_ok
        )

        if not buy_signal and not sell_signal:
            continue

        entry = row["close"]
        risk_amount = balance * (RISK_PERCENT / 100)
        result = None

        if buy_signal:
            sl = entry - (row["ATR"] * params["sl_atr"])
            tp = entry + (row["ATR"] * params["tp_atr"])

            for _, candle in future.iterrows():
                if candle["low"] <= sl:
                    result = -risk_amount
                    break
                if candle["high"] >= tp:
                    result = risk_amount * (params["tp_atr"] / params["sl_atr"])
                    break

        if sell_signal:
            sl = entry + (row["ATR"] * params["sl_atr"])
            tp = entry - (row["ATR"] * params["tp_atr"])

            for _, candle in future.iterrows():
                if candle["high"] >= sl:
                    result = -risk_amount
                    break
                if candle["low"] <= tp:
                    result = risk_amount * (params["tp_atr"] / params["sl_atr"])
                    break

        if result is None:
            continue

        balance += result
        if result > 0:
            wins += 1
            gross_win += result
        else:
            losses += 1
            gross_loss += abs(result)

        peak = max(peak, balance)
        max_drawdown = max(max_drawdown, ((peak - balance) / peak) * 100)

    trades = wins + losses
    return {
        **params,
        "trades": trades,
        "wins": wins,
        "losses": losses,
        "win_rate": round((wins / trades) * 100, 2) if trades else 0.0,
        "profit": round(balance - 1000.0, 2),
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss else 0.0,
        "max_drawdown": round(max_drawdown, 2),
    }


def run_optimizer():
    df = get_candles(SYMBOL, timeframe=mt5.TIMEFRAME_M15, count=2000)
    df["EMA20"] = calculate_ema(df, 20)
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)
    df["RSI"] = calculate_rsi(df)
    df["ATR"] = calculate_atr(df)

    grid = product(
        [58, 60, 62],
        [70, 72, 74],
        [26, 28, 30],
        [38, 40, 42],
        [2.0, 2.2],
        [3.0, 3.5],
        [2.0, 3.0, 4.0],
        [25.0, 30.0, 35.0],
        [0.06, 0.08, 0.10],
    )

    results = []
    for values in grid:
        params = {
            "buy_rsi_min": values[0],
            "buy_rsi_max": values[1],
            "sell_rsi_min": values[2],
            "sell_rsi_max": values[3],
            "sl_atr": values[4],
            "tp_atr": values[5],
            "min_atr": values[6],
            "max_atr": values[7],
            "min_ema_gap_atr": values[8],
        }
        results.append(_simulate(df, params))

    results.sort(
        key=lambda row: (row["profit_factor"], row["profit"], row["win_rate"]),
        reverse=True,
    )

    path = Path(OPTIMIZER_RESULTS_FILE)
    path.parent.mkdir(exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    return results[:10]
