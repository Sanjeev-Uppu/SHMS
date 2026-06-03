from fastapi import APIRouter, Depends

from app.services.dashboard_service import get_dashboard_data
from app.auth.jwt_handler import get_current_user

router = APIRouter()


@router.get("/")
def dashboard(
    email: str = Depends(get_current_user)
):
    return get_dashboard_data(email)