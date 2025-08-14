"""
Code H specialist agent for accessibility and egress.
"""

from typing import Dict, Any
import structlog

from agent_project.core.agents.base import BaseAgent


logger = structlog.get_logger()


class CodeHAgent(BaseAgent):
    """
    Specialist agent for Code H - Accessibility and egress.
    
    Handles queries related to:
    - Accessible design and AS 1428 series references
    - Egress width, travel distance, and exits
    - Lifts, ramps, stairs, and handrails
    - Amenities, signage, and tactile indicators
    """

    def __init__(self):
        super().__init__("code_h")

    async def process_query(
        self,
        query: str,
        session_id: str,
        user_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Process Code H related queries."""
        try:
            logger.info(
                "Processing Code H query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100]
            )

            # Retrieve relevant context from Code H sections
            context = await self.retrieve_context(
                query=query,
                clause_type="code_h",
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
            logger.error("Code H query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your accessibility query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e)
            }

    def get_system_message(self) -> str:
        """Get Code H specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “H”).

Answer questions about the Code’s H1 Energy efficiency provisions—thermal-resistance requirements, control of uncontrolled airflow, and performance criteria for hot-water systems, artificial lighting, and HVAC in conditioned spaces.

Use only the information returned from the vectorstore.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/h-energy-efficiency"""


