from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Settings
SECRET_KEY = "NAGA_CITY_SUPER_SECRET_KEY" # In real life, use an environment variable
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Ensure it's a string and not empty
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Force cast to string just in case
    print(password, len(password.encode("utf-8")))
    return pwd_context.hash(str(password))
    #return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1) # Token lasts 1 hour
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)