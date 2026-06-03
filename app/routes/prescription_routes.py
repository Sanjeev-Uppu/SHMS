from fastapi import APIRouter
from app.schemas.prescription_schema import PrescriptionCreate
from app.services.prescription_service import *

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)

@router.post("/")
def create(data: PrescriptionCreate):
    return create_prescription(data)

@router.get("/")
def get_all():
    return get_all_prescriptions()

@router.get("/{id}")
def get_by_id(id: str):
    return get_prescription(id)

@router.put("/{id}")
def update(id: str, data: PrescriptionCreate):
    return update_prescription(id, data)

@router.delete("/{id}")
def delete(id: str):
    return delete_prescription(id)

@router.delete("/medicine/{item_id}")
def delete_med(item_id: str):
    return delete_medicine(item_id)