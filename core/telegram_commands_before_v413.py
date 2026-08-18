from pathlib import Path
from time import time

import requests

from config.settings import TELEGRAM_COMMANDS_ENABLED, TELEGRAM_OFFSET_FILE
from core.bot_state import is_paused, pause_bot, resume_bot
from core.close_all import close_all_positions
from core.dashboard import build_dashboard_message
from core.telegram_alert import BOT_TOKEN, CHAT_ID, send_telegram


def _read_offset():
    path = Path(TELEGRAM_OFFSET_FILE)
    if not path.exists():
        return None

    value = path.read_text(encoding="utf-8").strip()
    return int(value) if value else None


def _write_offset(offset):
    path = Path(TELEGRAM_OFFSET_FILE)
    path.parent.mkdir(exist_ok=True)
    path.write_text(str(offset), encoding="utf-8")


def _reply_for_command(text):
    command = text.strip().split()[0].lower()

    if command == "/status":
        state = "PAUSED" if is_paused() else "RUNNING"
        return f"Prime T Genesis status: {state}"

    if command == "/today":
        return build_dashboard_message()

    if command == "/pause":
        pause_bot()
        return "Bot paused"

    if command == "/resume":
        resume_bot()
        return "Bot resumed"

    if command == "/close_all":
        if text.strip().lower() != "/close_all confirm":
            return "Use /close_all confirm to close all positions"
        close_all_positions()
        return "Close all command executed"

    if command == "/help":
        return "Commands: /status /today /pause /resume /close_all confirm"

    return None


def handle_telegram_commands():
    if not TELEGRAM_COMMANDS_ENABLED or not BOT_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 1}
    offset = _read_offset()
    if offset is not None:
        params["offset"] = offset

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    for update in data.get("result", []):
        _write_offset(update["update_id"] + 1)
        message = update.get("message", {})
        chat = message.get("chat", {})

        if str(chat.get("id")) != str(CHAT_ID):
            continue

        if int(time()) - int(message.get("date", 0)) > 300:
            continue

        text = message.get("text", "")
        reply = _reply_for_command(text)
        if reply:
            send_telegram(reply)
