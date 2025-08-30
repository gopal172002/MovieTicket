from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    genre = Column(String(100))
    language = Column(String(50))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    shows = relationship("Show", back_populates="movie")

class Theater(Base):
    __tablename__ = "theaters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    pincode = Column(String(10))
    phone = Column(String(20))
    email = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    halls = relationship("Hall", back_populates="theater")

class Hall(Base):
    __tablename__ = "halls"
    
    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    name = Column(String(100), nullable=False)
    total_rows = Column(Integer, nullable=False)
    seats_per_row = Column(JSON, nullable=False)  # Store as JSON: {"row1": 7, "row2": 8, ...}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    theater = relationship("Theater", back_populates="halls")
    shows = relationship("Show", back_populates="hall")
    seats = relationship("Seat", back_populates="hall")

class Show(Base):
    __tablename__ = "shows"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    show_time = Column(DateTime, nullable=False, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    movie = relationship("Movie", back_populates="shows")
    theater = relationship("Theater")
    hall = relationship("Hall", back_populates="shows")
    seats = relationship("Seat", back_populates="show")

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    is_aisle = Column(Boolean, default=False)  # True if it's an aisle seat (columns 1, 2, 3)
    is_booked = Column(Boolean, default=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    show = relationship("Show", back_populates="seats")
    hall = relationship("Hall", back_populates="seats")
    booking = relationship("Booking", back_populates="seats")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # In a real app, this would be ForeignKey to User table
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    booking_reference = Column(String(50), unique=True, nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    booking_status = Column(String(20), default="confirmed")  # confirmed, cancelled, completed
    booking_time = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    show = relationship("Show")
    seats = relationship("Seat", back_populates="booking")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
