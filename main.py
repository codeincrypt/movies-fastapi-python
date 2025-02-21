from fastapi import FastAPI

from app.routes.admin import admin_router
from app.routes.user import user_router
# from app.database import Base, engine

app = FastAPI()

# Create database tables
# Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(admin_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI with PostgreSQL"}
