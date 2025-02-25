from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base  # Ensure Base is imported

from app.routes.admin import admin_router
from app.routes.user import user_router

API_VERSION = "/api/v1"

# Initialize FastAPI app
app = FastAPI(title="Python FastAPI with PostgreSQL")

origins = [
    "https://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables (only if you're not using Alembic)
Base.metadata.create_all(bind=engine)

# Include routers with the correct prefix
app.include_router(admin_router, prefix=API_VERSION)
app.include_router(user_router, prefix=API_VERSION)

@app.get("/")
def home():
    return {"message": "Welcome to Python FastAPI with PostgreSQL"}
