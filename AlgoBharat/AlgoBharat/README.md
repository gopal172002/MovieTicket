# AlgoBharat Movie Ticket Booking System

A comprehensive movie ticket booking web application built with Python FastAPI.

## Features

- **Movie Management**: CRUD operations for movies with pricing
- **Theater Management**: Register theaters with multiple halls
- **Hall Layout Management**: Configure hall layouts with rows and seats
- **Show Management**: Schedule multiple shows throughout the day
- **Seat Booking**: Book seats individually or as a group
- **Concurrent Booking Protection**: Prevent double booking with Redis locks
- **Smart Seat Suggestions**: Suggest alternative times when seats aren't available together
- **Analytics**: Track booking statistics and GMV

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching & Locks**: Redis
- **Task Queue**: Celery
- **Deployment**: Railway/Heroku ready

## API Endpoints

### Movies
- `GET /movies` - List all movies
- `POST /movies` - Create a new movie
- `GET /movies/{movie_id}` - Get movie details
- `PUT /movies/{movie_id}` - Update movie
- `DELETE /movies/{movie_id}` - Delete movie

### Theaters
- `GET /theaters` - List all theaters
- `POST /theaters` - Create a new theater
- `GET /theaters/{theater_id}` - Get theater details
- `PUT /theaters/{theater_id}` - Update theater
- `DELETE /theaters/{theater_id}` - Delete theater

### Halls
- `GET /theaters/{theater_id}/halls` - List theater halls
- `POST /theaters/{theater_id}/halls` - Create a new hall
- `GET /halls/{hall_id}/layout` - Get hall layout
- `PUT /halls/{hall_id}/layout` - Update hall layout

### Shows
- `GET /shows` - List all shows
- `POST /shows` - Create a new show
- `GET /shows/{show_id}` - Get show details
- `PUT /shows/{show_id}` - Update show
- `DELETE /shows/{show_id}` - Delete show

### Bookings
- `POST /bookings` - Create a new booking
- `GET /bookings/{booking_id}` - Get booking details
- `GET /bookings` - List user bookings

### Analytics
- `GET /analytics/movies/{movie_id}` - Get movie analytics
- `GET /analytics/theaters/{theater_id}` - Get theater analytics

## Installation & Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run database migrations: `alembic upgrade head`
5. Start the server: `uvicorn app.main:app --reload`

## Database Schema

The application uses a relational database with the following main entities:
- Movies
- Theaters
- Halls
- Shows
- Seats
- Bookings
- Users

## Deployment

The application is configured for deployment on Railway, Heroku, or any other cloud platform that supports Python applications.

## License

MIT License
