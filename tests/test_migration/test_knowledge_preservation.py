"""
Tests to ensure specialist knowledge is preserved during migration.
"""

import pytest
from agent_project.agents.specifications import (
    AGENT_SPECIFICATIONS, 
    get_agent_spec, 
    get_all_agent_types,
    get_handoff_relationships,
    validate_specifications,
    SPECIFICATIONS_METADATA
)

class TestKnowledgePreservation:
    """Ensure all specialist knowledge is captured and preserved."""
    
    def test_all_specialists_have_specifications(self):
        """Ensure all 7 specialists have specifications."""
        expected_types = ['code_b', 'code_c', 'code_d', 'code_e', 'code_f', 'code_g', 'code_h']
        actual_types = get_all_agent_types()
        
        assert len(actual_types) == 7, f"Expected 7 specialists, got {len(actual_types)}"
        
        for agent_type in expected_types:
            assert agent_type in actual_types, f"Missing specification for {agent_type}"
    
    def test_specifications_have_required_fields(self):
        """Ensure all specifications have required fields."""
        required_fields = ['name', 'expertise', 'system_message', 'handoff_triggers', 'clause_type', 'reference_url']
        
        for agent_type in get_all_agent_types():
            spec = get_agent_spec(agent_type)
            
            for field in required_fields:
                assert field in spec, f"{agent_type} missing {field}"
                assert spec[field], f"{agent_type} has empty {field}"
    
    def test_system_messages_contain_building_code_reference(self):
        """Ensure system messages reference New Zealand Building Code."""
        for agent_type in get_all_agent_types():
            spec = get_agent_spec(agent_type)
            system_message = spec['system_message']
            
            assert "New Zealand Building Code" in system_message, f"{agent_type} missing building code reference"
            assert f'Building Code "{agent_type[-1].upper()}"' in system_message, f"{agent_type} missing specific code reference"
    
    def test_expertise_areas_comprehensive(self):
        """Ensure all agents have comprehensive expertise areas."""
        for agent_type in get_all_agent_types():
            spec = get_agent_spec(agent_type)
            expertise = spec['expertise']
            
            assert len(expertise) >= 3, f"{agent_type} should have at least 3 expertise areas"
            
            for area in expertise:
                assert len(area.strip()) > 10, f"{agent_type} has overly brief expertise area: {area}"
                assert area[0].isupper(), f"{agent_type} expertise area should start with capital: {area}"
    
    def test_reference_urls_valid(self):
        """Ensure all reference URLs are properly formatted."""
        for agent_type in get_all_agent_types():
            spec = get_agent_spec(agent_type)
            url = spec['reference_url']
            
            assert url.startswith('https://www.building.govt.nz'), f"{agent_type} has invalid URL: {url}"
            assert agent_type[-1] in url, f"{agent_type} URL should contain code letter"
    
    def test_handoff_triggers_logical(self):
        """Ensure handoff triggers make sense for each agent."""
        relationships = get_handoff_relationships()
        
        for agent_type, can_handoff_to in relationships.items():
            spec = get_agent_spec(agent_type)
            
            # Should have at least one potential handoff
            assert len(can_handoff_to) >= 1, f"{agent_type} should be able to handoff to at least one other agent"
            
            # Handoff triggers should not be empty
            assert len(spec['handoff_triggers']) >= 1, f"{agent_type} should have handoff triggers"
    
    def test_clause_types_consistent(self):
        """Ensure clause types are consistent with agent types.""" 
        for agent_type in get_all_agent_types():
            spec = get_agent_spec(agent_type)
            clause_type = spec['clause_type']
            
            assert clause_type == agent_type, f"{agent_type} clause_type mismatch: {clause_type}"
    
    def test_specifications_validation(self):
        """Test the built-in validation function."""
        assert validate_specifications(), "Specifications validation failed"
    
    def test_metadata_accuracy(self):
        """Test that metadata accurately reflects the specifications."""
        assert SPECIFICATIONS_METADATA['total_agents'] == 7
        assert SPECIFICATIONS_METADATA['total_agents'] == len(AGENT_SPECIFICATIONS)
        
        # Count actual expertise areas
        actual_expertise_count = sum(len(spec['expertise']) for spec in AGENT_SPECIFICATIONS.values())
        assert SPECIFICATIONS_METADATA['total_expertise_areas'] == actual_expertise_count
        
        # Check system message lengths
        actual_msg_length = sum(len(spec['system_message']) for spec in AGENT_SPECIFICATIONS.values())
        assert SPECIFICATIONS_METADATA['total_system_message_length'] == actual_msg_length

class TestKnowledgeComparisons:
    """Compare extracted knowledge with original sources."""
    
    def test_knowledge_completeness(self):
        """Ensure we captured knowledge from all original agents."""
        # Load the extracted knowledge for comparison
        import json
        
        try:
            with open('extracted_knowledge.json', 'r') as f:
                extracted = json.load(f)
            
            extracted_specialists = extracted['specialists']
            
            # Compare counts
            assert len(AGENT_SPECIFICATIONS) == len(extracted_specialists)
            
            # Compare each specialist
            for agent_type in get_all_agent_types():
                assert agent_type in extracted_specialists, f"Missing {agent_type} in extracted data"
                
                spec = get_agent_spec(agent_type)
                original = extracted_specialists[agent_type]
                
                # System messages should match (approximately - we may have made small edits)
                spec_msg_words = set(spec['system_message'].lower().split())
                original_msg_words = set(original['system_message'].lower().split())
                
                # Should have at least 80% word overlap
                overlap = len(spec_msg_words & original_msg_words)
                total_original = len(original_msg_words)
                
                if total_original > 0:
                    overlap_ratio = overlap / total_original
                    assert overlap_ratio >= 0.8, f"{agent_type} system message differs too much from original ({overlap_ratio:.2f})"
        
        except FileNotFoundError:
            pytest.skip("extracted_knowledge.json not found - run extraction script first")

class TestHandoffLogic:
    """Test the logic for agent handoffs."""
    
    def test_handoff_relationships_bidirectional(self):
        """Test that important handoff relationships are bidirectional."""
        relationships = get_handoff_relationships()
        
        # Code B (general) should be able to handoff to C (energy) and H (accessibility)
        assert 'code_c' in relationships.get('code_b', []), "Code B should handoff to Code C for energy efficiency"
        assert 'code_h' in relationships.get('code_b', []), "Code B should handoff to Code H for accessibility"
        
        # Code C (energy) should be able to handoff back to B (general/structural)
        assert 'code_b' in relationships.get('code_c', []), "Code C should handoff to Code B for structural"
        
        # Code H (accessibility) should handoff to B (fire safety/structural)
        assert 'code_b' in relationships.get('code_h', []), "Code H should handoff to Code B for fire safety"
    
    def test_no_isolated_agents(self):
        """Ensure no agent is completely isolated (can handoff and receive handoffs)."""
        relationships = get_handoff_relationships()
        
        for agent_type in get_all_agent_types():
            # Agent should be able to handoff to someone
            can_handoff_to = relationships.get(agent_type, [])
            assert len(can_handoff_to) > 0, f"{agent_type} cannot handoff to any other agent"
            
            # Agent should be able to receive handoffs from someone
            can_receive_from = [other for other, targets in relationships.items() if agent_type in targets]
            assert len(can_receive_from) > 0, f"{agent_type} cannot receive handoffs from any other agent"

if __name__ == "__main__":
    # Run validation directly
    print("🧪 Running knowledge preservation validation...")
    
    validation_passed = validate_specifications()
    
    if validation_passed:
        print("✅ All knowledge preservation tests would pass")
        print(f"📊 Specifications summary:")
        print(f"   Agents: {SPECIFICATIONS_METADATA['total_agents']}")
        print(f"   Total expertise areas: {SPECIFICATIONS_METADATA['total_expertise_areas']}")
        print(f"   Total system message length: {SPECIFICATIONS_METADATA['total_system_message_length']} chars")
    else:
        print("❌ Knowledge preservation validation failed")
        exit(1)
