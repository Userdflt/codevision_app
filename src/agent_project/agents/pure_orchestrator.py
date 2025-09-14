"""
Pure SDK orchestrator - no adapters, direct SDK usage.
Replaces AgentController with 100% native OpenAI Agents SDK implementation.
"""

from typing import Dict, Any, Optional
from agents import Runner
import structlog

from .pure_sdk import get_pure_sdk_specialists, get_pure_sdk_triage

logger = structlog.get_logger()

class PureSDKOrchestrator:
    """
    Pure OpenAI Agents SDK orchestrator.
    
    Completely replaces AgentController and all adapter layers.
    Uses native SDK agents with handoffs and guardrails.
    """
    
    def __init__(self):
        self.specialists = get_pure_sdk_specialists()
        self.triage_agent = get_pure_sdk_triage()
        logger.info(
            "Initialized pure SDK orchestrator",
            specialist_count=len(self.specialists),
            triage_enabled=self.triage_agent is not None
        )
    
    async def process_query(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process query using pure SDK with native handoffs and guardrails.
        
        Args:
            query: User's building code query
            context: Additional context (session_id, user_id, etc.)
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            logger.info(
                "Processing query with pure SDK",
                query_length=len(query),
                has_context=context is not None,
                context_keys=list((context or {}).keys())
            )
            
            # Use SDK's native orchestration with guardrails and handoffs
            result = await Runner.run(
                self.triage_agent,
                query,
                context=context or {}
            )
            
            # Extract result data
            final_output = result.final_output if hasattr(result, 'final_output') else str(result)
            last_agent_name = (
                result.last_agent.name 
                if hasattr(result, 'last_agent') and result.last_agent 
                else self.triage_agent.name
            )
            
            # Check for trace information
            trace_id = getattr(result, 'trace_id', None)
            
            logger.info(
                "Pure SDK query completed",
                last_agent=last_agent_name,
                response_length=len(final_output),
                trace_id=trace_id
            )
            
            return {
                "final_output": final_output,
                "last_agent": last_agent_name,
                "routing_method": "pure_sdk_handoffs",
                "context": context or {},
                "trace_id": trace_id,
                "orchestrator_type": "pure_sdk",
                "success": True
            }
            
        except Exception as e:
            logger.error(
                "Pure SDK orchestration failed", 
                error=str(e), 
                query=query[:100],
                error_type=type(e).__name__
            )
            return {
                "final_output": "I encountered an error processing your building code query. Please try again.",
                "last_agent": "error_handler",
                "routing_method": "pure_sdk_error",
                "error": str(e),
                "error_type": type(e).__name__,
                "context": context or {},
                "orchestrator_type": "pure_sdk",
                "success": False
            }
    
    async def get_specialist_directly(
        self, 
        agent_type: str, 
        query: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Direct access to specialist agent (bypassing triage).
        
        Args:
            agent_type: Type of specialist ('code_b', 'code_c', etc.)
            query: User's query
            context: Additional context
            
        Returns:
            Dictionary with response and metadata
        """
        if agent_type not in self.specialists:
            available_types = list(self.specialists.keys())
            raise ValueError(f"Unknown agent type: {agent_type}. Available: {available_types}")
        
        try:
            logger.info(
                "Running specialist directly",
                agent_type=agent_type,
                query_length=len(query)
            )
            
            specialist = self.specialists[agent_type]
            result = await Runner.run(specialist, query, context=context or {})
            
            # Extract result data
            final_output = result.final_output if hasattr(result, 'final_output') else str(result)
            last_agent_name = (
                result.last_agent.name 
                if hasattr(result, 'last_agent') and result.last_agent 
                else specialist.name
            )
            
            logger.info(
                "Direct specialist completed",
                agent_type=agent_type,
                actual_agent=last_agent_name,
                response_length=len(final_output)
            )
            
            return {
                "final_output": final_output,
                "last_agent": last_agent_name,
                "routing_method": "direct_specialist",
                "specialist_type": agent_type,
                "context": context or {},
                "orchestrator_type": "pure_sdk",
                "success": True
            }
            
        except Exception as e:
            logger.error(
                "Direct specialist access failed", 
                agent_type=agent_type, 
                error=str(e),
                error_type=type(e).__name__
            )
            return {
                "final_output": f"I encountered an error processing your {agent_type} query. Please try again.",
                "last_agent": agent_type,
                "routing_method": "direct_specialist_error",
                "error": str(e),
                "error_type": type(e).__name__,
                "specialist_type": agent_type,
                "context": context or {},
                "orchestrator_type": "pure_sdk",
                "success": False
            }
    
    async def stream_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Stream query processing (placeholder for future streaming support).
        
        Currently processes normally and returns the full result.
        Can be enhanced when SDK supports streaming.
        """
        logger.info("Stream query requested (using normal processing for now)")
        
        # For now, use normal processing
        # TODO: Implement true streaming when SDK supports it
        result = await self.process_query(query, context)
        result["streaming_requested"] = True
        result["streaming_available"] = False
        
        return result
    
    def get_available_specialists(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available specialists."""
        from .specifications import get_agent_spec
        
        specialists_info = {}
        for agent_type, agent in self.specialists.items():
            spec = get_agent_spec(agent_type)
            specialists_info[agent_type] = {
                "name": agent.name,
                "expertise": spec.get('expertise', []),
                "handoff_triggers": spec.get('handoff_triggers', []),
                "tools_count": len(agent.tools) if hasattr(agent, 'tools') else 0,
                "handoffs_count": len(agent.handoffs) if hasattr(agent, 'handoffs') and agent.handoffs else 0,
                "guardrails_enabled": {
                    "input": len(agent.input_guardrails) if hasattr(agent, 'input_guardrails') else 0,
                    "output": len(agent.output_guardrails) if hasattr(agent, 'output_guardrails') else 0
                }
            }
        
        return specialists_info
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get status information about the orchestrator."""
        return {
            "orchestrator_type": "pure_sdk",
            "sdk_native": True,
            "specialists_loaded": len(self.specialists),
            "triage_available": self.triage_agent is not None,
            "legacy_components": 0,
            "adapters_used": 0,
            "performance_optimized": True,
            "handoffs_enabled": True,
            "guardrails_enabled": True,
            "tools_enabled": True
        }

# Convenience function for quick access
async def run_pure_sdk_query(query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Quick function to run a query with the pure SDK orchestrator.
    
    Args:
        query: User's query
        context: Optional context
        
    Returns:
        Result dictionary
    """
    orchestrator = PureSDKOrchestrator()
    return await orchestrator.process_query(query, context)

# Metadata
PURE_ORCHESTRATOR_METADATA = {
    'replacement_for': ['AgentController', 'AdvancedOrchestrator'],
    'sdk_native': True,
    'supports_streaming': False,  # Future enhancement
    'supports_direct_access': True,
    'supports_triage': True,
    'error_handling': 'comprehensive',
    'logging_enabled': True,
    'performance_optimized': True,
}
