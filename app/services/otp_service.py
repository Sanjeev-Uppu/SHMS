from datetime import datetime, timedelta
from app.database.supabase_client import supabase


def save_otp(email: str, otp: str):

    expires_at = (
        datetime.utcnow() +
        timedelta(minutes=5)
    ).isoformat()

    supabase.table(
        "password_reset_otps"
    ).insert({
        "email": email,
        "otp": otp,
        "expires_at": expires_at
    }).execute()


def verify_otp(email: str, otp: str):

    result = (
        supabase.table("password_reset_otps")
        .select("*")
        .eq("email", email)
        .eq("otp", otp)
        .execute()
    )

    if not result.data:
        return False

    record = result.data[0]

    expires_at = datetime.fromisoformat(
        record["expires_at"]
    )

    if datetime.utcnow() > expires_at:
        return False

    return True


def delete_otp(email: str):

    (
        supabase.table("password_reset_otps")
        .delete()
        .eq("email", email)
        .execute()
    )