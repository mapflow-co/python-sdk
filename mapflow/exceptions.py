"""Custom exceptions for MapFlow SDK."""


class MapFlowError(Exception):
    """Base exception for all MapFlow SDK errors."""
    
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(MapFlowError):
    """Raised when authentication fails (401)."""
    pass


class NotFoundError(MapFlowError):
    """Raised when a resource is not found (404)."""
    pass


class ValidationError(MapFlowError):
    """Raised when request validation fails (400)."""
    pass


class ForbiddenError(MapFlowError):
    """Raised when access is forbidden (403)."""
    pass


class ServerError(MapFlowError):
    """Raised when server returns 5xx error."""
    pass


class RateLimitError(MapFlowError):
    """Raised when rate limit is exceeded (429)."""
    pass

