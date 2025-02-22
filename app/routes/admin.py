from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/users")
def get_users(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    response = {"status":"1", "users": result} 
    if not response:
        return {"status":"0", "message": "User not found"}
    return response

@admin_router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    response = db.query(models.User).filter(models.User.id == user_id).first()
    if not response:
        return {"status":"0", "message": "Invalid user id"}
    return response


@admin_router.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    response = {"status":"1", "data": result} 
    if not response:
        return {"status":"0", "message": "Movies data not available"}
    return response


@admin_router.get("/movies/{movie_id}")
def get_movie(db: Session = Depends(get_db)):
    result = db.query(models.Movies).all()
    response = {"status":"1", "data": result} 
    if not response:
        return {"status":"0", "message": "No movies found"}
    return response


@admin_router.post("/add-movies")
def add_movies(moviename: str, image: str, db: Session = Depends(get_db)):
    data = models.User(moviename=moviename, image=image, status=1)
    db.add(data)
    db.commit()
    db.refresh(data)
    response = {"status":"1", "message": "Data added successfully", "data": result} 
    if not response:
        return {"status":"0", "message": "User not found"}
    return response


@admin_router.get("/seller")
def get_seller(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    response = {"status":"1", "users": result} 
    if not response:
        return {"status":"0", "message": "User not found"}
    return response


@admin_router.get("/seller/{seller_id}")
def get_users(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    response = {"status":"1", "users": result} 
    if not response:
        return {"status":"0", "message": "User not found"}
    return response
