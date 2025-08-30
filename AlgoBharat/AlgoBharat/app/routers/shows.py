from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import Show, ShowCreate, ShowUpdate
from ..services import ShowService
from ..exceptions import (
    MovieNotFoundException,
    TheaterNotFoundException,
    HallNotFoundException
)

router = APIRouter(prefix="/shows", tags=["shows"])

@router.post("/", response_model=Show, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowCreate, db: Session = Depends(get_db)):
    """Create a new show"""
    try:
        return ShowService.create_show(db, show)
    except (MovieNotFoundException, TheaterNotFoundException, HallNotFoundException) as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[Show])
def get_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all shows"""
    shows = ShowService.get_shows(db, skip=skip, limit=limit)
    return shows

@router.get("/{show_id}", response_model=Show)
def get_show(show_id: int, db: Session = Depends(get_db)):
    """Get a specific show by ID"""
    show = ShowService.get_show(db, show_id)
    if show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return show

@router.get("/movie/{movie_id}", response_model=List[Show])
def get_shows_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get all shows for a specific movie"""
    shows = ShowService.get_shows_by_movie(db, movie_id)
    return shows

@router.get("/theater/{theater_id}", response_model=List[Show])
def get_shows_by_theater(theater_id: int, db: Session = Depends(get_db)):
    """Get all shows for a specific theater"""
    shows = ShowService.get_shows_by_theater(db, theater_id)
    return shows

@router.put("/{show_id}", response_model=Show)
def update_show(show_id: int, show: ShowUpdate, db: Session = Depends(get_db)):
    """Update a show"""
    show_data = {k: v for k, v in show.dict().items() if v is not None}
    # Note: In a real application, you'd want to add validation here
    # to ensure the show can be updated safely
    updated_show = ShowService.update_show(db, show_id, show_data)
    if updated_show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return updated_show

@router.delete("/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_show(show_id: int, db: Session = Depends(get_db)):
    """Delete a show"""
    success = ShowService.delete_show(db, show_id)
    if not success:
        raise HTTPException(status_code=404, detail="Show not found")
    return None
