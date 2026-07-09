import csv
from datetime import datetime
from pathlib import Path

from config.settings import TRADE_JOURNAL_FILE


FIELDS = [
    "time",
    "symbol",
    "signal",
    "mode",
    "entry",
    "sl",
    "tp",
    "volume",
    "rsi",
    "atr",
    "spread",
    "trend",
    "reasons",
]


def record_signal(
    symbol,
    signal,
    mode,
    entry=None,
    sl=None,
    tp=None,
    volume=None,
    rsi=None,
    atr=None,
    spread=None,
    trend=None,
    reasons=None,
):
    path = Path(TRADE_JOURNAL_FILE)
    path.parent.mkdir(exist_ok=True)
    is_new = not path.exists()

    row = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "signal": signal,
        "mode": mode,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "volume": volume,
        "rsi": rsi,
        "atr": atr,
        "spread": spread,
        "trend": trend,
        "reasons": "; ".join(reasons or []),
    }

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)
