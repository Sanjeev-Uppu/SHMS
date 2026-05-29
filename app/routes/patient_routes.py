from fastapi import APIRouter
from app.schemas.patient_schema import PatientSchema
from app.services.patient_service import (
    create_patient,
    get_all_patients,
    get_patient_by_mobile,
    update_patient,
    delete_patient
)

router = APIRouter()

@router.post("/")
def add_patient(data: PatientSchema):
    return create_patient(data)

@router.get("/")
def all_patients():
    return get_all_patients()

@router.get("/{mobile}")
def single_patient(mobile: str):
    return get_patient_by_mobile(mobile)

@router.put("/{mobile}")
def edit_patient(mobile: str, data: PatientSchema):
    return update_patient(mobile, data)

@router.delete("/{mobile}")
def remove_patient(mobile: str):
    return delete_patient(mobile)