"""
OpenAI Agents SDK integration layer for CodeVision.

This module provides the integration between the CodeVision app and the OpenAI Agents SDK,
replacing the previous LangChain/LangGraph implementation.
"""

# Pure OpenAI Agents SDK integration - no legacy adapters
from .pure_orchestrator import PureSDKOrchestrator
from .pure_sdk import get_pure_sdk_specialists, get_pure_sdk_triage

# Advanced SDK features
from .advanced.agents import AdvancedOrchestrator

__all__ = [
    "PureSDKOrchestrator",
    "get_pure_sdk_specialists", 
    "get_pure_sdk_triage",
    "AdvancedOrchestrator"
]
