from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

# SQLAlchemy Model
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(String, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    theater_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    show_date = Column(String, nullable=False)
    show_time = Column(String, nullable=False)
    seat_number = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    payment_mode = Column(String, nullable=False)
    booking_status = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())  
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Use string-based references in relationships to avoid ordering issues
    user = relationship("User", back_populates="bookings") 
    seller = relationship("Seller", back_populates="bookings") 
    theatre = relationship("Theatre", back_populates="bookings")
    movie = relationship("Movies")
