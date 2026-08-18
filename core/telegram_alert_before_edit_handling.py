import os
import requests

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message, reply_markup=None):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram config missing")
        return None

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    if reply_markup:
        import json
        data["reply_markup"] = json.dumps(reply_markup)

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Telegram Error:", e)
        return None

def answer_callback_query(callback_query_id, text=None):
    if not BOT_TOKEN or not callback_query_id:
        return False
    data = {"callback_query_id": callback_query_id}
    if text:
        data["text"] = text
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
            data=data,
            timeout=5,
        )
        response.raise_for_status()
        return bool(response.json().get("ok"))
    except Exception as exc:
        print("Telegram callback acknowledgement error:", exc)
        return False

def edit_telegram_message(message_id, message, reply_markup=None):
    if not BOT_TOKEN or not CHAT_ID or not message_id:
        return None
    import json
    data = {"chat_id": CHAT_ID, "message_id": message_id, "text": message}
    if reply_markup is not None:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            data=data,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        print("Telegram edit error:", exc)
        return None
