from fastapi import APIRouter, Depends # type: ignore
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
        return {"status":"0", "message": "User not found"}
    return response
