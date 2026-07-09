from datetime import datetime
from zoneinfo import ZoneInfo

from config.settings import (
    SESSION_END_HOUR,
    SESSION_FILTER_ENABLED,
    SESSION_START_HOUR,
)


LOCAL_TZ = ZoneInfo("Asia/Ulaanbaatar")


def session_block_reason(now=None):
    if not SESSION_FILTER_ENABLED:
        return None

    now = now or datetime.now(LOCAL_TZ)
    hour = now.hour

    if SESSION_START_HOUR <= SESSION_END_HOUR:
        in_session = SESSION_START_HOUR <= hour < SESSION_END_HOUR
    else:
        in_session = hour >= SESSION_START_HOUR or hour < SESSION_END_HOUR

    if in_session:
        return None

    return (
        f"SESSION BLOCK: outside trading hours "
        f"{SESSION_START_HOUR:02d}:00-{SESSION_END_HOUR:02d}:00"
    )
