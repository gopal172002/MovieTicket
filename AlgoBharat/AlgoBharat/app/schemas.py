from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Movie Schemas
class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0)
    genre: Optional[str] = None
    language: Optional[str] = None
    price: float = Field(..., gt=0)

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    genre: Optional[str] = None
    language: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)

class Movie(MovieBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Theater Schemas
class TheaterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str
    city: str = Field(..., min_length=1, max_length=100)
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class TheaterCreate(TheaterBase):
    pass

class TheaterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = None
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class Theater(TheaterBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Hall Schemas
class HallBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    total_rows: int = Field(..., gt=0)
    seats_per_row: Dict[str, int] = Field(..., description="JSON object with row names and seat counts")

class HallCreate(HallBase):
    pass

class HallUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    total_rows: Optional[int] = Field(None, gt=0)
    seats_per_row: Optional[Dict[str, int]] = None

class Hall(HallBase):
    id: int
    theater_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Show Schemas
class ShowBase(BaseModel):
    movie_id: int
    theater_id: int
    hall_id: int
    show_time: datetime
    price: float = Field(..., gt=0)

class ShowCreate(ShowBase):
    pass

class ShowUpdate(BaseModel):
    movie_id: Optional[int] = None
    theater_id: Optional[int] = None
    hall_id: Optional[int] = None
    show_time: Optional[datetime] = None
    price: Optional[float] = Field(None, gt=0)

class Show(ShowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Seat Schemas
class SeatBase(BaseModel):
    row_number: int = Field(..., gt=0)
    seat_number: int = Field(..., gt=0)
    is_aisle: bool = False

class Seat(SeatBase):
    id: int
    show_id: int
    hall_id: int
    is_booked: bool
    booking_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    user_id: int
    show_id: int
    seat_ids: List[int] = Field(..., description="List of seat IDs to book")

class BookingCreate(BookingBase):
    pass

class BookingResponse(BaseModel):
    id: int
    user_id: int
    show_id: int
    booking_reference: str
    total_amount: float
    booking_status: str
    booking_time: datetime
    seats: List[Seat]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Hall Layout Schemas
class HallLayout(BaseModel):
    hall_id: int
    total_rows: int
    seats_per_row: Dict[str, int]
    booked_seats: List[Dict[str, Any]]
    available_seats: List[Dict[str, Any]]

# Seat Suggestion Schemas
class SeatSuggestion(BaseModel):
    show_id: int
    movie_title: str
    theater_name: str
    hall_name: str
    show_time: datetime
    available_seats: List[Dict[str, Any]]
    total_available: int

# Analytics Schemas
class MovieAnalytics(BaseModel):
    movie_id: int
    movie_title: str
    total_bookings: int
    total_tickets: int
    total_gmv: float
    period_start: datetime
    period_end: datetime
    daily_stats: List[Dict[str, Any]]

class TheaterAnalytics(BaseModel):
    theater_id: int
    theater_name: str
    total_bookings: int
    total_tickets: int
    total_gmv: float
    period_start: datetime
    period_end: datetime
    hall_stats: List[Dict[str, Any]]

# Error Response Schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
