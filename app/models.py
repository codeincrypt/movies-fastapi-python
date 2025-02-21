from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Use Base from database.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Integer)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User")  # Define relationship
