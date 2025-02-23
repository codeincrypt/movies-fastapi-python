import uuid
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False) 
    family_name = Column(String, nullable=True)
    given_name = Column(String, nullable=True)
    social_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True) 
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    doc = Column(String, nullable=True)