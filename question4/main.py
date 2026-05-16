from fastapi import FastAPI, HTTPException
from models import Doctor, Prescription
import data

app = FastAPI()

# Add a Doctor
@app.post("/doctors", status_code=201)
def add_doctor(doctor: Doctor):
    data.doctors[data.doctor_id_counter] = doctor
    data.doctor_id_counter += 1
    return {"message": "Doctor added successfully", "doctor": doctor}

# Add Prescription for a Patient
@app.post("/patients/{patient_id}/prescriptions", status_code=201)
def add_prescription(patient_id: int, prescription: Prescription):
    # Find the doctor
    doctor = None
    for d in data.doctors.values():
        if d.name == prescription.doctor_name:
            doctor = d
            break

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Save prescription
    prescription.patient_id = patient_id
    data.prescriptions[data.prescription_id_counter] = prescription
    data.prescription_id_counter += 1
    return {"message": "Prescription added", "prescription": prescription}

# Get all Prescriptions for a Patient
@app.get("/patients/{patient_id}/prescriptions")
def get_prescriptions(patient_id: int):
    result = [p for p in data.prescriptions.values() if p.patient_id == patient_id]
    if not result:
        raise HTTPException(status_code=404, detail="No prescriptions found")
    return result

# Get a specific Prescription
@app.get("/prescriptions/{id}")
def get_prescription(id: int):
    if id not in data.prescriptions:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return data.prescriptions[id]