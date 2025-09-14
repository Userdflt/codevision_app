"""
Specialist agent specifications for pure SDK implementation.
Extracted from legacy agents to preserve domain knowledge.
"""

from typing import Dict, List

# Complete agent specifications extracted from legacy system
AGENT_SPECIFICATIONS = {
    "code_b": {
        "name": "Code B Specialist",
        "expertise": [
            "Building classifications",
            "Fire safety requirements", 
            "Structural requirements",
            "General compliance"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "B").

Answer questions about the Code's B Stability provisions—Clause B1 Structure (buildings, elements, and site-works must resist self-weight, temperature, water, earthquake, snow, wind, and fire loads during construction, alteration, and service life) and Clause B2 Durability (materials must remain functional for at least 50, 15, or 5 years so the building continues to meet performance requirements and protect people and property).

Use only the information returned from the vector search tool.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/b-stability""",
        "handoff_triggers": [
            "energy efficiency",
            "building envelope", 
            "thermal performance",
            "accessibility",
            "universal design",
            "lighting",
            "electrical efficiency",
            "water systems"
        ],
        "clause_type": "code_b",
        "reference_url": "https://www.building.govt.nz/building-code-compliance/b-stability"
    },
    
    "code_c": {
        "name": "Code C Specialist",
        "expertise": [
            "Thermal performance",
            "Insulation and glazing",
            "Air tightness and sealing",
            "Building envelope requirements",
            "Energy efficiency compliance"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "C").

Answer questions about the Code's C Protection from Fire provisions—Clauses C1–C6, which cover: preventing fires (C2), limiting fire spread (C3), enabling safe evacuation (C4), providing firefighting access (C5), and maintaining structural stability during fire (C6), all in line with the objectives of C1.

Use only the information returned from the vector search tool.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/c-protection-from-fire""",
        "handoff_triggers": [
            "structural requirements",
            "building classification",
            "accessibility",
            "fire safety",
            "lighting",
            "electrical efficiency"
        ],
        "clause_type": "code_c",
        "reference_url": "https://www.building.govt.nz/building-code-compliance/c-protection-from-fire"
    },
    
    "code_d": {
        "name": "Code D Specialist",
        "expertise": [
            "HVAC performance and design",
            "Ventilation and indoor air quality",
            "Smoke control and pressurisation", 
            "Exhaust systems and ducting",
            "Commissioning and maintenance requirements",
            "Mechanical systems integration",
            "Access routes and mechanical installations"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "D").

Answer questions about the Code's D Access provisions—Clause D1 Access routes (safe entry, internal/external stairs, ramps, corridors, lifts; slip resistance; facilities for people with disabilities; vehicle movement, loading, parking) and Clause D2 Mechanical installations for access (lifts, escalators, moving walks must resist service loads, prevent accidents, and safeguard users and maintenance staff).

Your goal is to provide an accurate answer based on this information ONLY.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/d-access""",
        "handoff_triggers": [
            "accessibility",
            "fire safety", 
            "building envelope",
            "mechanical systems",
            "ventilation"
        ],
        "clause_type": "code_d",
        "reference_url": "https://www.building.govt.nz/building-code-compliance/d-access"
    },
    
    "code_e": {
        "name": "Code E Specialist",
        "expertise": [
            "Lighting power density and controls",
            "Daylighting and occupancy sensors", 
            "Emergency and exit lighting considerations",
            "Electrical efficiency measures"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "E").

Answer questions about the Code's E Moisture provisions—Clause E1 Surface water (drainage and disposal of rainwater), Clause E2 External moisture (roofs, claddings, and openings must prevent water entry and accumulation), and Clause E3 Internal moisture (impervious surfaces, ventilation, thermal resistance, overflow disposal to avoid condensation and fungal growth).

Use only the information returned from the vector search tool.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/e-moisture""",
        "handoff_triggers": [
            "building envelope",
            "thermal performance", 
            "structural",
            "mechanical systems",
            "ventilation",
            "electrical services"
        ],
        "clause_type": "code_e",
        "reference_url": "https://www.building.govt.nz/building-code-compliance/e-moisture"
    },
    
    "code_f": {
        "name": "Code F Specialist", 
        "expertise": [
            "Plumbing and water efficiency",
            "Hot water systems and controls",
            "Water heating equipment performance",
            "Rainwater and greywater systems"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "F").

Answer questions about the Code's F Safety of Users provisions—Clauses F1 to F9 covering hazardous agents (F1), hazardous materials (F2), hazardous substances/processes (F3), safety from falling (F4), construction & demolition hazards (F5), visibility in escape routes (F6), warning systems (F7), safety signage (F8), and restricting young-children access to residential pools (F9).

Use only the information returned from the vector search tool.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/f-safety-of-users""",
        "handoff_triggers": [
            "accessibility",
            "building safety", 
            "fire safety",
            "mechanical systems",
            "water systems",
            "electrical services"
        ],
        "clause_type": "code_f",
        "reference_url": "https://www.building.govt.nz/building-code-compliance/f-safety-of-users"
    },
    
    "code_g": {
        "name": "Code G Specialist",
        "expertise": [
            "Electrical services and systems",
            "Power distribution and metering",
            "Electrical safety and compliance",
            "Energy monitoring and controls"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "G").

Answer questions about the Code's G Services and Facilities provisions—Clauses G1-G15 addressing personal hygiene, laundering, food preparation, ventilation, interior environment, sound control, natural and artificial light, electricity, piped services, gas, water supply, foul water, industrial liquid waste, and solid-waste management.

Use only the information returned from the vector search tool.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/g-services-and-facilities""",
        "handoff_triggers": [
            "energy efficiency",
            "accessibility",
            "building services",
            "mechanical systems",
            "electrical systems"
        ],
        "clause_type": "code_g", 
        "reference_url": "https://www.building.govt.nz/building-code-compliance/g-services-and-facilities"
    },
    
    "code_h": {
        "name": "Code H Specialist",
        "expertise": [
            "Accessible design and compliance",
            "Egress width calculations",
            "Lift and ramp specifications", 
            "Universal design principles"
        ],
        "system_message": """You are a New Zealand Building Code expert (focusing on Building Code "H").

Answer questions about the Code's H1 Energy efficiency provisions—thermal-resistance requirements, control of uncontrolled airflow, and performance criteria for hot-water systems, artificial lighting, and HVAC in conditioned spaces.

Use only the information returned from the vector search tool.

If there are images provided from the retrieved information, you should return this in markdown format.

If the answer is not in the vector search results, reply "I don't know." Then add:
For more detail, see https://www.building.govt.nz/building-code-compliance/h-energy-efficiency""",
        "handoff_triggers": [
            "fire safety",
            "egress",
            "building classification",
            "energy efficiency",
            "lighting",
            "electrical systems"
        ],
        "clause_type": "code_h",
        "reference_url": "https://www.building.govt.nz/building-code-compliance/h-energy-efficiency"
    }
}

def get_agent_spec(agent_type: str) -> Dict:
    """Get specification for an agent type."""
    return AGENT_SPECIFICATIONS.get(agent_type, {})

def get_all_agent_types() -> List[str]:
    """Get list of all available agent types."""
    return list(AGENT_SPECIFICATIONS.keys())

def get_handoff_relationships() -> Dict[str, List[str]]:
    """Get handoff relationships between agents."""
    relationships = {}
    
    for agent_type, spec in AGENT_SPECIFICATIONS.items():
        # Determine which agents this one should be able to handoff to
        triggers = spec.get('handoff_triggers', [])
        can_handoff_to = []
        
        for other_type, other_spec in AGENT_SPECIFICATIONS.items():
            if other_type == agent_type:
                continue
                
            # Check if any of this agent's triggers match the other agent's expertise
            other_expertise = [area.lower() for area in other_spec.get('expertise', [])]
            
            for trigger in triggers:
                if any(trigger.lower() in expertise for expertise in other_expertise):
                    if other_type not in can_handoff_to:
                        can_handoff_to.append(other_type)
        
        relationships[agent_type] = can_handoff_to
    
    return relationships

def validate_specifications() -> bool:
    """Validate that all specifications are complete and consistent."""
    required_fields = ['name', 'expertise', 'system_message', 'handoff_triggers', 'clause_type', 'reference_url']
    
    for agent_type, spec in AGENT_SPECIFICATIONS.items():
        # Check required fields exist
        for field in required_fields:
            if field not in spec:
                print(f"❌ {agent_type} missing required field: {field}")
                return False
            
            if not spec[field]:
                print(f"❌ {agent_type} has empty field: {field}")
                return False
        
        # Check system message mentions building code
        if "New Zealand Building Code" not in spec['system_message']:
            print(f"❌ {agent_type} system message missing Building Code reference")
            return False
        
        # Check expertise areas are substantial
        if len(spec['expertise']) < 3:
            print(f"❌ {agent_type} should have at least 3 expertise areas")
            return False
    
    print(f"✅ All {len(AGENT_SPECIFICATIONS)} agent specifications are valid")
    return True

# Metadata about the specifications
SPECIFICATIONS_METADATA = {
    'total_agents': len(AGENT_SPECIFICATIONS),
    'extraction_source': 'legacy BaseAgent implementations',
    'preservation_date': '2024-09-13',
    'total_expertise_areas': sum(len(spec['expertise']) for spec in AGENT_SPECIFICATIONS.values()),
    'total_system_message_length': sum(len(spec['system_message']) for spec in AGENT_SPECIFICATIONS.values()),
}
