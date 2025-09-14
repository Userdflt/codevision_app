"""
Tests for advanced OpenAI Agents SDK features.

This module tests the advanced implementation including:
- Input and output guardrails
- Native handoffs between agents
- Advanced orchestration patterns
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from agent_project.agents.advanced import (
    BuildingCodeValidation,
    building_code_input_guardrail,
    safety_output_guardrail,
    create_triage_agent,
    create_specialist_agents,
    AdvancedOrchestrator,
    parallel_analysis,
    sequential_chain,
)

@pytest.mark.asyncio
class TestGuardrails:
    """Test guardrail functionality."""
    
    async def test_building_code_validation_structure(self):
        """Test that validation models are properly structured."""
        validation = BuildingCodeValidation(
            is_building_code_query=True,
            reasoning="Query about fire safety requirements",
            confidence=0.95,
            topic_detected="fire_safety"
        )
        
        assert validation.is_building_code_query is True
        assert validation.confidence == 0.95
        assert "fire_safety" in validation.topic_detected
    
    async def test_guardrail_exception_handling(self):
        """Test that guardrail exceptions are handled properly."""
        from agent_project.agents.advanced.guardrails import handle_guardrail_exceptions
        from agents.exceptions import InputGuardrailTripwireTriggered
        
        async def mock_function():
            raise InputGuardrailTripwireTriggered("Test guardrail trigger")
        
        result = await handle_guardrail_exceptions(mock_function)
        
        assert "error" in result
        assert result["error"] == "input_guardrail_triggered"
        assert "guardrail_info" in result

@pytest.mark.asyncio  
class TestAdvancedAgents:
    """Test advanced agent functionality."""
    
    async def test_specialist_agent_creation(self):
        """Test that specialist agents are created with handoffs."""
        agents = create_specialist_agents()
        
        assert "code_b" in agents
        assert "code_c" in agents
        assert "code_h" in agents
        
        # Check that agents have handoffs configured
        code_b = agents["code_b"]
        assert hasattr(code_b, 'handoffs')
        assert len(code_b.handoffs) == 2  # Should have handoffs to C and H
    
    async def test_triage_agent_creation(self):
        """Test that triage agent is created with proper configuration."""
        specialists = create_specialist_agents()
        triage = create_triage_agent(specialists)
        
        assert triage.name == "CodeVision Triage Agent"
        assert hasattr(triage, 'handoffs')
        assert len(triage.handoffs) == 3  # Should have handoffs to all specialists
        assert hasattr(triage, 'input_guardrails')
        assert hasattr(triage, 'output_guardrails')
    
    async def test_advanced_orchestrator_initialization(self):
        """Test advanced orchestrator initialization."""
        orchestrator = AdvancedOrchestrator()
        
        assert orchestrator.specialist_agents is not None
        assert orchestrator.triage_agent is not None
        assert len(orchestrator.specialist_agents) == 3
    
    async def test_direct_specialist_access(self):
        """Test direct access to specialist agents."""
        orchestrator = AdvancedOrchestrator()
        
        # Mock the Runner.run to avoid actual API calls
        with pytest.mock.patch('agent_project.agents.advanced.agents.Runner.run') as mock_run:
            mock_result = MagicMock()
            mock_result.final_output = "Test response"
            mock_result.last_agent.name = "Code B Specialist"
            mock_run.return_value = mock_result
            
            result = await orchestrator.get_specialist_directly(
                "code_b", 
                "What are fire safety requirements?"
            )
            
            assert result["routing_method"] == "direct_specialist"
            assert result["specialist_type"] == "code_b"
            assert "final_output" in result

@pytest.mark.asyncio
class TestOrchestrationPatterns:
    """Test advanced orchestration patterns."""
    
    async def test_parallel_analysis_structure(self):
        """Test that parallel analysis has the right structure."""
        # Mock all the agents and Runner to avoid API calls
        with pytest.mock.patch('agent_project.agents.advanced.orchestration.Runner.run') as mock_run:
            # Mock successful results
            mock_result = MagicMock()
            mock_result.final_output = MagicMock()
            mock_result.final_output.agent_name = "Test Agent"
            mock_result.final_output.confidence = 0.8
            mock_result.final_output.analysis = "Test analysis"
            mock_result.final_output.recommendations = ["Test recommendation"]
            mock_run.return_value = mock_result
            
            # Mock consensus result
            def mock_run_side_effect(*args, **kwargs):
                if "Consensus Agent" in str(args[0]):
                    result = MagicMock()
                    result.final_output = MagicMock()
                    result.final_output.final_recommendation = "Test consensus"
                    result.final_output.consensus_level = 0.9
                    result.final_output.dissenting_opinions = []
                    return result
                return mock_result
            
            mock_run.side_effect = mock_run_side_effect
            
            result = await parallel_analysis("Test building code query")
            
            assert result["routing_method"] == "parallel_analysis"
            assert "parallel_analyses" in result
            assert "consensus_level" in result
            assert "final_output" in result
    
    async def test_sequential_chain_structure(self):
        """Test that sequential chain has the right structure."""
        with pytest.mock.patch('agent_project.agents.advanced.orchestration.Runner.run') as mock_run:
            mock_result = MagicMock()
            mock_result.final_output = "Test output"
            mock_run.return_value = mock_result
            
            result = await sequential_chain("Test building code query")
            
            assert result["routing_method"] == "sequential_chain"
            assert "research_phase" in result
            assert "analysis_phase" in result
            assert result["chain_length"] == 3
            assert "final_output" in result

@pytest.mark.asyncio
class TestIntegration:
    """Integration tests for advanced features."""
    
    async def test_end_to_end_advanced_flow(self):
        """Test complete flow with advanced orchestrator."""
        orchestrator = AdvancedOrchestrator()
        
        # Mock the entire flow
        with pytest.mock.patch('agent_project.agents.advanced.agents.Runner.run') as mock_run:
            mock_result = MagicMock()
            mock_result.final_output = "Advanced test response"
            mock_result.last_agent.name = "CodeVision Triage Agent"
            mock_run.return_value = mock_result
            
            result = await orchestrator.process_query(
                "What are the accessibility requirements for building entrances?"
            )
            
            assert "final_output" in result
            assert result["routing_method"] == "native_sdk_handoffs"
            assert "last_agent" in result
    
    async def test_guardrail_integration(self):
        """Test that guardrails integrate properly with agents."""
        from agent_project.agents.advanced.agents import create_triage_agent, create_specialist_agents
        
        specialists = create_specialist_agents()
        triage = create_triage_agent(specialists)
        
        # Verify guardrails are attached
        assert hasattr(triage, 'input_guardrails')
        assert len(triage.input_guardrails) > 0
        
        # Verify specialists have output guardrails
        for agent in specialists.values():
            assert hasattr(agent, 'output_guardrails')
            assert len(agent.output_guardrails) > 0

@pytest.mark.asyncio  
class TestErrorHandling:
    """Test error handling in advanced features."""
    
    async def test_invalid_agent_type(self):
        """Test handling of invalid agent types."""
        orchestrator = AdvancedOrchestrator()
        
        with pytest.raises(ValueError):
            await orchestrator.get_specialist_directly("invalid_type", "test query")
    
    async def test_parallel_analysis_with_failures(self):
        """Test parallel analysis when some agents fail."""
        with pytest.mock.patch('agent_project.agents.advanced.orchestration.Runner.run') as mock_run:
            # Make some calls fail, others succeed
            def mock_run_side_effect(*args, **kwargs):
                if "Structural" in str(args[0]):
                    raise Exception("Structural analysis failed")
                elif "Consensus" in str(args[0]):
                    result = MagicMock()
                    result.final_output = MagicMock()
                    result.final_output.final_recommendation = "Partial consensus"
                    result.final_output.consensus_level = 0.7
                    result.final_output.dissenting_opinions = []
                    return result
                else:
                    result = MagicMock()
                    result.final_output = MagicMock()
                    result.final_output.agent_name = "Test Agent"
                    result.final_output.confidence = 0.8
                    result.final_output.analysis = "Test analysis"
                    result.final_output.recommendations = ["Test rec"]
                    return result
            
            mock_run.side_effect = mock_run_side_effect
            
            result = await parallel_analysis("Test query")
            
            assert "errors" in result
            assert len(result["errors"]) > 0
            assert "final_output" in result  # Should still have output from working agents

# Performance and configuration tests
class TestConfiguration:
    """Test configuration and performance aspects."""
    
    def test_agent_configuration(self):
        """Test that agents are configured with proper settings."""
        agents = create_specialist_agents()
        
        for agent_type, agent in agents.items():
            assert agent.name is not None
            assert len(agent.instructions) > 100  # Should have substantial instructions
            assert "RECOMMENDED_PROMPT_PREFIX" in agent.instructions or "handoff" in agent.instructions.lower()
    
    def test_handoff_configuration(self):
        """Test that handoffs are properly configured."""
        agents = create_specialist_agents()
        
        for agent in agents.values():
            if hasattr(agent, 'handoffs') and agent.handoffs:
                for handoff in agent.handoffs:
                    assert hasattr(handoff, 'agent')
                    assert handoff.agent is not None

if __name__ == "__main__":
    # Run a simple demo if executed directly
    async def demo():
        print("🚀 Advanced OpenAI Agents SDK Demo")
        
        # Create orchestrator
        orchestrator = AdvancedOrchestrator()
        print("✅ Advanced orchestrator created")
        
        # Test queries (would need API key to actually run)
        test_queries = [
            "What are the fire safety requirements for a Class 5 building?",
            "What insulation R-values are required for roof assemblies?", 
            "What is the minimum door width for wheelchair access?",
        ]
        
        for query in test_queries:
            print(f"\n🔍 Test Query: {query}")
            print("   (Would process with real API key)")
        
        print("\n✅ Demo completed - all advanced features configured!")
    
    asyncio.run(demo())
