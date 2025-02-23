import os
import requests

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.movies import Movies
from app.database import get_db
from app.schemas import MovieBase

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MOVIE_IMAGE_URL = os.getenv("MOVIE_IMAGE_URL")

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/users")
def get_users(db: Session = Depends(get_db)):
    result = db.query(User).all()
    response = {"status":"1", "users": result} 
    if not response:
        return {"status":"0", "message": "User not found"}
    return response

@admin_router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    response = db.query(User).filter(User.id == user_id).first()
    if not response:
        return {"status":"0", "message": "Invalid user id"}
    return response


@admin_router.get("/movie")
def search_movie(query: str = Query(...), db: Session = Depends(get_db)):
    print("Query:", query)

    # Search movie in local database
    result = db.query(Movies).filter(Movies.title == query).first()
    print("-----------Movies", result)

    if not result:
        url = "https://api.themoviedb.org/3/search/move"
        params = {"query": query}
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return {"status": "1", "data": data}
        else:
            return {"status": "0", "error": response.json()}
    
    return {"status": "1", "data": result}

@admin_router.get("/movies")
def get_movie_list(db: Session = Depends(get_db)):
    result = db.query(Movies).all()
    response = {"status":"1", "data": result} 
    if not response:
        return {"status":"0", "message": "Movies data not available"}
    return response


@admin_router.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    result = db.query(Movies).filter(Movies.movie_id == movie_id).first()
    if result:
        return {"status":"1", "data": result} 
    return {"status":"0", "message": "No movies found"}


@admin_router.post("/add-movies")
def add_movies(movie:MovieBase, db: Session = Depends(get_db)):
    try:
        existing_movie = db.query(Movies).filter(Movies.movie_id == movie.movie_id).first()
        if existing_movie:
            return {"status": "0", "message": "Movie already Exists", "data": existing_movie}

        new_movie = Movies(
            adult=movie.adult,
            movie_id=movie.movie_id,
            backdrop_path=MOVIE_IMAGE_URL + movie.backdrop_path,
            genre_ids=movie.genre_ids,  # Assuming genre_ids is stored as JSON
            original_language=movie.original_language,
            original_title=movie.original_title,
            overview=movie.overview,
            popularity=movie.popularity,
            poster_path=MOVIE_IMAGE_URL + movie.poster_path,
            release_date=movie.release_date,
            title=movie.title,
            video=movie.video,
            vote_average=movie.vote_average,
            vote_count=movie.vote_count
        )
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)  

        return {"status": "1", "message": "Data added successfully", "data": new_movie}
    except Exception as e:
        print("Error adding movie:", e)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@admin_router.get("/seller")
def get_seller(db: Session = Depends(get_db)):
    result = db.query(User).all()
    response = {"status":"1", "users": result} 
    return response


@admin_router.get("/seller/{seller_id}")
def get_users(db: Session = Depends(get_db)):
    result = db.query(User).all()
    response = {"status":"1", "users": result} 
    return response
