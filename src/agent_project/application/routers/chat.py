"""
Chat API endpoints for interacting with AI agents.
"""

from typing import Dict, Any
from uuid import uuid4

import structlog
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agent_project.core.agents.orchestrator.agent import OrchestratorAgent
from agent_project.infrastructure.auth.dependencies import get_current_user


logger = structlog.get_logger()
router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""
    content: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    sources: list[Dict[str, Any]] = []
    agent_used: str | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    message: ChatMessage,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> ChatResponse:
    """
    Main chat endpoint for processing user queries.
    
    Routes queries through the orchestrator agent to appropriate specialists.
    """
    try:
        # Generate session ID if not provided
        session_id = message.session_id or str(uuid4())
        
        logger.info(
            "Processing chat message",
            user_id=current_user.get("sub"),
            session_id=session_id,
            content_length=len(message.content)
        )
        
        # Initialize orchestrator agent
        orchestrator = OrchestratorAgent()
        
        # Process the message
        result = await orchestrator.process_query(
            query=message.content,
            session_id=session_id,
            user_id=current_user.get("sub")
        )
        
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            sources=result.get("sources", []),
            agent_used=result.get("agent_used")
        )
        
    except Exception as e:
        logger.error("Error processing chat message", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message"
        )


@router.post("/chat/stream")
async def chat_stream_endpoint(
    message: ChatMessage,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> StreamingResponse:
    """
    Streaming chat endpoint for real-time responses.
    """
    try:
        session_id = message.session_id or str(uuid4())
        
        logger.info(
            "Starting streaming chat",
            user_id=current_user.get("sub"),
            session_id=session_id
        )
        
        orchestrator = OrchestratorAgent()
        
        async def generate_response():
            async for chunk in orchestrator.stream_query(
                query=message.content,
                session_id=session_id,
                user_id=current_user.get("sub")
            ):
                yield f"data: {chunk}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"}
        )
        
    except Exception as e:
        logger.error("Error in streaming chat", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start streaming chat"
        )


@router.delete("/chat/session/{session_id}")
async def end_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, str]:
    """
    End a chat session and clean up ephemeral memory.
    """
    try:
        logger.info(
            "Ending chat session",
            user_id=current_user.get("sub"),
            session_id=session_id
        )
        
        # TODO: Implement session cleanup
        # This would delete ephemeral chat messages from the database
        
        return {"message": "Session ended successfully", "session_id": session_id}
        
    except Exception as e:
        logger.error("Error ending session", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to end session"
        )