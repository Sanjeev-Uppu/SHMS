from fastapi import APIRouter, Query, Depends
from app.database.supabase_client import supabase
from app.auth.jwt_handler import get_current_user

router = APIRouter()

@router.get("/patient-search")
def search_patients(
    keyword: str = Query(..., min_length=1),
    email: str = Depends(get_current_user)
):

    response = (
        supabase
        .table("patients")
        .select(
            "id,patient_name,mobile_number,appointment_status"
        )
        .eq("doctor_email", email)  # <-- only logged-in doctor's patients
        .or_(
            f"patient_name.ilike.%{keyword}%,"
            f"mobile_number.ilike.%{keyword}%,"
            f"symptoms.ilike.%{keyword}%,"
            f"diagnosis.ilike.%{keyword}%,"
            f"appointment_status.ilike.%{keyword}%"
        )
        .limit(10)
        .execute()
    )

    return response.data