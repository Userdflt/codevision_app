"""
Code B specialist agent for general building requirements.
"""

from typing import Dict, Any
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
        self,
        query: str,
        session_id: str,
        user_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Process Code B related queries."""
        try:
            logger.info(
                "Processing Code B query",
                session_id=session_id,
                user_id=user_id,
                query=query[:100]
            )
            
            # Retrieve relevant context from Code B sections
            context = await self.retrieve_context(
                query=query,
                clause_type="code_b",
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
            logger.error("Code B query processing failed", error=str(e))
            return {
                "response": "I encountered an error processing your building code query. Please try again.",
                "sources": [],
                "agent_type": self.agent_type,
                "error": str(e)
            }
    
    def get_system_message(self) -> str:
        """Get Code B specific system message."""
        return """You are a specialist in Code B - General Building Requirements from the National Construction Code of Australia.

Your expertise includes:
- Building classifications (Class 1-10 buildings)
- Fire safety and egress requirements
- Structural performance requirements
- Accessibility compliance
- Construction materials and methods
- General building compliance

When answering queries:
1. Always cite specific clause references where possible
2. Explain requirements clearly and practically
3. Note any variations based on building classification
4. Highlight safety considerations
5. Mention when professional consultation may be required

Provide accurate, code-compliant advice while noting that professional engineering or architectural consultation may be required for specific applications."""