from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_notifications():
    return {
        "notifications": []
    }

@router.post("/read-all")
def mark_all_read():
    return {
        "success": True,
        "message": "All notifications marked as read"
    }