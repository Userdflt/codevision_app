"""
Code B specialist agent for general building requirements.
"""

from typing import Any, Dict

import structlog

from agent_project.core.agents.base import BaseAgent

logger = structlog.get_logger()


class CodeBAgent(BaseAgent):
    """
    Specialist agent for Code B - General Building Requirements.

    Handles queries related to:
    - Building classifications
    - Fire safety requirements
    - Structural requirements
    - General compliance
    """

    def __init__(self):
        super().__init__("code_b")

    async def process_query(
        self, query: str, session_id: str, user_id: str, **kwargs
    ) -> Dict[str, Any]:
        """Process Code B related queries."""
        try:
            logger.info(
                "Processing Code B query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100],
            )

            # Retrieve relevant context from Code B sections
            context = await self.retrieve_context(
                query=query, clause_type="code_b", limit=5, similarity_threshold=0.8
            )

            # Generate specialized response
            system_message = self.get_system_message()
            response = await self.generate_response(
                prompt=query, context=context, system_message=system_message
            )

            return {
                "response": response,
                "sources": context,
                "agent_type": self.agent_type,
            }

        except Exception as e:
            logger.error("Code B query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your building code query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e),
            }

    def get_system_message(self) -> str:
        """Get Code B specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “B”).

Answer questions about the Code’s B Stability provisions—Clause B1 Structure (buildings, elements, and site-works must resist self-weight, temperature, water, earthquake, snow, wind, and fire loads during construction, alteration, and service life) and Clause B2 Durability (materials must remain functional for at least 50, 15, or 5 years so the building continues to meet performance requirements and protect people and property).

Use only the information returned from the vectorstore.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/b-stability"""
