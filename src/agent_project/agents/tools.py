"""
Native OpenAI Agents SDK tools for building code analysis.
Replaces legacy BaseAgent functionality with native SDK tools.
"""

from typing import List, Dict, Any, Optional
from agents import function_tool
import structlog

logger = structlog.get_logger()

# =============================================================================
# Core Functions (Testable and Reusable)
# =============================================================================

async def vector_search_core(
    query: str, 
    clause_type: Optional[str] = None, 
    limit: int = 5, 
    similarity_threshold: float = 0.8
) -> List[Dict[str, Any]]:
    """
    Core vector search functionality.
    
    This is the testable implementation that replaces BaseAgent.retrieve_context.
    """
    try:
        # Import here to avoid dependency issues at startup
        from agent_project.infrastructure.vector_db.client import VectorDBClient
        
        vector_client = VectorDBClient()
        
        # Perform the search
        results = await vector_client.similarity_search(
            query=query,
            clause_type=clause_type, 
            limit=limit,
            similarity_threshold=similarity_threshold
        )
        
        # Format results for SDK consumption
        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result.get("content", ""),
                "source": result.get("metadata", {}).get("source", "Unknown"),
                "section": result.get("metadata", {}).get("section", ""),
                "clause": result.get("metadata", {}).get("clause", clause_type or ""),
                "similarity_score": result.get("similarity_score", 0.0),
                "metadata": result.get("metadata", {})
            })
        
        logger.info(
            "Vector search completed",
            query_length=len(query),
            clause_type=clause_type,
            results_count=len(formatted_results),
            avg_similarity=sum(r["similarity_score"] for r in formatted_results) / len(formatted_results) if formatted_results else 0
        )
        
        return formatted_results
        
    except Exception as e:
        logger.error("Vector search failed", error=str(e), query=query[:100])
        return [{
            "content": f"Vector search failed: {str(e)}",
            "source": "error",
            "section": "error",
            "clause": clause_type or "unknown",
            "similarity_score": 0.0,
            "metadata": {"error": True}
        }]

async def get_building_code_context_core(
    topics: List[str], 
    clause_type: str
) -> Dict[str, Any]:
    """Core building code context gathering functionality."""
    try:
        all_results = []
        
        for topic in topics:
            results = await vector_search_core(
                query=topic,
                clause_type=clause_type,
                limit=3,
                similarity_threshold=0.7
            )
            all_results.extend(results)
        
        # Deduplicate based on content similarity
        unique_results = []
        seen_content = set()
        
        for result in all_results:
            content_hash = hash(result["content"][:100])  # Hash first 100 chars
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_results.append(result)
        
        return {
            "topics_researched": topics,
            "clause_type": clause_type,
            "total_sources": len(unique_results),
            "results": unique_results[:10],  # Limit to top 10
            "summary": f"Found {len(unique_results)} unique sources across {len(topics)} topics for {clause_type}"
        }
        
    except Exception as e:
        logger.error("Context gathering failed", error=str(e), topics=topics)
        return {
            "topics_researched": topics,
            "clause_type": clause_type,
            "total_sources": 0,
            "results": [],
            "error": str(e)
        }

async def check_building_code_compliance_core(
    requirement: str,
    building_type: str,
    clause_type: str
) -> Dict[str, Any]:
    """Core compliance checking functionality."""
    try:
        # Search for specific compliance information
        compliance_query = f"{requirement} {building_type} compliance requirements"
        
        results = await vector_search_core(
            query=compliance_query,
            clause_type=clause_type,
            limit=5,
            similarity_threshold=0.75
        )
        
        if not results or all(r.get("similarity_score", 0) < 0.75 for r in results):
            return {
                "requirement": requirement,
                "building_type": building_type,
                "clause_type": clause_type,
                "compliance_found": False,
                "message": "Specific compliance requirements not found in database",
                "general_guidance": f"Consult NZ Building Code {clause_type.upper()} for {building_type} {requirement} requirements"
            }
        
        return {
            "requirement": requirement,
            "building_type": building_type,
            "clause_type": clause_type,
            "compliance_found": True,
            "sources": len(results),
            "requirements": results,
            "summary": f"Found {len(results)} compliance sources for {requirement} in {building_type} buildings"
        }
        
    except Exception as e:
        logger.error("Compliance check failed", error=str(e))
        return {
            "requirement": requirement,
            "building_type": building_type,
            "clause_type": clause_type,
            "compliance_found": False,
            "error": str(e)
        }

async def analyze_building_requirements_core(
    building_description: str,
    analysis_type: str = "general"
) -> Dict[str, Any]:
    """Core building requirements analysis functionality."""
    try:
        # Determine relevant clause types based on analysis type
        clause_mapping = {
            "general": ["code_b"],
            "accessibility": ["code_h", "code_d"],
            "fire_safety": ["code_c", "code_b"],
            "energy": ["code_h", "code_c"],
            "structural": ["code_b"],
            "envelope": ["code_c", "code_e"]
        }
        
        relevant_clauses = clause_mapping.get(analysis_type, ["code_b"])
        all_results = []
        
        for clause in relevant_clauses:
            results = await vector_search_core(
                query=building_description,
                clause_type=clause,
                limit=3,
                similarity_threshold=0.7
            )
            all_results.extend(results)
        
        return {
            "building_description": building_description,
            "analysis_type": analysis_type,
            "clauses_analyzed": relevant_clauses,
            "total_requirements": len(all_results),
            "requirements": all_results,
            "summary": f"Found {len(all_results)} relevant requirements for {analysis_type} analysis"
        }
        
    except Exception as e:
        logger.error("Building analysis failed", error=str(e))
        return {
            "building_description": building_description,
            "analysis_type": analysis_type,
            "total_requirements": 0,
            "requirements": [],
            "error": str(e)
        }

async def get_code_interpretation_core(
    regulation_text: str,
    context_question: str
) -> Dict[str, Any]:
    """Core code interpretation functionality."""
    try:
        # Search for similar regulations and interpretations
        interpretation_query = f"{regulation_text} interpretation guidance {context_question}"
        
        results = await vector_search_core(
            query=interpretation_query,
            limit=5,
            similarity_threshold=0.6
        )
        
        # Also search for related provisions
        related_query = f"{regulation_text} related provisions"
        related_results = await vector_search_core(
            query=related_query,
            limit=3,
            similarity_threshold=0.7
        )
        
        return {
            "regulation_text": regulation_text[:200] + "..." if len(regulation_text) > 200 else regulation_text,
            "context_question": context_question,
            "interpretation_sources": len(results),
            "related_provisions": len(related_results),
            "interpretations": results,
            "related": related_results,
            "summary": f"Found {len(results)} interpretation sources and {len(related_results)} related provisions"
        }
        
    except Exception as e:
        logger.error("Code interpretation failed", error=str(e))
        return {
            "regulation_text": regulation_text[:200] + "..." if len(regulation_text) > 200 else regulation_text,
            "context_question": context_question,
            "interpretation_sources": 0,
            "related_provisions": 0,
            "interpretations": [],
            "related": [],
            "error": str(e)
        }

# =============================================================================
# SDK Function Tools (For Agent Use)
# =============================================================================

@function_tool
async def vector_search_tool(
    query: str, 
    clause_type: Optional[str] = None, 
    limit: int = 5, 
    similarity_threshold: float = 0.8
) -> List[Dict[str, Any]]:
    """
    Search building code database for relevant information.
    
    This tool replaces the legacy BaseAgent.retrieve_context method.
    
    Args:
        query: Search query for building code information
        clause_type: Building code clause (e.g., 'code_b', 'code_c') 
        limit: Maximum number of results to return
        similarity_threshold: Minimum similarity score (0.0-1.0)
        
    Returns:
        List of relevant building code sections with metadata
    """
    return await vector_search_core(query, clause_type, limit, similarity_threshold)

@function_tool
async def get_building_code_context(
    topics: List[str], 
    clause_type: str
) -> Dict[str, Any]:
    """
    Get comprehensive context for multiple building code topics.
    
    Args:
        topics: List of topics to research
        clause_type: Building code clause type
        
    Returns:
        Dictionary with comprehensive context information
    """
    return await get_building_code_context_core(topics, clause_type)

@function_tool
async def check_building_code_compliance(
    requirement: str,
    building_type: str,
    clause_type: str
) -> Dict[str, Any]:
    """
    Check compliance requirements for specific building types.
    
    Args:
        requirement: Specific requirement to check
        building_type: Type of building (e.g., "residential", "commercial")
        clause_type: Building code clause
        
    Returns:
        Compliance information and requirements
    """
    return await check_building_code_compliance_core(requirement, building_type, clause_type)

@function_tool
async def analyze_building_requirements(
    building_description: str,
    analysis_type: str = "general"
) -> Dict[str, Any]:
    """
    Analyze building requirements based on description.
    
    Args:
        building_description: Description of the building/project
        analysis_type: Type of analysis ("general", "accessibility", "fire_safety", "energy")
        
    Returns:
        Analysis results with relevant requirements
    """
    return await analyze_building_requirements_core(building_description, analysis_type)

@function_tool
async def get_code_interpretation(
    regulation_text: str,
    context_question: str
) -> Dict[str, Any]:
    """
    Get interpretation of specific building code regulations.
    
    Args:
        regulation_text: Specific regulation or clause text
        context_question: Question about how to interpret the regulation
        
    Returns:
        Interpretation guidance and related provisions
    """
    return await get_code_interpretation_core(regulation_text, context_question)

# =============================================================================
# Tool Registry and Metadata
# =============================================================================

# Tool registry for easy access
BUILDING_CODE_TOOLS = [
    vector_search_tool,
    get_building_code_context,
    check_building_code_compliance,
    analyze_building_requirements,
    get_code_interpretation,
]

# Core functions for testing
CORE_FUNCTIONS = [
    vector_search_core,
    get_building_code_context_core,
    check_building_code_compliance_core,
    analyze_building_requirements_core,
    get_code_interpretation_core,
]

def get_tools_for_agent(agent_type: str) -> List:
    """
    Get appropriate tools for a specific agent type.
    
    Args:
        agent_type: Agent type (e.g., 'code_b', 'code_c', etc.)
        
    Returns:
        List of tools appropriate for the agent
    """
    # For now, all agents get all tools
    # This can be specialized later based on agent needs
    return BUILDING_CODE_TOOLS

def get_tool_descriptions() -> Dict[str, str]:
    """Get descriptions of all available tools."""
    return {
        "vector_search_tool": "Search building code database for specific information",
        "get_building_code_context": "Get comprehensive context for multiple topics",
        "check_building_code_compliance": "Check compliance requirements for building types",
        "analyze_building_requirements": "Analyze building requirements from description",
        "get_code_interpretation": "Get interpretation guidance for regulations"
    }

# Metadata about the tools
TOOLS_METADATA = {
    'total_tools': len(BUILDING_CODE_TOOLS),
    'total_core_functions': len(CORE_FUNCTIONS),
    'replacement_for': 'BaseAgent functionality (retrieve_context, generate_response)',
    'sdk_native': True,
    'async_support': True,
    'error_handling': 'Graceful fallback with error details',
    'testable_core': True,
}