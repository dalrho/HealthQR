from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    age: int

class UserCreate(UserBase):
    blood_type: str
    emergency_contact_name: str
    emergency_contact_phone: str
    allergies: str
    medical_history: str

class UserResponse(BaseModel):
    id: UUID
    qr_token: UUID

    class Config:
        from_attributes = True

# What we send back when a QR is scanned
class PatientIdentify(BaseModel):
    id: UUID
    full_name: str
    
    class Config:
        from_attributes = True

# What we require for the QR scan request
class ScanRequest(BaseModel):
    qr_token: str
    doctor_id: UUID # The ID of the professional doing the scan

class EmergencyOverrideRequest(BaseModel):
    doctor_id: UUID
    patient_id: UUID  # In a real app, this could be searched by name/SSN
    reason: str       # e.g., "Unconscious, Cardiac Arrest"