from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

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

class Medic(Base):
    __tablename__ = "medics"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    target_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String) # e.g., "VIEW_RECORD"
    timestamp = Column(TIMESTAMP, server_default=text("now()"))