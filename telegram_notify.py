import requests


BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


def send_telegram_message(message: str) -> bool:
    """Отправляет сообщение в Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as error:
        print(f"Ошибка отправки сообщения: {error}")
        return False


if __name__ == "__main__":
    result = send_telegram_message(
        "FitTrack: создана новая тренировка «Кардио» на 45 минут."
    )

    if result:
        print("Сообщение успешно отправлено")
    else:
        print("Сообщение не отправлено")