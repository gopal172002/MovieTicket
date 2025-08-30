#!/usr/bin/env python3
"""
API Tests for AlgoBharat Movie Ticket Booking System
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

from app.main import app
from app.database import get_db, Base
from app.models import Movie, Theater, Hall, Show, Seat, Booking


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestMoviesAPI:
    def test_create_movie(self):
        movie_data = {
            "title": "Test Movie",
            "description": "A test movie description",
            "duration_minutes": 120,
            "genre": "Action",
            "language": "English",
            "price": 10.99
        }
        response = client.post("/api/v1/movies/", json=movie_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == movie_data["title"]
        assert data["price"] == movie_data["price"]
        assert "id" in data

    def test_get_movies(self):
        response = client.get("/api/v1/movies/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_movie(self):
        # First create a movie
        movie_data = {
            "title": "Test Movie 2",
            "description": "Another test movie",
            "duration_minutes": 90,
            "genre": "Comedy",
            "language": "English",
            "price": 8.99
        }
        create_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(f"/api/v1/movies/{movie_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == movie_data["title"]

    def test_update_movie(self):
        # First create a movie
        movie_data = {
            "title": "Test Movie 3",
            "description": "A test movie to update",
            "duration_minutes": 110,
            "genre": "Drama",
            "language": "English",
            "price": 9.99
        }
        create_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = create_response.json()["id"]
        
        # Then update it
        update_data = {"price": 12.99}
        response = client.put(f"/api/v1/movies/{movie_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 12.99

    def test_delete_movie(self):
        # First create a movie
        movie_data = {
            "title": "Test Movie 4",
            "description": "A test movie to delete",
            "duration_minutes": 100,
            "genre": "Thriller",
            "language": "English",
            "price": 11.99
        }
        create_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/movies/{movie_id}")
        assert response.status_code == 204

class TestTheatersAPI:
    def test_create_theater(self):
        theater_data = {
            "name": "Test Theater",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "TS",
            "pincode": "12345",
            "phone": "+1-555-0123",
            "email": "test@theater.com"
        }
        response = client.post("/api/v1/theaters/", json=theater_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == theater_data["name"]
        assert "id" in data

    def test_get_theaters(self):
        response = client.get("/api/v1/theaters/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_hall(self):
        # First create a theater
        theater_data = {
            "name": "Test Theater for Hall",
            "address": "456 Test Avenue",
            "city": "Test City",
            "state": "TS",
            "pincode": "12346",
            "phone": "+1-555-0124",
            "email": "hall@theater.com"
        }
        theater_response = client.post("/api/v1/theaters/", json=theater_data)
        theater_id = theater_response.json()["id"]
        
        # Then create a hall
        hall_data = {
            "name": "Test Hall",
            "total_rows": 5,
            "seats_per_row": {
                "row1": 6, "row2": 7, "row3": 8, "row4": 7, "row5": 6
            }
        }
        response = client.post(f"/api/v1/theaters/{theater_id}/halls", json=hall_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == hall_data["name"]
        assert data["theater_id"] == theater_id

class TestShowsAPI:
    def test_create_show(self):
        # Create movie, theater, and hall first
        movie_data = {
            "title": "Show Test Movie",
            "description": "A movie for show testing",
            "duration_minutes": 130,
            "genre": "Action",
            "language": "English",
            "price": 13.99
        }
        movie_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        theater_data = {
            "name": "Show Test Theater",
            "address": "789 Show Street",
            "city": "Show City",
            "state": "SC",
            "pincode": "12347",
            "phone": "+1-555-0125",
            "email": "show@theater.com"
        }
        theater_response = client.post("/api/v1/theaters/", json=theater_data)
        theater_id = theater_response.json()["id"]
        
        hall_data = {
            "name": "Show Test Hall",
            "total_rows": 3,
            "seats_per_row": {"row1": 6, "row2": 7, "row3": 6}
        }
        hall_response = client.post(f"/api/v1/theaters/{theater_id}/halls", json=hall_data)
        hall_id = hall_response.json()["id"]
        
        # Create show
        show_time = datetime.now() + timedelta(days=1)
        show_data = {
            "movie_id": movie_id,
            "theater_id": theater_id,
            "hall_id": hall_id,
            "show_time": show_time.isoformat(),
            "price": 15.99
        }
        response = client.post("/api/v1/shows/", json=show_data)
        assert response.status_code == 201
        data = response.json()
        assert data["movie_id"] == movie_id
        assert data["theater_id"] == theater_id
        assert data["hall_id"] == hall_id

class TestBookingsAPI:
    def test_get_hall_layout(self):
        # Create all necessary data
        movie_data = {
            "title": "Booking Test Movie",
            "description": "A movie for booking testing",
            "duration_minutes": 140,
            "genre": "Drama",
            "language": "English",
            "price": 14.99
        }
        movie_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        theater_data = {
            "name": "Booking Test Theater",
            "address": "321 Booking Street",
            "city": "Booking City",
            "state": "BC",
            "pincode": "12348",
            "phone": "+1-555-0126",
            "email": "booking@theater.com"
        }
        theater_response = client.post("/api/v1/theaters/", json=theater_data)
        theater_id = theater_response.json()["id"]
        
        hall_data = {
            "name": "Booking Test Hall",
            "total_rows": 2,
            "seats_per_row": {"row1": 6, "row2": 7}
        }
        hall_response = client.post(f"/api/v1/theaters/{theater_id}/halls", json=hall_data)
        hall_id = hall_response.json()["id"]
        
        show_time = datetime.now() + timedelta(days=2)
        show_data = {
            "movie_id": movie_id,
            "theater_id": theater_id,
            "hall_id": hall_id,
            "show_time": show_time.isoformat(),
            "price": 16.99
        }
        show_response = client.post("/api/v1/shows/", json=show_data)
        show_id = show_response.json()["id"]
        
        # Get hall layout
        response = client.get(f"/api/v1/bookings/halls/{hall_id}/layout?show_id={show_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["hall_id"] == hall_id
        assert "available_seats" in data
        assert "booked_seats" in data

    def test_find_consecutive_seats(self):
        # Create all necessary data
        movie_data = {
            "title": "Consecutive Test Movie",
            "description": "A movie for consecutive seat testing",
            "duration_minutes": 150,
            "genre": "Comedy",
            "language": "English",
            "price": 15.99
        }
        movie_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        theater_data = {
            "name": "Consecutive Test Theater",
            "address": "654 Consecutive Street",
            "city": "Consecutive City",
            "state": "CC",
            "pincode": "12349",
            "phone": "+1-555-0127",
            "email": "consecutive@theater.com"
        }
        theater_response = client.post("/api/v1/theaters/", json=theater_data)
        theater_id = theater_response.json()["id"]
        
        hall_data = {
            "name": "Consecutive Test Hall",
            "total_rows": 2,
            "seats_per_row": {"row1": 8, "row2": 8}
        }
        hall_response = client.post(f"/api/v1/theaters/{theater_id}/halls", json=hall_data)
        hall_id = hall_response.json()["id"]
        
        show_time = datetime.now() + timedelta(days=3)
        show_data = {
            "movie_id": movie_id,
            "theater_id": theater_id,
            "hall_id": hall_id,
            "show_time": show_time.isoformat(),
            "price": 17.99
        }
        show_response = client.post("/api/v1/shows/", json=show_data)
        show_id = show_response.json()["id"]
        
        # Find consecutive seats
        response = client.get(f"/api/v1/bookings/shows/{show_id}/consecutive-seats?num_seats=3")
        assert response.status_code == 200
        data = response.json()
        assert data["show_id"] == show_id
        assert data["num_seats_requested"] == 3
        assert "consecutive_seats_found" in data

class TestAnalyticsAPI:
    def test_movie_analytics(self):
        # Create movie
        movie_data = {
            "title": "Analytics Test Movie",
            "description": "A movie for analytics testing",
            "duration_minutes": 160,
            "genre": "Thriller",
            "language": "English",
            "price": 16.99
        }
        movie_response = client.post("/api/v1/movies/", json=movie_data)
        movie_id = movie_response.json()["id"]
        
        # Test analytics endpoint
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
        end_date = datetime.now().isoformat()
        
        response = client.get(f"/api/v1/analytics/movies/{movie_id}?start_date={start_date}&end_date={end_date}")
        assert response.status_code == 200
        data = response.json()
        assert data["movie_id"] == movie_id
        assert "total_bookings" in data
        assert "total_tickets" in data
        assert "total_gmv" in data

if __name__ == "__main__":
    pytest.main([__file__])
