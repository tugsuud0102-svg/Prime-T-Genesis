import os
import requests

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def _safe_json(response):
    try:
        payload = response.json()
        return payload if isinstance(payload, dict) else {}
    except (TypeError, ValueError):
        return {}


def _log_api_error(action, payload, response=None):
    error_code = payload.get("error_code")
    if error_code is None and response is not None:
        error_code = getattr(response, "status_code", None)
    description = payload.get("description") or "Telegram API request failed"
    print(f"{action}: error_code={error_code} description={description}")


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
        data["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)

    try:
        response = requests.post(url, data=data, timeout=10)
        payload = _safe_json(response)
        if payload.get("ok"):
            return payload
        _log_api_error("Telegram send error", payload, response)
        return None
    except requests.RequestException as exc:
        print(f"Telegram send error: network_error={type(exc).__name__}")
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
        payload = _safe_json(response)
        if payload.get("ok"):
            return True
        _log_api_error("Telegram callback acknowledgement error", payload, response)
        return False
    except requests.RequestException as exc:
        print(
            "Telegram callback acknowledgement error: "
            f"network_error={type(exc).__name__}"
        )
        return False

def edit_telegram_message(message_id, message, reply_markup=None, chat_id=None):
    target_chat_id = chat_id if chat_id is not None else CHAT_ID
    if not BOT_TOKEN or not target_chat_id or not message_id:
        return None
    import json
    data = {
        "chat_id": target_chat_id,
        "message_id": message_id,
        "text": message,
    }
    if reply_markup is not None:
        data["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            data=data,
            timeout=10,
        )
        payload = _safe_json(response)
        if payload.get("ok"):
            return payload
        description = str(payload.get("description") or "")
        if "message is not modified" in description.lower():
            # Repeated buttons/refreshes with identical text and markup are valid.
            return {"ok": True, "no_op": True}
        _log_api_error("Telegram edit error", payload, response)
        return None
    except requests.RequestException as exc:
        print(f"Telegram edit error: network_error={type(exc).__name__}")
        return None
