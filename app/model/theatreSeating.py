from pydantic import BaseModel

class TheatreSeatingBase(BaseModel):
    theatre_id: int
    row_letter: str
    seat_number: int
    seat_type: str
    price: int
    is_blocked: bool

class TheatreSeatingCreate(TheatreSeatingBase):
    pass  # Used for creating a new seat entry

class TheatreSeatingUpdate(TheatreSeatingBase):
    pass  # Used for updating an existing seat

class TheatreSeatingResponse(TheatreSeatingBase):
    id: int

    class Config:
        from_attributes = True
