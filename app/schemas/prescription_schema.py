from pydantic import BaseModel
from typing import List, Optional

class PrescriptionItem(BaseModel):
    medicine_name: str

    early_morning: bool = False
    morning: bool = False
    afternoon: bool = False
    night: bool = False

    before_food: bool = False
    after_food: bool = False

    duration_days: Optional[int] = None
    remarks: Optional[str] = None


class PrescriptionCreate(BaseModel):
    patient_mobile: str
    doctor_name: str
    notes: Optional[str] = None

    medicines: List[PrescriptionItem]