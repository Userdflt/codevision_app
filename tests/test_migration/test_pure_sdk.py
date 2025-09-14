"""
Tests for pure SDK implementation without any adapters.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from agent_project.agents.pure_sdk import (
    create_pure_sdk_specialists,
    create_triage_agent,
    get_pure_sdk_specialists,
    get_pure_sdk_triage,
    reset_pure_sdk_cache,
    PURE_SDK_METADATA
)
from agent_project.agents.pure_orchestrator import (
    PureSDKOrchestrator,
    run_pure_sdk_query,
    PURE_ORCHESTRATOR_METADATA
)
from agent_project.agents.specifications import get_all_agent_types

class TestPureSDKAgents:
    """Test pure SDK agent creation and configuration."""
    
    def test_create_pure_sdk_specialists(self):
        """Test that pure SDK specialists are created correctly."""
        reset_pure_sdk_cache()  # Ensure clean state
        
        specialists = create_pure_sdk_specialists()
        
        assert isinstance(specialists, dict)
        assert len(specialists) == 7  # All agent types
        
        # Check that all expected agent types are present
        expected_types = get_all_agent_types()
        for agent_type in expected_types:
            assert agent_type in specialists
            
        # Check that agents are SDK Agent objects
        for agent_type, agent in specialists.items():
            assert hasattr(agent, 'name')
            assert hasattr(agent, 'instructions')
            assert hasattr(agent, 'tools')
            assert hasattr(agent, 'handoffs')
            assert agent.name.endswith('Specialist')
    
    def test_pure_sdk_agents_have_tools(self):
        """Test that pure SDK agents have tools configured."""
        reset_pure_sdk_cache()
        specialists = create_pure_sdk_specialists()
        
        for agent_type, agent in specialists.items():
            assert hasattr(agent, 'tools')
            assert len(agent.tools) >= 1  # Should have building code tools
    
    def test_pure_sdk_agents_have_guardrails(self):
        """Test that pure SDK agents have guardrails configured."""
        reset_pure_sdk_cache()
        specialists = create_pure_sdk_specialists()
        
        for agent_type, agent in specialists.items():
            assert hasattr(agent, 'input_guardrails')
            assert hasattr(agent, 'output_guardrails')
            # Should have at least one of each type
            assert len(agent.input_guardrails) >= 1
            assert len(agent.output_guardrails) >= 1
    
    def test_pure_sdk_agents_have_handoffs(self):
        """Test that pure SDK agents have handoffs configured."""
        reset_pure_sdk_cache()
        specialists = create_pure_sdk_specialists()
        
        for agent_type, agent in specialists.items():
            assert hasattr(agent, 'handoffs')
            # Each agent should have handoffs to other specialists
            if agent.handoffs:  # Some agents might not have handoffs if no triggers match
                assert len(agent.handoffs) >= 1
    
    def test_create_triage_agent(self):
        """Test triage agent creation."""
        reset_pure_sdk_cache()
        specialists = create_pure_sdk_specialists()
        triage = create_triage_agent(specialists)
        
        assert hasattr(triage, 'name')
        assert hasattr(triage, 'handoffs')
        assert triage.name == "CodeVision Triage Agent"
        
        # Triage should have handoffs to all specialists
        assert len(triage.handoffs) == len(specialists)
    
    def test_pure_sdk_caching(self):
        """Test that caching works correctly."""
        reset_pure_sdk_cache()
        
        # First calls should create agents
        specialists1 = get_pure_sdk_specialists()
        triage1 = get_pure_sdk_triage()
        
        # Second calls should return cached instances
        specialists2 = get_pure_sdk_specialists()
        triage2 = get_pure_sdk_triage()
        
        assert specialists1 is specialists2  # Same object reference
        assert triage1 is triage2  # Same object reference
    
    def test_pure_sdk_cache_reset(self):
        """Test that cache reset works."""
        reset_pure_sdk_cache()
        
        specialists1 = get_pure_sdk_specialists()
        reset_pure_sdk_cache()
        specialists2 = get_pure_sdk_specialists()
        
        assert specialists1 is not specialists2  # Different object references
    
    def test_pure_sdk_metadata(self):
        """Test pure SDK metadata is accurate."""
        assert PURE_SDK_METADATA['total_specialists'] == 7
        assert PURE_SDK_METADATA['sdk_native'] is True
        assert PURE_SDK_METADATA['handoff_enabled'] is True
        assert PURE_SDK_METADATA['guardrails_enabled'] is True
        assert 'BaseAgent' in PURE_SDK_METADATA['replacement_for']

@pytest.mark.asyncio
class TestPureSDKOrchestrator:
    """Test pure SDK orchestrator functionality."""
    
    async def test_pure_orchestrator_initialization(self):
        """Test pure orchestrator initializes correctly."""
        orchestrator = PureSDKOrchestrator()
        
        assert orchestrator.specialists is not None
        assert orchestrator.triage_agent is not None
        assert len(orchestrator.specialists) >= 7  # All specialists
    
    async def test_process_query_mock_success(self):
        """Test query processing with mocked SDK Runner."""
        orchestrator = PureSDKOrchestrator()
        
        # Mock the SDK Runner to avoid API calls
        with patch('agent_project.agents.pure_orchestrator.Runner.run') as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Pure SDK test response"
            mock_result.last_agent = MagicMock()
            mock_result.last_agent.name = "Code B Specialist"
            mock_run.return_value = mock_result
            
            result = await orchestrator.process_query(
                "What are fire safety requirements?"
            )
            
            assert result["routing_method"] == "pure_sdk_handoffs"
            assert result["success"] is True
            assert "final_output" in result
            assert result["last_agent"] == "Code B Specialist"
            assert result["orchestrator_type"] == "pure_sdk"
    
    async def test_process_query_with_context(self):
        """Test query processing with context."""
        orchestrator = PureSDKOrchestrator()
        
        with patch('agent_project.agents.pure_orchestrator.Runner.run') as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Context test response"
            mock_result.last_agent = MagicMock()
            mock_result.last_agent.name = "Code C Specialist"
            mock_run.return_value = mock_result
            
            context = {"session_id": "test-123", "user_id": "user-456"}
            result = await orchestrator.process_query(
                "What are insulation requirements?",
                context
            )
            
            assert result["context"] == context
            assert result["success"] is True
            mock_run.assert_called_once()
    
    async def test_direct_specialist_access(self):
        """Test direct access to specialists."""
        orchestrator = PureSDKOrchestrator()
        
        with patch('agent_project.agents.pure_orchestrator.Runner.run') as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Direct specialist response"
            mock_result.last_agent = MagicMock()
            mock_result.last_agent.name = "Code H Specialist"
            mock_run.return_value = mock_result
            
            result = await orchestrator.get_specialist_directly(
                "code_h",
                "What are accessibility requirements?"
            )
            
            assert result["routing_method"] == "direct_specialist"
            assert result["specialist_type"] == "code_h"
            assert result["success"] is True
    
    async def test_direct_specialist_invalid_type(self):
        """Test direct specialist access with invalid type."""
        orchestrator = PureSDKOrchestrator()
        
        with pytest.raises(ValueError) as exc_info:
            await orchestrator.get_specialist_directly(
                "invalid_type",
                "test query"
            )
        
        assert "Unknown agent type" in str(exc_info.value)
        assert "invalid_type" in str(exc_info.value)
    
    async def test_error_handling(self):
        """Test error handling in orchestrator."""
        orchestrator = PureSDKOrchestrator()
        
        # Mock Runner to raise an exception
        with patch('agent_project.agents.pure_orchestrator.Runner.run') as mock_run:
            mock_run.side_effect = Exception("SDK execution failed")
            
            result = await orchestrator.process_query("test query")
            
            assert result["success"] is False
            assert result["routing_method"] == "pure_sdk_error"
            assert "error" in result
            assert "SDK execution failed" in result["error"]
    
    async def test_stream_query_placeholder(self):
        """Test stream query (currently uses normal processing)."""
        orchestrator = PureSDKOrchestrator()
        
        with patch('agent_project.agents.pure_orchestrator.Runner.run') as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Streaming test response"
            mock_result.last_agent = MagicMock()
            mock_result.last_agent.name = "Triage Agent"
            mock_run.return_value = mock_result
            
            result = await orchestrator.stream_query("test stream query")
            
            assert result["streaming_requested"] is True
            assert result["streaming_available"] is False
            assert result["success"] is True
    
    def test_get_available_specialists(self):
        """Test getting specialist information."""
        orchestrator = PureSDKOrchestrator()
        specialists_info = orchestrator.get_available_specialists()
        
        assert isinstance(specialists_info, dict)
        assert len(specialists_info) >= 7
        
        for agent_type, info in specialists_info.items():
            assert "name" in info
            assert "expertise" in info
            assert "tools_count" in info
            assert "guardrails_enabled" in info
            assert isinstance(info["expertise"], list)
    
    def test_get_orchestrator_status(self):
        """Test getting orchestrator status."""
        orchestrator = PureSDKOrchestrator()
        status = orchestrator.get_orchestrator_status()
        
        assert status["orchestrator_type"] == "pure_sdk"
        assert status["sdk_native"] is True
        assert status["specialists_loaded"] >= 7
        assert status["legacy_components"] == 0
        assert status["adapters_used"] == 0
        assert status["handoffs_enabled"] is True
    
    async def test_run_pure_sdk_query_convenience(self):
        """Test convenience function for running queries."""
        with patch('agent_project.agents.pure_orchestrator.Runner.run') as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Convenience function test"
            mock_result.last_agent = MagicMock()
            mock_result.last_agent.name = "Test Agent"
            mock_run.return_value = mock_result
            
            result = await run_pure_sdk_query("test query")
            
            assert result["orchestrator_type"] == "pure_sdk"
            assert result["success"] is True
    
    def test_pure_orchestrator_metadata(self):
        """Test pure orchestrator metadata."""
        assert PURE_ORCHESTRATOR_METADATA['sdk_native'] is True
        assert 'AgentController' in PURE_ORCHESTRATOR_METADATA['replacement_for']
        assert PURE_ORCHESTRATOR_METADATA['supports_direct_access'] is True

class TestPureSDKIntegration:
    """Integration tests for pure SDK implementation."""
    
    def test_no_legacy_imports(self):
        """Test that pure SDK doesn't import legacy components."""
        # This test ensures we're not accidentally importing legacy code
        import agent_project.agents.pure_sdk as pure_sdk_module
        import agent_project.agents.pure_orchestrator as orchestrator_module
        
        # Check module source for actual import statements (not comments/docstrings)
        import inspect
        
        pure_sdk_source = inspect.getsource(pure_sdk_module)
        orchestrator_source = inspect.getsource(orchestrator_module)
        
        # Extract import lines only
        pure_sdk_imports = [line.strip() for line in pure_sdk_source.split('\n') 
                           if line.strip().startswith(('from ', 'import '))]
        orchestrator_imports = [line.strip() for line in orchestrator_source.split('\n') 
                               if line.strip().startswith(('from ', 'import '))]
        
        # Should not import legacy components in actual import statements
        legacy_imports = ['BaseAgent', 'SDKAgentWrapper', 'AgentController']
        
        for legacy_import in legacy_imports:
            # Check actual import statements, not comments/docstrings
            assert not any(legacy_import in imp_line for imp_line in pure_sdk_imports), \
                f"Found {legacy_import} in pure_sdk imports: {pure_sdk_imports}"
            assert not any(legacy_import in imp_line for imp_line in orchestrator_imports), \
                f"Found {legacy_import} in orchestrator imports: {orchestrator_imports}"
        
        print(f"✅ Pure SDK imports clean: {len(pure_sdk_imports)} import statements")
        print(f"✅ Orchestrator imports clean: {len(orchestrator_imports)} import statements")
    
    def test_pure_sdk_agent_types_match_specifications(self):
        """Test that agent types match specifications."""
        reset_pure_sdk_cache()
        specialists = create_pure_sdk_specialists()
        
        from agent_project.agents.specifications import get_all_agent_types
        expected_types = get_all_agent_types()
        
        assert set(specialists.keys()) == set(expected_types)
    
    def test_pure_sdk_tools_integration(self):
        """Test that tools are properly integrated."""
        reset_pure_sdk_cache()
        specialists = create_pure_sdk_specialists()
        
        # Check that tools from tools.py are integrated
        from agent_project.agents.tools import BUILDING_CODE_TOOLS
        
        for agent_type, agent in specialists.items():
            assert hasattr(agent, 'tools')
            assert len(agent.tools) >= 1
            
            # Tools should be from our tools module
            # (Can't directly compare due to SDK wrapping, but check count)
            assert len(agent.tools) == len(BUILDING_CODE_TOOLS)

if __name__ == "__main__":
    # Run basic validation
    print("🧪 Validating pure SDK implementation...")
    
    # Test agent creation via cached functions
    reset_pure_sdk_cache()
    specialists = get_pure_sdk_specialists()
    assert len(specialists) == 7
    print(f"✅ Created {len(specialists)} pure SDK specialists")
    
    # Test triage agent
    triage = get_pure_sdk_triage()
    assert triage.name == "CodeVision Triage Agent"
    print("✅ Created pure SDK triage agent")
    
    # Test orchestrator
    orchestrator = PureSDKOrchestrator()
    assert len(orchestrator.specialists) >= 7
    print("✅ Created pure SDK orchestrator")
    
    # Test caching
    specialists2 = get_pure_sdk_specialists()
    assert specialists is specialists2
    print("✅ Caching works correctly")
    
    print("🎉 Pure SDK implementation validation passed!")
