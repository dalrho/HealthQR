from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, default='PATIENT') 
    qr_token = Column(String, unique=True, index=True)
    created_at = Column(TIMESTAMP, server_default=text("now()"))

    medical_record = relationship("MedicalRecord", back_populates="patient", uselist=False)

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    blood_type = Column(String(5)) # Added
    emergency_contact_name = Column(String) # Added
    emergency_contact_phone = Column(String) # Added
    allergies = Column(Text)
    medical_history = Column(Text)
    updated_at = Column(TIMESTAMP, server_default=text("now()"), onupdate=text("now()"))

    patient = relationship("User", back_populates="medical_record")