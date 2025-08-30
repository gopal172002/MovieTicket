# AlgoBharat Movie Ticket Booking System - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- Redis (for distributed locking - optional for development)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AlgoBharat
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp env.example .env
```

Edit `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=sqlite:///./algobharat.db

# Redis Configuration (optional for development)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Application Configuration
DEBUG=True
```

### 5. Initialize Database

```bash
# Create database tables
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"

# Or use Alembic for migrations
alembic upgrade head
```

### 6. Populate Sample Data (Optional)

```bash
python scripts/sample_data.py
```

### 7. Run the Application

```bash
# Using the startup script
python start.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- API: http://localhost:8000
- Interactive API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run tests with coverage
pytest --cov=app tests/
```

## Database Migrations

### Using Alembic

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade to previous version
alembic downgrade -1

# View migration history
alembic history
```

## Deployment

### Option 1: Railway Deployment

1. Create a Railway account at https://railway.app
2. Connect your GitHub repository
3. Railway will automatically detect the Python application
4. Set environment variables in Railway dashboard:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `REDIS_HOST`: Your Redis host
   - `REDIS_PORT`: Your Redis port
   - `DEBUG`: False

### Option 2: Heroku Deployment

1. Create a Heroku account
2. Install Heroku CLI
3. Create a new Heroku app:

```bash
heroku create your-app-name
```

4. Add PostgreSQL addon:

```bash
heroku addons:create heroku-postgresql:mini
```

5. Set environment variables:

```bash
heroku config:set DEBUG=False
heroku config:set REDIS_HOST=your-redis-host
heroku config:set REDIS_PORT=your-redis-port
```

6. Deploy:

```bash
git push heroku main
```

### Option 3: Docker Deployment

1. Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run:

```bash
docker build -t algobharat .
docker run -p 8000:8000 algobharat
```

## API Usage Examples

### 1. Create a Movie

```bash
curl -X POST "http://localhost:8000/api/v1/movies/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Dark Knight",
    "description": "A superhero movie",
    "duration_minutes": 152,
    "genre": "Action",
    "language": "English",
    "price": 12.99
  }'
```

### 2. Create a Theater

```bash
curl -X POST "http://localhost:8000/api/v1/theaters/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cineplex Downtown",
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "pincode": "10001",
    "phone": "+1-555-0101",
    "email": "info@cineplex.com"
  }'
```

### 3. Create a Hall

```bash
curl -X POST "http://localhost:8000/api/v1/theaters/1/halls" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hall 1",
    "total_rows": 10,
    "seats_per_row": {
      "row1": 8, "row2": 8, "row3": 9, "row4": 9, "row5": 10,
      "row6": 10, "row7": 11, "row8": 11, "row9": 12, "row10": 12
    }
  }'
```

### 4. Create a Show

```bash
curl -X POST "http://localhost:8000/api/v1/shows/" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "theater_id": 1,
    "hall_id": 1,
    "show_time": "2024-01-15T14:00:00",
    "price": 15.99
  }'
```

### 5. Book Seats

```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "show_id": 1,
    "seat_ids": [1, 2, 3]
  }'
```

### 6. Find Consecutive Seats

```bash
curl "http://localhost:8000/api/v1/bookings/shows/1/consecutive-seats?num_seats=3"
```

### 7. Get Analytics

```bash
curl "http://localhost:8000/api/v1/analytics/movies/1?start_date=2024-01-01T00:00:00&end_date=2024-01-31T23:59:59"
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure the database URL is correct
   - Check if the database server is running
   - Verify database credentials

2. **Redis Connection Error**
   - Redis is optional for development
   - Install Redis locally or use a cloud Redis service
   - Update Redis configuration in `.env`

3. **Import Errors**
   - Ensure you're in the correct directory
   - Activate the virtual environment
   - Install all dependencies with `pip install -r requirements.txt`

4. **Port Already in Use**
   - Change the port in the startup command
   - Kill the process using the port
   - Use a different port in the `.env` file

### Getting Help

- Check the API documentation at `/docs`
- Review the logs for error messages
- Run tests to verify functionality
- Check the database schema and data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.
