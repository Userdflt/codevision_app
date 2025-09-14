#!/usr/bin/env python3
"""
Extract specialist agent knowledge for SDK migration.
"""

import sys
import json
import re
sys.path.insert(0, 'src')

from agent_project.core.agents.code_b.agent import CodeBAgent
from agent_project.core.agents.code_c.agent import CodeCAgent
from agent_project.core.agents.code_d.agent import CodeDAgent
from agent_project.core.agents.code_e.agent import CodeEAgent
from agent_project.core.agents.code_f.agent import CodeFAgent
from agent_project.core.agents.code_g.agent import CodeGAgent
from agent_project.core.agents.code_h.agent import CodeHAgent

def extract_knowledge():
    """Extract all specialist knowledge."""
    specialists = {
        'code_b': CodeBAgent(),
        'code_c': CodeCAgent(),
        'code_d': CodeDAgent(),
        'code_e': CodeEAgent(),
        'code_f': CodeFAgent(),
        'code_g': CodeGAgent(),
        'code_h': CodeHAgent(),
    }
    
    knowledge = {}
    for agent_type, agent in specialists.items():
        knowledge[agent_type] = {
            'system_message': agent.get_system_message(),
            'description': agent.__class__.__doc__,
            'expertise_areas': extract_expertise_from_docstring(agent),
            'class_name': agent.__class__.__name__,
            'agent_type': agent.agent_type,
        }
    
    return knowledge

def extract_expertise_from_docstring(agent):
    """Extract expertise areas from agent docstring."""
    doc = agent.__class__.__doc__ or ""
    lines = doc.split('\n')
    expertise = []
    
    in_handles_section = False
    for line in lines:
        line = line.strip()
        if "Handles queries related to:" in line:
            in_handles_section = True
            continue
        if in_handles_section and line.startswith('-'):
            expertise.append(line[1:].strip())
        elif in_handles_section and line == "":
            break
    
    return expertise

def analyze_system_messages(knowledge):
    """Analyze system messages to extract patterns."""
    analysis = {}
    
    for agent_type, data in knowledge.items():
        system_message = data['system_message']
        
        # Extract building code focus
        code_match = re.search(r'Building Code["\s]*([A-H])', system_message)
        code_letter = code_match.group(1) if code_match else agent_type[-1].upper()
        
        # Extract main provisions/clauses
        provisions_match = re.search(r'([A-Z][^.]*provisions[^.]*)', system_message)
        provisions = provisions_match.group(1) if provisions_match else ""
        
        # Extract URL pattern
        url_match = re.search(r'https://[^\s]+', system_message)
        reference_url = url_match.group(0) if url_match else ""
        
        analysis[agent_type] = {
            'code_letter': code_letter,
            'provisions': provisions,
            'reference_url': reference_url,
            'system_message_length': len(system_message),
        }
    
    return analysis

def identify_handoff_triggers(knowledge):
    """Identify potential handoff triggers between agents."""
    handoff_map = {}
    
    # Common handoff scenarios based on domain knowledge
    handoff_patterns = {
        'code_b': ['energy efficiency', 'building envelope', 'thermal performance', 'accessibility', 'universal design'],
        'code_c': ['structural requirements', 'building classification', 'accessibility', 'fire safety'],
        'code_d': ['accessibility', 'fire safety', 'building envelope'],
        'code_e': ['building envelope', 'thermal performance', 'structural'],
        'code_f': ['accessibility', 'building safety', 'fire safety'],
        'code_g': ['energy efficiency', 'accessibility', 'building services'],
        'code_h': ['fire safety', 'egress', 'building classification', 'energy efficiency'],
    }
    
    for agent_type, triggers in handoff_patterns.items():
        handoff_map[agent_type] = triggers
    
    return handoff_map

if __name__ == "__main__":
    print("🔍 Extracting specialist agent knowledge...")
    
    try:
        # Extract knowledge
        knowledge = extract_knowledge()
        print(f"✅ Extracted knowledge from {len(knowledge)} specialists")
        
        # Analyze system messages
        analysis = analyze_system_messages(knowledge)
        print("✅ Analyzed system message patterns")
        
        # Identify handoff triggers
        handoffs = identify_handoff_triggers(knowledge)
        print("✅ Identified handoff triggers")
        
        # Combine all data
        full_extraction = {
            'specialists': knowledge,
            'analysis': analysis,
            'handoff_triggers': handoffs,
            'extraction_metadata': {
                'total_specialists': len(knowledge),
                'total_system_message_length': sum(len(data['system_message']) for data in knowledge.values()),
                'extraction_date': '2024-09-13'
            }
        }
        
        # Save to file
        with open('extracted_knowledge.json', 'w') as f:
            json.dump(full_extraction, f, indent=2)
        
        print("✅ Saved complete extraction to extracted_knowledge.json")
        
        # Print summary
        print(f"\n📊 Extraction Summary:")
        print(f"   Specialists: {len(knowledge)}")
        for agent_type, data in knowledge.items():
            expertise_count = len(data['expertise_areas'])
            msg_length = len(data['system_message'])
            print(f"   {agent_type.upper()}: {expertise_count} expertise areas, {msg_length} char system message")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Review extracted_knowledge.json")
        print(f"   2. Create agent specifications from this data")
        print(f"   3. Proceed to Phase 2: Create SDK Native Tools")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
