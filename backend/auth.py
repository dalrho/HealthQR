from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY') # just for prototype, not for production\
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    if not password:
        raise ValueError("Password cannot be empty")
    
    print(password, len(password.encode("utf-8")))
    return pwd_context.hash(str(password))

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1) 
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)