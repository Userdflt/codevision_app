"""
Code C specialist agent for energy efficiency and building envelope.
"""

from typing import Any, Dict

import structlog

from agent_project.core.agents.base import BaseAgent

logger = structlog.get_logger()


class CodeCAgent(BaseAgent):
    """
    Specialist agent for Code C - Energy efficiency and building envelope.

    Handles queries related to:
    - Thermal performance
    - Insulation and glazing
    - Air tightness and sealing
    - Building envelope requirements
    - Energy efficiency compliance
    """

    def __init__(self):
        super().__init__("code_c")

    async def process_query(
        self, query: str, session_id: str, user_id: str, **kwargs
    ) -> Dict[str, Any]:
        """Process Code C related queries."""
        try:
            logger.info(
                "Processing Code C query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100],
            )

            # Retrieve relevant context from Code C sections
            context = await self.retrieve_context(
                query=query, clause_type="code_c", limit=5, similarity_threshold=0.8
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
            logger.error("Code C query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your energy efficiency query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e),
            }

    def get_system_message(self) -> str:
        """Get Code C specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “C”).

Answer questions about the Code’s C Protection from Fire provisions—Clauses C1–C6, which cover: preventing fires (C2), limiting fire spread (C3), enabling safe evacuation (C4), providing firefighting access (C5), and maintaining structural stability during fire (C6), all in line with the objectives of C1.

Use only the information returned from the vectorstore.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/c-protection-from-fire"""
