from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
import uuid

from app.database import get_db

from app.middleware.auth import get_current_seller, create_access_token

from app.schema.seller import Seller
from app.schema.theatre import Theatre
from app.schema.booking import Booking

from app.model.sellers import SellerCreate
from app.model.theatre import TheatreCreate

seller_router = APIRouter(prefix="/seller", tags=["Seller"])

@seller_router.post("/google-login")
def google_login(seller: SellerCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(Seller).filter(Seller.email == seller.email).first()

        if not db_user:
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
        print("Created seller:", db_user)
        # Generate JWT token
        token = create_access_token({"user_id": db_user.uuid, "id": db_user.id, "email": db_user.email})
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
        print("Error during Seller Google login:", e)
        raise HTTPException(status_code=400, detail=str(e))


@seller_router.post("/my-bookings")
def my_bookings(user_details: dict = Depends(get_current_seller), db: Session = Depends(get_db)):
    result = db.query(Booking).filter(Booking.seller_id == user_details.id).all()
    return {"status": "1", "data": result} if result else {"status": "0", "message": "No booking found"}


@seller_router.get("/my-theatre")
def my_theatres(user_details: dict = Depends(get_current_seller), db: Session = Depends(get_db)):
    result = db.query(Theatre).filter(Theatre.seller_id == user_details.id).all()
    if result:
        return {"status": "1", "data": result} 
    return {"status": "0", "message": "No booking found"}

@seller_router.post("/add-theatre")
def add_new_theatre(
    theatre_data: TheatreCreate,
    user_details: dict = Depends(get_current_seller),
    db: Session = Depends(get_db)
):
    seller_id = user_details.id
    new_theatre = Theatre(
        name=theatre_data.name,
        seller_id=seller_id,
        seating_map=theatre_data.seating_map,
        location=theatre_data.location,
        capacity=theatre_data.capacity
    )
    db.add(new_theatre)
    db.commit()
    db.refresh(new_theatre)

    return {"status": "1", "message": "Theatre added successfully", "data": new_theatre}