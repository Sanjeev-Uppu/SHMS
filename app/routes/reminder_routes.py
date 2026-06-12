from fastapi import APIRouter
from app.services.reminder_service import get_due_reminders

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"]
)


@router.get("/due")
def fetch_due_reminders():
    return get_due_reminders()