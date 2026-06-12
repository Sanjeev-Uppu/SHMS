from fastapi import APIRouter, Depends
from app.schemas.auth_schema import SignupSchema, LoginSchema
from app.services.auth_service import signup_user, login_user
from app.auth.jwt_handler import get_current_user
from app.database.supabase_client import supabase

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