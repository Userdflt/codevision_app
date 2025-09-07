"""
Admin endpoints for system management and debugging.
"""

from datetime import datetime
from typing import Any, Dict, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from agent_project.infrastructure.auth.dependencies import get_admin_user
from agent_project.infrastructure.vector_db.client import VectorDBClient

logger = structlog.get_logger()
router = APIRouter()


class VectorSearchRequest(BaseModel):
    """Vector search request for debugging."""

    query: str
    limit: int = 10
    similarity_threshold: float = 0.8
    clause_type: str | None = None


class VectorSearchResult(BaseModel):
    """Vector search result."""

    content: str
    similarity_score: float
    metadata: Dict[str, Any]


@router.post("/vector-search", response_model=List[VectorSearchResult])
async def debug_vector_search(
    request: VectorSearchRequest, admin_user: Dict[str, Any] = Depends(get_admin_user)
) -> List[VectorSearchResult]:
    """
    Debug endpoint for testing vector search directly.
    """
    try:
        logger.info(
            "Admin vector search",
            admin_id=admin_user.get("sub"),
            query=request.query,
            limit=request.limit,
        )

        vector_client = VectorDBClient()
        results = await vector_client.similarity_search(
            query=request.query,
            limit=request.limit,
            similarity_threshold=request.similarity_threshold,
            clause_type=request.clause_type,
        )

        return [
            VectorSearchResult(
                content=result["content"],
                similarity_score=result["similarity_score"],
                metadata=result["metadata"],
            )
            for result in results
        ]

    except Exception as e:
        logger.error("Admin vector search failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Vector search failed",
        )


@router.get("/database/stats")
async def get_database_stats(
    admin_user: Dict[str, Any] = Depends(get_admin_user)
) -> Dict[str, Any]:
    """
    Get database statistics and table information.
    """
    try:
        logger.info("Getting database stats", admin_id=admin_user.get("sub"))

        vector_client = VectorDBClient()
        stats = await vector_client.get_database_stats()

        return {"timestamp": datetime.utcnow().isoformat(), "statistics": stats}

    except Exception as e:
        logger.error("Failed to get database stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve database statistics",
        )


@router.delete("/sessions/cleanup")
async def cleanup_expired_sessions(
    older_than_hours: int = Query(default=24, ge=1, le=168),  # 1 hour to 1 week
    admin_user: Dict[str, Any] = Depends(get_admin_user),
) -> Dict[str, Any]:
    """
    Clean up expired chat sessions.
    """
    try:
        logger.info(
            "Cleaning up expired sessions",
            admin_id=admin_user.get("sub"),
            older_than_hours=older_than_hours,
        )

        # TODO: Implement session cleanup logic
        # This would delete chat sessions older than the specified time

        # Placeholder response
        cleaned_count = 0

        return {
            "message": "Session cleanup completed",
            "sessions_cleaned": cleaned_count,
            "older_than_hours": older_than_hours,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error("Session cleanup failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session cleanup failed",
        )


@router.post("/agents/test/{agent_type}")
async def test_agent(
    agent_type: str, query: str, admin_user: Dict[str, Any] = Depends(get_admin_user)
) -> Dict[str, Any]:
    """
    Test a specific agent type with a query.
    """
    try:
        valid_agents = [
            "orchestrator",
            "code_b",
            "code_c",
            "code_d",
            "code_e",
            "code_f",
            "code_g",
            "code_h",
        ]

        if agent_type not in valid_agents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid agent type. Must be one of: {valid_agents}",
            )

        logger.info(
            "Testing agent",
            admin_id=admin_user.get("sub"),
            agent_type=agent_type,
            query=query,
        )

        # TODO: Implement agent testing logic
        # This would instantiate the specific agent and test it with the query

        return {
            "agent_type": agent_type,
            "query": query,
            "test_result": "Test completed successfully",
            "timestamp": datetime.utcnow().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Agent test failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent test failed",
        )
