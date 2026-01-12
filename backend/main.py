import uuid
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Import your local modules
from .database import engine, get_db
from . import models, schemas

from fastapi.middleware.cors import CORSMiddleware


# Create tables in Postgres automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "success", "message": "HealthQR Backend is Fresh and Running"}

# Add this block:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registration and QR Logic ---
@app.post("/register", response_model=schemas.UserResponse)
def register_patient(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # 1. Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Generate a secure unique token for the QR code
    generated_token = uuid.uuid4()
    
    # 3. Create and save the new user record
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        age=user.age,
        qr_token=str(generated_token)
    )
    
    db.add(new_user)
    db.flush() # This gives us new_user.id

    # 2. Create Medical Record linked to that User
    new_record = models.MedicalRecord(
        patient_id=new_user.id,
        blood_type=user.blood_type,
        emergency_contact_name=user.emergency_contact_name,
        emergency_contact_phone=user.emergency_contact_phone,
        allergies=user.allergies,
        medical_history=user.medical_history
    )
    db.add(new_record)
    
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/scan/{token}")
def scan_qr_code(token: str, db: Session = Depends(get_db)):
    # 1. Find the user
    user = db.query(models.User).filter(models.User.qr_token == token).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Invalid QR Code")
    
    # 2. Access the linked medical record
    # SQLAlchemy handles the 'join' automatically via the relationship we defined
    record = user.medical_record
    
    # 3. Combine the data into one response for the frontend
    return {
        "full_name": user.full_name,
        "age": user.age,
        "blood_type": record.blood_type if record else "Unknown",
        "emergency_contact_name": record.emergency_contact_name if record else "N/A",
        "emergency_contact_phone": record.emergency_contact_phone if record else "N/A",
        "allergies": record.allergies if record else "None",
        "medical_history": record.medical_history if record else "None"
    }

@app.get("/scan/{token}")
def get_user_by_token(token: str, db: Session = Depends(get_db)):
    # Find the user with this specific QR token
    user = db.query(models.User).filter(models.User.qr_token == token).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Invalid QR Code: Patient not found")
    
    # Return user info + their medical records
    return {
        "full_name": user.full_name,
        "age": user.age,
        "medical_history": user.medical_record.medical_history if user.medical_record else "No history recorded",
        "allergies": user.medical_record.allergies if user.medical_record else "None"
    }