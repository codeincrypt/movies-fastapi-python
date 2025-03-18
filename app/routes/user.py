from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
import uuid

from app.middleware.auth import create_access_token, verify_password
from app.database import get_db
from app.schema.user import User
from app.schema.booking import Booking
from app.model.users import UserCreate

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print("Error logging in user:", e)
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post("/google-login")
def google_login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            # Create new user
            new_user = User(
                email=user.email,
                family_name=user.family_name,
                given_name=user.given_name,
                social_id=user.social_id,
                name=user.name,
                uuid=str(uuid.uuid4()),
                picture=user.picture,
                status=1
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db_user = new_user

        # Generate JWT token
        token = auth.create_access_token({"user_id": db_user.uuid, "email": db_user.email})
        data = {
            "email": db_user.email,
            "family_name": db_user.family_name,
            "given_name": db_user.given_name,
            "social_id": db_user.social_id,
            "name": db_user.name,
            "picture": db_user.picture,
            "uuid": db_user.uuid,
        }
        print("Google login successful", token)
        return {"status":"1", "message": "Login successful", "token": token, "data": data}

    except Exception as e:
        print("Error during Google login:", e)
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get("/my-bookings/")
def my_bookings(authorization: str = Header(), db: Session = Depends(get_db)):
    result = db.query(Booking).filter(Booking.user_id == "user_id").all()
    if result:
        return {"status": "1", "data": result} 
    
    return {"status": "0", "message": "No booking found"}