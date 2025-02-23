from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    moviename = Column(String, unique=True, index=True, nullable=False)
    image = Column(String, nullable=False)
    language = Column(String, nullable=False)
    status = Column(Integer)
