from fastapi import FastAPI
from app.database import engine, Base  # Ensure Base is imported

from app.routes.admin import admin_router
from app.routes.user import user_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(admin_router)
app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Welcome to Python FastAPI with PostgreSQL"}
