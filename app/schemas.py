from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    email: EmailStr
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    social_id: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    status: int
    doc: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    uuid: UUID4

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes  = True

class MovieBase(BaseModel):
    adult: bool
    movie_id: int
    backdrop_path: Optional[str] = None
    genre_ids: List[int]
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
