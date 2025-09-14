#!/usr/bin/env python3
"""
Hello World example for OpenAI Agents SDK integration.
Based on the official documentation example.
"""

import os
import asyncio
from agents import Agent, Runner

async def main():
    """Run the hello world example."""
    # Ensure API key is set (will use environment variable if available)
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please set it to run this example.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return

    # Create an agent with the exact pattern from the documentation
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    try:
        # Run the agent with the haiku example
        result = await Runner.run(agent, "Write a haiku about recursion in programming.")
        
        print("🎉 OpenAI Agents SDK working successfully!")
        print(f"Response: {result.final_output}")
        
        # Expected output should be something like:
        # Code within the code,
        # Functions calling themselves,
        # Infinite loop's dance.
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your OPENAI_API_KEY is valid and you have credits.")

if __name__ == "__main__":
    asyncio.run(main())
