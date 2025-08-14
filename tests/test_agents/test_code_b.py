"""
Tests for Code B specialist agent.
"""

import pytest
from unittest.mock import AsyncMock, patch

from agent_project.core.agents.code_b.agent import CodeBAgent


class TestCodeBAgent:
    """Test suite for Code B agent."""
    
    @pytest.fixture
    def code_b_agent(self):
        """Create Code B agent instance."""
        return CodeBAgent()
    
    @pytest.mark.asyncio
    async def test_process_query_success(self, code_b_agent, sample_vector_search_results):
        """Test successful query processing."""
        with patch.object(code_b_agent, 'retrieve_context') as mock_retrieve:
            mock_retrieve.return_value = sample_vector_search_results
            
            with patch.object(code_b_agent, 'generate_response') as mock_generate:
                mock_generate.return_value = "Class 1 buildings are houses and other small residential buildings."
                
                result = await code_b_agent.process_query(
                    query="What are Class 1 buildings?",
                    session_id="test-session",
                    user_id="test-user"
                )
                
                assert result["response"] == "Class 1 buildings are houses and other small residential buildings."
                assert result["agent_type"] == "code_b"
                assert len(result["sources"]) == 2
    
    @pytest.mark.asyncio
    async def test_error_handling(self, code_b_agent):
        """Test error handling in Code B agent."""
        with patch.object(code_b_agent, 'retrieve_context') as mock_retrieve:
            mock_retrieve.side_effect = Exception("Database error")
            
            result = await code_b_agent.process_query(
                query="Test query",
                session_id="test-session",
                user_id="test-user"
            )
            
            assert "error" in result["response"].lower()
            assert result["agent_type"] == "code_b"
            assert "error" in result
    
    def test_system_message(self, code_b_agent):
        """Test Code B specific system message."""
        system_message = code_b_agent.get_system_message()
        
        assert "New Zealand Building Code" in system_message
        assert "Building Code “B”" in system_message
        assert "B1" in system_message or "Structure" in system_message
        assert "B2" in system_message or "Durability" in system_message
        assert "vectorstore" in system_message.lower()
    
    @pytest.mark.asyncio
    async def test_retrieve_context_filters(self, code_b_agent):
        """Test that Code B agent uses appropriate filters."""
        with patch.object(code_b_agent, 'vector_client') as mock_client:
            mock_client.similarity_search.return_value = []
            
            await code_b_agent.retrieve_context("test query")
            
            # Verify the call was made with code_b clause type
            mock_client.similarity_search.assert_called_once()
            call_args = mock_client.similarity_search.call_args
            assert call_args[1]["clause_type"] == "code_b"