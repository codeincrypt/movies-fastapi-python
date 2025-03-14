from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    theatre_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)

    movie_id = Column(String, nullable=False)
    show_date = Column(String, nullable=False)
    show_time = Column(String, nullable=False)
    seat_number = Column(String, nullable=False)
    price = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    total_price = Column(String, nullable=False)
    payment_mode = Column(String, nullable=False)
    booking_status = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())  
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships 
    user = relationship("User", back_populates="bookings") 
    seller = relationship("Seller", back_populates="bookings")  
    theatre = relationship("Theatre", back_populates="bookings")
