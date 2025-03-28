from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False) 
    password = Column(String, nullable=True) 
    family_name = Column(String, nullable=True)
    given_name = Column(String, nullable=True)
    social_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True) 
    uuid = Column(String, unique=True, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())  
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    bookings = relationship("Booking", back_populates="user")