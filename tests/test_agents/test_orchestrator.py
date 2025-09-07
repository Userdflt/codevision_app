"""
Tests for the orchestrator agent.
"""

from unittest.mock import AsyncMock, patch

import pytest

from agent_project.core.agents.orchestrator.agent import (
    OrchestratorAgent,
    OrchestratorState,
)


class TestOrchestratorAgent:
    """Test suite for the orchestrator agent."""

    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator agent instance."""
        return OrchestratorAgent()

    @pytest.mark.asyncio
    async def test_process_query_success(
        self, orchestrator, mock_vector_client, mock_llm_client
    ):
        """Test successful query processing."""
        with patch.object(orchestrator, "intent_classifier") as mock_classifier:
            mock_classifier.classify.return_value = "energy_efficiency"

            with patch.object(orchestrator, "_get_specialist_agent") as mock_get_agent:
                mock_agent = AsyncMock()
                mock_agent.process_query.return_value = {
                    "response": "The minimum R-value for Zone 3 walls is R2.8.",
                    "sources": [],
                }
                mock_get_agent.return_value = mock_agent

                result = await orchestrator.process_query(
                    query="What is the minimum R-value for Zone 3 walls?",
                    session_id="test-session",
                    user_id="test-user",
                )

                assert (
                    result["response"]
                    == "The minimum R-value for Zone 3 walls is R2.8."
                )
                assert result["agent_used"] == "code_c"
                assert "sources" in result

    @pytest.mark.asyncio
    async def test_general_query_handling(self, orchestrator, mock_vector_client):
        """Test handling of general queries that don't need specialist routing."""
        with patch.object(orchestrator, "intent_classifier") as mock_classifier:
            mock_classifier.classify.return_value = "unknown"

            with patch.object(orchestrator, "vector_client", mock_vector_client):
                with patch.object(
                    orchestrator, "_generate_general_response"
                ) as mock_generate:
                    mock_generate.return_value = (
                        "General response about building codes."
                    )

                    result = await orchestrator.process_query(
                        query="Tell me about building codes",
                        session_id="test-session",
                        user_id="test-user",
                    )

                    assert "General response" in result["response"]
                    assert result["agent_used"] == "general"

    @pytest.mark.asyncio
    async def test_error_handling(self, orchestrator):
        """Test error handling in orchestrator."""
        with patch.object(orchestrator, "intent_classifier") as mock_classifier:
            mock_classifier.classify.side_effect = Exception("Classification failed")

            result = await orchestrator.process_query(
                query="Test query", session_id="test-session", user_id="test-user"
            )

            assert "error" in result["response"].lower()
            assert result["agent_used"] == "orchestrator"

    def test_should_route_to_specialist(self, orchestrator):
        """Test specialist routing logic."""
        # Test routing to specialist
        state = OrchestratorState(
            query="test", user_id="test", session_id="test", intent="energy_efficiency"
        )

        result = orchestrator._should_route_to_specialist(state)
        assert result == "specialist"

        # Test routing to general
        state.intent = "unknown_intent"
        result = orchestrator._should_route_to_specialist(state)
        assert result == "general"

        # Test error state
        state.error = "Some error"
        result = orchestrator._should_route_to_specialist(state)
        assert result == "general"

    @pytest.mark.asyncio
    async def test_stream_query(self, orchestrator):
        """Test streaming query processing."""
        with patch.object(orchestrator, "process_query") as mock_process:
            mock_process.return_value = {"response": "Test response"}

            chunks = []
            async for chunk in orchestrator.stream_query(
                query="Test query", session_id="test-session", user_id="test-user"
            ):
                chunks.append(chunk)

            assert len(chunks) == 1
            assert chunks[0] == "Test response"
