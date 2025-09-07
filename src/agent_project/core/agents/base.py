"""
Base agent class for all AI agents in the system.
"""

import inspect
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict

import structlog

from agent_project.infrastructure.llm.client import LLMClient

logger = structlog.get_logger()


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.

    Provides common functionality like LLM access, vector search,
    and standardized interfaces for query processing.
    """

    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.llm_client = LLMClient()
        # Lazily initialize vector client to avoid optional dependency import at import-time
        self.vector_client = None
        logger.info("Initialized agent", agent_type=agent_type)

    @abstractmethod
    async def process_query(
        self, query: str, session_id: str, user_id: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Process a user query and return a response.

        Args:
            query: The user's question or request
            session_id: Unique session identifier
            user_id: User identifier
            **kwargs: Additional parameters specific to the agent

        Returns:
            Dictionary containing response, sources, and metadata
        """
        pass

    async def stream_query(
        self, query: str, session_id: str, user_id: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream query processing for real-time responses.

        Default implementation yields the full response at once.
        Subclasses can override for true streaming.
        """
        result = await self.process_query(query, session_id, user_id, **kwargs)
        yield result["response"]

    async def retrieve_context(
        self,
        query: str,
        clause_type: str | None = None,
        limit: int = 5,
        similarity_threshold: float = 0.8,
    ) -> list[Dict[str, Any]]:
        """
        Retrieve relevant context from the vector database.

        Args:
            query: Search query
            clause_type: Optional clause type filter
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score

        Returns:
            List of relevant documents with metadata
        """
        try:
            # Lazy import and initialize the vector DB client if not provided/mocked
            if self.vector_client is None:
                try:
                    from agent_project.infrastructure.vector_db.client import (
                        VectorDBClient,  # type: ignore
                    )

                    self.vector_client = VectorDBClient()
                except Exception as e:
                    logger.error(
                        "Failed to initialize vector client",
                        agent_type=self.agent_type,
                        error=str(e),
                    )
                    return []
            # Default clause type to this agent's type if not provided
            effective_clause_type = clause_type or self.agent_type

            call_result = self.vector_client.similarity_search(
                query=query,
                clause_type=effective_clause_type,
                limit=limit,
                similarity_threshold=similarity_threshold,
            )

            results = (
                await call_result if inspect.isawaitable(call_result) else call_result
            )

            logger.debug(
                "Retrieved context",
                agent_type=self.agent_type,
                results_count=len(results),
                query=query[:100],
            )

            return results

        except Exception as e:
            logger.error(
                "Context retrieval failed", agent_type=self.agent_type, error=str(e)
            )
            return []

    async def generate_response(
        self,
        prompt: str,
        context: list[Dict[str, Any]] | None = None,
        system_message: str | None = None,
        **llm_kwargs,
    ) -> str:
        """
        Generate a response using the LLM.

        Args:
            prompt: User prompt or question
            context: Retrieved context documents
            system_message: System message for the LLM
            **llm_kwargs: Additional LLM parameters

        Returns:
            Generated response text
        """
        try:
            # Build context string if provided
            context_str = ""
            if context:
                context_str = "\n\n".join(
                    [
                        f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}\n"
                        f"Content: {doc.get('content', '')}"
                        for doc in context
                    ]
                )

            # Create full prompt with context
            full_prompt = prompt
            if context_str:
                full_prompt = (
                    f"Context:\n{context_str}\n\nQuestion: {prompt}\n\nAnswer:"
                )

            response = await self.llm_client.generate(
                prompt=full_prompt, system_message=system_message, **llm_kwargs
            )

            logger.debug(
                "Generated response",
                agent_type=self.agent_type,
                response_length=len(response),
            )

            return response

        except Exception as e:
            logger.error(
                "Response generation failed", agent_type=self.agent_type, error=str(e)
            )
            return "I encountered an error generating a response. Please try again."

    def get_system_message(self) -> str:
        """
        Get the system message for this agent type.
        Subclasses should override to provide agent-specific instructions.
        """
        return (
            f"You are a helpful AI assistant specializing in {self.agent_type} queries."
        )
