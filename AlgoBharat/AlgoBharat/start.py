#!/usr/bin/env python3
"""
Startup script for AlgoBharat Movie Ticket Booking System
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"Starting AlgoBharat Movie Ticket Booking System...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug mode: {reload}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print(f"ReDoc Documentation: http://{host}:{port}/redoc")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
