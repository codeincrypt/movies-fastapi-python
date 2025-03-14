from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Pydantic Model
class UserBase(BaseModel):
    email: EmailStr
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    social_id: str
    name: str
    picture: Optional[str] = None
    status: Optional[int] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
