import csv
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from config.settings import (
    FOREX_FACTORY_CURRENCIES,
    FOREX_FACTORY_ENABLED,
    FOREX_FACTORY_URLS,
    NEWS_BLACKOUT_FILE,
    NEWS_BLOCK_IMPACTS,
)


LOCAL_TZ = ZoneInfo("Asia/Ulaanbaatar")


def _parse_forexfactory_time(value):
    return datetime.fromisoformat(value).astimezone(LOCAL_TZ)


def _fetch_events():
    events = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0 Safari/537.36"
        )
    }

    for url in FOREX_FACTORY_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            events.extend(response.json())
        except requests.RequestException as e:
            print(f"ForexFactory feed skipped: {url} | {e}")

    return events


def update_news_blackout():
    if not FOREX_FACTORY_ENABLED:
        return False

    events = _fetch_events()
    if not events:
        print("ForexFactory update skipped: no events fetched")
        return False

    rows = []

    for event in events:
        currency = event.get("country", "").strip().upper()
        impact = event.get("impact", "").strip().upper()

        if currency not in FOREX_FACTORY_CURRENCIES:
            continue

        if impact not in NEWS_BLOCK_IMPACTS:
            continue

        news_time = _parse_forexfactory_time(event.get("date", ""))
        rows.append(
            {
                "time": news_time.strftime("%Y-%m-%d %H:%M"),
                "currency": currency,
                "impact": impact,
                "title": event.get("title", "").strip(),
            }
        )

    rows.sort(key=lambda row: row["time"])

    if not rows:
        print("ForexFactory update skipped: no matching news events")
        return False

    with open(NEWS_BLACKOUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["time", "currency", "impact", "title"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"ForexFactory news updated: {len(rows)} events")
    return True
