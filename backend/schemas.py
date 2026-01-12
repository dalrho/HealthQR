from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    age: int

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: UUID
    qr_token: UUID

    class Config:
        from_attributes = True