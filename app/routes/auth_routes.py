from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth_schema import (
    SignupSchema,
    LoginSchema,
    ForgotPasswordSchema,
    VerifyOTPSchema,
    ResetPasswordSchema
)
from app.services.auth_service import signup_user, login_user
from app.auth.jwt_handler import get_current_user
from app.database.supabase_client import supabase
from app.auth.password_handler import hash_password
from app.services.email_service import send_otp_email
from app.services.otp_service import (
    save_otp,
    verify_otp,
    delete_otp
)

import random

router = APIRouter()


@router.post("/signup")
def signup(data: SignupSchema):
    return signup_user(data)


@router.post("/login")
def login(data: LoginSchema):
    return login_user(data)


@router.get("/me")
def me(email: str = Depends(get_current_user)):

    result = (
        supabase.table("doctors")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not result.data:
        return {
            "success": False,
            "message": "Doctor not found"
        }

    doctor = result.data[0]

    return {
        "user": {
            "id": doctor.get("id"),
            "fullName": doctor.get("full_name"),
            "hospital": doctor.get("hospital_name"),
            "email": doctor.get("email"),
            "phone": doctor.get("phone_number"),
        }
    }


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema):

    result = (
        supabase.table("doctors")
        .select("*")
        .eq("email", data.email)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Email not registered"
        )

    otp = str(random.randint(100000, 999999))

    save_otp(data.email, otp)

    await send_otp_email(
        data.email,
        otp
    )

    return {
        "success": True,
        "message": "OTP sent successfully"
    }


@router.post("/verify-otp")
def verify_otp_route(data: VerifyOTPSchema):

    if not verify_otp(
        data.email,
        data.otp
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    return {
        "success": True,
        "message": "OTP verified successfully"
    }


@router.post("/reset-password")
def reset_password(data: ResetPasswordSchema):

    if not verify_otp(
        data.email,
        data.otp
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    hashed_password = hash_password(
        data.new_password
    )

    (
        supabase.table("doctors")
        .update({
            "hashed_password": hashed_password
        })
        .eq("email", data.email)
        .execute()
    )

    delete_otp(data.email)

    return {
        "success": True,
        "message": "Password reset successful"
    }