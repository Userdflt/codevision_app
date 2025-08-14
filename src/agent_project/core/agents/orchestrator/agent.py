"""
Orchestrator agent that analyzes intent and routes to appropriate specialists.
"""

from typing import Dict, Any, AsyncGenerator
import structlog
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from agent_project.core.agents.base import BaseAgent
from agent_project.core.tools.intent_classifier import IntentClassifier


logger = structlog.get_logger()


class OrchestratorState(BaseModel):
    """State for the orchestrator agent."""
    query: str
    user_id: str
    session_id: str
    intent: str | None = None
    specialist_agent: str | None = None
    response: str | None = None
    sources: list[Dict[str, Any]] = []
    error: str | None = None


class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator agent that routes queries to appropriate specialists.
    
    This agent analyzes the user's query intent and determines which
    clause-specific specialist should handle the request.
    """
    
    def __init__(self):
        super().__init__("orchestrator")
        self.intent_classifier = IntentClassifier()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph for orchestration."""
        graph = StateGraph(OrchestratorState)
        
        # Add nodes
        graph.add_node("classify_intent", self._classify_intent)
        graph.add_node("route_to_specialist", self._route_to_specialist)
        graph.add_node("handle_general_query", self._handle_general_query)
        
        # Add edges
        graph.set_entry_point("classify_intent")
        graph.add_conditional_edges(
            "classify_intent",
            self._should_route_to_specialist,
            {
                "specialist": "route_to_specialist",
                "general": "handle_general_query"
            }
        )
        graph.add_edge("route_to_specialist", END)
        graph.add_edge("handle_general_query", END)
        
        return graph.compile()
    
    async def _classify_intent(self, state: OrchestratorState) -> Dict[str, Any]:
        """Classify the intent of the user query."""
        try:
            logger.info("Classifying query intent", query=state.query[:100])
            
            intent_result = self.intent_classifier.classify(state.query)
            intent = await intent_result if hasattr(intent_result, "__await__") else intent_result
            
            logger.info("Intent classified", intent=intent)
            
            return {"intent": intent}
            
        except Exception as e:
            logger.error("Intent classification failed", error=str(e))
            return {"error": f"Intent classification failed: {str(e)}"}
    
    def _should_route_to_specialist(self, state: OrchestratorState) -> str:
        """Determine if query should go to specialist or general handler."""
        if state.error:
            return "general"
        
        # Map intents to specialist agents
        specialist_mapping = {
            "energy_efficiency": "code_c",
            "building_envelope": "code_c", 
            "mechanical_systems": "code_d",
            "lighting": "code_e",
            "plumbing": "code_f",
            "electrical": "code_g",
            "accessibility": "code_h",
            "general_building": "code_b"
        }
        
        if state.intent in specialist_mapping:
            return "specialist"
        
        return "general"
    
    async def _route_to_specialist(self, state: OrchestratorState) -> Dict[str, Any]:
        """Route query to the appropriate specialist agent."""
        try:
            # Map intent to specialist
            specialist_mapping = {
                "energy_efficiency": "code_c",
                "building_envelope": "code_c",
                "mechanical_systems": "code_d", 
                "lighting": "code_e",
                "plumbing": "code_f",
                "electrical": "code_g",
                "accessibility": "code_h",
                "general_building": "code_b"
            }
            
            specialist = specialist_mapping.get(state.intent, "code_b")
            
            logger.info("Routing to specialist", specialist=specialist, intent=state.intent)
            
            # Import and instantiate the specialist agent
            specialist_agent = await self._get_specialist_agent(specialist)
            
            # Process query with specialist
            result = await specialist_agent.process_query(
                query=state.query,
                session_id=state.session_id,
                user_id=state.user_id
            )
            
            return {
                "specialist_agent": specialist,
                "response": result["response"],
                "sources": result.get("sources", [])
            }
            
        except Exception as e:
            logger.error("Specialist routing failed", error=str(e))
            return {"error": f"Specialist routing failed: {str(e)}"}
    
    async def _handle_general_query(self, state: OrchestratorState) -> Dict[str, Any]:
        """Handle general queries that don't need specialist routing."""
        try:
            logger.info("Handling general query")
            
            # For general queries, perform basic vector search. Use patched client if present
            vector_client = getattr(self, "vector_client", None)
            if vector_client is None:
                # Lazy import to avoid optional dependency during initial import
                from agent_project.infrastructure.vector_db.client import VectorDBClient
                vector_client = VectorDBClient()

            call_result = vector_client.similarity_search(
                query=state.query,
                limit=5,
                similarity_threshold=0.7
            )
            results = await call_result if hasattr(call_result, "__await__") else call_result
            
            # Generate response using retrieved context
            response = await self._generate_general_response(state.query, results)
            
            return {
                "response": response,
                "sources": results,
                "specialist_agent": "general"
            }
            
        except Exception as e:
            logger.error("General query handling failed", error=str(e))
            return {"error": f"General query handling failed: {str(e)}"}
    
    async def _get_specialist_agent(self, specialist_type: str):
        """Dynamically import and instantiate specialist agent."""
        try:
            if specialist_type == "code_b":
                from agent_project.core.agents.code_b.agent import CodeBAgent
                return CodeBAgent()
            if specialist_type == "code_c":
                from agent_project.core.agents.code_c.agent import CodeCAgent
                return CodeCAgent()
            if specialist_type == "code_d":
                from agent_project.core.agents.code_d.agent import CodeDAgent
                return CodeDAgent()
            if specialist_type == "code_e":
                from agent_project.core.agents.code_e.agent import CodeEAgent
                return CodeEAgent()
            if specialist_type == "code_f":
                from agent_project.core.agents.code_f.agent import CodeFAgent
                return CodeFAgent()
            if specialist_type == "code_g":
                from agent_project.core.agents.code_g.agent import CodeGAgent
                return CodeGAgent()
            if specialist_type == "code_h":
                from agent_project.core.agents.code_h.agent import CodeHAgent
                return CodeHAgent()

            # Default fallback
            from agent_project.core.agents.code_b.agent import CodeBAgent
            return CodeBAgent()
        except Exception as e:
            logger.error("Failed to load specialist agent", specialist_type=specialist_type, error=str(e))
            # Fallback to Code B agent
            from agent_project.core.agents.code_b.agent import CodeBAgent
            return CodeBAgent()
    
    async def _generate_general_response(self, query: str, context: list) -> str:
        """Generate response for general queries using retrieved context."""
        # TODO: Implement LLM-based response generation
        if not context:
            return "I couldn't find specific information about your query. Could you please rephrase or be more specific?"
        
        return f"Based on the available information, here's what I found regarding your query about building codes: {context[0].get('content', '')[:200]}..."
    
    async def process_query(
        self,
        query: str,
        session_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Process a query through the orchestrator graph."""
        initial_state = OrchestratorState(
            query=query,
            session_id=session_id,
            user_id=user_id
        )
        
        try:
            # Run the graph
            result = await self.graph.ainvoke(initial_state)
            
            # result may be a BaseModel or dict-like; access safely
            result_error = result.get("error") if hasattr(result, "get") else getattr(result, "error", None)
            if result_error:
                logger.error("Orchestrator processing failed", error=result.error)
                return {
                    "response": "I encountered an error processing your query. Please try again.",
                    "sources": [],
                    "agent_used": "orchestrator",
                    "error": result_error
                }

            response_val = result.get("response") if hasattr(result, "get") else getattr(result, "response", None)
            sources_val = result.get("sources") if hasattr(result, "get") else getattr(result, "sources", [])
            specialist_val = result.get("specialist_agent") if hasattr(result, "get") else getattr(result, "specialist_agent", None)

            return {
                "response": response_val or "",
                "sources": sources_val or [],
                "agent_used": specialist_val or "orchestrator"
            }
            
        except Exception as e:
            logger.error("Orchestrator graph execution failed", error=str(e))
            return {
                "response": "I encountered an error processing your query. Please try again.",
                "sources": [],
                "agent_used": "orchestrator", 
                "error": str(e)
            }
    
    async def stream_query(
        self,
        query: str,
        session_id: str,
        user_id: str
    ) -> AsyncGenerator[str, None]:
        """Stream query processing for real-time responses."""
        # TODO: Implement streaming response
        result = await self.process_query(query, session_id, user_id)
        yield result["response"]