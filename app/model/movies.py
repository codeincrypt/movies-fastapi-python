from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class MovieBase(BaseModel):
    adult: bool
    movie_id: int
    backdrop_path: Optional[str] = None
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
