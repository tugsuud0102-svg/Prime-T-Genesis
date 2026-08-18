"""Stable Telegram facade for alerts, polling, and the v4.1.3 menu."""
from core.telegram_alert import send_telegram
from core.telegram_commands import handle_telegram_commands
from core.telegram_menu import MAIN_TEXT, MAIN_KEYBOARD
__all__ = ["send_telegram", "handle_telegram_commands", "MAIN_TEXT", "MAIN_KEYBOARD"]
