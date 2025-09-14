"""
Tests for the orchestrator controller and advanced agents.
"""

from unittest.mock import AsyncMock, patch

import pytest

from agent_project.agents.orchestrator.controller import AgentController
from agent_project.agents.advanced import AdvancedOrchestrator


class TestAgentController:
    """Test suite for the new SDK-based agent controller."""

    @pytest.fixture
    def controller(self):
        """Create agent controller instance."""
        return AgentController()

    @pytest.mark.asyncio
    async def test_orchestrate_success(
        self, controller, mock_vector_client, mock_llm_client
    ):
        """Test successful query orchestration."""
        with patch.object(controller, "intent_classifier") as mock_classifier:
            mock_classifier.classify.return_value = "energy_efficiency"

            with patch("agent_project.agents.orchestrator.routing.get_specialist_agent") as mock_get_agent:
                mock_agent = AsyncMock()
                mock_agent.run.return_value = {
                    "final_output": "The minimum R-value for Zone 3 walls is R2.8.",
                    "sources": [],
                    "agent_type": "code_c",
                }
                mock_get_agent.return_value = mock_agent

                payload = {
                    "query": "What is the minimum R-value for Zone 3 walls?",
                    "session_id": "test-session",
                    "user_id": "test-user",
                    "context": {}
                }

                result = await controller.orchestrate(payload)

                assert (
                    result["final_output"]
                    == "The minimum R-value for Zone 3 walls is R2.8."
                )
                assert result["agent_type"] == "code_c"
                assert "sources" in result

    @pytest.mark.asyncio
    async def test_general_query_handling(self, controller, mock_vector_client):
        """Test handling of general queries that don't need specialist routing."""
        with patch.object(controller, "intent_classifier") as mock_classifier:
            mock_classifier.classify.return_value = "unknown"

            with patch("agent_project.agents.orchestrator.routing.get_specialist_agent") as mock_get_agent:
                mock_agent = AsyncMock()
                mock_agent.run.return_value = {
                    "final_output": "General response about building codes.",
                    "sources": [],
                    "agent_type": "code_b",  # Default fallback
                }
                mock_get_agent.return_value = mock_agent

                payload = {
                    "query": "Tell me about building codes",
                    "session_id": "test-session", 
                    "user_id": "test-user",
                    "context": {}
                }

                result = await controller.orchestrate(payload)

                assert "General response" in result["final_output"]
                assert result["agent_type"] == "code_b"

    @pytest.mark.asyncio
    async def test_error_handling(self, controller):
        """Test error handling in controller."""
        with patch.object(controller, "intent_classifier") as mock_classifier:
            mock_classifier.classify.side_effect = Exception("Classification failed")

            payload = {
                "query": "Test query",
                "session_id": "test-session",
                "user_id": "test-user", 
                "context": {}
            }

            result = await controller.orchestrate(payload)

            assert "error" in result["final_output"].lower()
            assert "agent_type" in result

    @pytest.mark.asyncio
    async def test_streaming_response(self, controller):
        """Test streaming query processing."""
        with patch.object(controller, "orchestrate") as mock_orchestrate:
            mock_orchestrate.return_value = {"final_output": "Test response"}

            payload = {
                "query": "Test query",
                "session_id": "test-session",
                "user_id": "test-user",
                "context": {}
            }

            chunks = []
            async for chunk in controller.stream_response(payload):
                chunks.append(chunk)

            assert len(chunks) >= 1
            assert "Test response" in "".join(chunks)


class TestAdvancedOrchestrator:
    """Test suite for the advanced OpenAI Agents SDK orchestrator."""

    @pytest.fixture
    def orchestrator(self):
        """Create advanced orchestrator instance."""
        return AdvancedOrchestrator()

    @pytest.mark.asyncio
    async def test_process_query_with_guardrails(self, orchestrator):
        """Test query processing with guardrails."""
        with patch("agent_project.agents.advanced.agents.Runner.run") as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Safe building code response with disclaimers."
            mock_result.last_agent.name = "Code B Specialist"
            mock_run.return_value = mock_result

            result = await orchestrator.process_query(
                "What are fire safety requirements for Class 5 buildings?"
            )

            assert result["routing_method"] == "native_sdk_handoffs"
            assert "final_output" in result
            assert result["last_agent"] == "Code B Specialist"

    @pytest.mark.asyncio 
    async def test_direct_specialist_access(self, orchestrator):
        """Test direct access to specialist agents."""
        with patch("agent_project.agents.advanced.agents.Runner.run") as mock_run:
            mock_result = AsyncMock()
            mock_result.final_output = "Energy efficiency response."
            mock_result.last_agent.name = "Code C Specialist"
            mock_run.return_value = mock_result

            result = await orchestrator.get_specialist_directly(
                "code_c",
                "What are insulation requirements?"
            )

            assert result["routing_method"] == "direct_specialist"
            assert result["specialist_type"] == "code_c"
            assert "final_output" in result

    @pytest.mark.asyncio
    async def test_invalid_specialist_type(self, orchestrator):
        """Test error handling for invalid specialist types."""
        with pytest.raises(ValueError):
            await orchestrator.get_specialist_directly(
                "invalid_type",
                "Test query"
            )

    @pytest.mark.asyncio
    async def test_guardrail_integration(self, orchestrator):
        """Test that guardrails are properly integrated."""
        # Verify the triage agent has guardrails
        assert hasattr(orchestrator.triage_agent, 'input_guardrails')
        assert hasattr(orchestrator.triage_agent, 'output_guardrails')
        assert len(orchestrator.triage_agent.input_guardrails) > 0

        # Verify specialists have output guardrails
        for agent in orchestrator.specialist_agents.values():
            assert hasattr(agent, 'output_guardrails')
            assert len(agent.output_guardrails) > 0

    @pytest.mark.asyncio
    async def test_handoff_configuration(self, orchestrator):
        """Test that handoffs are properly configured."""
        # Verify the triage agent has handoffs to all specialists
        assert hasattr(orchestrator.triage_agent, 'handoffs')
        assert len(orchestrator.triage_agent.handoffs) == 3  # B, C, H specialists

        # Verify specialists have handoffs to each other
        for agent in orchestrator.specialist_agents.values():
            assert hasattr(agent, 'handoffs')
            if hasattr(agent, 'handoffs') and agent.handoffs:
                assert len(agent.handoffs) >= 1  # At least one handoff


class TestMigrationCompatibility:
    """Test compatibility between old and new systems."""

    @pytest.mark.asyncio
    async def test_controller_vs_advanced_orchestrator(self):
        """Compare basic controller vs advanced orchestrator."""
        controller = AgentController()
        advanced = AdvancedOrchestrator()

        # Both should be able to process basic queries
        assert controller is not None
        assert advanced is not None
        assert hasattr(controller, 'orchestrate')
        assert hasattr(advanced, 'process_query')

    def test_backward_compatibility(self):
        """Test that new implementation maintains compatibility."""
        # Basic controller should still work for existing endpoints
        controller = AgentController()
        assert hasattr(controller, 'orchestrate')
        assert hasattr(controller, 'stream_response')

        # Advanced orchestrator provides enhanced features
        advanced = AdvancedOrchestrator()
        assert hasattr(advanced, 'process_query')
        assert hasattr(advanced, 'get_specialist_directly')
        assert advanced.specialist_agents is not None
        assert advanced.triage_agent is not None