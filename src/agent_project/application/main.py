"""
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from agent_project.application.routers import admin, chat, health
from agent_project.config import settings
from agent_project.core.utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    setup_logging(level=settings.log_level)
    logger = structlog.get_logger()
    logger.info("Starting Code Vision Agent API", version=settings.app_version)

    yield

    # Shutdown
    logger.info("Shutting down Code Vision Agent API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI agent system for querying building codes and regulations",
        lifespan=lifespan,
        docs_url=f"/api/{settings.api_version}/docs",
        openapi_url=f"/api/{settings.api_version}/openapi.json",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(
        chat.router, prefix=f"/api/{settings.api_version}", tags=["chat"]
    )
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(
        admin.router, prefix=f"/api/{settings.api_version}/admin", tags=["admin"]
    )

    # Prometheus metrics endpoint
    if settings.enable_metrics:
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)

    return app


# Create the app instance
app = create_app()
