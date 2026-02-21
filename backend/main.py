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

from database import engine, get_db
import models, auth, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "success", "message": "HealthQR Backend is Fresh and Running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserResponse)
def register_patient(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    generated_token = uuid.uuid4()

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        age=user.age,
        qr_token=str(generated_token)
    )

    db.add(new_user)
    db.flush() 

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
    user = db.query(models.User).filter(models.User.qr_token == token).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid QR Code")

    record = user.medical_record

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
    user = db.query(models.User).filter(models.User.qr_token == token).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid QR Code: Patient not found")

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
    patient = db.query(models.User).filter(
        models.User.qr_token == request.qr_token,
        models.User.role == "PATIENT"
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Invalid QR Code")

    return patient

@app.post("/view-record")
def view_medical_record(request: schemas.ScanRequest, db: Session = Depends(get_db)):
    actor = db.query(models.User).filter(models.User.id == request.doctor_id).first()
    if not actor or actor.role not in ["DOCTOR", "PHARMACIST"]:
        raise HTTPException(status_code=403, detail="Unauthorized: Only medical staff can scan.")

    patient = db.query(models.User).filter(models.User.qr_token == request.qr_token).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Invalid QR Code.")

    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.patient_id == patient.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found.")

    print(f"Saving log: Actor {actor.id} scanned Target {patient.id}")
    new_log = models.AuditLog(
        actor_id=actor.id, 
        target_id=patient.id, 
        action="SCAN_SUCCESS"
    )
    db.add(new_log)
    db.commit()
    print("Commit successful!")

    if actor.role == "PHARMACIST":
        return {
            "patient_name": patient.full_name,
            "allergies": record.allergies,
            "note": "Clinical history hidden for Pharmacist role."
        }

    return {
        "patient_name": patient.full_name,
        "blood_type": record.blood_type,
        "allergies": record.allergies,
        "clinical_history": record.medical_history
    }   

@app.post("/emergency-override")
def emergency_override(request: schemas.EmergencyOverrideRequest, db: Session = Depends(get_db)):
    doctor = db.query(models.User).filter(models.User.id == request.doctor_id).first()
    if not doctor or doctor.role != "DOCTOR":
        raise HTTPException(status_code=403, detail="Emergency override reserved for Doctors.")

    patient = db.query(models.User).filter(models.User.id == request.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    new_log = models.AuditLog(
        actor_id=doctor.id,
        target_id=patient.id,
        action=f"EMERGENCY_OVERRIDE: {request.reason}"
    )
    db.add(new_log)
    db.commit()

    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.patient_id == patient.id).first()

    return {
        "alert": "EMERGENCY ACCESS GRANTED",
        "patient_name": patient.full_name,
        "blood_type": record.blood_type,
        "allergies": record.allergies,
        "medical_history": record.medical_history,
        "audit_reference": new_log.id
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="medic/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

@app.get("/medic/verify")
def verify_token(current_user: str = Depends(get_current_user)):
    return {"status": "valid", "user": current_user}