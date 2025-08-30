from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import Theater, TheaterCreate, TheaterUpdate, Hall, HallCreate, HallUpdate
from ..services import TheaterService, HallService
from ..exceptions import TheaterNotFoundException

router = APIRouter(prefix="/theaters", tags=["theaters"])

# Theater endpoints
@router.post("/", response_model=Theater, status_code=status.HTTP_201_CREATED)
def create_theater(theater: TheaterCreate, db: Session = Depends(get_db)):
    """Create a new theater"""
    return TheaterService.create_theater(db, theater)

@router.get("/", response_model=List[Theater])
def get_theaters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all theaters"""
    theaters = TheaterService.get_theaters(db, skip=skip, limit=limit)
    return theaters

@router.get("/{theater_id}", response_model=Theater)
def get_theater(theater_id: int, db: Session = Depends(get_db)):
    """Get a specific theater by ID"""
    theater = TheaterService.get_theater(db, theater_id)
    if theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater

@router.put("/{theater_id}", response_model=Theater)
def update_theater(theater_id: int, theater: TheaterUpdate, db: Session = Depends(get_db)):
    """Update a theater"""
    theater_data = {k: v for k, v in theater.dict().items() if v is not None}
    updated_theater = TheaterService.update_theater(db, theater_id, theater_data)
    if updated_theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return updated_theater

@router.delete("/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_theater(theater_id: int, db: Session = Depends(get_db)):
    """Delete a theater"""
    success = TheaterService.delete_theater(db, theater_id)
    if not success:
        raise HTTPException(status_code=404, detail="Theater not found")
    return None

# Hall endpoints
@router.post("/{theater_id}/halls", response_model=Hall, status_code=status.HTTP_201_CREATED)
def create_hall(theater_id: int, hall: HallCreate, db: Session = Depends(get_db)):
    """Create a new hall for a theater"""
    try:
        return HallService.create_hall(db, theater_id, hall)
    except TheaterNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{theater_id}/halls", response_model=List[Hall])
def get_halls_by_theater(theater_id: int, db: Session = Depends(get_db)):
    """Get all halls for a theater"""
    halls = HallService.get_halls_by_theater(db, theater_id)
    return halls

@router.get("/halls/{hall_id}", response_model=Hall)
def get_hall(hall_id: int, db: Session = Depends(get_db)):
    """Get a specific hall by ID"""
    hall = HallService.get_hall(db, hall_id)
    if hall is None:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall

@router.put("/halls/{hall_id}", response_model=Hall)
def update_hall_layout(hall_id: int, hall: HallUpdate, db: Session = Depends(get_db)):
    """Update hall layout"""
    hall_data = {k: v for k, v in hall.dict().items() if v is not None}
    updated_hall = HallService.update_hall_layout(db, hall_id, hall_data)
    if updated_hall is None:
        raise HTTPException(status_code=404, detail="Hall not found")
    return updated_hall
