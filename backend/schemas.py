from pydantic import BaseModel, EmailStr
from uuid import UUID

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