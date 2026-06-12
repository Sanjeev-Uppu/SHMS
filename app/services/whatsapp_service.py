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
🏥 *SHMS Hospital - Medicine Reminder*

Dear Patient,

💊 *Medicine:* {medicine_name}

⏰ *Timing:* {timing}

Please take your medicine as prescribed by your doctor.

*SHMS Hospital Team* ❤️
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

    print(response.text)


def send_consultation_reminder(
    mobile,
    patient_name,
    consultation_date
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
🏥 *SHMS Hospital - Consultation Reminder*

Dear *{patient_name}*,

📅 *Follow-up Consultation Date:*
{consultation_date}

Your doctor has scheduled a follow-up consultation for tomorrow.

Please reply with:

✅ *1* - I will come
❌ *2* - My health is good

If you choose *2*, your follow-up appointment will be cancelled automatically.

*SHMS Hospital Team* ❤️
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
        f"Consultation WhatsApp Status: {response.status_code}"
    )

    print(response.text)