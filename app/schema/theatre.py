from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Theatre(Base):
    __tablename__ = 'theatres'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    seating_map = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Use string-based relationships
    seller = relationship("Seller", back_populates="theatres")
    bookings = relationship("Booking", back_populates="theatre")
    seatings = relationship("Seating", back_populates="theatre")