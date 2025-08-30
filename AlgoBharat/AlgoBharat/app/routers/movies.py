from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import Movie, MovieCreate, MovieUpdate
from ..services import MovieService

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """Create a new movie"""
    return MovieService.create_movie(db, movie)

@router.get("/", response_model=List[Movie])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all movies"""
    movies = MovieService.get_movies(db, skip=skip, limit=limit)
    return movies

@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get a specific movie by ID"""
    movie = MovieService.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    """Update a movie"""
    movie_data = {k: v for k, v in movie.dict().items() if v is not None}
    updated_movie = MovieService.update_movie(db, movie_id, movie_data)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie"""
    success = MovieService.delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None
