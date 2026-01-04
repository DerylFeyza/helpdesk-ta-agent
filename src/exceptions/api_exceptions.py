"""Custom exceptions for API operations."""

from functools import wraps
from typing import Callable, Any
import httpx


class APIException(Exception):
    """Base exception for API-related errors."""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ConnectionException(APIException):
    """Raised when unable to connect to the API server."""

    pass


class TimeoutException(APIException):
    """Raised when an API request times out."""

    pass


class HTTPException(APIException):
    """Raised when API returns an HTTP error status."""

    def __init__(
        self, message: str, status_code: int = None, original_error: Exception = None
    ):
        self.status_code = status_code
        super().__init__(message, original_error)


def handle_httpx_errors(service_name: str = "API", base_url: str = None) -> Callable:
    """
    Decorator to handle common httpx errors and convert them to custom exceptions.

    Args:
        service_name: Name of the service for error messages (e.g., "SCMT", "Payment API")
        base_url: Base URL of the service for error messages

    Usage:
        @handle_httpx_errors(service_name="SCMT", base_url=SCMT_BASE)
        async def get_data():
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except httpx.ConnectError as e:
                server_info = f" at {base_url}" if base_url else ""
                raise ConnectionException(
                    f"Cannot connect to {service_name} server{server_info}",
                    original_error=e,
                ) from e
            except httpx.TimeoutException as e:
                raise TimeoutException(
                    f"Request to {service_name} server timed out",
                    original_error=e,
                ) from e
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    f"{service_name} API returned error: {e.response.text}",
                    status_code=e.response.status_code,
                    original_error=e,
                ) from e
            except (APIException, ConnectionException, TimeoutException, HTTPException):
                # Re-raise custom exceptions without wrapping
                raise
            except Exception as e:
                raise APIException(
                    f"Error in {service_name} operation: {str(e)}",
                    original_error=e,
                ) from e

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except httpx.ConnectError as e:
                server_info = f" at {base_url}" if base_url else ""
                raise ConnectionException(
                    f"Cannot connect to {service_name} server{server_info}",
                    original_error=e,
                ) from e
            except httpx.TimeoutException as e:
                raise TimeoutException(
                    f"Request to {service_name} server timed out",
                    original_error=e,
                ) from e
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    f"{service_name} API returned error: {e.response.text}",
                    status_code=e.response.status_code,
                    original_error=e,
                ) from e
            except (APIException, ConnectionException, TimeoutException, HTTPException):
                # Re-raise custom exceptions without wrapping
                raise
            except Exception as e:
                raise APIException(
                    f"Error in {service_name} operation: {str(e)}",
                    original_error=e,
                ) from e

        # Return appropriate wrapper based on whether function is async
        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
