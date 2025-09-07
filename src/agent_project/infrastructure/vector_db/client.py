"""
Supabase pgvector client for semantic search operations.
"""

from typing import Any, Dict, List, Optional

import asyncpg
import structlog
from supabase import Client, create_client

from agent_project.config import settings

logger = structlog.get_logger()


class VectorDBClient:
    """
    Client for interacting with Supabase pgvector database.

    Provides methods for semantic search, database health checks,
    and metadata retrieval.
    """

    def __init__(self):
        self.supabase: Client = create_client(
            settings.supabase_url, settings.supabase_anon_key
        )
        self._connection_pool: Optional[asyncpg.Pool] = None

    async def _get_connection_pool(self) -> asyncpg.Pool:
        """Get or create the async connection pool."""
        if self._connection_pool is None:
            # Parse database URL from Supabase URL
            db_url = (
                settings.database_url
                or f"{settings.supabase_url.replace('https://', 'postgresql://postgres:')}@db.{settings.supabase_url.split('//')[1]}/postgres"
            )

            self._connection_pool = await asyncpg.create_pool(
                db_url, min_size=1, max_size=5, command_timeout=30
            )

        return self._connection_pool

    async def similarity_search(
        self,
        query: str,
        clause_type: Optional[str] = None,
        limit: int = 10,
        similarity_threshold: float = 0.8,
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity search on clause embeddings.

        Args:
            query: Search query text
            clause_type: Optional filter by clause type (e.g., 'code_b', 'code_c')
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of matching documents with similarity scores
        """
        try:
            logger.info(
                "Performing vector similarity search",
                query=query[:100],
                clause_type=clause_type,
                limit=limit,
                threshold=similarity_threshold,
            )

            # Use Supabase client for now, can be optimized with direct SQL later
            query_params = {
                "query_text": query,
                "match_threshold": similarity_threshold,
                "match_count": limit,
            }

            if clause_type:
                query_params["clause_type"] = clause_type

            # Call stored procedure or use RPC
            # This assumes a stored procedure exists for vector search
            response = self.supabase.rpc("match_documents", query_params).execute()

            results = response.data or []

            logger.info(
                "Vector search completed", results_count=len(results), query=query[:100]
            )

            return [
                {
                    "content": result.get("content", ""),
                    "similarity_score": result.get("similarity", 0.0),
                    "metadata": {
                        "source": result.get("source", ""),
                        "clause_type": result.get("clause_type", ""),
                        "section": result.get("section", ""),
                        "page_number": result.get("page_number"),
                        "document_id": result.get("document_id"),
                    },
                }
                for result in results
            ]

        except Exception as e:
            logger.error("Vector similarity search failed", error=str(e))
            return []

    async def health_check(self) -> bool:
        """
        Check if the vector database is accessible and healthy.

        Returns:
            True if database is healthy, False otherwise
        """
        try:
            # Simple query to check connectivity
            response = (
                self.supabase.from_("clause_embeddings").select("id").limit(1).execute()
            )
            return response.data is not None

        except Exception as e:
            logger.warning("Vector DB health check failed", error=str(e))
            return False

    async def get_database_info(self) -> Dict[str, Any]:
        """
        Get database information and statistics.

        Returns:
            Dictionary with database metadata
        """
        try:
            # Get table statistics
            stats_response = self.supabase.rpc("get_table_stats").execute()

            return {
                "status": "connected",
                "statistics": stats_response.data if stats_response.data else {},
                "connection_info": {"url": settings.supabase_url, "pool_size": "1-5"},
            }

        except Exception as e:
            logger.error("Failed to get database info", error=str(e))
            return {"status": "error", "error": str(e)}

    async def get_database_stats(self) -> Dict[str, Any]:
        """
        Get detailed database statistics for admin endpoints.

        Returns:
            Dictionary with detailed statistics
        """
        try:
            pool = await self._get_connection_pool()

            async with pool.acquire() as conn:
                # Get table row counts
                clause_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM clause_embeddings"
                )

                # Get storage statistics
                storage_stats = await conn.fetch(
                    """
                    SELECT 
                        schemaname,
                        tablename,
                        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                    FROM pg_tables 
                    WHERE tablename LIKE '%embedding%' OR tablename LIKE '%clause%'
                """
                )

                return {
                    "total_clauses": clause_count,
                    "storage_info": [dict(row) for row in storage_stats],
                    "vector_dimensions": 1536,  # Assuming OpenAI embeddings
                    "similarity_function": "cosine",
                }

        except Exception as e:
            logger.error("Failed to get database stats", error=str(e))
            return {"error": str(e)}

    async def close(self):
        """Close database connections."""
        if self._connection_pool:
            await self._connection_pool.close()
            self._connection_pool = None
