from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import List, Dict, Any, Optional, Tuple
import redis
import json
import uuid
from datetime import datetime, timedelta
import os
from .models import Movie, Theater, Hall, Show, Seat, Booking
from .schemas import MovieCreate, TheaterCreate, HallCreate, ShowCreate, BookingCreate
from .exceptions import (
    SeatAlreadyBookedException,
    InsufficientSeatsException,
    ShowNotFoundException,
    HallNotFoundException,
    TheaterNotFoundException,
    MovieNotFoundException
)

# Redis connection for distributed locking
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

class MovieService:
    @staticmethod
    def create_movie(db: Session, movie_data: MovieCreate) -> Movie:
        movie = Movie(**movie_data.dict())
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie
    
    @staticmethod
    def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.id == movie_id).first()
    
    @staticmethod
    def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
        return db.query(Movie).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_movie(db: Session, movie_id: int, movie_data: dict) -> Optional[Movie]:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            for key, value in movie_data.items():
                if value is not None:
                    setattr(movie, key, value)
            db.commit()
            db.refresh(movie)
        return movie
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int) -> bool:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            db.delete(movie)
            db.commit()
            return True
        return False

class TheaterService:
    @staticmethod
    def create_theater(db: Session, theater_data: TheaterCreate) -> Theater:
        theater = Theater(**theater_data.dict())
        db.add(theater)
        db.commit()
        db.refresh(theater)
        return theater
    
    @staticmethod
    def get_theater(db: Session, theater_id: int) -> Optional[Theater]:
        return db.query(Theater).filter(Theater.id == theater_id).first()
    
    @staticmethod
    def get_theaters(db: Session, skip: int = 0, limit: int = 100) -> List[Theater]:
        return db.query(Theater).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_theater(db: Session, theater_id: int, theater_data: dict) -> Optional[Theater]:
        theater = db.query(Theater).filter(Theater.id == theater_id).first()
        if theater:
            for key, value in theater_data.items():
                if value is not None:
                    setattr(theater, key, value)
            db.commit()
            db.refresh(theater)
        return theater
    
    @staticmethod
    def delete_theater(db: Session, theater_id: int) -> bool:
        theater = db.query(Theater).filter(Theater.id == theater_id).first()
        if theater:
            db.delete(theater)
            db.commit()
            return True
        return False

class HallService:
    @staticmethod
    def create_hall(db: Session, theater_id: int, hall_data: HallCreate) -> Hall:
        # Validate theater exists
        theater = TheaterService.get_theater(db, theater_id)
        if not theater:
            raise TheaterNotFoundException(f"Theater with id {theater_id} not found")
        
        hall = Hall(**hall_data.dict(), theater_id=theater_id)
        db.add(hall)
        db.commit()
        db.refresh(hall)
        return hall
    
    @staticmethod
    def get_hall(db: Session, hall_id: int) -> Optional[Hall]:
        return db.query(Hall).filter(Hall.id == hall_id).first()
    
    @staticmethod
    def get_halls_by_theater(db: Session, theater_id: int) -> List[Hall]:
        return db.query(Hall).filter(Hall.theater_id == theater_id).all()
    
    @staticmethod
    def update_hall_layout(db: Session, hall_id: int, layout_data: dict) -> Optional[Hall]:
        hall = db.query(Hall).filter(Hall.id == hall_id).first()
        if hall:
            for key, value in layout_data.items():
                if value is not None:
                    setattr(hall, key, value)
            db.commit()
            db.refresh(hall)
        return hall

class ShowService:
    @staticmethod
    def create_show(db: Session, show_data: ShowCreate) -> Show:
        # Validate movie, theater, and hall exist
        movie = MovieService.get_movie(db, show_data.movie_id)
        if not movie:
            raise MovieNotFoundException(f"Movie with id {show_data.movie_id} not found")
        
        theater = TheaterService.get_theater(db, show_data.theater_id)
        if not theater:
            raise TheaterNotFoundException(f"Theater with id {show_data.theater_id} not found")
        
        hall = HallService.get_hall(db, show_data.hall_id)
        if not hall:
            raise HallNotFoundException(f"Hall with id {show_data.hall_id} not found")
        
        show = Show(**show_data.dict())
        db.add(show)
        db.commit()
        db.refresh(show)
        
        # Create seats for this show
        SeatService.create_seats_for_show(db, show.id, hall)
        
        return show
    
    @staticmethod
    def get_show(db: Session, show_id: int) -> Optional[Show]:
        return db.query(Show).filter(Show.id == show_id).first()
    
    @staticmethod
    def get_shows(db: Session, skip: int = 0, limit: int = 100) -> List[Show]:
        return db.query(Show).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_shows_by_movie(db: Session, movie_id: int) -> List[Show]:
        return db.query(Show).filter(Show.movie_id == movie_id).all()
    
    @staticmethod
    def get_shows_by_theater(db: Session, theater_id: int) -> List[Show]:
        return db.query(Show).filter(Show.theater_id == theater_id).all()
    
    @staticmethod
    def update_show(db: Session, show_id: int, show_data: dict) -> Optional[Show]:
        show = db.query(Show).filter(Show.id == show_id).first()
        if show:
            for key, value in show_data.items():
                if value is not None:
                    setattr(show, key, value)
            db.commit()
            db.refresh(show)
        return show
    
    @staticmethod
    def delete_show(db: Session, show_id: int) -> bool:
        show = db.query(Show).filter(Show.id == show_id).first()
        if show:
            db.delete(show)
            db.commit()
            return True
        return False

class SeatService:
    @staticmethod
    def create_seats_for_show(db: Session, show_id: int, hall: Hall):
        """Create all seats for a show based on hall layout"""
        seats = []
        for row_name, seat_count in hall.seats_per_row.items():
            row_number = int(row_name.replace("row", ""))
            for seat_num in range(1, seat_count + 1):
                is_aisle = seat_num <= 3  # First 3 seats are aisle seats
                seat = Seat(
                    show_id=show_id,
                    hall_id=hall.id,
                    row_number=row_number,
                    seat_number=seat_num,
                    is_aisle=is_aisle,
                    is_booked=False
                )
                seats.append(seat)
        
        db.add_all(seats)
        db.commit()
    
    @staticmethod
    def get_hall_layout(db: Session, hall_id: int, show_id: int) -> Dict[str, Any]:
        """Get hall layout with booked and available seats"""
        hall = HallService.get_hall(db, hall_id)
        if not hall:
            raise HallNotFoundException(f"Hall with id {hall_id} not found")
        
        seats = db.query(Seat).filter(
            and_(Seat.hall_id == hall_id, Seat.show_id == show_id)
        ).all()
        
        booked_seats = []
        available_seats = []
        
        for seat in seats:
            seat_data = {
                "id": seat.id,
                "row_number": seat.row_number,
                "seat_number": seat.seat_number,
                "is_aisle": seat.is_aisle
            }
            
            if seat.is_booked:
                booked_seats.append(seat_data)
            else:
                available_seats.append(seat_data)
        
        return {
            "hall_id": hall_id,
            "total_rows": hall.total_rows,
            "seats_per_row": hall.seats_per_row,
            "booked_seats": booked_seats,
            "available_seats": available_seats
        }
    
    @staticmethod
    def find_consecutive_seats(db: Session, show_id: int, num_seats: int) -> List[Dict[str, Any]]:
        """Find consecutive available seats for a group booking"""
        # Get all available seats for the show
        available_seats = db.query(Seat).filter(
            and_(Seat.show_id == show_id, Seat.is_booked == False)
        ).order_by(Seat.row_number, Seat.seat_number).all()
        
        if len(available_seats) < num_seats:
            return []
        
        # Group seats by row
        seats_by_row = {}
        for seat in available_seats:
            if seat.row_number not in seats_by_row:
                seats_by_row[seat.row_number] = []
            seats_by_row[seat.row_number].append(seat)
        
        # Find consecutive seats in each row
        for row_number, seats in seats_by_row.items():
            seats.sort(key=lambda x: x.seat_number)
            
            for i in range(len(seats) - num_seats + 1):
                consecutive_seats = seats[i:i + num_seats]
                
                # Check if seats are consecutive
                seat_numbers = [seat.seat_number for seat in consecutive_seats]
                if seat_numbers == list(range(seat_numbers[0], seat_numbers[0] + num_seats)):
                    return [
                        {
                            "id": seat.id,
                            "row_number": seat.row_number,
                            "seat_number": seat.seat_number,
                            "is_aisle": seat.is_aisle
                        }
                        for seat in consecutive_seats
                    ]
        
        return []
    
    @staticmethod
    def suggest_alternative_shows(db: Session, movie_id: int, num_seats: int, 
                                preferred_time: datetime = None) -> List[Dict[str, Any]]:
        """Suggest alternative shows with consecutive seats available"""
        # Get all shows for the movie
        shows = ShowService.get_shows_by_movie(db, movie_id)
        
        suggestions = []
        for show in shows:
            consecutive_seats = SeatService.find_consecutive_seats(db, show.id, num_seats)
            if consecutive_seats:
                movie = MovieService.get_movie(db, show.movie_id)
                theater = TheaterService.get_theater(db, show.theater_id)
                hall = HallService.get_hall(db, show.hall_id)
                
                suggestions.append({
                    "show_id": show.id,
                    "movie_title": movie.title,
                    "theater_name": theater.name,
                    "hall_name": hall.name,
                    "show_time": show.show_time,
                    "available_seats": consecutive_seats,
                    "total_available": len(consecutive_seats),
                    "price_per_seat": show.price
                })
        
        # Sort by show time if preferred_time is provided
        if preferred_time:
            suggestions.sort(key=lambda x: abs((x["show_time"] - preferred_time).total_seconds()))
        
        return suggestions

class BookingService:
    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate) -> Booking:
        """Create a booking with distributed locking to prevent concurrent bookings"""
        show = ShowService.get_show(db, booking_data.show_id)
        if not show:
            raise ShowNotFoundException(f"Show with id {booking_data.show_id} not found")
        
        # Create a lock key for the seats
        lock_key = f"booking_lock:{booking_data.show_id}:{','.join(map(str, sorted(booking_data.seat_ids)))}"
        
        # Try to acquire lock
        lock_acquired = redis_client.set(lock_key, "1", ex=30, nx=True)  # 30 seconds timeout
        
        if not lock_acquired:
            raise SeatAlreadyBookedException("Seats are being booked by another user. Please try again.")
        
        try:
            # Check if seats are available
            seats = db.query(Seat).filter(
                and_(
                    Seat.id.in_(booking_data.seat_ids),
                    Seat.show_id == booking_data.show_id,
                    Seat.is_booked == False
                )
            ).all()
            
            if len(seats) != len(booking_data.seat_ids):
                raise InsufficientSeatsException("Some seats are not available")
            
            # Calculate total amount
            total_amount = len(seats) * show.price
            
            # Create booking
            booking_reference = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
            booking = Booking(
                user_id=booking_data.user_id,
                show_id=booking_data.show_id,
                booking_reference=booking_reference,
                total_amount=total_amount,
                booking_status="confirmed"
            )
            
            db.add(booking)
            db.flush()  # Get the booking ID
            
            # Update seats
            for seat in seats:
                seat.is_booked = True
                seat.booking_id = booking.id
            
            db.commit()
            db.refresh(booking)
            
            return booking
            
        finally:
            # Release the lock
            redis_client.delete(lock_key)
    
    @staticmethod
    def get_booking(db: Session, booking_id: int) -> Optional[Booking]:
        return db.query(Booking).filter(Booking.id == booking_id).first()
    
    @staticmethod
    def get_user_bookings(db: Session, user_id: int) -> List[Booking]:
        return db.query(Booking).filter(Booking.user_id == user_id).all()

class AnalyticsService:
    @staticmethod
    def get_movie_analytics(db: Session, movie_id: int, start_date: datetime, 
                           end_date: datetime) -> Dict[str, Any]:
        """Get analytics for a movie in a given period"""
        # Get movie details
        movie = MovieService.get_movie(db, movie_id)
        if not movie:
            raise MovieNotFoundException(f"Movie with id {movie_id} not found")
        
        # Get bookings for the movie in the period
        bookings = db.query(Booking).join(Show).filter(
            and_(
                Show.movie_id == movie_id,
                Booking.booking_time >= start_date,
                Booking.booking_time <= end_date,
                Booking.booking_status == "confirmed"
            )
        ).all()
        
        total_bookings = len(bookings)
        total_tickets = sum(len(booking.seats) for booking in bookings)
        total_gmv = sum(booking.total_amount for booking in bookings)
        
        # Daily statistics
        daily_stats = db.query(
            func.date(Booking.booking_time).label('date'),
            func.count(Booking.id).label('bookings'),
            func.sum(func.coalesce(func.json_array_length(Booking.seats), 0)).label('tickets'),
            func.sum(Booking.total_amount).label('gmv')
        ).join(Show).filter(
            and_(
                Show.movie_id == movie_id,
                Booking.booking_time >= start_date,
                Booking.booking_time <= end_date,
                Booking.booking_status == "confirmed"
            )
        ).group_by(func.date(Booking.booking_time)).all()
        
        return {
            "movie_id": movie_id,
            "movie_title": movie.title,
            "total_bookings": total_bookings,
            "total_tickets": total_tickets,
            "total_gmv": total_gmv,
            "period_start": start_date,
            "period_end": end_date,
            "daily_stats": [
                {
                    "date": str(stat.date),
                    "bookings": stat.bookings,
                    "tickets": stat.tickets or 0,
                    "gmv": float(stat.gmv or 0)
                }
                for stat in daily_stats
            ]
        }
    
    @staticmethod
    def get_theater_analytics(db: Session, theater_id: int, start_date: datetime, 
                             end_date: datetime) -> Dict[str, Any]:
        """Get analytics for a theater in a given period"""
        # Get theater details
        theater = TheaterService.get_theater(db, theater_id)
        if not theater:
            raise TheaterNotFoundException(f"Theater with id {theater_id} not found")
        
        # Get bookings for the theater in the period
        bookings = db.query(Booking).join(Show).filter(
            and_(
                Show.theater_id == theater_id,
                Booking.booking_time >= start_date,
                Booking.booking_time <= end_date,
                Booking.booking_status == "confirmed"
            )
        ).all()
        
        total_bookings = len(bookings)
        total_tickets = sum(len(booking.seats) for booking in bookings)
        total_gmv = sum(booking.total_amount for booking in bookings)
        
        # Hall statistics
        hall_stats = db.query(
            Show.hall_id,
            func.count(Booking.id).label('bookings'),
            func.sum(func.coalesce(func.json_array_length(Booking.seats), 0)).label('tickets'),
            func.sum(Booking.total_amount).label('gmv')
        ).join(Booking).filter(
            and_(
                Show.theater_id == theater_id,
                Booking.booking_time >= start_date,
                Booking.booking_time <= end_date,
                Booking.booking_status == "confirmed"
            )
        ).group_by(Show.hall_id).all()
        
        return {
            "theater_id": theater_id,
            "theater_name": theater.name,
            "total_bookings": total_bookings,
            "total_tickets": total_tickets,
            "total_gmv": total_gmv,
            "period_start": start_date,
            "period_end": end_date,
            "hall_stats": [
                {
                    "hall_id": stat.hall_id,
                    "bookings": stat.bookings,
                    "tickets": stat.tickets or 0,
                    "gmv": float(stat.gmv or 0)
                }
                for stat in hall_stats
            ]
        }
