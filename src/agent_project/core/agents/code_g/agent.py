"""
Code G specialist agent for electrical systems.
"""

from typing import Dict, Any
import structlog

from agent_project.core.agents.base import BaseAgent


logger = structlog.get_logger()


class CodeGAgent(BaseAgent):
    """
    Specialist agent for Code G - Electrical systems.
    
    Handles queries related to:
    - Electrical distribution and protection
    - Wiring methods and safety
    - Coordination with emergency and exit systems
    - Power quality and reliability considerations
    """

    def __init__(self):
        super().__init__("code_g")

    async def process_query(
        self,
        query: str,
        session_id: str,
        user_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Process Code G related queries."""
        try:
            logger.info(
                "Processing Code G query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100]
            )

            # Retrieve relevant context from Code G sections
            context = await self.retrieve_context(
                query=query,
                clause_type="code_g",
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
            logger.error("Code G query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your electrical systems query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e)
            }

    def get_system_message(self) -> str:
        """Get Code G specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “G”).

Answer questions about the Code’s G Services and Facilities provisions—Clauses G1-G15 addressing personal hygiene, laundering, food preparation, ventilation, interior environment, sound control, natural and artificial light, electricity, piped services, gas, water supply, foul water, industrial liquid waste, and solid-waste management.

Use only the information returned from the vectorstore.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/g-services-and-facilities"""


