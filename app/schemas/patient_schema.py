from pydantic import BaseModel
from typing import Optional
from datetime import date


class PatientSchema(BaseModel):
    patient_name: str
    mobile_number: str
    age: int
    gender: str
    blood_pressure: str
    sugar_level: str
    weight: str
    height: str
    blood_group: str
    symptoms: str
    diagnosis: str
    allergies: str
    address: str

    next_consultation_date: Optional[date] = None

    appointment_status: Optional[str] = "PENDING"