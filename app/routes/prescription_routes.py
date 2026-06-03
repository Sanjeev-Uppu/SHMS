from fastapi import APIRouter, Depends

from app.schemas.prescription_schema import PrescriptionCreate
from app.services.prescription_service import (
    create_prescription,
    get_all_prescriptions,
    get_prescription,
    update_prescription,
    delete_prescription,
    delete_medicine
)
from app.auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


@router.post("/")
def create(
    data: PrescriptionCreate,
    email: str = Depends(get_current_user)
):
    return create_prescription(data, email)


@router.get("/")
def get_all(
    email: str = Depends(get_current_user)
):
    return get_all_prescriptions(email)


@router.get("/{id}")
def get_by_id(
    id: str,
    email: str = Depends(get_current_user)
):
    return get_prescription(id, email)


@router.put("/{id}")
def update(
    id: str,
    data: PrescriptionCreate,
    email: str = Depends(get_current_user)
):
    return update_prescription(id, data, email)


@router.delete("/{id}")
def delete(
    id: str,
    email: str = Depends(get_current_user)
):
    return delete_prescription(id, email)


@router.delete("/medicine/{item_id}")
def delete_med(item_id: str):
    return delete_medicine(item_id)