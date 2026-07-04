def calculate_atr(df, period: int = 14):
    high_low = df["high"] - df["low"]

    high_prev_close = abs(
        df["high"] - df["close"].shift()
    )

    low_prev_close = abs(
        df["low"] - df["close"].shift()
    )

    true_range = high_low.to_frame("hl")

    true_range["hpc"] = high_prev_close
    true_range["lpc"] = low_prev_close

    tr = true_range.max(axis=1)

    return tr.rolling(period).mean()