import smtplib
from email.mime.text import MIMEText

from app.config.settings import (
    MAIL_USERNAME,
    MAIL_PASSWORD
)


async def send_otp_email(
    email: str,
    otp: str
):

    msg = MIMEText(
        f"""
Your SHMS password reset OTP is:

{otp}

Valid for 5 minutes.
"""
    )

    msg["Subject"] = "SHMS Password Reset OTP"
    msg["From"] = MAIL_USERNAME
    msg["To"] = email

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        MAIL_USERNAME,
        MAIL_PASSWORD
    )

    server.send_message(msg)

    server.quit()