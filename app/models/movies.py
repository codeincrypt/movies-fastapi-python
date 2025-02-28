from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base  # Ensure Base is imported from database.py

# SQLAlchemy Model
class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    adult = Column(Boolean, nullable=False, default=False)
    movie_id = Column(Integer, nullable=False)
    backdrop_path = Column(String, nullable=True)
    genre_ids = Column(String, nullable=True)
    original_language = Column(String, nullable=False)
    original_title = Column(String, nullable=False)
    overview = Column(String, nullable=True)
    popularity = Column(Float, nullable=True)
    poster_path = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    title = Column(String, nullable=False)
    video = Column(Boolean, default=False)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)
