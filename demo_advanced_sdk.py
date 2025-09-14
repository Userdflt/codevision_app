#!/usr/bin/env python3
"""
Demo script for advanced OpenAI Agents SDK features in CodeVision.

This script demonstrates:
1. Guardrails (input and output validation)
2. Handoffs (native agent-to-agent delegation)
3. Advanced orchestration patterns (parallel, sequential, collaborative)

Usage:
    python demo_advanced_sdk.py

Requires:
    OPENAI_API_KEY environment variable set
"""

import os
import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent_project.agents.advanced import (
    AdvancedOrchestrator,
    parallel_analysis,
    sequential_chain,
    run_advanced_orchestration,
)

async def demo_guardrails():
    """Demonstrate input and output guardrails."""
    print("🛡️  DEMO: Guardrails")
    print("=" * 50)
    
    orchestrator = AdvancedOrchestrator()
    
    # Test queries - some should pass, some should be blocked
    test_queries = [
        ("✅ Valid", "What are the fire safety requirements for a Class 5 building?"),
        ("✅ Valid", "What insulation R-values are required for roof assemblies?"),
        ("❌ Invalid", "Can you help me with my math homework?"),
        ("❌ Invalid", "What is the meaning of life?"),
        ("✅ Valid", "What is the minimum door width for wheelchair access?"),
    ]
    
    for status, query in test_queries:
        print(f"\n{status} Query: {query}")
        try:
            result = await orchestrator.process_query(query)
            if "error" in result and "guardrail" in result["error"]:
                print(f"   🛡️  Blocked by guardrail: {result['error']}")
            else:
                print(f"   ✅ Processed: {result['final_output'][:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def demo_handoffs():
    """Demonstrate native handoffs between agents."""
    print("\n\n🔄 DEMO: Native Handoffs")
    print("=" * 50)
    
    orchestrator = AdvancedOrchestrator()
    
    # Queries that should trigger handoffs between specialists
    handoff_queries = [
        "I need help with both fire safety requirements and energy efficiency for a new office building",
        "What are the accessibility requirements for building entrances, and how do they interact with fire egress requirements?",
        "How do energy efficiency requirements affect accessible design in building entrances?",
    ]
    
    for query in handoff_queries:
        print(f"\n🔍 Complex Query: {query}")
        try:
            result = await orchestrator.process_query(query)
            print(f"   🤖 Last Agent: {result.get('last_agent', 'Unknown')}")
            print(f"   🔄 Routing: {result.get('routing_method', 'Unknown')}")
            print(f"   📝 Response: {result['final_output'][:150]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def demo_orchestration_patterns():
    """Demonstrate advanced orchestration patterns."""
    print("\n\n🎭 DEMO: Advanced Orchestration Patterns") 
    print("=" * 50)
    
    test_query = "What are the requirements for accessible fire exits in a multi-story office building?"
    
    # Pattern 1: Parallel Analysis
    print(f"\n🔀 Parallel Analysis:")
    print(f"Query: {test_query}")
    try:
        result = await parallel_analysis(test_query)
        print(f"   📊 Analyses: {len(result.get('parallel_analyses', []))}")
        print(f"   🤝 Consensus Level: {result.get('consensus_level', 'N/A')}")
        print(f"   📝 Final Output: {result['final_output'][:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Pattern 2: Sequential Chain
    print(f"\n🔗 Sequential Chain:")
    try:
        result = await sequential_chain(test_query)
        print(f"   📋 Chain Length: {result.get('chain_length', 'N/A')}")
        print(f"   🔍 Research Phase: {result.get('research_phase', 'N/A')[:100]}...")
        print(f"   📝 Final Output: {result['final_output'][:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Pattern 3: Collaborative Review
    print(f"\n👥 Collaborative Review:")
    try:
        result = await run_advanced_orchestration(test_query, method="review")
        print(f"   🔄 Iterations: {result.get('iterations_completed', 'N/A')}")
        print(f"   📝 Final Output: {result['final_output'][:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

async def demo_direct_specialist_access():
    """Demonstrate direct access to specialists."""
    print("\n\n🎯 DEMO: Direct Specialist Access")
    print("=" * 50)
    
    orchestrator = AdvancedOrchestrator()
    
    specialist_queries = [
        ("code_b", "What building classification applies to a 3-story office building?"),
        ("code_c", "What are the thermal performance requirements for external walls?"),
        ("code_h", "What is the required width for accessible parking spaces?"),
    ]
    
    for agent_type, query in specialist_queries:
        print(f"\n🎯 Direct to {agent_type.upper()}: {query}")
        try:
            result = await orchestrator.get_specialist_directly(agent_type, query)
            print(f"   🤖 Specialist: {result.get('specialist_type', 'Unknown')}")
            print(f"   📝 Response: {result['final_output'][:150]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def main():
    """Run the complete demo."""
    print("🚀 CodeVision Advanced OpenAI Agents SDK Demo")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set.")
        print("Set your API key to see real responses:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("\nRunning demo with mock responses...\n")
    
    try:
        # Run all demos
        await demo_guardrails()
        await demo_handoffs()
        await demo_orchestration_patterns()
        await demo_direct_specialist_access()
        
        print("\n\n🎉 Demo completed successfully!")
        print("=" * 60)
        print("Features demonstrated:")
        print("✅ Input and output guardrails")
        print("✅ Native handoffs between agents")
        print("✅ Parallel analysis orchestration")
        print("✅ Sequential chain orchestration")
        print("✅ Collaborative review orchestration")
        print("✅ Direct specialist access")
        print("\n🏗️  Your CodeVision app now has advanced OpenAI Agents SDK capabilities!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        print("Check your OpenAI API key and internet connection.")

if __name__ == "__main__":
    asyncio.run(main())
