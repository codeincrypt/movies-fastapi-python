from pydantic import BaseModel, EmailStr
from typing import List, Optional
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


class MovieBase(BaseModel):
    adult: bool
    movie_id: int
    backdrop_path: str = ""
    genre_ids: Optional[str] = None
    original_language: str
    original_title: str
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    title: str
    video: bool
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes  = True  # Allows ORM mode


class SellerBase(BaseModel):
    email: EmailStr
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    social_id: str
    name: str
    picture: Optional[str] = None
    status: Optional[int] = None

class SellerCreate(SellerBase):
    pass

class SellerResponse(SellerBase):
    id: int

    class Config:
        from_attributes = True
