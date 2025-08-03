"""
Intent classification tool for routing queries to appropriate agents.
"""

import re
from typing import Dict, List
import structlog

from agent_project.infrastructure.llm.client import LLMClient


logger = structlog.get_logger()


class IntentClassifier:
    """
    Classifies user queries to determine the appropriate specialist agent.
    
    Uses a combination of keyword matching and LLM-based classification
    to route queries to the correct building code specialist.
    """
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.keyword_patterns = self._build_keyword_patterns()
    
    def _build_keyword_patterns(self) -> Dict[str, List[str]]:
        """Build keyword patterns for each building code section."""
        return {
            "general_building": [
                "building classification", "class 1", "class 2", "class 3",
                "fire safety", "egress", "structural", "general building",
                "building code", "compliance", "permit"
            ],
            "energy_efficiency": [
                "energy", "insulation", "r-value", "thermal", "hvac efficiency",
                "energy rating", "stars", "thermal performance", "glazing",
                "wall insulation", "roof insulation", "thermal bridge"
            ],
            "building_envelope": [
                "envelope", "wall", "roof", "floor", "window", "door",
                "weatherproofing", "moisture", "air leakage", "ventilation",
                "building fabric", "external wall", "ceiling"
            ],
            "mechanical_systems": [
                "mechanical", "hvac", "heating", "cooling", "ventilation",
                "air conditioning", "ductwork", "boiler", "heat pump",
                "refrigeration", "mechanical equipment"
            ],
            "lighting": [
                "lighting", "artificial lighting", "natural light", "daylight",
                "illumination", "lux", "lighting control", "emergency lighting",
                "exit lighting", "light fixture"
            ],
            "plumbing": [
                "plumbing", "water", "drainage", "sewer", "pipe", "fixture",
                "tap", "toilet", "basin", "water supply", "waste water",
                "greywater", "rainwater", "water efficiency"
            ],
            "electrical": [
                "electrical", "wiring", "circuit", "switchboard", "outlet",
                "power", "electricity", "electrical safety", "rcd", "rcbo",
                "electrical installation", "cable", "conduit"
            ],
            "accessibility": [
                "accessibility", "disabled access", "wheelchair", "ramp",
                "accessible toilet", "hearing loop", "tactile", "accessible parking",
                "disabled facilities", "universal design", "ada"
            ]
        }
    
    async def classify(self, query: str) -> str:
        """
        Classify the intent of a user query.
        
        Args:
            query: User query text
            
        Returns:
            Intent classification string
        """
        try:
            logger.debug("Classifying query intent", query=query[:100])
            
            # First try keyword-based classification
            keyword_intent = self._classify_by_keywords(query)
            if keyword_intent:
                logger.debug("Intent classified by keywords", intent=keyword_intent)
                return keyword_intent
            
            # Fall back to LLM-based classification
            llm_intent = await self._classify_by_llm(query)
            logger.debug("Intent classified by LLM", intent=llm_intent)
            return llm_intent
            
        except Exception as e:
            logger.error("Intent classification failed", error=str(e))
            return "general_building"  # Default fallback
    
    def _classify_by_keywords(self, query: str) -> str | None:
        """
        Classify intent using keyword pattern matching.
        
        Args:
            query: User query text
            
        Returns:
            Intent classification or None if no match
        """
        query_lower = query.lower()
        
        # Score each intent based on keyword matches
        intent_scores = {}
        
        for intent, keywords in self.keyword_patterns.items():
            score = 0
            for keyword in keywords:
                # Use word boundaries for more accurate matching
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                matches = len(re.findall(pattern, query_lower))
                score += matches
            
            if score > 0:
                intent_scores[intent] = score
        
        # Return highest scoring intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            if intent_scores[best_intent] >= 1:  # Minimum score threshold
                return best_intent
        
        return None
    
    async def _classify_by_llm(self, query: str) -> str:
        """
        Classify intent using LLM when keyword matching fails.
        
        Args:
            query: User query text
            
        Returns:
            Intent classification
        """
        try:
            system_message = """You are an expert in Australian building codes and regulations. Classify the following query into one of these categories:

- general_building: General building requirements, classifications, fire safety, structural
- energy_efficiency: Energy performance, insulation, thermal requirements, HVAC efficiency
- building_envelope: Building fabric, walls, roofs, windows, weatherproofing
- mechanical_systems: HVAC, heating, cooling, ventilation, mechanical equipment
- lighting: Artificial and natural lighting, illumination requirements
- plumbing: Water supply, drainage, plumbing fixtures, water efficiency
- electrical: Electrical systems, wiring, power, electrical safety
- accessibility: Disability access, universal design, accessible facilities

Respond with only the category name, nothing else."""

            prompt = f"Query: {query}\n\nCategory:"
            
            response = await self.llm_client.generate(
                prompt=prompt,
                system_message=system_message,
                temperature=0.1,  # Low temperature for consistent classification
                max_tokens=50
            )
            
            # Clean and validate response
            intent = response.strip().lower()
            
            # Validate that response is one of our known intents
            valid_intents = list(self.keyword_patterns.keys())
            if intent in valid_intents:
                return intent
            
            # If invalid response, try to find partial match
            for valid_intent in valid_intents:
                if valid_intent in intent or intent in valid_intent:
                    return valid_intent
            
            # Final fallback
            return "general_building"
            
        except Exception as e:
            logger.error("LLM intent classification failed", error=str(e))
            return "general_building"
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intent classifications."""
        return list(self.keyword_patterns.keys())