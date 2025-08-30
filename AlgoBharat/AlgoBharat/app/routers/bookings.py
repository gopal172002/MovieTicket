from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from ..database import get_db
from ..schemas import BookingCreate, BookingResponse, HallLayout, SeatSuggestion
from ..services import BookingService, SeatService
from ..exceptions import (
    SeatAlreadyBookedException,
    InsufficientSeatsException,
    ShowNotFoundException,
    HallNotFoundException
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking for seats"""
    try:
        return BookingService.create_booking(db, booking)
    except (SeatAlreadyBookedException, InsufficientSeatsException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ShowNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID"""
    booking = BookingService.get_booking(db, booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a specific user"""
    bookings = BookingService.get_user_bookings(db, user_id)
    return bookings

@router.get("/halls/{hall_id}/layout", response_model=HallLayout)
def get_hall_layout(
    hall_id: int, 
    show_id: int = Query(..., description="Show ID to get layout for"),
    db: Session = Depends(get_db)
):
    """Get hall layout with booked and available seats"""
    try:
        return SeatService.get_hall_layout(db, hall_id, show_id)
    except HallNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/shows/{show_id}/consecutive-seats")
def find_consecutive_seats(
    show_id: int,
    num_seats: int = Query(..., ge=1, le=20, description="Number of consecutive seats needed"),
    db: Session = Depends(get_db)
):
    """Find consecutive available seats for a show"""
    consecutive_seats = SeatService.find_consecutive_seats(db, show_id, num_seats)
    return {
        "show_id": show_id,
        "num_seats_requested": num_seats,
        "consecutive_seats_found": consecutive_seats,
        "total_available": len(consecutive_seats)
    }

@router.get("/movies/{movie_id}/suggestions", response_model=List[SeatSuggestion])
def get_seat_suggestions(
    movie_id: int,
    num_seats: int = Query(..., ge=1, le=20, description="Number of consecutive seats needed"),
    preferred_time: datetime = Query(None, description="Preferred show time"),
    db: Session = Depends(get_db)
):
    """Get alternative show suggestions with consecutive seats available"""
    suggestions = SeatService.suggest_alternative_shows(
        db, movie_id, num_seats, preferred_time
    )
    return suggestions

@router.post("/group-booking")
def create_group_booking(
    show_id: int = Query(..., description="Show ID"),
    user_id: int = Query(..., description="User ID"),
    num_seats: int = Query(..., ge=1, le=20, description="Number of seats needed"),
    db: Session = Depends(get_db)
):
    """Create a group booking with automatic consecutive seat selection"""
    try:
        # Find consecutive seats
        consecutive_seats = SeatService.find_consecutive_seats(db, show_id, num_seats)
        
        if not consecutive_seats:
            # If no consecutive seats, get suggestions
            suggestions = SeatService.suggest_alternative_shows(db, show_id, num_seats)
            return {
                "success": False,
                "message": "No consecutive seats available for this show",
                "suggestions": suggestions
            }
        
        # Create booking with the found seats
        seat_ids = [seat["id"] for seat in consecutive_seats]
        booking_data = BookingCreate(
            user_id=user_id,
            show_id=show_id,
            seat_ids=seat_ids
        )
        
        booking = BookingService.create_booking(db, booking_data)
        
        return {
            "success": True,
            "booking": booking,
            "seats_booked": consecutive_seats
        }
        
    except (SeatAlreadyBookedException, InsufficientSeatsException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ShowNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
