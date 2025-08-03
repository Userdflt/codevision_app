#!/usr/bin/env python3
"""
CLI tool to test individual agents with queries.
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_project.core.agents.orchestrator.agent import OrchestratorAgent
from agent_project.core.agents.code_b.agent import CodeBAgent
from agent_project.core.utils.logging import setup_logging


AVAILABLE_AGENTS = {
    "orchestrator": OrchestratorAgent,
    "code_b": CodeBAgent,
    # Add other agents as they are implemented
}


async def run_agent_query(agent_type: str, query: str, session_id: str = "cli-session"):
    """Run a query against a specific agent."""
    if agent_type not in AVAILABLE_AGENTS:
        print(f"Error: Agent type '{agent_type}' not found.")
        print(f"Available agents: {', '.join(AVAILABLE_AGENTS.keys())}")
        return
    
    print(f"Initializing {agent_type} agent...")
    agent_class = AVAILABLE_AGENTS[agent_type]
    agent = agent_class()
    
    print(f"Processing query: {query}")
    print("-" * 60)
    
    try:
        result = await agent.process_query(
            query=query,
            session_id=session_id,
            user_id="cli-user"
        )
        
        print("Response:")
        print(result.get("response", "No response"))
        print()
        
        if result.get("sources"):
            print("Sources:")
            for i, source in enumerate(result["sources"], 1):
                print(f"  {i}. {source.get('metadata', {}).get('section', 'Unknown section')}")
                print(f"     Similarity: {source.get('similarity_score', 0):.2f}")
                print(f"     Content: {source.get('content', '')[:100]}...")
                print()
        
        if result.get("agent_used"):
            print(f"Agent used: {result['agent_used']}")
        
        if result.get("error"):
            print(f"Error: {result['error']}")
    
    except Exception as e:
        print(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Test AI agents with queries")
    parser.add_argument("agent", choices=list(AVAILABLE_AGENTS.keys()), 
                       help="Agent type to test")
    parser.add_argument("query", help="Query to send to the agent")
    parser.add_argument("--session-id", default="cli-session",
                       help="Session ID for the query")
    parser.add_argument("--log-level", default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    # Run the agent query
    asyncio.run(run_agent_query(args.agent, args.query, args.session_id))


if __name__ == "__main__":
    main()