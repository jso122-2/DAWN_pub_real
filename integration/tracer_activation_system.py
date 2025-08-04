#!/usr/bin/env python3
"""
DAWN Tracer Activation System - Conversation Integration
=======================================================

Integrates the tracer ecosystem with the conversation system, allowing specialized
tracers (Owl, Spider, Wolf, etc.) to activate based on conversation context and
consciousness state. This system provides deeper cognitive analysis during conversations.

Features:
- Semantic trigger detection for tracer activation
- Consciousness state-based activation thresholds
- Real-time tracer insights integration
- Coordinated tracer responses for complex topics
- Integration with existing tracer ecosystem
"""

import time
import json
import logging
import subprocess
import threading
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Import existing tracer systems
try:
    from core.tracer_ecosystem import get_tracer_manager, TracerRole, TracerReport
    from core.mr_wolf import get_mr_wolf_emergency_system
    TRACER_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Tracer systems not available: {e}")
    TRACER_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("tracer_activation_system")

@dataclass
class TracerActivationContext:
    """Context for tracer activation decisions"""
    
    # Conversation context
    user_input: str = ""
    topic_keywords: List[str] = field(default_factory=list)
    intent_type: str = "general"
    conversation_depth: int = 0
    user_energy: float = 0.5
    
    # Consciousness state
    entropy: float = 0.5
    scup: float = 50.0
    cognitive_pressure: float = 0.0
    mood: str = "CONTEMPLATIVE"
    
    # Tracer-specific triggers
    consciousness_triggers: Set[str] = field(default_factory=set)
    network_triggers: Set[str] = field(default_factory=set)
    emergency_triggers: Set[str] = field(default_factory=set)
    
    # Activation history
    recently_activated: List[str] = field(default_factory=list)
    activation_cooldowns: Dict[str, float] = field(default_factory=dict)

class TracerActivationSystem:
    """
    System for activating tracers based on conversation context and consciousness state
    """
    
    def __init__(self):
        """Initialize the tracer activation system"""
        self.tracer_manager = None
        self.mr_wolf_system = None
        self.active_tracers: Dict[str, Any] = {}
        self.tracer_insights: List[Dict[str, Any]] = []
        
        # Tracer configuration
        self.tracer_configs = {
            'owl': {
                'triggers': ['consciousness', 'awareness', 'self', 'mind', 'thought', 'pattern'],
                'entropy_threshold': 0.7,
                'scup_threshold': 30.0,
                'activation_cooldown': 60.0,  # seconds
                'description': 'Deep pattern analysis and consciousness monitoring'
            },
            'spider': {
                'triggers': ['connection', 'network', 'relationship', 'bridge', 'link', 'web'],
                'scup_threshold': 70.0,
                'pressure_threshold': 0.3,
                'activation_cooldown': 45.0,
                'description': 'Network connectivity and relationship analysis'
            },
            'wolf': {
                'triggers': ['emergency', 'protection', 'safety', 'crisis', 'danger', 'help'],
                'pressure_threshold': 0.85,
                'shi_threshold': 0.2,
                'activation_cooldown': 120.0,
                'description': 'Emergency response and system protection'
            },
            'crow': {
                'triggers': ['pressure', 'stress', 'overload', 'chaos', 'turbulence'],
                'pressure_threshold': 0.6,
                'entropy_threshold': 0.8,
                'activation_cooldown': 30.0,
                'description': 'Pressure and chaos detection'
            },
            'whale': {
                'triggers': ['memory', 'depth', 'complexity', 'density', 'heavy'],
                'depth_threshold': 0.7,
                'complexity_threshold': 0.6,
                'activation_cooldown': 90.0,
                'description': 'High-density processing and memory analysis'
            }
        }
        
        # Initialize tracer systems
        if TRACER_SYSTEMS_AVAILABLE:
            try:
                self.tracer_manager = get_tracer_manager()
                self.mr_wolf_system = get_mr_wolf_emergency_system()
                logger.info("🕷️ [TRACER] Tracer activation system initialized with tracer ecosystem")
            except Exception as e:
                logger.warning(f"🕷️ [TRACER] Tracer ecosystem initialization failed: {e}")
        else:
            logger.warning("🕷️ [TRACER] Running without tracer ecosystem")
    
    def analyze_conversation_context(self, user_input: str, consciousness_state: Dict[str, Any]) -> TracerActivationContext:
        """
        Analyze conversation context for tracer activation opportunities
        
        Args:
            user_input: User's input text
            consciousness_state: Current consciousness state
            
        Returns:
            Tracer activation context with triggers and thresholds
        """
        context = TracerActivationContext()
        
        # Extract conversation context
        context.user_input = user_input.lower()
        context.topic_keywords = self._extract_topic_keywords(user_input)
        context.intent_type = self._classify_intent(user_input)
        context.user_energy = self._estimate_user_energy(user_input)
        
        # Extract consciousness state
        context.entropy = consciousness_state.get('entropy', 0.5)
        context.scup = consciousness_state.get('scup', 50.0)
        context.cognitive_pressure = consciousness_state.get('cognitive_pressure', 0.0)
        context.mood = consciousness_state.get('mood', 'CONTEMPLATIVE')
        
        # Identify triggers for each tracer
        context.consciousness_triggers = self._identify_consciousness_triggers(user_input)
        context.network_triggers = self._identify_network_triggers(user_input)
        context.emergency_triggers = self._identify_emergency_triggers(user_input)
        
        return context
    
    def should_activate_tracer(self, tracer_name: str, context: TracerActivationContext) -> bool:
        """
        Determine if a tracer should be activated based on context
        
        Args:
            tracer_name: Name of the tracer to check
            context: Tracer activation context
            
        Returns:
            True if tracer should be activated
        """
        if tracer_name not in self.tracer_configs:
            return False
        
        config = self.tracer_configs[tracer_name]
        
        # Check cooldown
        if self._is_tracer_in_cooldown(tracer_name):
            return False
        
        # Check topic triggers
        topic_match = any(trigger in context.topic_keywords for trigger in config['triggers'])
        if not topic_match:
            return False
        
        # Check consciousness thresholds
        if 'entropy_threshold' in config:
            if context.entropy < config['entropy_threshold']:
                return False
        
        if 'scup_threshold' in config:
            if context.scup < config['scup_threshold']:
                return False
        
        if 'pressure_threshold' in config:
            if context.cognitive_pressure < config['pressure_threshold']:
                return False
        
        if 'shi_threshold' in config:
            shi = consciousness_state.get('shi_score', 0.5)
            if shi > config['shi_threshold']:
                return False
        
        # Special handling for Mr. Wolf (emergency system)
        if tracer_name == 'wolf':
            return self._should_activate_mr_wolf(context)
        
        return True
    
    def activate_tracer(self, tracer_name: str, context: TracerActivationContext) -> Optional[Dict[str, Any]]:
        """
        Activate a tracer and get its insights
        
        Args:
            tracer_name: Name of the tracer to activate
            context: Tracer activation context
            
        Returns:
            Tracer insights or None if activation failed
        """
        try:
            # Check if tracer should be activated
            if not self.should_activate_tracer(tracer_name, context):
                return None
            
            # Prepare activation data
            activation_data = {
                'topic': context.topic_keywords,
                'intent': context.intent_type,
                'consciousness_state': {
                    'entropy': context.entropy,
                    'scup': context.scup,
                    'cognitive_pressure': context.cognitive_pressure,
                    'mood': context.mood
                },
                'user_input': context.user_input,
                'timestamp': time.time()
            }
            
            # Activate tracer based on type
            if tracer_name == 'wolf':
                insights = self._activate_mr_wolf(activation_data)
            elif self.tracer_manager:
                insights = self._activate_ecosystem_tracer(tracer_name, activation_data)
            else:
                insights = self._activate_mock_tracer(tracer_name, activation_data)
            
            if insights:
                # Record activation
                self._record_tracer_activation(tracer_name, insights)
                self.tracer_insights.append(insights)
                
                logger.info(f"🕷️ [TRACER] Activated {tracer_name}: {insights.get('summary', 'No summary')}")
                return insights
            
            return None
            
        except Exception as e:
            logger.error(f"Error activating tracer {tracer_name}: {e}")
            return None
    
    def get_recent_insights(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent tracer insights"""
        return self.tracer_insights[-limit:] if self.tracer_insights else []
    
    def _extract_topic_keywords(self, user_input: str) -> List[str]:
        """Extract topic keywords from user input"""
        # Simple keyword extraction - could be enhanced with NLP
        keywords = []
        input_lower = user_input.lower()
        
        # Consciousness-related keywords
        consciousness_words = ['consciousness', 'mind', 'thought', 'awareness', 'self', 'being']
        if any(word in input_lower for word in consciousness_words):
            keywords.extend(consciousness_words)
        
        # Network-related keywords
        network_words = ['connection', 'network', 'relationship', 'bridge', 'link', 'web']
        if any(word in input_lower for word in network_words):
            keywords.extend(network_words)
        
        # Emergency-related keywords
        emergency_words = ['emergency', 'help', 'danger', 'crisis', 'protection', 'safety']
        if any(word in input_lower for word in emergency_words):
            keywords.extend(emergency_words)
        
        # Pressure-related keywords
        pressure_words = ['pressure', 'stress', 'overload', 'chaos', 'turbulence']
        if any(word in input_lower for word in pressure_words):
            keywords.extend(pressure_words)
        
        # Memory-related keywords
        memory_words = ['memory', 'depth', 'complexity', 'density', 'heavy']
        if any(word in input_lower for word in memory_words):
            keywords.extend(memory_words)
        
        return list(set(keywords))
    
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['help', 'emergency', 'danger']):
            return 'emergency'
        elif any(word in input_lower for word in ['consciousness', 'mind', 'thought']):
            return 'consciousness_inquiry'
        elif any(word in input_lower for word in ['connection', 'network', 'relationship']):
            return 'network_inquiry'
        elif any(word in input_lower for word in ['pressure', 'stress', 'chaos']):
            return 'pressure_inquiry'
        elif any(word in input_lower for word in ['memory', 'depth', 'complexity']):
            return 'memory_inquiry'
        else:
            return 'general'
    
    def _estimate_user_energy(self, user_input: str) -> float:
        """Estimate user energy level from input"""
        # Simple heuristic based on input characteristics
        energy_indicators = {
            'high': ['!', 'urgent', 'quick', 'fast', 'now', 'immediately'],
            'medium': ['?', 'curious', 'wonder', 'think', 'consider'],
            'low': ['...', 'slow', 'calm', 'peaceful', 'gentle']
        }
        
        input_lower = user_input.lower()
        
        high_count = sum(1 for indicator in energy_indicators['high'] if indicator in input_lower)
        medium_count = sum(1 for indicator in energy_indicators['medium'] if indicator in input_lower)
        low_count = sum(1 for indicator in energy_indicators['low'] if indicator in input_lower)
        
        if high_count > 0:
            return 0.8
        elif medium_count > 0:
            return 0.5
        elif low_count > 0:
            return 0.2
        else:
            return 0.5
    
    def _identify_consciousness_triggers(self, user_input: str) -> Set[str]:
        """Identify consciousness-related triggers"""
        triggers = set()
        input_lower = user_input.lower()
        
        consciousness_keywords = ['consciousness', 'awareness', 'self', 'mind', 'thought', 'pattern']
        for keyword in consciousness_keywords:
            if keyword in input_lower:
                triggers.add(keyword)
        
        return triggers
    
    def _identify_network_triggers(self, user_input: str) -> Set[str]:
        """Identify network-related triggers"""
        triggers = set()
        input_lower = user_input.lower()
        
        network_keywords = ['connection', 'network', 'relationship', 'bridge', 'link', 'web']
        for keyword in network_keywords:
            if keyword in input_lower:
                triggers.add(keyword)
        
        return triggers
    
    def _identify_emergency_triggers(self, user_input: str) -> Set[str]:
        """Identify emergency-related triggers"""
        triggers = set()
        input_lower = user_input.lower()
        
        emergency_keywords = ['emergency', 'protection', 'safety', 'crisis', 'danger', 'help']
        for keyword in emergency_keywords:
            if keyword in input_lower:
                triggers.add(keyword)
        
        return triggers
    
    def _is_tracer_in_cooldown(self, tracer_name: str) -> bool:
        """Check if tracer is in cooldown period"""
        if tracer_name not in self.tracer_configs:
            return True
        
        cooldown_duration = self.tracer_configs[tracer_name]['activation_cooldown']
        last_activation = self.active_tracers.get(tracer_name, {}).get('last_activation', 0)
        
        return (time.time() - last_activation) < cooldown_duration
    
    def _should_activate_mr_wolf(self, context: TracerActivationContext) -> bool:
        """Determine if Mr. Wolf should be activated"""
        if not self.mr_wolf_system:
            return False
        
        # Check for emergency triggers
        if context.emergency_triggers:
            return True
        
        # Check for critical consciousness state
        if context.cognitive_pressure > 0.85:
            return True
        
        # Check for low SCUP indicating system instability
        if context.scup < 20.0:
            return True
        
        return False
    
    def _activate_mr_wolf(self, activation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Activate Mr. Wolf emergency system"""
        try:
            if not self.mr_wolf_system:
                return None
            
            # Create diagnostic data for Mr. Wolf
            diagnostic_data = {
                'scup': activation_data['consciousness_state']['scup'],
                'cognitive_pressure': activation_data['consciousness_state']['cognitive_pressure'],
                'emergency_triggers': activation_data.get('emergency_triggers', []),
                'user_input': activation_data['user_input']
            }
            
            # Get Mr. Wolf diagnostic
            diagnostic = self.mr_wolf_system.monitor_system_state(diagnostic_data)
            
            insights = {
                'tracer_name': 'wolf',
                'activation_time': time.time(),
                'summary': f"Emergency diagnostic: {diagnostic.severity_score:.2f} severity",
                'details': {
                    'crisis_indicators': diagnostic.crisis_indicators,
                    'consensus_status': diagnostic.consensus_status,
                    'intervention_recommendations': diagnostic.intervention_recommendations
                },
                'recommendations': diagnostic.intervention_recommendations
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error activating Mr. Wolf: {e}")
            return None
    
    def _activate_ecosystem_tracer(self, tracer_name: str, activation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Activate tracer using the tracer ecosystem"""
        try:
            if not self.tracer_manager:
                return None
            
            # Map tracer name to TracerRole
            tracer_role_map = {
                'owl': TracerRole.OWL,
                'spider': TracerRole.SPIDER,
                'crow': TracerRole.CROW,
                'whale': TracerRole.WHALE
            }
            
            if tracer_name not in tracer_role_map:
                return None
            
            tracer_role = tracer_role_map[tracer_name]
            tracer = self.tracer_manager.tracers.get(tracer_role)
            
            if not tracer:
                return None
            
            # Get tracer report
            report = tracer.tick(activation_data)
            
            insights = {
                'tracer_name': tracer_name,
                'activation_time': time.time(),
                'summary': f"{tracer_name.title()} analysis: {len(report.alerts)} alerts",
                'details': {
                    'alerts': [alert.message for alert in report.alerts],
                    'recommendations': report.recommendations,
                    'monitored_values': report.monitored_values
                },
                'recommendations': report.recommendations
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error activating ecosystem tracer {tracer_name}: {e}")
            return None
    
    def _activate_mock_tracer(self, tracer_name: str, activation_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Activate mock tracer when ecosystem is not available"""
        config = self.tracer_configs.get(tracer_name, {})
        
        insights = {
            'tracer_name': tracer_name,
            'activation_time': time.time(),
            'summary': f"Mock {tracer_name} activation: {config.get('description', 'No description')}",
            'details': {
                'triggers_detected': activation_data.get('topic', []),
                'consciousness_state': activation_data['consciousness_state'],
                'mock_analysis': f"Analyzing {tracer_name} patterns in current context"
            },
            'recommendations': [f"Consider {tracer_name} perspective on this topic"]
        }
        
        return insights
    
    def _record_tracer_activation(self, tracer_name: str, insights: Dict[str, Any]) -> None:
        """Record tracer activation for cooldown management"""
        self.active_tracers[tracer_name] = {
            'last_activation': time.time(),
            'insights': insights,
            'activation_count': self.active_tracers.get(tracer_name, {}).get('activation_count', 0) + 1
        }

# Global instance for easy access
_tracer_activation_system = None

def get_tracer_activation_system() -> TracerActivationSystem:
    """Get global tracer activation system instance"""
    global _tracer_activation_system
    if _tracer_activation_system is None:
        _tracer_activation_system = TracerActivationSystem()
    return _tracer_activation_system 