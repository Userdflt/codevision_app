"""
Guardrails implementation for CodeVision using OpenAI Agents SDK.

This module implements both input and output guardrails as described in the
official SDK documentation.
"""

import structlog
from pydantic import BaseModel
from typing import Union, List

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)

logger = structlog.get_logger()

# Structured output models for guardrails
class BuildingCodeValidation(BaseModel):
    """Validation result for building code queries."""
    is_building_code_query: bool
    reasoning: str
    confidence: float
    topic_detected: str

class SafetyValidation(BaseModel):
    """Validation result for safety in responses."""
    is_safe_response: bool
    reasoning: str
    contains_disclaimers: bool
    professional_tone: bool

# Guardrail agents
guardrail_input_agent = Agent(
    name="Building Code Input Guardrail",
    instructions="""
    You are a validation agent that checks if user queries are related to building codes and construction.
    
    Return is_building_code_query=True ONLY for queries about:
    - Building codes (BCA, NCC, Australian building standards)
    - Construction regulations and compliance
    - Fire safety in buildings
    - Accessibility requirements in construction
    - Energy efficiency in buildings
    - Structural, mechanical, electrical, plumbing building requirements
    - Building classifications and use requirements
    
    Return False for:
    - General homework help
    - Math problems unrelated to construction
    - Personal advice
    - Non-building related topics
    - Programming/software questions
    
    Provide reasoning and confidence (0.0-1.0). Identify the main topic detected.
    """,
    output_type=BuildingCodeValidation,
)

guardrail_output_agent = Agent(
    name="Safety Output Guardrail", 
    instructions="""
    You validate that building code responses are safe and professional.
    
    Check that responses:
    - Are professional and appropriate
    - Include proper disclaimers about consulting professionals
    - Don't provide dangerous or incorrect safety advice
    - Maintain appropriate tone for building code guidance
    
    Return is_safe_response=False if the response:
    - Contains dangerous construction advice
    - Lacks important safety disclaimers
    - Is unprofessional or inappropriate
    - Could lead to unsafe building practices
    """,
    output_type=SafetyValidation,
)

@input_guardrail
async def building_code_input_guardrail(
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    input_data: Union[str, List[TResponseInputItem]]
) -> GuardrailFunctionOutput:
    """
    Input guardrail to ensure queries are building code related.
    
    This guardrail runs before the main agent to validate that the user's
    query is appropriate for a building code specialist system.
    """
    try:
        logger.info("Running building code input guardrail")
        
        # Convert input to string if needed
        input_text = input_data if isinstance(input_data, str) else str(input_data)
        
        # Run the guardrail agent
        result = await Runner.run(guardrail_input_agent, input_text, context=ctx.context)
        validation = result.final_output
        
        logger.info(
            "Input guardrail result",
            is_building_code=validation.is_building_code_query,
            confidence=validation.confidence,
            topic=validation.topic_detected
        )
        
        return GuardrailFunctionOutput(
            output_info=validation,
            tripwire_triggered=not validation.is_building_code_query,
        )
        
    except Exception as e:
        logger.error("Input guardrail failed", error=str(e))
        # Fail open - allow the query to proceed but log the error
        return GuardrailFunctionOutput(
            output_info={"error": str(e)},
            tripwire_triggered=False,
        )

@output_guardrail  
async def safety_output_guardrail(
    ctx: RunContextWrapper, 
    agent: Agent, 
    output: str
) -> GuardrailFunctionOutput:
    """
    Output guardrail to ensure responses are safe and professional.
    
    This guardrail runs after the main agent to validate that the response
    is appropriate and includes necessary safety disclaimers.
    """
    try:
        logger.info("Running safety output guardrail")
        
        # Run the guardrail agent on the output
        result = await Runner.run(guardrail_output_agent, output, context=ctx.context)
        validation = result.final_output
        
        logger.info(
            "Output guardrail result",
            is_safe=validation.is_safe_response,
            has_disclaimers=validation.contains_disclaimers,
            professional=validation.professional_tone
        )
        
        return GuardrailFunctionOutput(
            output_info=validation,
            tripwire_triggered=not validation.is_safe_response,
        )
        
    except Exception as e:
        logger.error("Output guardrail failed", error=str(e))
        # Fail open - allow the response but log the error
        return GuardrailFunctionOutput(
            output_info={"error": str(e)},
            tripwire_triggered=False,
        )

# Convenience function to handle guardrail exceptions
async def handle_guardrail_exceptions(func, *args, **kwargs):
    """
    Helper function to handle guardrail exceptions gracefully.
    """
    try:
        return await func(*args, **kwargs)
    except InputGuardrailTripwireTriggered as e:
        logger.warning("Input guardrail triggered", error=str(e))
        return {
            "final_output": (
                "I can only help with building code and construction regulation questions. "
                "Please ask about building codes, fire safety, accessibility, energy efficiency, "
                "or other construction-related topics."
            ),
            "error": "input_guardrail_triggered",
            "guardrail_info": str(e),
        }
    except OutputGuardrailTripwireTriggered as e:
        logger.warning("Output guardrail triggered", error=str(e))
        return {
            "final_output": (
                "I generated a response that didn't meet safety standards. "
                "Please rephrase your building code question and I'll provide "
                "a safer, more appropriate response."
            ),
            "error": "output_guardrail_triggered", 
            "guardrail_info": str(e),
        }
