from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    user_id: int
    theatre_id: int
    seller_id: int
    movie_id: str
    show_date: str
    show_time: str
    seat_number: str
    price: str
    quantity: str
    total_price: str
    payment_mode: str
    booking_status: int

class BookingCreate(BookingBase):
    pass  # Used for creating a new booking

class BookingUpdate(BookingBase):
    pass  # Used for updating a booking

class BookingResponse(BookingBase):
    id: int
    booking_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
