from fastapi import APIRouter, Depends

from app.schemas.patient_schema import PatientSchema
from app.services.patient_service import (
    create_patient,
    get_all_patients,
    get_patient_by_mobile,
    update_patient,
    delete_patient
)
from app.auth.jwt_handler import get_current_user

router = APIRouter()


@router.post("/")
def add_patient(
    data: PatientSchema,
    email: str = Depends(get_current_user)
):
    return create_patient(data, email)


@router.get("/")
def all_patients(
    email: str = Depends(get_current_user)
):
    return get_all_patients(email)


@router.get("/{mobile}")
def single_patient(
    mobile: str,
    email: str = Depends(get_current_user)
):
    return get_patient_by_mobile(mobile, email)


@router.put("/{mobile}")
def edit_patient(
    mobile: str,
    data: PatientSchema,
    email: str = Depends(get_current_user)
):
    return update_patient(mobile, data, email)


@router.delete("/{mobile}")
def remove_patient(
    mobile: str,
    email: str = Depends(get_current_user)
):
    return delete_patient(mobile, email)