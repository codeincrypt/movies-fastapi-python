from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# SQLAlchemy Model
class TheatreSeating(Base):
    __tablename__ = "theatre_seating"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"))
    row_letter = Column(String(1), nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)

    # Relationship
    theatre = relationship("Theatre", back_populates="theatre_seating")
