
"""
Sample Data Population Script for AlgoBharat Movie Ticket Booking System
This script creates sample movies, theaters, halls, and shows for testing.
"""

import sys
import os
from datetime import datetime, timedelta


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import SessionLocal
from app.models import Movie, Theater, Hall, Show, Seat
from app.services import MovieService, TheaterService, HallService, ShowService, SeatService

def create_sample_data():
    """Create sample data for the movie ticket booking system"""
    db = SessionLocal()
    
    try:
        print("Creating sample data...")
        
        # Create Movies
        print("Creating movies...")
        movies_data = [
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "duration_minutes": 152,
                "genre": "Action, Crime, Drama",
                "language": "English",
                "price": 12.99
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "duration_minutes": 148,
                "genre": "Action, Adventure, Sci-Fi",
                "language": "English",
                "price": 14.99
            },
            {
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "duration_minutes": 169,
                "genre": "Adventure, Drama, Sci-Fi",
                "language": "English",
                "price": 13.99
            },
            {
                "title": "The Shawshank Redemption",
                "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "duration_minutes": 142,
                "genre": "Drama",
                "language": "English",
                "price": 11.99
            },
            {
                "title": "Pulp Fiction",
                "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "duration_minutes": 154,
                "genre": "Crime, Drama",
                "language": "English",
                "price": 12.49
            }
        ]
        
        movies = []
        for movie_data in movies_data:
            movie = Movie(**movie_data)
            db.add(movie)
            db.flush()  # Get the ID
            movies.append(movie)
            print(f"Created movie: {movie.title}")
        
        # Theaters
        print("Creating theaters...")
        theaters_data = [
            {
                "name": "Cineplex Downtown",
                "address": "123 Main Street, Downtown",
                "city": "New York",
                "state": "NY",
                "pincode": "10001",
                "phone": "+1-555-0101",
                "email": "info@cineplexdowntown.com"
            },
            {
                "name": "MegaPlex Cinema",
                "address": "456 Broadway Avenue",
                "city": "Los Angeles",
                "state": "CA",
                "pincode": "90210",
                "phone": "+1-555-0202",
                "email": "contact@megaplex.com"
            },
            {
                "name": "Starlight Theater",
                "address": "789 Oak Street",
                "city": "Chicago",
                "state": "IL",
                "pincode": "60601",
                "phone": "+1-555-0303",
                "email": "hello@starlight.com"
            }
        ]
        
        theaters = []
        for theater_data in theaters_data:
            theater = Theater(**theater_data)
            db.add(theater)
            db.flush()  # Get the ID
            theaters.append(theater)
            print(f"Created theater: {theater.name}")
        
        # Create Halls for each theater
        print("Creating halls...")
        halls = []
        for theater in theaters:
            # Create 2 halls per theater
            for hall_num in range(1, 3):
                hall_data = {
                    "name": f"Hall {hall_num}",
                    "total_rows": 10,
                    "seats_per_row": {
                        "row1": 8, "row2": 8, "row3": 9, "row4": 9, "row5": 10,
                        "row6": 10, "row7": 11, "row8": 11, "row9": 12, "row10": 12
                    }
                }
                hall = Hall(**hall_data, theater_id=theater.id)
                db.add(hall)
                db.flush()  # Get the ID
                halls.append(hall)
                print(f"Created hall: {hall.name} in {theater.name}")
        
        # Create Shows
        print("Creating shows...")
        shows = []
        base_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        for movie in movies:
            for theater in theaters:
                for hall in [h for h in halls if h.theater_id == theater.id]:
                    # Create 3 shows per movie-theater-hall combination
                    for show_num in range(3):
                        show_time = base_time + timedelta(
                            days=show_num,
                            hours=show_num * 4  # 10 AM, 2 PM, 6 PM
                        )
                        
                        show_data = {
                            "movie_id": movie.id,
                            "theater_id": theater.id,
                            "hall_id": hall.id,
                            "show_time": show_time,
                            "price": movie.price + (show_num * 2)  # Slight price variation
                        }
                        
                        show = Show(**show_data)
                        db.add(show)
                        db.flush()  # Get the ID
                        shows.append(show)
                        
                        # Create seats for this show
                        SeatService.create_seats_for_show(db, show.id, hall)
                        
                        print(f"Created show: {movie.title} at {theater.name} {hall.name} - {show_time.strftime('%Y-%m-%d %H:%M')}")
        
        db.commit()
        print(f"\nSample data created successfully!")
        print(f"Created {len(movies)} movies")
        print(f"Created {len(theaters)} theaters")
        print(f"Created {len(halls)} halls")
        print(f"Created {len(shows)} shows")
        print(f"Created seats for all shows")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
