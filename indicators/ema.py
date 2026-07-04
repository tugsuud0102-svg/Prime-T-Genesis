def calculate_ema(
    df,
    period: int,
    price_column: str = "close"
):
    return df[price_column].ewm(
        span=period,
        adjust=False
    ).mean()