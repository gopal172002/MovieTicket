from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import engine
from .models import Base
from .routers import movies, theaters, shows, bookings, analytics
from .exceptions import AlgoBharatException

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AlgoBharat Movie Ticket Booking System",
    description="A comprehensive movie ticket booking API with seat management, group bookings, and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router, prefix="/api/v1")
app.include_router(theaters.router, prefix="/api/v1")
app.include_router(shows.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")

# Exception handler for custom exceptions
@app.exception_handler(AlgoBharatException)
async def algobharat_exception_handler(request, exc: AlgoBharatException):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "error_code": exc.__class__.__name__}
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to AlgoBharat Movie Ticket Booking System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AlgoBharat Movie Ticket Booking System"}

# API info endpoint
@app.get("/api/info")
async def api_info():
    return {
        "name": "AlgoBharat Movie Ticket Booking API",
        "version": "1.0.0",
        "description": "A comprehensive movie ticket booking system with advanced features",
        "features": [
            "Movie and Theater Management",
            "Hall Layout Configuration",
            "Show Scheduling",
            "Seat Booking with Concurrency Control",
            "Group Booking with Consecutive Seat Selection",
            "Smart Seat Suggestions",
            "Analytics and Reporting"
        ],
        "endpoints": {
            "movies": "/api/v1/movies",
            "theaters": "/api/v1/theaters",
            "shows": "/api/v1/shows",
            "bookings": "/api/v1/bookings",
            "analytics": "/api/v1/analytics"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

