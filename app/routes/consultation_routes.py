from fastapi import APIRouter, Depends
from datetime import date, timedelta

from app.database.supabase_client import supabase
from app.schemas.consultation_schema import ConsultationResponseSchema
from app.auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/consultations",
    tags=["Consultations"]
)


# ==========================================
# PROTECTED ROUTES (Frontend)
# ==========================================

@router.get("/today")
def get_today_consultations(
    email: str = Depends(get_current_user)
):
    today = date.today().isoformat()

    result = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .eq("next_consultation_date", today)
        .execute()
    )

    return result.data


@router.get("/tomorrow")
def get_tomorrow_consultations(
    email: str = Depends(get_current_user)
):
    tomorrow = (
        date.today() + timedelta(days=1)
    ).isoformat()

    result = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .eq("next_consultation_date", tomorrow)
        .execute()
    )

    return result.data


@router.get("/upcoming")
def get_upcoming_consultations(
    email: str = Depends(get_current_user)
):
    today = date.today().isoformat()

    result = (
        supabase
        .table("patients")
        .select("*")
        .eq("doctor_email", email)
        .gte(
            "next_consultation_date",
            today
        )
        .order(
            "next_consultation_date"
        )
        .execute()
    )

    return result.data


# ==========================================
# PUBLIC ROUTES (n8n)
# ==========================================

@router.get("/tomorrow-public")
def get_tomorrow_consultations_public():

    tomorrow = (
        date.today() + timedelta(days=1)
    ).isoformat()

    result = (
        supabase
        .table("patients")
        .select("*")
        .eq(
            "next_consultation_date",
            tomorrow
        )
        .execute()
    )

    return result.data


@router.get("/upcoming-public")
def get_upcoming_consultations_public():

    today = date.today().isoformat()

    result = (
        supabase
        .table("patients")
        .select("*")
        .gte(
            "next_consultation_date",
            today
        )
        .order(
            "next_consultation_date"
        )
        .execute()
    )

    return result.data


# ==========================================
# WHATSAPP RESPONSE HANDLER
# ==========================================
@router.post("/respond")
def consultation_response(
    data: ConsultationResponseSchema
):

    mobile = str(
        data.mobile_number
    ).strip()

    if len(mobile) > 10:
        mobile = mobile[-10:]

    response = (
        data.response
        .upper()
        .strip()
    )

    # CANCEL

    if response in ["NO", "2"]:

        result = (
            supabase
            .table("patients")
            .update({
                "next_consultation_date": None,
                "appointment_status": "CANCELLED"
            })
            .eq(
                "mobile_number",
                mobile
            )
            .execute()
        )

        return {
            "message":
            "Consultation cancelled",
            "data":
            result.data
        }

    # CONFIRM

    elif response in ["YES", "1"]:

        result = (
            supabase
            .table("patients")
            .update({
                "appointment_status":
                "CONFIRMED"
            })
            .eq(
                "mobile_number",
                mobile
            )
            .execute()
        )

        return {
            "message":
            "Appointment confirmed",
            "data":
            result.data
        }

    return {
        "message":
        "Invalid response"
    }