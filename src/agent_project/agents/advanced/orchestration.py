"""
Advanced orchestration patterns for CodeVision using OpenAI Agents SDK.

This module implements the orchestration patterns described in the official documentation:
- Parallel agent execution
- Sequential chaining
- Collaborative analysis
"""

import asyncio
import structlog
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel

from agents import Agent, Runner, ItemHelpers, trace

logger = structlog.get_logger()

class AnalysisResult(BaseModel):
    """Result from building code analysis."""
    analysis: str
    confidence: float
    agent_name: str
    recommendations: List[str]

class ConsensusResult(BaseModel):
    """Result from consensus analysis."""
    final_recommendation: str
    consensus_level: float
    dissenting_opinions: List[str]

# Analysis agents for parallel execution
structural_analysis_agent = Agent(
    name="Structural Analysis Agent",
    instructions="""
    You analyze building code queries from a structural engineering perspective.
    Focus on:
    - Structural requirements and load specifications
    - Building classifications impact on structural design
    - Fire resistance ratings for structural elements
    - Earthquake and wind load considerations
    
    Provide confidence rating (0.0-1.0) for your analysis.
    Include specific recommendations for compliance.
    """,
    output_type=AnalysisResult,
)

fire_safety_analysis_agent = Agent(
    name="Fire Safety Analysis Agent", 
    instructions="""
    You analyze building code queries from a fire safety perspective.
    Focus on:
    - Fire safety requirements and egress provisions
    - Smoke control and fire separation
    - Fire resistance ratings and materials
    - Emergency access and evacuation
    
    Provide confidence rating (0.0-1.0) for your analysis.
    Include specific recommendations for fire safety compliance.
    """,
    output_type=AnalysisResult,
)

accessibility_analysis_agent = Agent(
    name="Accessibility Analysis Agent",
    instructions="""
    You analyze building code queries from an accessibility perspective.
    Focus on:
    - Universal design and accessibility compliance
    - AS 1428 series requirements
    - Accessible routes and facilities
    - Inclusive design principles
    
    Provide confidence rating (0.0-1.0) for your analysis.
    Include specific recommendations for accessibility compliance.
    """,
    output_type=AnalysisResult,
)

consensus_agent = Agent(
    name="Consensus Agent",
    instructions="""
    You analyze multiple expert opinions on building code matters and provide consensus.
    
    Your role:
    1. Review all expert analyses provided
    2. Identify areas of agreement and disagreement
    3. Synthesize a balanced final recommendation
    4. Highlight any conflicting opinions that need resolution
    
    Calculate consensus level (0.0-1.0) based on agreement between experts.
    Provide a comprehensive final recommendation that considers all perspectives.
    """,
    output_type=ConsensusResult,
)

async def parallel_analysis(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run parallel analysis of a building code query from multiple perspectives.
    
    This implements the parallelization pattern from the SDK documentation,
    running multiple specialized agents in parallel for comprehensive analysis.
    
    Args:
        query: Building code query to analyze
        context: Additional context for the analysis
        
    Returns:
        Dictionary with parallel analysis results and consensus
    """
    logger.info("Starting parallel analysis", query_length=len(query))
    
    # Ensure the entire workflow is a single trace
    with trace("Parallel Building Code Analysis"):
        # Run all analysis agents in parallel
        structural_result, fire_result, accessibility_result = await asyncio.gather(
            Runner.run(structural_analysis_agent, query, context=context or {}),
            Runner.run(fire_safety_analysis_agent, query, context=context or {}),
            Runner.run(accessibility_analysis_agent, query, context=context or {}),
            return_exceptions=True
        )
        
        # Collect results, handling any exceptions
        analyses = []
        errors = []
        
        for result, agent_name in [
            (structural_result, "Structural Analysis"),
            (fire_result, "Fire Safety Analysis"), 
            (accessibility_result, "Accessibility Analysis")
        ]:
            if isinstance(result, Exception):
                logger.error(f"{agent_name} failed", error=str(result))
                errors.append(f"{agent_name}: {str(result)}")
            else:
                analyses.append(result.final_output)
        
        if not analyses:
            return {
                "final_output": "Analysis failed due to errors in all parallel agents.",
                "errors": errors,
                "routing_method": "parallel_analysis_failed"
            }
        
        # Create summary of all analyses
        analysis_summary = "\n\n".join([
            f"**{analysis.agent_name}** (Confidence: {analysis.confidence:.2f})\n"
            f"{analysis.analysis}\n"
            f"Recommendations: {', '.join(analysis.recommendations)}"
            for analysis in analyses
        ])
        
        logger.info("Parallel analyses completed", num_analyses=len(analyses))
        
        # Generate consensus from parallel results
        consensus_input = f"Query: {query}\n\nExpert Analyses:\n{analysis_summary}"
        consensus_result = await Runner.run(consensus_agent, consensus_input, context=context or {})
        consensus = consensus_result.final_output
        
        logger.info("Consensus analysis completed", consensus_level=consensus.consensus_level)
        
        return {
            "final_output": consensus.final_recommendation,
            "parallel_analyses": [analysis.dict() for analysis in analyses],
            "consensus_level": consensus.consensus_level,
            "dissenting_opinions": consensus.dissenting_opinions,
            "routing_method": "parallel_analysis",
            "errors": errors if errors else None,
        }

async def sequential_chain(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run sequential analysis chain for complex building code queries.
    
    This implements the chaining pattern from the SDK documentation,
    where each agent builds upon the previous agent's output.
    
    Args:
        query: Building code query to analyze
        context: Additional context for the analysis
        
    Returns:
        Dictionary with sequential analysis results
    """
    logger.info("Starting sequential chain analysis", query_length=len(query))
    
    # Research agent - gathers initial information
    research_agent = Agent(
        name="Research Agent",
        instructions="""
        You research building code requirements for the given query.
        Identify relevant code sections, standards, and compliance requirements.
        Provide a comprehensive research foundation for detailed analysis.
        """,
    )
    
    # Analysis agent - analyzes the research
    analysis_agent = Agent(
        name="Analysis Agent", 
        instructions="""
        You analyze the research provided and identify key compliance requirements.
        Break down complex requirements into specific, actionable items.
        Highlight any potential conflicts or areas needing clarification.
        """,
    )
    
    # Recommendation agent - provides final recommendations
    recommendation_agent = Agent(
        name="Recommendation Agent",
        instructions="""
        You provide final recommendations based on the research and analysis.
        Create practical, step-by-step guidance for building code compliance.
        Include appropriate disclaimers about consulting professionals.
        """,
    )
    
    with trace("Sequential Building Code Analysis"):
        # Step 1: Research
        logger.info("Sequential step 1: Research")
        research_result = await Runner.run(research_agent, query, context=context or {})
        research_output = research_result.final_output
        
        # Step 2: Analysis  
        logger.info("Sequential step 2: Analysis")
        analysis_input = f"Original Query: {query}\n\nResearch Results:\n{research_output}"
        analysis_result = await Runner.run(analysis_agent, analysis_input, context=context or {})
        analysis_output = analysis_result.final_output
        
        # Step 3: Recommendations
        logger.info("Sequential step 3: Recommendations")
        recommendation_input = f"Original Query: {query}\n\nResearch:\n{research_output}\n\nAnalysis:\n{analysis_output}"
        recommendation_result = await Runner.run(recommendation_agent, recommendation_input, context=context or {})
        
        return {
            "final_output": recommendation_result.final_output,
            "research_phase": research_output,
            "analysis_phase": analysis_output,
            "routing_method": "sequential_chain",
            "chain_length": 3,
        }

async def collaborative_review(query: str, initial_response: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Run collaborative review with critique and improvement loop.
    
    This implements the review pattern from the SDK documentation,
    where an evaluator provides feedback until criteria are met.
    
    Args:
        query: Original building code query
        initial_response: Initial response to review
        context: Additional context
        
    Returns:
        Dictionary with improved response after review
    """
    logger.info("Starting collaborative review")
    
    # Critic agent - evaluates responses
    critic_agent = Agent(
        name="Building Code Critic",
        instructions="""
        You evaluate building code responses for accuracy, completeness, and safety.
        
        Check for:
        - Technical accuracy of code references
        - Completeness of compliance guidance  
        - Appropriate safety disclaimers
        - Professional tone and clarity
        
        Rate responses as: excellent, good, needs_improvement, inadequate
        Provide specific feedback for improvement.
        """,
    )
    
    # Improver agent - improves responses based on feedback
    improver_agent = Agent(
        name="Response Improver",
        instructions="""
        You improve building code responses based on critic feedback.
        
        Address all concerns raised by the critic while maintaining accuracy.
        Enhance clarity, add missing information, and strengthen disclaimers.
        Ensure the improved response meets professional standards.
        """,
    )
    
    max_iterations = 3
    current_response = initial_response
    
    with trace("Collaborative Review Loop"):
        for iteration in range(max_iterations):
            logger.info(f"Review iteration {iteration + 1}")
            
            # Get critique
            critique_input = f"Original Query: {query}\n\nResponse to Evaluate:\n{current_response}"
            critique_result = await Runner.run(critic_agent, critique_input, context=context or {})
            critique = critique_result.final_output
            
            # Check if response is acceptable
            if "excellent" in critique.lower() or "good" in critique.lower():
                logger.info("Response approved by critic", iteration=iteration + 1)
                break
            
            # Improve the response
            improvement_input = f"Original Query: {query}\n\nCurrent Response:\n{current_response}\n\nCritic Feedback:\n{critique}"
            improvement_result = await Runner.run(improver_agent, improvement_input, context=context or {})
            current_response = improvement_result.final_output
            
            logger.info(f"Response improved in iteration {iteration + 1}")
    
    return {
        "final_output": current_response,
        "initial_response": initial_response,
        "iterations_completed": iteration + 1,
        "routing_method": "collaborative_review",
        "final_critique": critique,
    }

# Convenience function for advanced orchestration
async def run_advanced_orchestration(
    query: str, 
    method: str = "parallel", 
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Run advanced orchestration using the specified method.
    
    Args:
        query: Building code query
        method: Orchestration method ('parallel', 'sequential', 'review')
        context: Additional context
        
    Returns:
        Dictionary with orchestration results
    """
    if method == "parallel":
        return await parallel_analysis(query, context)
    elif method == "sequential":
        return await sequential_chain(query, context)
    elif method == "review":
        # For review, we need an initial response first
        from .agents import AdvancedOrchestrator
        orchestrator = AdvancedOrchestrator()
        initial = await orchestrator.process_query(query, context)
        return await collaborative_review(query, initial["final_output"], context)
    else:
        raise ValueError(f"Unknown orchestration method: {method}")
