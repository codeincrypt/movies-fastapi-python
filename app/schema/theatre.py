from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Theatre(Base):
    __tablename__ = 'theatres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    seating_map = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    bookings = relationship("Bookings", back_populates="theatre")
    seller = relationship("Seller", back_populates="theatres")