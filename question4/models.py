from pydantic import BaseModel
from typing import List, Optional

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str

class Prescription(BaseModel):
    id: int
    patient_id: int
    doctor_name: str
    medicines: List[str]
    dosage: str
    date: str