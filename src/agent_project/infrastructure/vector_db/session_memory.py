"""
Ephemeral chat memory management for session-based conversations.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import asyncpg
import structlog

from agent_project.config import settings

logger = structlog.get_logger()


@dataclass
class ChatMessage:
    """Represents a single chat message in a session."""

    session_id: str
    message_id: str
    role: str  # 'user' or 'assistant'
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class SessionMemoryClient:
    """
    Client for managing ephemeral chat session memory.

    Messages are stored temporarily during active chat sessions
    and automatically deleted when sessions end or expire.
    """

    def __init__(self):
        self._connection_pool: Optional[asyncpg.Pool] = None

    async def _get_connection_pool(self) -> asyncpg.Pool:
        """Get or create the async connection pool."""
        if self._connection_pool is None:
            # Use the same database URL pattern as VectorDBClient
            db_url = (
                settings.database_url
                or f"{settings.supabase_url.replace('https://', 'postgresql://postgres:')}@db.{settings.supabase_url.split('//')[1]}/postgres"
            )

            self._connection_pool = await asyncpg.create_pool(
                db_url, min_size=1, max_size=5, command_timeout=30
            )

        return self._connection_pool

    async def initialize_tables(self) -> bool:
        """
        Create the session_messages table if it doesn't exist.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pool = await self._get_connection_pool()

            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS session_messages (
                        message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        session_id UUID NOT NULL,
                        user_id UUID,
                        role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
                        content TEXT NOT NULL,
                        metadata JSONB DEFAULT '{}',
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '24 hours')
                    );
                    
                    -- Index for efficient session lookups
                    CREATE INDEX IF NOT EXISTS idx_session_messages_session_id 
                    ON session_messages(session_id, created_at);
                    
                    -- Index for automatic cleanup
                    CREATE INDEX IF NOT EXISTS idx_session_messages_expires_at 
                    ON session_messages(expires_at);
                    
                    -- Row Level Security policies (if using Supabase)
                    ALTER TABLE session_messages ENABLE ROW LEVEL SECURITY;
                    
                    -- Policy: Users can only access their own session messages
                    DROP POLICY IF EXISTS "Users can access their own session messages" 
                    ON session_messages;
                    
                    CREATE POLICY "Users can access their own session messages" 
                    ON session_messages
                    FOR ALL
                    USING (auth.uid() = user_id);
                """
                )

                logger.info("Session messages table initialized successfully")
                return True

        except Exception as e:
            logger.error("Failed to initialize session messages table", error=str(e))
            return False

    async def create_session(self, user_id: Optional[str] = None) -> str:
        """
        Create a new chat session.

        Args:
            user_id: Optional user ID for RLS

        Returns:
            str: New session ID
        """
        session_id = str(uuid.uuid4())
        logger.info("Created new chat session", session_id=session_id, user_id=user_id)
        return session_id

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add a message to the session.

        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
            user_id: User ID for RLS
            metadata: Optional metadata

        Returns:
            str: Message ID
        """
        try:
            pool = await self._get_connection_pool()
            message_id = str(uuid.uuid4())

            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO session_messages 
                    (message_id, session_id, user_id, role, content, metadata)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """,
                    message_id,
                    session_id,
                    user_id,
                    role,
                    content,
                    metadata or {},
                )

                logger.debug(
                    "Added message to session",
                    session_id=session_id,
                    message_id=message_id,
                    role=role,
                )

                return message_id

        except Exception as e:
            logger.error(
                "Failed to add message to session", session_id=session_id, error=str(e)
            )
            raise

    async def get_session_messages(
        self, session_id: str, user_id: Optional[str] = None, limit: int = 50
    ) -> List[ChatMessage]:
        """
        Retrieve messages for a session.

        Args:
            session_id: Session identifier
            user_id: User ID for RLS
            limit: Maximum number of messages to retrieve

        Returns:
            List[ChatMessage]: List of messages in chronological order
        """
        try:
            pool = await self._get_connection_pool()

            async with pool.acquire() as conn:
                if user_id:
                    # With RLS - filter by user_id
                    rows = await conn.fetch(
                        """
                        SELECT message_id, session_id, role, content, metadata, created_at
                        FROM session_messages
                        WHERE session_id = $1 AND user_id = $2 AND expires_at > NOW()
                        ORDER BY created_at ASC
                        LIMIT $3
                    """,
                        session_id,
                        user_id,
                        limit,
                    )
                else:
                    # Without RLS - service role access
                    rows = await conn.fetch(
                        """
                        SELECT message_id, session_id, role, content, metadata, created_at
                        FROM session_messages
                        WHERE session_id = $1 AND expires_at > NOW()
                        ORDER BY created_at ASC
                        LIMIT $2
                    """,
                        session_id,
                        limit,
                    )

                messages = [
                    ChatMessage(
                        session_id=row["session_id"],
                        message_id=row["message_id"],
                        role=row["role"],
                        content=row["content"],
                        metadata=row["metadata"],
                        created_at=row["created_at"],
                    )
                    for row in rows
                ]

                logger.debug(
                    "Retrieved session messages",
                    session_id=session_id,
                    message_count=len(messages),
                )

                return messages

        except Exception as e:
            logger.error(
                "Failed to retrieve session messages",
                session_id=session_id,
                error=str(e),
            )
            raise

    async def end_session(self, session_id: str, user_id: Optional[str] = None) -> bool:
        """
        End a session and delete all its messages.

        Args:
            session_id: Session identifier
            user_id: User ID for RLS

        Returns:
            bool: True if successful
        """
        try:
            pool = await self._get_connection_pool()

            async with pool.acquire() as conn:
                if user_id:
                    # With RLS - filter by user_id
                    result = await conn.execute(
                        """
                        DELETE FROM session_messages
                        WHERE session_id = $1 AND user_id = $2
                    """,
                        session_id,
                        user_id,
                    )
                else:
                    # Without RLS - service role access
                    result = await conn.execute(
                        """
                        DELETE FROM session_messages
                        WHERE session_id = $1
                    """,
                        session_id,
                    )

                deleted_count = int(result.split()[-1])
                logger.info(
                    "Ended chat session",
                    session_id=session_id,
                    deleted_messages=deleted_count,
                )

                return True

        except Exception as e:
            logger.error("Failed to end session", session_id=session_id, error=str(e))
            return False

    async def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired session messages.

        Returns:
            int: Number of messages deleted
        """
        try:
            pool = await self._get_connection_pool()

            async with pool.acquire() as conn:
                result = await conn.execute(
                    """
                    DELETE FROM session_messages
                    WHERE expires_at <= NOW()
                """
                )

                deleted_count = int(result.split()[-1])
                logger.info(
                    "Cleaned up expired session messages", deleted_count=deleted_count
                )

                return deleted_count

        except Exception as e:
            logger.error("Failed to cleanup expired sessions", error=str(e))
            return 0

    async def close(self):
        """Close the connection pool."""
        if self._connection_pool:
            await self._connection_pool.close()
