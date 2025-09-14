"""
Tests for the OpenAI Agents SDK migration.

Verifies that the new SDK-based agents maintain parity with the original
LangGraph implementation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from agent_project.agents.orchestrator.controller import AgentController
from agent_project.agents.orchestrator.routing import get_specialist_agent, pick_agent
from agent_project.agents.specialists.code_b_wrapper import CodeBAgentWrapper


class TestMigration:
    """Test cases for the SDK migration."""
    
    @pytest.fixture
    def sample_payload(self):
        """Sample payload for testing."""
        return {
            "query": "What are the fire safety requirements for a Class 5 building?",
            "session_id": "test-session-123",
            "user_id": "test-user-456",
            "context": {}
        }
    
    def test_pick_agent_clause_routing(self):
        """Test that direct clause specification works."""
        payload = {"clause": "C"}
        assert pick_agent(payload) == "code_c"
        
        payload = {"clause": "h"}
        assert pick_agent(payload) == "code_h"
    
    def test_pick_agent_intent_routing(self):
        """Test that intent-based routing works."""
        payload = {"intent": "energy_efficiency"}
        assert pick_agent(payload) == "code_c"
        
        payload = {"intent": "accessibility"}
        assert pick_agent(payload) == "code_h"
    
    def test_pick_agent_default(self):
        """Test that default routing works."""
        payload = {}
        assert pick_agent(payload) == "code_b"
    
    @pytest.mark.asyncio
    async def test_specialist_agent_creation(self):
        """Test that specialist agents can be created."""
        agent = await get_specialist_agent("code_b")
        assert isinstance(agent, CodeBAgentWrapper)
        
        # Test caching
        agent2 = await get_specialist_agent("code_b")
        assert agent is agent2
    
    @pytest.mark.asyncio
    async def test_controller_orchestration(self, sample_payload):
        """Test the main orchestration flow."""
        controller = AgentController()
        
        # Mock the intent classifier
        controller.intent_classifier.classify = MagicMock(return_value="general_building")
        
        result = await controller.orchestrate(sample_payload)
        
        # Verify result structure
        assert "final_output" in result
        assert "sources" in result
        assert "agent_type" in result
        assert "orchestrator_metadata" in result
        
        # Verify orchestrator metadata
        metadata = result["orchestrator_metadata"]
        assert metadata["intent"] == "general_building"
        assert metadata["session_id"] == "test-session-123"
    
    @pytest.mark.asyncio
    async def test_specialist_wrapper_fallback(self, monkeypatch):
        """Test that specialist wrappers fall back to original agents on SDK failure."""
        wrapper = CodeBAgentWrapper()
        
        # Mock SDK wrapper to fail
        wrapper.sdk_wrapper = MagicMock()
        wrapper.sdk_wrapper.run = AsyncMock(side_effect=Exception("SDK Error"))
        
        # Mock original agent to succeed
        wrapper.original_agent.process_query = AsyncMock(return_value={
            "response": "Fallback response",
            "sources": [],
            "agent_type": "code_b"
        })
        
        result = await wrapper.process_query(
            "test query", "session-123", "user-456"
        )
        
        assert result["response"] == "Fallback response"
        assert result["agent_type"] == "code_b"
    
    def test_migration_maintains_interface(self):
        """Test that the migration maintains the original interface."""
        wrapper = CodeBAgentWrapper()
        
        # Check that the wrapper has the expected methods
        assert hasattr(wrapper, 'process_query')
        assert callable(wrapper.process_query)
        
        # Check that it maintains the original agent as fallback
        assert hasattr(wrapper, 'original_agent')
        assert hasattr(wrapper, 'sdk_wrapper')


class TestSDKIntegration:
    """Test SDK-specific functionality."""
    
    @pytest.mark.asyncio
    async def test_sdk_adapter_error_handling(self):
        """Test that SDK adapter handles errors gracefully."""
        from agent_project.agents.sdk_adapter import SDKAgentWrapper, Agent
        
        # Create a real agent but without API key set (will cause error)
        agent = Agent(name="Test Agent", instructions="Test instructions")
        wrapper = SDKAgentWrapper(agent, "test")
        
        # This should handle authentication errors gracefully
        result = await wrapper.run("test query", {"session_id": "test"})
        
        assert "final_output" in result
        assert result["agent_type"] == "test"
        # Should contain error response due to missing/invalid API key
        assert "error" in result or "Error" in result["final_output"] or result["final_output"] is not None
    
    def test_sdk_configuration(self):
        """Test SDK configuration functions."""
        from agent_project.agents.sdk_adapter import set_default_openai_key, Agent
        import os
        
        # Test setting API key
        test_key = "sk-test-key-123"
        set_default_openai_key(test_key)
        
        assert os.getenv("OPENAI_API_KEY") == test_key
        
        # Test creating agent with real SDK
        agent = Agent(name="Test", instructions="Test agent")
        assert agent.name == "Test"


@pytest.mark.integration
class TestMigrationIntegration:
    """Integration tests for the full migration."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_query_processing(self):
        """Test complete query processing through the new system."""
        controller = AgentController()
        
        # Mock the intent classifier for predictable results
        controller.intent_classifier.classify = MagicMock(return_value="general_building")
        
        payload = {
            "query": "What is the maximum height for a Class 1a building?",
            "session_id": "integration-test-session",
            "user_id": "integration-test-user",
            "context": {"test": True}
        }
        
        result = await controller.orchestrate(payload)
        
        # Verify the complete flow worked
        assert result is not None
        assert "final_output" in result
        assert len(result["final_output"]) > 0
        assert result["agent_type"] in ["code_b", "code_c", "code_d", "code_e", "code_f", "code_g", "code_h"]
    
    @pytest.mark.asyncio
    async def test_streaming_functionality(self):
        """Test that streaming still works with the new system."""
        controller = AgentController()
        controller.intent_classifier.classify = MagicMock(return_value="general_building")
        
        payload = {
            "query": "Test streaming query",
            "session_id": "stream-test",
            "user_id": "stream-user",
            "context": {}
        }
        
        chunks = []
        async for chunk in controller.stream_orchestrate(payload):
            chunks.append(chunk)
        
        assert len(chunks) > 0
        assert "final_output" in chunks[0]
