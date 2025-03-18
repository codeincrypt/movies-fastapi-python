import os
import requests

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.movies import MovieBase

from app.schema.user import User
from app.schema.movies import Movies
from app.schema.seller import Seller

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
MOVIE_IMAGE_URL = os.getenv("MOVIE_IMAGE_URL")

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("/users")
def get_user_list(db: Session = Depends(get_db)):
    result = db.query(User).all()
    response = {"status":"1", "users": result} 
    if not response:
        return {"status":"0", "message": "User not found"}
    return response


@admin_router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    response = db.query(User).filter(User.id == user_id).first()
    if not response:
        return {"status":"0", "message": "Invalid user id"}
    return response


@admin_router.get("/movie")
def search_movie(query: str = Query(...), db: Session = Depends(get_db)):
    print("search query from admin:", query)

    # Search movie in local database
    result = db.query(Movies).filter(Movies.title == query).first()
    print("database result", result)

    if not result:
        # Search movie in TMDB API
        print("Searching in TMDB API")
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"query": query, "include_adult": "false", "language": "en-US", "page": 1}
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            data["status"] = "1"
            return data
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
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    result = db.query(Movies).filter(Movies.movie_id == movie_id).first()
    if result:
        return {"status":"1", "data": result} 
    return {"status":"0", "message": "No movies found"}


@admin_router.post("/add-movies")
def add_movies(movie:MovieBase, db: Session = Depends(get_db)):
    print("add movies payload data", movie)
    try:
        existing_movie = db.query(Movies).filter(Movies.movie_id == movie.movie_id).first()
        if existing_movie:
            return {"status": "0", "message": "Movie already Exists", "data": existing_movie}
        
        if movie.backdrop_path == "":
            backdrop_path = ""
        else:
            backdrop_path = MOVIE_IMAGE_URL + movie.backdrop_path

        if movie.poster_path == "":
            poster_path = ""
        else:
            poster_path = MOVIE_IMAGE_URL + movie.poster_path

        new_movie = Movies(
            adult=movie.adult,
            movie_id=movie.movie_id,
            backdrop_path=backdrop_path,
            genre_ids=movie.genre_ids,
            original_language=movie.original_language,
            original_title=movie.original_title,
            overview=movie.overview,
            popularity=movie.popularity,
            poster_path=poster_path,
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
def get_sellers(db: Session = Depends(get_db)):
    result = db.query(Seller).all()
    response = {"status":"1", "users": result} 
    return response


@admin_router.get("/seller/{seller_id}")
def get_seller_by_id(seller_id: str, db: Session = Depends(get_db)):
    result = db.query(Seller).filter(Seller.id == seller_id).first()
    if result:
        return {"status": "1", "data": result}
    return {"status": "0", "data":{},"message": "No data found"}
