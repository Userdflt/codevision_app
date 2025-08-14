"""
Code F specialist agent for plumbing and hydraulics.
"""

from typing import Dict, Any
import structlog

from agent_project.core.agents.base import BaseAgent


logger = structlog.get_logger()


class CodeFAgent(BaseAgent):
    """
    Specialist agent for Code F - Plumbing and hydraulics.
    
    Handles queries related to:
    - Water supply and pressure
    - Sanitary and stormwater drainage
    - Hot water systems and temperature control
    - Backflow prevention and cross-connection control
    """

    def __init__(self):
        super().__init__("code_f")

    async def process_query(
        self,
        query: str,
        session_id: str,
        user_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Process Code F related queries."""
        try:
            logger.info(
                "Processing Code F query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100]
            )

            # Retrieve relevant context from Code F sections
            context = await self.retrieve_context(
                query=query,
                clause_type="code_f",
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
            logger.error("Code F query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your plumbing query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e)
            }

    def get_system_message(self) -> str:
        """Get Code F specific system message."""
        return """You are a New Zealand Building Code expert (focusing on Building Code “F”).

Answer questions about the Code’s F Safety of Users provisions—Clauses F1 to F9 covering hazardous agents (F1), hazardous materials (F2), hazardous substances/processes (F3), safety from falling (F4), construction & demolition hazards (F5), visibility in escape routes (F6), warning systems (F7), safety signage (F8), and restricting young-children access to residential pools (F9).

Use only the information returned from the vectorstore.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vectorstore, reply “I don’t know.” Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/f-safety-of-users"""


