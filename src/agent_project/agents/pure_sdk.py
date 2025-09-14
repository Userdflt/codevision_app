"""
Pure OpenAI Agents SDK specialist agents.
No adapters, no legacy code - 100% native SDK implementation.
"""

from typing import Dict, List, Any
from agents import Agent, Runner, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import structlog

from .specifications import AGENT_SPECIFICATIONS, get_agent_spec, get_all_agent_types
from .tools import get_tools_for_agent
from .advanced.guardrails import building_code_input_guardrail, safety_output_guardrail

logger = structlog.get_logger()

class HandoffData:
    """Data structure for handoffs."""
    def __init__(self, reason: str, context: str, priority: str = "normal"):
        self.reason = reason
        self.context = context
        self.priority = priority

async def on_handoff_callback(ctx, input_data: HandoffData):
    """Callback executed when handoff occurs."""
    logger.info(
        "Pure SDK agent handoff",
        reason=input_data.reason,
        priority=input_data.priority,
        context_length=len(input_data.context)
    )

def create_pure_sdk_specialists() -> Dict[str, Agent]:
    """
    Create all specialist agents using pure OpenAI Agents SDK.
    
    This completely replaces the legacy BaseAgent + wrapper architecture.
    """
    specialists = {}
    
    # Create all agents first (needed for handoff setup)
    for agent_type in get_all_agent_types():
        spec = get_agent_spec(agent_type)
        tools = get_tools_for_agent(agent_type)
        
        # Create enhanced system message with handoff instructions
        enhanced_instructions = f"""{RECOMMENDED_PROMPT_PREFIX}

{spec['system_message']}

## HANDOFF GUIDELINES

You can transfer queries to other specialists when appropriate:
"""
        
        # Add specific handoff descriptions for each agent
        for other_type in get_all_agent_types():
            if other_type != agent_type:
                other_spec = get_agent_spec(other_type)
                enhanced_instructions += f"- **{other_spec['name']}**: {', '.join(other_spec['expertise'][:2])}\n"
        
        enhanced_instructions += f"""
Use handoffs when queries involve topics outside your expertise:
{chr(10).join([f"- {trigger}" for trigger in spec.get('handoff_triggers', [])])}

## TOOL USAGE

You have access to building code search tools:
- Use `vector_search_tool` for specific code sections
- Use `get_building_code_context` for comprehensive research
- Use `check_building_code_compliance` for compliance verification
- Use `analyze_building_requirements` for building analysis
- Use `get_code_interpretation` for regulation interpretation

Always cite specific building code clauses and provide disclaimers about consulting professionals.

## RESPONSE FORMAT

Provide clear, structured responses with:
1. Direct answer to the query
2. Relevant building code references
3. Source citations
4. Professional disclaimer when appropriate
"""
        
        # Create the pure SDK agent
        agent = Agent(
            name=spec['name'],
            instructions=enhanced_instructions,
            tools=tools,
            input_guardrails=[building_code_input_guardrail],
            output_guardrails=[safety_output_guardrail],
            model="gpt-4-turbo-preview"  # Can be configured
        )
        
        specialists[agent_type] = agent
        logger.info(f"Created pure SDK agent: {spec['name']}")
    
    # Set up handoffs after all agents exist
    _setup_handoffs(specialists)
    
    return specialists

def _setup_handoffs(specialists: Dict[str, Agent]) -> None:
    """Set up handoffs between specialist agents based on specifications."""
    
    for agent_type, agent in specialists.items():
        spec = get_agent_spec(agent_type)
        handoff_targets = []
        
        # Determine handoff targets based on triggers and expertise overlap
        for trigger in spec.get('handoff_triggers', []):
            for other_type, other_agent in specialists.items():
                if other_type == agent_type:
                    continue
                    
                other_spec = get_agent_spec(other_type)
                other_expertise = [area.lower() for area in other_spec.get('expertise', [])]
                
                # Check if trigger matches other agent's expertise
                if any(trigger.lower() in expertise for expertise in other_expertise):
                    if other_agent not in handoff_targets:
                        handoff_targets.append(other_agent)
        
        # Set up handoffs
        if handoff_targets:
            agent.handoffs = []
            for target_agent in handoff_targets:
                agent.handoffs.append(
                    handoff(
                        agent=target_agent,
                        tool_description_override=f"Transfer to {target_agent.name} for specialized assistance",
                    )
                )
            
            logger.info(
                f"Set up handoffs for {agent.name}",
                handoff_count=len(handoff_targets),
                targets=[target.name for target in handoff_targets]
            )

def create_triage_agent(specialists: Dict[str, Agent]) -> Agent:
    """
    Create main triage agent with handoffs to all specialists.
    
    This replaces the AgentController orchestration logic.
    """
    # Create handoff descriptions for each specialist
    specialist_descriptions = []
    for agent_type, agent in specialists.items():
        spec = get_agent_spec(agent_type)
        expertise_summary = ", ".join(spec['expertise'][:3])
        specialist_descriptions.append(f"- **{agent.name}**: {expertise_summary}")
    
    triage_instructions = f"""{RECOMMENDED_PROMPT_PREFIX}

You are the main triage agent for the CodeVision building code assistance system.

## YOUR ROLE

Analyze building code queries and route them to the most appropriate specialist. You have access to these specialists:

{chr(10).join(specialist_descriptions)}

## ROUTING STRATEGY

1. **Analyze the query** to identify the primary building code area
2. **Route immediately** to the most appropriate specialist using handoffs
3. **Let specialists collaborate** - they can handoff to each other as needed

## ROUTING EXAMPLES

- "Fire safety requirements" → Code B or Code C Specialist
- "Insulation R-values" → Code C Specialist  
- "Wheelchair access" → Code H or Code D Specialist
- "Building classification" → Code B Specialist
- "Energy efficiency" → Code C or Code H Specialist

## IMPORTANT

- Always route to a specialist - don't try to answer directly
- Use the most specific specialist for the query
- Trust specialists to collaborate via handoffs if needed
- Ensure queries are about New Zealand Building Code

If the query is unclear or not about building codes, clarify before routing.
"""
    
    # Create handoffs to all specialists
    specialist_handoffs = []
    for agent in specialists.values():
        specialist_handoffs.append(
            handoff(
                agent=agent,
                tool_description_override=f"Route query to {agent.name} for specialized building code assistance",
            )
        )
    
    triage_agent = Agent(
        name="CodeVision Triage Agent",
        instructions=triage_instructions,
        handoffs=specialist_handoffs,
        input_guardrails=[building_code_input_guardrail],
        output_guardrails=[safety_output_guardrail],
        model="gpt-4-turbo-preview"
    )
    
    logger.info(
        "Created pure SDK triage agent",
        specialist_count=len(specialists),
        handoff_count=len(specialist_handoffs)
    )
    return triage_agent

# Global instances (created once, used everywhere)
_specialists_cache = None
_triage_cache = None

def get_pure_sdk_specialists() -> Dict[str, Agent]:
    """Get or create pure SDK specialists (cached)."""
    global _specialists_cache
    if _specialists_cache is None:
        logger.info("Creating pure SDK specialists (first time)")
        _specialists_cache = create_pure_sdk_specialists()
    else:
        logger.debug("Returning cached pure SDK specialists")
    return _specialists_cache

def get_pure_sdk_triage() -> Agent:
    """Get or create pure SDK triage agent (cached)."""
    global _triage_cache
    if _triage_cache is None:
        logger.info("Creating pure SDK triage agent (first time)")
        specialists = get_pure_sdk_specialists()
        _triage_cache = create_triage_agent(specialists)
    else:
        logger.debug("Returning cached pure SDK triage agent")
    return _triage_cache

def reset_pure_sdk_cache():
    """Reset the cache (useful for testing)."""
    global _specialists_cache, _triage_cache
    _specialists_cache = None
    _triage_cache = None

# Metadata about the pure SDK implementation
PURE_SDK_METADATA = {
    'total_specialists': 7,
    'handoff_enabled': True,
    'guardrails_enabled': True,
    'tools_per_agent': 5,
    'replacement_for': ['BaseAgent', 'SDKAgentWrapper', 'AgentController'],
    'sdk_native': True,
    'caching_enabled': True,
    'performance_optimized': True,
}
