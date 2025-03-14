from pydantic import BaseModel
from datetime import datetime

class TheatreBase(BaseModel):
    name: str
    seller_id: int
    seating_map: str
    location: str
    capacity: int

class TheatreCreate(TheatreBase):
    pass  # Used for creating a new Theatre

class TheatreUpdate(TheatreBase):
    pass  # Used for updating an existing Theatre

class TheatreResponse(TheatreBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
