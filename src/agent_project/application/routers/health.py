"""
Health check and system status endpoints.
"""

from datetime import datetime
from typing import Dict, Any

import structlog
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from agent_project.config import settings


logger = structlog.get_logger()
router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.
    """
    services = {}
    
    # Check vector database connection
    try:
        vector_client = VectorDBClient()
        await vector_client.health_check()
        services["vector_db"] = "healthy"
    except Exception as e:
        logger.warning("Vector DB health check failed", error=str(e))
        services["vector_db"] = "unhealthy"
    
    # Check LLM provider availability
    try:
        # TODO: Implement LLM provider health check
        services["llm_provider"] = "healthy"
    except Exception as e:
        logger.warning("LLM provider health check failed", error=str(e))
        services["llm_provider"] = "unhealthy"
    
    # Determine overall status
    overall_status = "healthy" if all(
        status == "healthy" for status in services.values()
    ) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        services=services
    )


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with additional system information.
    """
    try:
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.app_version,
            "environment": settings.app_env,
            "services": {
                "vector_db": {"status": "unknown", "details": {}},
                "llm_provider": {"status": "unknown", "details": {}},
            },
            "configuration": {
                "max_vector_results": settings.max_vector_results,
                "vector_similarity_threshold": settings.vector_similarity_threshold,
                "default_llm_provider": settings.default_llm_provider,
                "enable_parallel_agents": settings.enable_parallel_agents,
            }
        }
        
        # Detailed vector DB check
        try:
            vector_client = VectorDBClient()
            db_info = await vector_client.get_database_info()
            health_data["services"]["vector_db"] = {
                "status": "healthy",
                "details": db_info
            }
        except Exception as e:
            health_data["services"]["vector_db"] = {
                "status": "unhealthy",
                "details": {"error": str(e)}
            }
        
        # Check if any critical services are down
        critical_services = ["vector_db"]
        unhealthy_critical = [
            service for service in critical_services
            if health_data["services"][service]["status"] != "healthy"
        ]
        
        if unhealthy_critical:
            health_data["status"] = "unhealthy"
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=health_data
            )
        
        return health_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Detailed health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed"
        )