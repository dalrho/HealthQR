from database import SessionLocal
import models
from auth import hash_password 

def create_initial_medic():
    db = SessionLocal()
    try:
        db.query(models.Medic).filter(models.Medic.username == "admin").delete()
        
        new_medic = models.Medic(
            username="admin",
            hashed_password=hash_password("naga123") 
        )
        
        db.add(new_medic)
        db.commit()
        print("Medic 'admin' created! Password is: naga123")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_medic()