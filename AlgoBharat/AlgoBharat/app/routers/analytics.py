from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta
from ..database import get_db
from ..schemas import MovieAnalytics, TheaterAnalytics
from ..services import AnalyticsService
from ..exceptions import MovieNotFoundException, TheaterNotFoundException

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/movies/{movie_id}", response_model=MovieAnalytics)
def get_movie_analytics(
    movie_id: int,
    start_date: datetime = Query(..., description="Start date for analytics period"),
    end_date: datetime = Query(..., description="End date for analytics period"),
    db: Session = Depends(get_db)
):
    """Get analytics for a movie in a given period"""
    try:
        return AnalyticsService.get_movie_analytics(db, movie_id, start_date, end_date)
    except MovieNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/movies/{movie_id}/last-30-days", response_model=MovieAnalytics)
def get_movie_analytics_last_30_days(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """Get analytics for a movie in the last 30 days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        return AnalyticsService.get_movie_analytics(db, movie_id, start_date, end_date)
    except MovieNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/theaters/{theater_id}", response_model=TheaterAnalytics)
def get_theater_analytics(
    theater_id: int,
    start_date: datetime = Query(..., description="Start date for analytics period"),
    end_date: datetime = Query(..., description="End date for analytics period"),
    db: Session = Depends(get_db)
):
    """Get analytics for a theater in a given period"""
    try:
        return AnalyticsService.get_theater_analytics(db, theater_id, start_date, end_date)
    except TheaterNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/theaters/{theater_id}/last-30-days", response_model=TheaterAnalytics)
def get_theater_analytics_last_30_days(
    theater_id: int,
    db: Session = Depends(get_db)
):
    """Get analytics for a theater in the last 30 days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        return AnalyticsService.get_theater_analytics(db, theater_id, start_date, end_date)
    except TheaterNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/dashboard")
def get_dashboard_analytics(
    start_date: datetime = Query(..., description="Start date for analytics period"),
    end_date: datetime = Query(..., description="End date for analytics period"),
    db: Session = Depends(get_db)
):
    """Get overall dashboard analytics"""
    # This would typically aggregate data from multiple sources
    # For now, we'll return a basic structure
    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "summary": {
            "total_bookings": 0,  # Would be calculated from database
            "total_revenue": 0.0,  # Would be calculated from database
            "total_tickets": 0,    # Would be calculated from database
            "average_booking_value": 0.0  # Would be calculated from database
        },
        "top_movies": [],  # Would be populated with top performing movies
        "top_theaters": []  # Would be populated with top performing theaters
    }
