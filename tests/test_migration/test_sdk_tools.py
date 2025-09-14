"""
Tests for SDK native tools that replace BaseAgent functionality.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agent_project.agents.tools import (
    # Core functions (testable)
    vector_search_core,
    get_building_code_context_core,
    check_building_code_compliance_core,
    analyze_building_requirements_core,
    get_code_interpretation_core,
    # SDK tools and utilities
    get_tools_for_agent,
    get_tool_descriptions,
    BUILDING_CODE_TOOLS,
    CORE_FUNCTIONS,
    TOOLS_METADATA
)

@pytest.mark.asyncio
class TestSDKCoreTools:
    """Test SDK core tool functionality (testable functions)."""
    
    async def test_vector_search_core_signature(self):
        """Test vector search core has correct signature and handles errors."""
        with patch('agent_project.infrastructure.vector_db.client.VectorDBClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.similarity_search.return_value = []
            mock_client.return_value = mock_instance
            
            result = await vector_search_core(
                query="fire safety requirements",
                clause_type="code_b",
                limit=5
            )
            
            assert isinstance(result, list)
            mock_instance.similarity_search.assert_called_once_with(
                query="fire safety requirements",
                clause_type="code_b",
                limit=5,
                similarity_threshold=0.8
            )
    
    async def test_vector_search_core_with_results(self):
        """Test vector search core formats results correctly."""
        mock_results = [
            {
                "content": "Fire safety requirements include...",
                "metadata": {
                    "source": "NZ Building Code",
                    "section": "C3.1",
                    "clause": "code_c"
                },
                "similarity_score": 0.95
            }
        ]
        
        with patch('agent_project.infrastructure.vector_db.client.VectorDBClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.similarity_search.return_value = mock_results
            mock_client.return_value = mock_instance
            
            result = await vector_search_core(
                query="fire safety requirements",
                clause_type="code_c"
            )
            
            assert len(result) == 1
            assert result[0]["content"] == "Fire safety requirements include..."
            assert result[0]["source"] == "NZ Building Code"
            assert result[0]["section"] == "C3.1"
            assert result[0]["similarity_score"] == 0.95
    
    async def test_vector_search_core_error_handling(self):
        """Test vector search core handles exceptions gracefully."""
        with patch('agent_project.infrastructure.vector_db.client.VectorDBClient') as mock_client:
            mock_client.side_effect = Exception("Database connection failed")
            
            result = await vector_search_core(
                query="test query",
                clause_type="code_b"
            )
            
            assert len(result) == 1
            assert "Vector search failed" in result[0]["content"]
            assert result[0]["metadata"]["error"] is True
    
    async def test_get_building_code_context_core_multiple_topics(self):
        """Test context gathering for multiple topics."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.return_value = [
                {"content": "test content", "source": "test", "similarity_score": 0.9}
            ]
            
            result = await get_building_code_context_core(
                topics=["fire safety", "accessibility"],
                clause_type="code_b"
            )
            
            assert "topics_researched" in result
            assert result["topics_researched"] == ["fire safety", "accessibility"]
            assert "total_sources" in result
            assert result["clause_type"] == "code_b"
            
            # Should have called vector_search_core for each topic
            assert mock_search.call_count == 2
    
    async def test_get_building_code_context_core_deduplication(self):
        """Test that context gathering deduplicates similar content."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            # Return duplicate content
            mock_search.return_value = [
                {"content": "duplicate content", "source": "test1", "similarity_score": 0.9},
                {"content": "duplicate content", "source": "test2", "similarity_score": 0.8}  # Same content
            ]
            
            result = await get_building_code_context_core(
                topics=["topic1"],
                clause_type="code_b"
            )
            
            # Should deduplicate based on content hash
            assert result["total_sources"] == 1  # Deduplicated from 2 to 1
    
    async def test_check_building_code_compliance_core_found(self):
        """Test compliance checking when requirements are found."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.return_value = [
                {"content": "Compliance requirement", "similarity_score": 0.8}
            ]
            
            result = await check_building_code_compliance_core(
                requirement="fire rating",
                building_type="commercial",
                clause_type="code_c"
            )
            
            assert result["compliance_found"] is True
            assert result["requirement"] == "fire rating"
            assert result["building_type"] == "commercial"
            assert result["sources"] == 1
    
    async def test_check_building_code_compliance_core_not_found(self):
        """Test compliance checking when no requirements are found."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.return_value = []
            
            result = await check_building_code_compliance_core(
                requirement="obscure requirement",
                building_type="special",
                clause_type="code_z"
            )
            
            assert result["compliance_found"] is False
            assert "not found in database" in result["message"]
            assert "general_guidance" in result
    
    async def test_analyze_building_requirements_core_general(self):
        """Test building requirements analysis for general type."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.return_value = [
                {"content": "Building requirement", "clause": "code_b"}
            ]
            
            result = await analyze_building_requirements_core(
                building_description="3-story office building",
                analysis_type="general"
            )
            
            assert result["analysis_type"] == "general"
            assert "code_b" in result["clauses_analyzed"]
            assert result["total_requirements"] >= 0
    
    async def test_analyze_building_requirements_core_accessibility(self):
        """Test building requirements analysis for accessibility type."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.return_value = [
                {"content": "Accessibility requirement", "clause": "code_h"}
            ]
            
            result = await analyze_building_requirements_core(
                building_description="public building",
                analysis_type="accessibility"
            )
            
            assert result["analysis_type"] == "accessibility"
            assert "code_h" in result["clauses_analyzed"]
            assert "code_d" in result["clauses_analyzed"]
    
    async def test_get_code_interpretation_core(self):
        """Test code interpretation functionality."""
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.side_effect = [
                [{"content": "Interpretation guidance", "source": "guide"}],  # First call
                [{"content": "Related provision", "source": "code"}]  # Second call
            ]
            
            result = await get_code_interpretation_core(
                regulation_text="Buildings must comply with clause X.Y.Z",
                context_question="How does this apply to residential buildings?"
            )
            
            assert result["interpretation_sources"] == 1
            assert result["related_provisions"] == 1
            assert "Buildings must comply" in result["regulation_text"]
            assert mock_search.call_count == 2  # Called twice (interpretation + related)
    
    async def test_get_code_interpretation_core_long_text(self):
        """Test code interpretation with long regulation text."""
        long_text = "This is a very long regulation text that exceeds 200 characters. " * 5
        
        with patch('agent_project.agents.tools.vector_search_core') as mock_search:
            mock_search.return_value = []
            
            result = await get_code_interpretation_core(
                regulation_text=long_text,
                context_question="How to interpret?"
            )
            
            # Should truncate long text
            assert len(result["regulation_text"]) <= 203  # 200 + "..."
            assert result["regulation_text"].endswith("...")

class TestSDKToolsRegistry:
    """Test SDK tools registry and metadata."""
    
    def test_get_tools_for_agent(self):
        """Test tool registry returns correct tools."""
        tools = get_tools_for_agent("code_b")
        assert len(tools) == 5
        
        # Check that all returned items are FunctionTool objects
        for tool in tools:
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'on_invoke_tool')
    
    def test_get_tool_descriptions(self):
        """Test tool descriptions are available."""
        descriptions = get_tool_descriptions()
        assert len(descriptions) == 5
        assert "vector_search_tool" in descriptions
        assert "Search building code database" in descriptions["vector_search_tool"]
    
    def test_tools_metadata(self):
        """Test tools metadata is accurate."""
        assert TOOLS_METADATA['total_tools'] == 5
        assert TOOLS_METADATA['total_core_functions'] == 5
        assert TOOLS_METADATA['sdk_native'] is True
        assert TOOLS_METADATA['async_support'] is True
        assert TOOLS_METADATA['testable_core'] is True
        assert 'BaseAgent functionality' in TOOLS_METADATA['replacement_for']
    
    def test_core_functions_count(self):
        """Test that core functions match tools count."""
        assert len(CORE_FUNCTIONS) == len(BUILDING_CODE_TOOLS)
        assert len(CORE_FUNCTIONS) == TOOLS_METADATA['total_core_functions']

@pytest.mark.asyncio 
class TestToolsIntegration:
    """Integration tests for tools working together."""
    
    async def test_tools_chain_together(self):
        """Test that core functions can be chained together logically."""
        with patch('agent_project.infrastructure.vector_db.client.VectorDBClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.similarity_search.return_value = [
                {
                    "content": "Fire safety requirements for commercial buildings",
                    "metadata": {"source": "Code C", "section": "C3"},
                    "similarity_score": 0.9
                }
            ]
            mock_client.return_value = mock_instance
            
            # First get context for multiple topics
            context_result = await get_building_code_context_core(
                topics=["fire safety", "commercial buildings"],
                clause_type="code_c"
            )
            
            assert context_result["total_sources"] > 0
            
            # Then check specific compliance
            compliance_result = await check_building_code_compliance_core(
                requirement="fire rating",
                building_type="commercial", 
                clause_type="code_c"
            )
            
            # Both should work with the same mock data
            assert compliance_result["compliance_found"] is True
    
    async def test_error_propagation(self):
        """Test that tool errors are handled gracefully throughout the chain."""
        with patch('agent_project.infrastructure.vector_db.client.VectorDBClient') as mock_client:
            mock_client.side_effect = Exception("Database unavailable")
            
            # All core functions should handle the database error gracefully
            # The key test is that no exceptions are raised - they should return structured error responses
            try:
                results = []
                
                results.append(await vector_search_core("test query"))
                results.append(await get_building_code_context_core(["topic"], "code_b"))
                results.append(await check_building_code_compliance_core("req", "type", "code_b"))
                results.append(await analyze_building_requirements_core("building"))
                results.append(await get_code_interpretation_core("text", "question"))
                
                # All functions completed without raising exceptions
                assert len(results) == 5, "All 5 functions should complete without exceptions"
                
                # Each result should be a valid return type (list or dict)
                for i, result in enumerate(results):
                    assert isinstance(result, (list, dict)), f"Result {i} should be list or dict, got {type(result)}"
                    
                print("✅ All core functions handled database errors gracefully")
                
            except Exception as e:
                pytest.fail(f"Core functions should not raise exceptions, but got: {e}")

class TestToolsCompatibility:
    """Test compatibility with legacy BaseAgent patterns."""
    
    def test_core_functions_replace_baseagent_methods(self):
        """Test that core functions provide equivalent functionality to BaseAgent methods."""
        # Core functions should replace these BaseAgent methods:
        # - retrieve_context -> vector_search_core, get_building_code_context_core
        # - generate_response -> handled by SDK Agent directly
        
        core_function_names = [func.__name__ for func in CORE_FUNCTIONS]
        
        # Should have context retrieval equivalent
        assert "vector_search_core" in core_function_names
        assert "get_building_code_context_core" in core_function_names
        
        # Should have analysis capabilities
        assert "analyze_building_requirements_core" in core_function_names
        assert "check_building_code_compliance_core" in core_function_names
        
        # Should have interpretation capabilities  
        assert "get_code_interpretation_core" in core_function_names
    
    def test_core_functions_async_compatible(self):
        """Test that all core functions are async-compatible."""
        import inspect
        
        for func in CORE_FUNCTIONS:
            assert inspect.iscoroutinefunction(func), f"{func.__name__} should be async"
    
    def test_sdk_tools_have_proper_attributes(self):
        """Test that SDK tools have proper FunctionTool attributes."""
        for tool in BUILDING_CODE_TOOLS:
            # FunctionTool should have required attributes
            assert hasattr(tool, 'name'), f"Tool should have name attribute"
            assert hasattr(tool, 'params_json_schema'), f"Tool should have params_json_schema"
            assert hasattr(tool, 'on_invoke_tool'), f"Tool should have on_invoke_tool method"
            
            # Check the schema has properties
            schema = tool.params_json_schema
            assert 'properties' in schema, f"{tool.name} should have properties in schema"
            
            # Should have at least one parameter
            assert len(schema['properties']) >= 1, f"{tool.name} should have parameters"

if __name__ == "__main__":
    # Run basic validation
    print("🧪 Validating SDK tools...")
    
    # Check tool count
    assert len(BUILDING_CODE_TOOLS) == 5, f"Expected 5 tools, got {len(BUILDING_CODE_TOOLS)}"
    print(f"✅ {len(BUILDING_CODE_TOOLS)} SDK tools defined")
    
    # Check core function count
    assert len(CORE_FUNCTIONS) == 5, f"Expected 5 core functions, got {len(CORE_FUNCTIONS)}"
    print(f"✅ {len(CORE_FUNCTIONS)} core functions defined")
    
    # Check all tools are FunctionTool objects
    for tool in BUILDING_CODE_TOOLS:
        assert hasattr(tool, 'name'), f"{tool} should be a FunctionTool with name attribute"
        assert hasattr(tool, 'on_invoke_tool'), f"{tool} should be a FunctionTool with on_invoke_tool"
    print("✅ All tools are FunctionTool objects")
    
    # Check all core functions are callable
    for func in CORE_FUNCTIONS:
        assert callable(func), f"{func} is not callable"
    print("✅ All core functions are callable")
    
    # Check metadata
    assert TOOLS_METADATA['total_tools'] == len(BUILDING_CODE_TOOLS)
    assert TOOLS_METADATA['total_core_functions'] == len(CORE_FUNCTIONS)
    print("✅ Metadata is accurate")
    
    print("🎉 SDK tools validation passed!")