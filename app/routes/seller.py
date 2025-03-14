from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
import uuid

from app import auth
from app.database import get_db
from app.schema.seller import Seller
from app.schema.booking import Booking
from app.model.sellers import SellerCreate

seller_router = APIRouter(prefix="/seller", tags=["Seller"])

@seller_router.post("/google-login")
def google_login(seller: SellerCreate, db: Session = Depends(get_db)):
    try:
        db_seller = db.query(Seller).filter(Seller.email == seller.email).first()

        if not db_seller:
            # Create new seller
            new_seller = Seller(
                email=seller.email,
                family_name=seller.family_name,
                given_name=seller.given_name,
                social_id=seller.social_id,
                name=seller.name,
                uuid=str(uuid.uuid4()),
                picture=seller.picture,
                status=1
            )
            db.add(new_seller)
            db.commit()
            db.refresh(new_seller)
            db_user = new_seller

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
        return {"status":"1", "message": "Seller Login successful", "token": token, "data": data}

    except Exception as e:
        print("Error during Google login:", e)
        raise HTTPException(status_code=400, detail=str(e))

@seller_router.post("/my-bookings/")
def my_bookings(authorization: str = Header(), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ")[1]
    payload = auth.decode_jwt(token)
    
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token data")

    result = db.query(Booking).filter(Booking.seller_id == user_id).all()  # Fetch all bookings
    if result:
        return {"status": "1", "data": result} 
    
    return {"status": "0", "message": "No booking found"}