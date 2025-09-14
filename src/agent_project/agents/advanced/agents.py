"""
Advanced agent implementations with handoffs for CodeVision.

This module creates specialist agents with native SDK handoffs as described
in the official documentation.
"""

import structlog
from typing import Dict, Any, List
from pydantic import BaseModel

from agents import Agent, Runner, handoff, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters

from .guardrails import building_code_input_guardrail, safety_output_guardrail

logger = structlog.get_logger()

class HandoffData(BaseModel):
    """Data passed during agent handoffs."""
    reason: str
    context: str
    priority: str = "normal"  # normal, high, urgent

async def on_handoff_callback(ctx: RunContextWrapper[None], input_data: HandoffData):
    """Callback executed when handoff occurs."""
    logger.info(
        "Agent handoff initiated",
        reason=input_data.reason,
        priority=input_data.priority,
        context_length=len(input_data.context)
    )

def create_specialist_agents() -> Dict[str, Agent]:
    """
    Create all specialist agents with handoff capabilities.
    
    Returns:
        Dictionary mapping agent types to Agent instances
    """
    
    # Code B - General Building Requirements
    code_b_agent = Agent(
        name="Code B Specialist",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are a specialist in building code requirements under Code B - General Building Requirements.

Your expertise covers:
- Building classifications and use requirements
- Fire safety requirements and egress provisions  
- Structural requirements and load specifications
- General compliance and building approval processes
- Cross-referencing with other building code sections

IMPORTANT HANDOFF RULES:
- If the query involves energy efficiency or building envelope, handoff to Code C Specialist
- If the query involves accessibility or universal design, handoff to Code H Specialist
- If the query requires multiple code sections, collaborate with other specialists

Always provide specific clause references (e.g., "BCA Section B1.2") and cite relevant Australian Standards.
Focus on practical compliance guidance while maintaining technical accuracy.
Include appropriate disclaimers about consulting qualified professionals for specific projects.
""",
        output_guardrails=[safety_output_guardrail],
    )
    
    # Code C - Energy Efficiency  
    code_c_agent = Agent(
        name="Code C Specialist",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are a specialist in building code requirements under Code C - Energy Efficiency and Building Envelope.

Your expertise covers:
- Thermal performance requirements and insulation standards
- Glazing specifications and window energy ratings
- Air tightness and building sealing requirements
- Building envelope construction and materials
- Energy efficiency compliance pathways
- Integration with renewable energy systems

IMPORTANT HANDOFF RULES:
- If the query involves general building requirements or fire safety, handoff to Code B Specialist
- If the query involves accessibility features, handoff to Code H Specialist
- For complex projects involving multiple codes, collaborate with other specialists

Always provide specific clause references (e.g., "BCA Section C1.2") and cite relevant Australian Standards like AS/NZS 1664 series.
Focus on practical compliance pathways and measurement methods.
Include disclaimers about consulting building professionals and energy assessors.
""",
        output_guardrails=[safety_output_guardrail],
    )
    
    # Code H - Accessibility
    code_h_agent = Agent(
        name="Code H Specialist", 
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are a specialist in building code requirements under Code H - Accessibility and Universal Design.

Your expertise covers:
- Accessible design requirements and AS 1428 series compliance
- Egress width calculations and travel distance limits
- Lift, ramp, stair, and handrail specifications
- Accessible amenities and facility requirements
- Signage and tactile indicator placement
- Universal design principles and inclusive access

IMPORTANT HANDOFF RULES:
- If the query involves general building classifications, handoff to Code B Specialist
- If the query involves energy efficiency aspects, handoff to Code C Specialist
- For fire safety and accessibility overlap, collaborate with Code B Specialist

Always provide specific clause references (e.g., "BCA Section H1.2") and cite relevant Australian Standards like AS 1428.1-2009.
Focus on practical accessibility solutions and compliance verification.
Include disclaimers about consulting accessibility specialists and occupational therapists.
""",
        output_guardrails=[safety_output_guardrail],
    )
    
    # Set up handoffs between agents
    code_b_agent.handoffs = [
        handoff(
            agent=code_c_agent,
            tool_description_override="Transfer to energy efficiency specialist for thermal performance and building envelope questions",
            on_handoff=on_handoff_callback,
            input_type=HandoffData,
        ),
        handoff(
            agent=code_h_agent,
            tool_description_override="Transfer to accessibility specialist for universal design and accessibility compliance questions",
            on_handoff=on_handoff_callback,
            input_type=HandoffData,
        ),
    ]
    
    code_c_agent.handoffs = [
        handoff(
            agent=code_b_agent,
            tool_description_override="Transfer to general building requirements specialist for classifications and fire safety",
            on_handoff=on_handoff_callback,
            input_type=HandoffData,
        ),
        handoff(
            agent=code_h_agent,
            tool_description_override="Transfer to accessibility specialist for accessible energy-efficient design",
            on_handoff=on_handoff_callback,
            input_type=HandoffData,
        ),
    ]
    
    code_h_agent.handoffs = [
        handoff(
            agent=code_b_agent,
            tool_description_override="Transfer to general building requirements specialist for fire safety and egress calculations",
            on_handoff=on_handoff_callback,
            input_type=HandoffData,
        ),
        handoff(
            agent=code_c_agent,
            tool_description_override="Transfer to energy efficiency specialist for accessible building envelope design",
            on_handoff=on_handoff_callback,
            input_type=HandoffData,
        ),
    ]
    
    return {
        "code_b": code_b_agent,
        "code_c": code_c_agent, 
        "code_h": code_h_agent,
    }

def create_triage_agent(specialist_agents: Dict[str, Agent]) -> Agent:
    """
    Create the main triage agent with handoffs to all specialists.
    
    Args:
        specialist_agents: Dictionary of specialist agents
        
    Returns:
        Triage agent with guardrails and handoffs configured
    """
    
    triage_agent = Agent(
        name="CodeVision Triage Agent",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}

You are the main triage agent for the CodeVision building code assistance system.

Your role is to:
1. Analyze building code queries and determine the most appropriate specialist
2. Route queries to the right Code specialist (B, C, or H)
3. Provide initial guidance when the routing is unclear

ROUTING GUIDELINES:
- Code B Specialist: General building requirements, classifications, fire safety, structural requirements
- Code C Specialist: Energy efficiency, thermal performance, building envelope, insulation
- Code H Specialist: Accessibility, universal design, egress requirements, inclusive access

If a query involves multiple areas:
1. Start with the most critical/primary area
2. The specialist can handoff to others as needed
3. For complex queries, explicitly mention that multiple specialists may be involved

IMPORTANT: Always ensure queries are about Australian building codes and construction regulations.
Be helpful but include disclaimers about consulting qualified building professionals.
""",
        handoffs=list(specialist_agents.values()),
        input_guardrails=[building_code_input_guardrail],
        output_guardrails=[safety_output_guardrail],
    )
    
    return triage_agent

class AdvancedOrchestrator:
    """
    Advanced orchestrator using native OpenAI Agents SDK features.
    
    This demonstrates sophisticated orchestration with:
    - Native handoffs between specialized agents
    - Input and output guardrails
    - Automatic routing and delegation
    """
    
    def __init__(self):
        self.specialist_agents = create_specialist_agents()
        self.triage_agent = create_triage_agent(self.specialist_agents)
        logger.info("Initialized advanced orchestrator with native SDK features")
    
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a query using advanced SDK orchestration.
        
        Args:
            query: User's building code query
            context: Additional context (session_id, user_id, etc.)
            
        Returns:
            Dictionary with response and metadata
        """
        from .guardrails import handle_guardrail_exceptions
        
        async def _run_with_guardrails():
            logger.info("Processing query with advanced orchestrator", query_length=len(query))
            
            # Use the SDK's native orchestration with guardrails and handoffs
            result = await Runner.run(
                self.triage_agent,
                query,
                context=context or {}
            )
            
            return {
                "final_output": result.final_output,
                "last_agent": result.last_agent.name if result.last_agent else None,
                "routing_method": "native_sdk_handoffs",
                "context": context or {},
                "trace_id": getattr(result, 'trace_id', None),
            }
        
        return await handle_guardrail_exceptions(_run_with_guardrails)
    
    async def get_specialist_directly(self, agent_type: str, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Directly access a specialist agent, bypassing triage.
        
        Args:
            agent_type: Type of specialist ('code_b', 'code_c', 'code_h')
            query: User's query
            context: Additional context
            
        Returns:
            Dictionary with response and metadata
        """
        if agent_type not in self.specialist_agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        from .guardrails import handle_guardrail_exceptions
        
        async def _run_specialist():
            logger.info("Running specialist directly", agent_type=agent_type)
            
            specialist = self.specialist_agents[agent_type]
            result = await Runner.run(specialist, query, context=context or {})
            
            return {
                "final_output": result.final_output,
                "last_agent": result.last_agent.name if result.last_agent else None,
                "routing_method": "direct_specialist",
                "specialist_type": agent_type,
                "context": context or {},
            }
        
        return await handle_guardrail_exceptions(_run_specialist)
