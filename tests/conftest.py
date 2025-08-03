"""
Pytest configuration and shared fixtures.
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock

from fastapi.testclient import TestClient
from httpx import AsyncClient

from agent_project.application.main import create_app
from agent_project.config import settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app():
    """Create FastAPI app instance for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
async def async_client(app):
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_vector_client():
    """Mock vector database client."""
    mock_client = AsyncMock()
    mock_client.similarity_search.return_value = [
        {
            "content": "Test clause content",
            "similarity_score": 0.95,
            "metadata": {
                "source": "NCC 2022",
                "clause_type": "code_b",
                "section": "B1.2",
                "page_number": 123
            }
        }
    ]
    mock_client.health_check.return_value = True
    mock_client.get_database_info.return_value = {"status": "healthy"}
    return mock_client


@pytest.fixture
def mock_llm_client():
    """Mock LLM client."""
    mock_client = AsyncMock()
    mock_client.generate.return_value = "Test response from LLM"
    mock_client.get_available_providers.return_value = {"openai": True, "anthropic": False}
    return mock_client


@pytest.fixture
def mock_user():
    """Mock authenticated user."""
    return {
        "sub": "test-user-id",
        "email": "test@example.com",
        "role": "user",
        "aud": "authenticated",
        "exp": 1234567890
    }


@pytest.fixture
def mock_admin_user():
    """Mock admin user."""
    return {
        "sub": "admin-user-id",
        "email": "admin@example.com",
        "role": "admin",
        "aud": "authenticated",
        "exp": 1234567890
    }


@pytest.fixture
def auth_headers(mock_user):
    """Create auth headers for testing."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def admin_auth_headers(mock_admin_user):
    """Create admin auth headers for testing."""
    return {"Authorization": "Bearer admin-test-token"}


@pytest.fixture
def sample_chat_message():
    """Sample chat message for testing."""
    return {
        "content": "What is the minimum R-value for Zone 3 walls?",
        "session_id": "test-session-123"
    }


@pytest.fixture
def sample_vector_search_results():
    """Sample vector search results."""
    return [
        {
            "content": "The minimum R-value for walls in Climate Zone 3 is R2.8 for steel frame construction and R2.5 for timber frame construction.",
            "similarity_score": 0.92,
            "metadata": {
                "source": "NCC 2022 Volume Two",
                "clause_type": "code_c",
                "section": "J1.5",
                "page_number": 245,
                "document_id": "ncc-2022-vol2"
            }
        },
        {
            "content": "Climate Zone 3 covers areas with moderate heating and cooling requirements...",
            "similarity_score": 0.88,
            "metadata": {
                "source": "NCC 2022 Volume Two",
                "clause_type": "code_c", 
                "section": "J0.1",
                "page_number": 201,
                "document_id": "ncc-2022-vol2"
            }
        }
    ]


@pytest.fixture(autouse=True)
def override_settings():
    """Override settings for testing."""
    # Use test database URL
    settings.database_url = "postgresql://test:test@localhost/test_db"
    settings.app_env = "testing"
    settings.jwt_secret_key = "test-secret-key"
    settings.enable_metrics = False
    settings.log_level = "WARNING"  # Reduce log noise during testing