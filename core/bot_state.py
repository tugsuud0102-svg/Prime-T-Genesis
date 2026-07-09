from pathlib import Path

from config.settings import PAUSE_FILE


def is_paused():
    return Path(PAUSE_FILE).exists()


def pause_bot():
    path = Path(PAUSE_FILE)
    path.parent.mkdir(exist_ok=True)
    path.write_text("paused", encoding="utf-8")


def resume_bot():
    path = Path(PAUSE_FILE)
    if path.exists():
        path.unlink()
