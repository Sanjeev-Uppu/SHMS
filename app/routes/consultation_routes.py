from fastapi import APIRouter, Depends
from datetime import date, timedelta

from app.database.supabase_client import supabase
from app.schemas.consultation_schema import ConsultationResponseSchema
from app.auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/consultations",
    tags=["Consultations"]
)


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


@router.post("/respond")
def consultation_response(
    data: ConsultationResponseSchema
):
    print("Raw Mobile:", data.mobile_number)
    print("Raw Mobile Repr:", repr(data.mobile_number))
    print("Response:", data.response)

    mobile = str(data.mobile_number).strip()

    # Take last 10 digits
    if len(mobile) > 10:
        mobile = mobile[-10:]

    print("DB Mobile:", mobile)

    patient = (
        supabase
        .table("patients")
        .select("*")
        .eq("mobile_number", mobile)
        .execute()
    )

    print("Patient Found:", patient.data)

    response = data.response.upper().strip()

    if response in ["NO", "2"]:

        result = (
            supabase
            .table("patients")
            .update({
                "next_consultation_date": None
            })
            .eq("mobile_number", mobile)
            .execute()
        )

        print("Update Result:", result.data)

        return {
            "message": "Consultation cancelled",
            "received_mobile": data.mobile_number,
            "db_mobile": mobile,
            "data": result.data
        }

    elif response in ["YES", "1"]:

        return {
            "message": "Appointment confirmed",
            "received_mobile": data.mobile_number,
            "db_mobile": mobile
        }

    return {
        "message": "Invalid response. Use YES/NO or 1/2"
    } 