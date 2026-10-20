import requests
from django.conf import settings


def send_message(chat_id: str, text: str) -> None:
    url = f"{settings.TELEGRAM_URL}{settings.TG_API_KEY}/sendMessage"
    requests.get(url, params={"chat_id": chat_id, "text": text}, timeout=10)
