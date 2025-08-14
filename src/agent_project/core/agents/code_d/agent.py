"""
Code D specialist agent for mechanical systems and ventilation.
"""

from typing import Dict, Any
import structlog

from agent_project.core.agents.base import BaseAgent


logger = structlog.get_logger()


class CodeDAgent(BaseAgent):
    """
    Specialist agent for Code D - Mechanical systems and ventilation.
    
    Handles queries related to:
    - HVAC performance and design
    - Ventilation and indoor air quality
    - Smoke control and pressurisation
    - Exhaust systems and ducting
    - Commissioning and maintenance requirements
    """

    def __init__(self):
        super().__init__("code_d")

    async def process_query(
        self,
        query: str,
        session_id: str,
        user_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Process Code D related queries."""
        try:
            logger.info(
                "Processing Code D query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100]
            )

            # Retrieve relevant context from Code D sections
            context = await self.retrieve_context(
                query=query,
                clause_type="code_d",
                limit=5,
                similarity_threshold=0.8
            )

            # Generate specialized response
            system_message = self.get_system_message()
            response = await self.generate_response(
                prompt=query,
                context=context,
                system_message=system_message
            )

            return {
                "response": response,
                "sources": context,
                "agent_type": self.agent_type
            }

        except Exception as e:
            logger.error("Code D query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your mechanical systems query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e)
            }

    def get_system_message(self) -> str:
        """Get Code D specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “D”).

Answer questions about the Code’s D Access provisions—Clause D1 Access routes (safe entry, internal/external stairs, ramps, corridors, lifts; slip resistance; facilities for people with disabilities; vehicle movement, loading, parking) and Clause D2 Mechanical installations for access (lifts, escalators, moving walks must resist service loads, prevent accidents, and safeguard users and maintenance staff).

your goal is to provide an accurate answer based on this information ONLY.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/d-access"""


