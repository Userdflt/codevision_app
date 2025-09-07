"""
Structured logging configuration using structlog.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.stdlib import LoggerFactory

from agent_project.config import settings


def setup_logging(level: str = "INFO") -> None:
    """
    Configure structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=getattr(logging, level.upper())
    )

    # Configure structlog
    structlog.configure(
        processors=[
            # Add logger name and level
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            # Add timestamp
            structlog.processors.TimeStamper(fmt="ISO"),
            # Add stack info for exceptions
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            # JSON formatting for production, console for development
            structlog.processors.JSONRenderer()
            if settings.app_env == "production"
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = __name__) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class RequestIDProcessor:
    """Structlog processor to add request ID to all log messages."""

    def __init__(self):
        self.request_id = None

    def __call__(self, logger: Any, method_name: str, event_dict: dict) -> dict:
        """Add request ID to log event if available."""
        if self.request_id:
            event_dict["request_id"] = self.request_id
        return event_dict

    def set_request_id(self, request_id: str):
        """Set the current request ID."""
        self.request_id = request_id

    def clear_request_id(self):
        """Clear the current request ID."""
        self.request_id = None


# Global request ID processor instance
request_id_processor = RequestIDProcessor()
