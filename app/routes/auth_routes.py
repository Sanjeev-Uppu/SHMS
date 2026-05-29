from fastapi import APIRouter
from app.schemas.auth_schema import SignupSchema, LoginSchema
from app.services.auth_service import signup_user, login_user

router = APIRouter()

@router.post("/signup")
def signup(data: SignupSchema):
    return signup_user(data)

@router.post("/login")
def login(data: LoginSchema):
    return login_user(data)

@router.get("/me")
def me():
    return {"message": "Protected Route"}