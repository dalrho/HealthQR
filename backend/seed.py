import uuid
from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    try:
        
        db.query(models.MedicalRecord).delete()
        db.query(models.User).delete()

        doctor = models.User(
            full_name="Dr. Elizabeth Smith",
            email="dr.smith@cityhospital.gov",
            role="DOCTOR",
            qr_token=None  
        )
        db.add(doctor)

        patient_id = uuid.uuid4()
        patient = models.User(
            id=patient_id,
            full_name="John Doe",
            email="john.doe@example.com",
            role="PATIENT",
            qr_token="TEST-QR-TOKEN-123" 
        )
        db.add(patient)

        medical_record = models.MedicalRecord(
            patient_id=patient_id,
            blood_type="O+",
            allergies="Peanuts, Penicillin",
            medical_history="Appendectomy in 2015. No chronic conditions."
        )
        db.add(medical_record)

        db.commit()
        print("--- DATABASE SEEDED SUCCESSFULLY ---")
        print(f"Patient QR Token: {patient.qr_token}")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()