from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app import schemas, auth

from app.database import get_db

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = auth.hash_password(user.password)
        db_user = User(email=user.email, password=hashed_password, status=1)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}
    except Exception as e:
        print("Error registering user:", e)
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not auth.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = auth.create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print("Error logging in user:", e)
        raise HTTPException(status_code=400, detail=str(e))
