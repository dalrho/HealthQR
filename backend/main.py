import uuid
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import time
from sqlalchemy.exc import OperationalError

def wait_for_db(engine, retries=10, delay=2):
    for _ in range(retries):
        try:
            with engine.connect():
                return
        except OperationalError:
            time.sleep(delay)
    raise RuntimeError("Database not ready")

# Import your local modules
from database import engine, get_db
import models, auth, schemas



# Create tables in Postgres automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

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

# This needs review because why does this return a lot
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

@app.post("/medic/login")
def login_medic(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    medic = db.query(models.Medic).filter(models.Medic.username == username).first()
    
    if not medic or not auth.verify_password(password, medic.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_access_token(data={"sub": medic.username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/scan", response_model=schemas.PatientIdentify)
def identify_patient(request: schemas.ScanRequest, db: Session = Depends(get_db)):
    # 1. Search for the patient by QR token
    patient = db.query(models.User).filter(
        models.User.qr_token == request.qr_token,
        models.User.role == "PATIENT"
    ).first()

    # 2. If not found, throw a 404
    if not patient:
        raise HTTPException(status_code=404, detail="Invalid QR Code")

    # 3. Return only basic info (Identity Layer)
    return patient


@app.post("/view-record")
def view_medical_record(request: schemas.ScanRequest, db: Session = Depends(get_db)):
    # 1. Identify the professional scanning
    actor = db.query(models.User).filter(models.User.id == request.doctor_id).first()
    if not actor or actor.role not in ["DOCTOR", "PHARMACIST"]:
        raise HTTPException(status_code=403, detail="Unauthorized: Only medical staff can scan.")

    # 2. Identify the patient via QR
    patient = db.query(models.User).filter(models.User.qr_token == request.qr_token).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Invalid QR Code.")

    # 3. Fetch the Medical Record
    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.patient_id == patient.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found.")

    # 4. THE AUDIT LOG (Happens for every successful scan)
    print(f"Saving log: Actor {actor.id} scanned Target {patient.id}")
    new_log = models.AuditLog(
        actor_id=actor.id, 
        target_id=patient.id, 
        action="SCAN_SUCCESS"
    )
    db.add(new_log)
    db.commit()
    print("Commit successful!")

    # 5. RBAC Logic: Filter what is returned to the user
    if actor.role == "PHARMACIST":
        return {
            "patient_name": patient.full_name,
            "allergies": record.allergies,
            "note": "Clinical history hidden for Pharmacist role."
        }

    # If it's a DOCTOR, return full view
    return {
        "patient_name": patient.full_name,
        "blood_type": record.blood_type,
        "allergies": record.allergies,
        "clinical_history": record.medical_history
    }   

@app.post("/emergency-override")
def emergency_override(request: schemas.EmergencyOverrideRequest, db: Session = Depends(get_db)):
    # 1. Verify the Actor is a DOCTOR (Pharmacists cannot use overrides)
    doctor = db.query(models.User).filter(models.User.id == request.doctor_id).first()
    if not doctor or doctor.role != "DOCTOR":
        raise HTTPException(status_code=403, detail="Emergency override reserved for Doctors.")

    # 2. Fetch the Patient
    patient = db.query(models.User).filter(models.User.id == request.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    # 3. HIGH-PRIORITY AUDIT LOG
    # This is the "Electronic Paper Trail" for legal protection
    new_log = models.AuditLog(
        actor_id=doctor.id,
        target_id=patient.id,
        action=f"EMERGENCY_OVERRIDE: {request.reason}"
    )
    db.add(new_log)
    db.commit()

    # 4. Fetch the full medical record immediately
    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.patient_id == patient.id).first()
    
    return {
        "alert": "EMERGENCY ACCESS GRANTED",
        "patient_name": patient.full_name,
        "blood_type": record.blood_type,
        "allergies": record.allergies,
        "medical_history": record.medical_history,
        "audit_reference": new_log.id
    }


# 1. Define where the frontend should send the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="medic/login")

# 2. Define the missing function
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # auth.SECRET_KEY and auth.ALGORITHM should match your auth.py settings
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# 3. Now your endpoint will work!
@app.get("/medic/verify")
def verify_token(current_user: str = Depends(get_current_user)):
    return {"status": "valid", "user": current_user}