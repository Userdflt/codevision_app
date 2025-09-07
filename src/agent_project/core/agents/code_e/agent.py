"""
Code E specialist agent for lighting and electrical efficiency.
"""

from typing import Any, Dict

import structlog

from agent_project.core.agents.base import BaseAgent

logger = structlog.get_logger()


class CodeEAgent(BaseAgent):
    """
    Specialist agent for Code E - Lighting and electrical efficiency.

    Handles queries related to:
    - Lighting power density and controls
    - Daylighting and occupancy sensors
    - Emergency and exit lighting considerations
    - Electrical efficiency measures
    """

    def __init__(self):
        super().__init__("code_e")

    async def process_query(
        self, query: str, session_id: str, user_id: str, **kwargs
    ) -> Dict[str, Any]:
        """Process Code E related queries."""
        try:
            logger.info(
                "Processing Code E query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100],
            )

            # Retrieve relevant context from Code E sections
            context = await self.retrieve_context(
                query=query, clause_type="code_e", limit=5, similarity_threshold=0.8
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
            logger.error("Code E query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your lighting query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e),
            }

    def get_system_message(self) -> str:
        """Get Code E specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “E”).

Answer questions about the Code’s E Moisture provisions—Clause E1 Surface water (drainage and disposal of rainwater), Clause E2 External moisture (roofs, claddings, and openings must prevent water entry and accumulation), and Clause E3 Internal moisture (impervious surfaces, ventilation, thermal resistance, overflow disposal to avoid condensation and fungal growth).

Use only the information returned from the vectorstore.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/e-moisture"""
