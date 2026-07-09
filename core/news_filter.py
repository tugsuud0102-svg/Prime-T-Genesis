import csv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from config.settings import (
    NEWS_BLACKOUT_FILE,
    NEWS_BLOCK_IMPACTS,
    NEWS_FILTER_ENABLED,
    NEWS_MINUTES_AFTER,
    NEWS_MINUTES_BEFORE,
)


LOCAL_TZ = ZoneInfo("Asia/Ulaanbaatar")


def _parse_news_time(value):
    value = value.strip()

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=LOCAL_TZ)
        except ValueError:
            continue

    raise ValueError(f"Invalid news time: {value}")


def load_news_events(filename=NEWS_BLACKOUT_FILE):
    events = []

    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                impact = row.get("impact", "").strip().upper()
                if impact not in NEWS_BLOCK_IMPACTS:
                    continue

                events.append(
                    {
                        "time": _parse_news_time(row.get("time", "")),
                        "currency": row.get("currency", "").strip().upper(),
                        "impact": impact,
                        "title": row.get("title", "").strip(),
                    }
                )
    except FileNotFoundError:
        return []

    return events


def news_blackout_reason(now=None):
    if not NEWS_FILTER_ENABLED:
        return None

    now = now or datetime.now(LOCAL_TZ)
    before = timedelta(minutes=NEWS_MINUTES_BEFORE)
    after = timedelta(minutes=NEWS_MINUTES_AFTER)

    for event in load_news_events():
        starts = event["time"] - before
        ends = event["time"] + after

        if starts <= now <= ends:
            title = event["title"] or "Scheduled news"
            return (
                f"NEWS BLOCK: {event['currency']} {event['impact']} {title} "
                f"at {event['time'].strftime('%Y-%m-%d %H:%M')}"
            )

    return None
