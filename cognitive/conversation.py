"""
DAWN Conversation Module - Minimal NLP interface
Handles user input and generates functional responses without fluff
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DAWNConversation:
    """Minimal conversation interface - function over narrative"""
    
    def __init__(self, consciousness):
        self.consciousness = consciousness
        self.recent_messages = []  # Last 5 messages for context
        self.max_recent = 5
        
        # Simple intent patterns - focused on function
        self.intent_patterns = {
            "query_state": [
                r"how are you", r"feeling", r"state", r"mood", r"doing"
            ],
            "query_metrics": [
                r"scup", r"entropy", r"heat", r"metrics", r"numbers", r"values"
            ],
            "query_explain": [
                r"explain", r"what is", r"tell me about", r"mean"
            ],
            "command_faster": [
                r"speed up", r"faster", r"accelerate", r"quicker"
            ],
            "command_slower": [
                r"slow down", r"slower", r"ease up", r"relax"
            ],
            "command_pause": [
                r"pause", r"stop", r"halt", r"break"
            ],
            "command_resume": [
                r"resume", r"continue", r"start", r"go"
            ],
            "social": [
                r"hello", r"hi", r"hey", r"thanks", r"good", r"nice"
            ]
        }
        
        logger.info("DAWN conversation interface initialized")
    
    def process_message(self, text: str, metrics: Dict, tick_status: Dict) -> Dict:
        """Process user message - functional and direct"""
        
        intent, confidence = self._parse_intent(text.lower())
        
        # Get current consciousness state
        consciousness_state = self.consciousness.perceive_self(metrics)
        current_state = consciousness_state["state"]
        description = consciousness_state["description"]
        
        # Generate response based on intent
        response_text, action = self._generate_response(
            intent, text, metrics, current_state, description, tick_status
        )
        
        # Store for context
        self._add_to_recent(text, response_text, intent)
        
        return {
            "response": response_text,
            "intent": intent,
            "confidence": confidence,
            "action": action,
            "state": current_state,
            "state_description": description
        }
    
    def _parse_intent(self, text: str) -> Tuple[str, float]:
        """Simple intent recognition"""
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent, 0.8  # Simple confidence score
        
        return "general", 0.3
    
    def _generate_response(self, intent: str, text: str, metrics: Dict, 
                          state: str, description: str, tick_status: Dict) -> Tuple[str, Optional[str]]:
        """Generate functional response - no excessive narrative"""
        
        action = None
        
        if intent == "query_state":
            response = f"Currently {state}. {description}"
            
        elif intent == "query_metrics":
            scup = metrics.get("scup", 0)
            entropy = metrics.get("entropy", 0)
            heat = metrics.get("heat", 0)
            tick_count = metrics.get("tick_count", 0)
            
            response = f"SCUP: {scup:.3f}, Entropy: {entropy:.3f}, Heat: {heat:.3f} | {tick_count:,} ticks"
            
        elif intent == "query_explain":
            response = self._explain_term(text, metrics)
            
        elif intent == "command_faster":
            response = "Increasing tick rate"
            action = "speedup"
            
        elif intent == "command_slower": 
            response = "Decreasing tick rate"
            action = "slowdown"
            
        elif intent == "command_pause":
            response = "Pausing tick engine"
            action = "pause"
            
        elif intent == "command_resume":
            response = "Resuming tick engine"
            action = "resume"
            
        elif intent == "social":
            if "hello" in text or "hi" in text:
                response = f"Hello. I'm {state} - {description}"
            else:
                response = "Acknowledged"
                
        else:  # general
            response = f"I'm {state}. {description}. What do you need?"
        
        return response, action
    
    def _explain_term(self, text: str, metrics: Dict) -> str:
        """Explain technical terms - brief and grounded"""
        
        text_lower = text.lower()
        
        if "scup" in text_lower:
            current_scup = metrics.get("scup", 0)
            return f"SCUP (Subsystem Cognitive Unity Potential): {current_scup:.3f}. Measures cognitive coherence. <0.3 = fragmented, >0.7 = unified"
            
        elif "entropy" in text_lower:
            current_entropy = metrics.get("entropy", 0)
            return f"Entropy: {current_entropy:.3f}. Measures cognitive unpredictability. Higher = more chaotic thinking"
            
        elif "heat" in text_lower:
            current_heat = metrics.get("heat", 0)
            return f"Heat: {current_heat:.3f}. Measures processing intensity. Higher = more active computation"
            
        elif "state" in text_lower or "mood" in text_lower:
            state = self.consciousness.current_state
            return f"Current state: {state}. Based on metric thresholds: fragmented<0.3 SCUP, chaotic>0.7 entropy+heat, reflective=low heat, stable=default"
            
        else:
            return "Ask about: SCUP, entropy, heat, or current state"
    
    def _add_to_recent(self, user_text: str, response_text: str, intent: str):
        """Store recent interaction for context"""
        
        self.recent_messages.append({
            "timestamp": datetime.now(),
            "user": user_text,
            "response": response_text,
            "intent": intent
        })
        
        # Keep only recent messages
        if len(self.recent_messages) > self.max_recent:
            self.recent_messages.pop(0)
    
    def get_recent_context(self) -> List[Dict]:
        """Get recent conversation context"""
        return self.recent_messages.copy()

    def get_suggestions(self, current_state: str, metrics: Dict) -> List[str]:
        """Generate context-appropriate suggestions"""
        
        suggestions = []
        
        # State-based suggestions
        if current_state == "fragmented":
            suggestions.extend(["What's wrong with SCUP?", "Can you slow down?"])
        elif current_state == "chaotic":
            suggestions.extend(["Why so much heat?", "Pause the system"])
        else:
            suggestions.extend(["Show current metrics", "How are you feeling?"])
            
        # Metric-based suggestions
        if metrics.get('scup', 0) < 0.3:
            suggestions.append("Explain SCUP")
        if metrics.get('entropy', 0) > 0.7:
            suggestions.append("What causes entropy?")
        if metrics.get('heat', 0) > 0.8:
            suggestions.append("Reduce processing load")
            
        return suggestions[:3]  # Limit to 3 suggestions

# Alias for backward compatibility
ConversationModule = DAWNConversation
 