class AlgoBharatException(Exception):
    """Base exception for AlgoBharat application"""
    pass

class SeatAlreadyBookedException(AlgoBharatException):
    """Raised when trying to book already booked seats"""
    pass

class InsufficientSeatsException(AlgoBharatException):
    """Raised when requested seats are not available"""
    pass

class ShowNotFoundException(AlgoBharatException):
    """Raised when show is not found"""
    pass

class HallNotFoundException(AlgoBharatException):
    """Raised when hall is not found"""
    pass

class TheaterNotFoundException(AlgoBharatException):
    """Raised when theater is not found"""
    pass

class MovieNotFoundException(AlgoBharatException):
    """Raised when movie is not found"""
    pass

class BookingNotFoundException(AlgoBharatException):
    """Raised when booking is not found"""
    pass

class InvalidSeatLayoutException(AlgoBharatException):
    """Raised when seat layout is invalid"""
    pass

class ConcurrentBookingException(AlgoBharatException):
    """Raised when concurrent booking attempt is detected"""
    pass
