import os
import jwt
from jose import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from dotenv import load_dotenv
load_dotenv()

from app.database import get_db
from app.schema.seller import Seller
from app.schema.user import User

# Token authentication scheme
security = HTTPBearer()

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

### **Password Utilities**
def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

### **JWT Token Utilities**
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    print("Creating access token", data, expires_delta)
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

### **Middleware: Authenticate & Get Current User**
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = decode_jwt(token)  # Decode token
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user_id payload")

    # Fetch user from DB
    user = db.query(User).filter(User.uuid == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def get_current_seller(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)) -> Seller:
    token = credentials.credentials
    payload = decode_jwt(token)  # Decode token
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user_id payload")

    # Fetch user from DB
    user = db.query(Seller).filter(Seller.uuid == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user 
