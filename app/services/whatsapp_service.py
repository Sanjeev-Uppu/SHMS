import requests

from app.config.settings import (
    WHATSAPP_PHONE_NUMBER_ID,
    WHATSAPP_ACCESS_TOKEN
)


def send_whatsapp_message(
    mobile,
    medicine_name,
    timing
):

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization":
            f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type":
            "application/json"
    }

    message = f"""
🏥 SHMS Medicine Reminder

Medicine: {medicine_name}
Timing: {timing}

Please take your medicine as prescribed by your doctor.

Stay healthy ❤️
"""

    payload = {
        "messaging_product": "whatsapp",
        "to": mobile,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print(
        f"WhatsApp Status: {response.status_code}"
    )

    print(
        response.text
    )