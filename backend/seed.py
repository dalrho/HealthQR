import uuid
from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    try:
        # 1. Clear existing data to avoid duplicates
        db.query(models.MedicalRecord).delete()
        db.query(models.User).delete()

        # 2. Create a Dummy Doctor
        doctor = models.User(
            full_name="Dr. Elizabeth Smith",
            email="dr.smith@cityhospital.gov",
            role="DOCTOR",
            qr_token=None  # Doctors don't need a patient QR
        )
        db.add(doctor)

        # 3. Create a Dummy Patient
        patient_id = uuid.uuid4()
        patient = models.User(
            id=patient_id,
            full_name="John Doe",
            email="john.doe@example.com",
            role="PATIENT",
            qr_token="TEST-QR-TOKEN-123" # A static token for testing
        )
        db.add(patient)

        # 4. Create Medical Record for that Patient
        medical_record = models.MedicalRecord(
            patient_id=patient_id,
            blood_type="O+",
            allergies="Peanuts, Penicillin",
            medical_history="Appendectomy in 2015. No chronic conditions."
        )
        db.add(medical_record)

        # Commit all changes to the Database
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