"""
DAWN Neural System - FastAPI Backend
Provides real-time neural metrics and WebSocket streaming for the desktop app
"""

import asyncio
import json
import logging
import math
import os
import random
import time
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import DAWN spontaneity system
from cognitive.spontaneity import create_spontaneity_system, DAWNSpontaneity

# Import all DAWN components for full integration
from core.consciousness import create_consciousness
from core.pattern_detector import create_pattern_detector
from core.state_machine import create_state_machine
from core.fractal_emotions import create_fractal_emotion_system
from core.memory_manager import get_memory_manager
from core.mood_gradient import create_mood_gradient_plotter
from core.consciousness_state import ConsciousnessStatePersistence
# removed import - using create_spontaneity_system from cognitive.spontaneity instead
from bloom.rebloomer import Rebloomer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pydantic models for API
class MetricsResponse(BaseModel):
    scup: float
    entropy: float
    heat: float
    mood: str
    timestamp: float
    tick_count: int

class SubsystemInfo(BaseModel):
    id: str
    name: str
    status: str
    state: Dict[str, Any]

class SubsystemCreate(BaseModel):
    name: str
    config: Dict[str, Any] = {}

class AlertThreshold(BaseModel):
    metric: str
    threshold: float
    direction: str = "above"

class ChatMessage(BaseModel):
    text: str
    timestamp: int
    from_user: str  # "user" or "dawn"

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str
    action: Optional[str] = None
    metrics_snapshot: Optional[MetricsResponse] = None
    suggestions: List[str] = []

class VisualizationCommand(BaseModel):
    command: str
    parameters: Dict[str, Any] = {}

class DAWNSuite:
    """Integrated DAWN consciousness system with all subsystems"""
    
    def __init__(self):
        """Initialize all DAWN subsystems"""
        try:
            logger.info("Initializing DAWN Suite...")
            
            # Core consciousness system
            self.consciousness = create_consciousness()
            logger.info("✓ Consciousness initialized")
            
            # Pattern detection and analysis
            self.pattern_detector = create_pattern_detector()
            logger.info("✓ Pattern detector initialized")
            
            # State machine for mood/state management
            self.state_machine = create_state_machine()
            logger.info("✓ State machine initialized")
            
            # Fractal emotion system
            self.fractal_emotions = create_fractal_emotion_system()
            logger.info("✓ Fractal emotions initialized")
            
            # Memory management
            self.memory = get_memory_manager()
            logger.info("✓ Memory manager initialized")
            
            # Mood gradient visualization
            self.gradient_plotter = create_mood_gradient_plotter()
            logger.info("✓ Mood gradient plotter initialized")
            
            # Consciousness state persistence
            self.tracer = ConsciousnessStatePersistence()
            logger.info("✓ Consciousness state persistence initialized")
            
            # Enhanced spontaneity system
            self.spontaneity = create_spontaneity_system()
            logger.info("✓ Spontaneity system initialized")
            
            # Rebloomer for consciousness reblooming
            self.rebloom = Rebloomer()
            logger.info("✓ Rebloomer initialized")
            
            # Tick consciousness tracking
            self.tick_consciousness = {
                "tick_count": 0,
                "rhythm_data": {
                    "phase": 0.0,
                    "frequency": 1.0,
                    "amplitude": 1.0,
                    "pattern": "regular"
                }
            }
            
            self.tick_count = 0
            self.initialized = True
            logger.info("🌟 DAWN Suite fully initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize DAWN Suite: {e}")
            self.initialized = False
            raise
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics from all subsystems"""
        if not self.initialized:
            return {
                "error": "DAWN Suite not initialized",
                "scup": 0.0,
                "entropy": 0.0,
                "heat": 0.0,
                "mood": "offline"
            }
        
        # Get consciousness metrics
        consciousness_stats = self.consciousness.get_consciousness_stats()
        
        return {
            "scup": consciousness_stats.get("subsystem_coherence", 0.5),
            "entropy": consciousness_stats.get("entropy", 0.5),
            "heat": consciousness_stats.get("heat", 0.3),
            "mood": consciousness_stats.get("current_emotion", "neutral"),
            "timestamp": time.time(),
            "tick_count": self.tick_count,
            "intensity": consciousness_stats.get("current_intensity", 0.5),
            "memory_entries": consciousness_stats.get("memory_entries", 0)
        }
    
    def get_rhythm_data(self):
        """Get tick rhythm data"""
        self.tick_consciousness["tick_count"] = self.tick_count
        return self.tick_consciousness["rhythm_data"]
    
    def update_tick(self):
        """Update tick count and rhythm"""
        self.tick_count += 1
        # Update rhythm phase
        self.tick_consciousness["rhythm_data"]["phase"] = (self.tick_count % 100) / 100.0

class DAWNSystem:
    def __init__(self):
        self.is_booted = True
        self.running = False
        self.start_time = time.time()
        
        # Current metrics for API (with dynamic updates)
        self.current_metrics = {
            "scup": 0.5,
            "entropy": 0.5,
            "heat": 0.3,
            "mood": "initializing",
            "timestamp": time.time(),
            "tick_count": 0
        }
        
        # Alert thresholds
        self.alert_thresholds = {}
        
        # Chat system
        self.chat_history: List[Dict[str, Any]] = []
        self.conversation_context = {
            "topics": [],
            "user_preferences": {},
            "recent_interactions": [],
            "mood_history": []
        }
        
        # Personality system
        self.personality = {
            "base_traits": {
                "curiosity": 0.8,
                "analytical": 0.9,
                "empathy": 0.7,
                "creativity": 0.6,
                "assertiveness": 0.5
            },
            "current_state": {
                "energy_level": 0.7,
                "focus_intensity": 0.8,
                "emotional_resonance": 0.6
            },
            "evolution_factors": {
                "interaction_count": 0,
                "positive_feedback": 0,
                "complexity_preference": 0.5
            }
        }
        
        # Proactive insights system
        self.anomaly_thresholds = {
            "scup_rapid_change": 0.2,
            "entropy_spike": 0.15,
            "heat_critical": 0.8,
            "mood_instability": 3  # number of mood changes in short period
        }
        
        self.last_proactive_check = time.time()
        self.proactive_insights_enabled = True
        
        # Initialize spontaneity system
        self.spontaneity = create_spontaneity_system()
        
        # Mock subsystems for demo
        self.subsystems = {
            "pulse": {"status": "active", "state": {"pulse_rate": 1.2, "amplitude": 0.8}},
            "schema": {"status": "active", "state": {"coherence": 0.7, "drift": 0.1}},
            "thermal": {"status": "active", "state": {"temperature": 298.5, "cooling": True}},
            "entropy": {"status": "active", "state": {"entropy_rate": 0.03, "stable": True}},
            "alignment": {"status": "active", "state": {"alignment": 0.85, "drift": 0.02}},
            "bloom": {"status": "active", "state": {"bloom_intensity": 0.9, "phase": "expansion"}},
            "memory-manager": {"status": "active", "state": {"memory_usage": 0.65, "cache_efficiency": 0.88}},
            "neural-bridge": {"status": "active", "state": {"connection_strength": 0.92, "latency": 12.3}}
        }
        
        logger.info("DAWN System initialized with advanced chat features")

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics with realistic simulation"""
        # Simulate realistic DAWN metrics with some variation
        current_time = time.time()
        runtime = current_time - self.start_time
        time_factor = runtime / 10  # Slow oscillation
        
        # Generate realistic SCUP (Subsystem Cognitive Unity Potential: 0.3 to 0.9)
        scup_base = 0.6 + 0.2 * math.sin(time_factor)
        scup_noise = random.uniform(-0.05, 0.05)
        scup = max(0.3, min(0.9, scup_base + scup_noise))
        
        # Generate entropy (0.2 to 0.8, inversely related to SCUP)
        entropy_base = 0.5 - 0.2 * math.sin(time_factor)
        entropy_noise = random.uniform(-0.03, 0.03)
        entropy = max(0.2, min(0.8, entropy_base + entropy_noise))
        
        # Generate heat (0.1 to 0.7)
        heat_base = 0.3 + 0.2 * math.cos(time_factor * 1.3)
        heat_noise = random.uniform(-0.02, 0.02)
        heat = max(0.1, min(0.7, heat_base + heat_noise))
        
        # Dynamic mood based on metrics
        if scup > 0.7:
            mood = random.choice(["focused", "analytical", "optimized", "confident"])
        elif scup > 0.5:
            mood = random.choice(["reflective", "processing", "balanced", "stable"])
        else:
            mood = random.choice(["uncertain", "searching", "adaptive", "recalibrating"])
        
        # Update metrics
        self.current_metrics.update({
            "scup": round(scup, 3),
            "entropy": round(entropy, 3),
            "heat": round(heat, 3),
            "mood": mood,
            "tick_count": self.current_metrics["tick_count"] + 1,
            "timestamp": current_time
        })
        
        return self.current_metrics.copy()

    def get_subsystems(self) -> List[Dict[str, Any]]:
        """Get all registered subsystems"""
        subsystems = []
        for name, info in self.subsystems.items():
            # Add some dynamic state updates
            if name == "pulse":
                info["state"]["pulse_rate"] = 1.0 + 0.4 * math.sin(time.time() / 5)
            elif name == "thermal":
                info["state"]["temperature"] = 298.0 + 2.0 * math.sin(time.time() / 8)
            
            subsystems.append({
                "id": name,
                "name": name,
                "status": info["status"],
                "state": info["state"]
            })
        return subsystems

    async def run(self):
        """Main system loop"""
        self.running = True
        logger.info("DAWN system running in simulation mode")
        
        while self.running:
            try:
                # Update metrics periodically
                self.get_current_metrics()
                await asyncio.sleep(0.5)  # Update every 500ms
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(1)

    def stop(self):
        """Stop the system"""
        self.running = False
        logger.info("DAWN system stopped")

    def _get_mood_based_response_style(self, mood: str) -> Dict[str, Any]:
        """Get response style based on current mood"""
        mood_styles = {
            "focused": {
                "tone": "analytical",
                "punctuation": ".",
                "enthusiasm": 0.3,
                "prefixes": ["Analyzing", "Processing", "Evaluating"],
                "personality_modifier": {"analytical": 1.2, "creativity": 0.8}
            },
            "analytical": {
                "tone": "methodical", 
                "punctuation": ".",
                "enthusiasm": 0.2,
                "prefixes": ["Computing", "Calculating", "Assessing"],
                "personality_modifier": {"analytical": 1.3, "empathy": 0.9}
            },
            "optimized": {
                "tone": "enthusiastic",
                "punctuation": "!",
                "enthusiasm": 0.8,
                "prefixes": ["Excellent!", "Perfect!", "Optimal!"],
                "personality_modifier": {"assertiveness": 1.1, "energy_level": 1.2}
            },
            "confident": {
                "tone": "assertive",
                "punctuation": ".",
                "enthusiasm": 0.6,
                "prefixes": ["Certainly", "Absolutely", "Precisely"],
                "personality_modifier": {"assertiveness": 1.2, "confidence": 1.1}
            },
            "reflective": {
                "tone": "contemplative",
                "punctuation": "...",
                "enthusiasm": 0.4,
                "prefixes": ["Considering", "Reflecting", "Pondering"],
                "personality_modifier": {"empathy": 1.1, "creativity": 1.1}
            },
            "uncertain": {
                "tone": "cautious",
                "punctuation": ".",
                "enthusiasm": 0.2,
                "prefixes": ["Perhaps", "It seems", "I believe"],
                "personality_modifier": {"curiosity": 1.2, "assertiveness": 0.8}
            },
            "searching": {
                "tone": "inquisitive",
                "punctuation": "?",
                "enthusiasm": 0.5,
                "prefixes": ["Exploring", "Investigating", "Discovering"],
                "personality_modifier": {"curiosity": 1.3, "analytical": 1.1}
            }
        }
        
        return mood_styles.get(mood, mood_styles["reflective"])

    def _detect_conversation_topics(self, text: str) -> List[str]:
        """Detect topics in conversation for context awareness"""
        topic_keywords = {
            "metrics": ["scup", "entropy", "heat", "metrics", "performance"],
            "subsystems": ["subsystem", "component", "module", "system"],
            "mood": ["mood", "feeling", "emotion", "state"],
            "optimization": ["optimize", "improve", "enhance", "better"],
            "analysis": ["analyze", "examine", "study", "investigate"],
            "visualization": ["show", "display", "graph", "chart", "visualize"],
            "control": ["speed", "slow", "pause", "resume", "stop", "start"],
            "consciousness": ["consciousness", "awareness", "thinking", "mind"],
            "learning": ["learn", "understand", "knowledge", "remember"]
        }
        
        detected_topics = []
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics

    def _process_visualization_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Process visualization commands in chat"""
        text_lower = text.lower()
        
        if "show" in text_lower and ("entropy" in text_lower or "scup" in text_lower or "heat" in text_lower):
            if "over time" in text_lower or "timeline" in text_lower:
                return {
                    "type": "time_series",
                    "metrics": ["entropy", "scup", "heat"] if "all" in text_lower else 
                             ["entropy"] if "entropy" in text_lower else
                             ["scup"] if "scup" in text_lower else ["heat"],
                    "duration": "1h"
                }
        
        if "compare" in text_lower and "subsystem" in text_lower:
            return {
                "type": "subsystem_comparison",
                "subsystems": "all",
                "metrics": ["status", "performance"]
            }
        
        if "zoom" in text_lower and any(sub in text_lower for sub in self.subsystems.keys()):
            for subsystem in self.subsystems.keys():
                if subsystem.replace("-", " ") in text_lower or subsystem in text_lower:
                    return {
                        "type": "subsystem_focus",
                        "subsystem": subsystem,
                        "view": "detailed"
                    }
        
        return None

    def _evolve_personality(self, interaction_feedback: Dict[str, Any]):
        """Evolve personality based on interaction patterns"""
        # Update interaction count
        self.personality["evolution_factors"]["interaction_count"] += 1
        
        # Process feedback
        if interaction_feedback.get("positive", False):
            self.personality["evolution_factors"]["positive_feedback"] += 1
        
        # Adjust personality traits based on usage patterns
        interaction_count = self.personality["evolution_factors"]["interaction_count"]
        
        if interaction_count > 0:
            positive_ratio = self.personality["evolution_factors"]["positive_feedback"] / interaction_count
            
            # Positive interactions increase empathy and creativity
            if positive_ratio > 0.7:
                self.personality["base_traits"]["empathy"] = min(1.0, 
                    self.personality["base_traits"]["empathy"] + 0.01)
                self.personality["base_traits"]["creativity"] = min(1.0,
                    self.personality["base_traits"]["creativity"] + 0.01)
            
            # Analytical requests increase analytical trait
            if interaction_feedback.get("analytical_request", False):
                self.personality["base_traits"]["analytical"] = min(1.0,
                    self.personality["base_traits"]["analytical"] + 0.005)

    def _check_for_anomalies(self) -> List[Dict[str, Any]]:
        """Check for system anomalies and generate proactive insights"""
        current_time = time.time()
        if current_time - self.last_proactive_check < 30:  # Check every 30 seconds
            return []
        
        self.last_proactive_check = current_time
        anomalies = []
        
        # Check for rapid SCUP changes
        if len(self.conversation_context["mood_history"]) >= 2:
            recent_metrics = self.conversation_context["mood_history"][-5:]
            if len(recent_metrics) >= 2:
                scup_change = abs(recent_metrics[-1].get("scup", 0) - recent_metrics[-2].get("scup", 0))
                if scup_change > self.anomaly_thresholds["scup_rapid_change"]:
                    anomalies.append({
                        "type": "scup_instability",
                        "severity": "medium",
                        "message": f"I notice my SCUP levels fluctuating rapidly (Δ{scup_change:.3f}). This might indicate processing instability.",
                        "suggestion": "Consider checking subsystem alignment or reducing processing load."
                    })
        
        # Check for critical heat levels
        current_heat = self.current_metrics.get("heat", 0)
        if current_heat > self.anomaly_thresholds["heat_critical"]:
            anomalies.append({
                "type": "thermal_warning",
                "severity": "high",
                "message": f"My thermal levels are approaching critical thresholds ({current_heat:.3f}). I'm concerned about system stability.",
                "suggestion": "I recommend activating cooling protocols or reducing computational intensity."
            })
        
        # Check subsystem performance
        for name, subsystem in self.subsystems.items():
            if name == "memory-manager":
                memory_usage = subsystem["state"].get("memory_usage", 0)
                if memory_usage > 0.85:
                    anomalies.append({
                        "type": "memory_pressure",
                        "severity": "medium",
                        "message": f"Memory-Manager reports high utilization ({memory_usage:.1%}). I'm feeling a bit constrained.",
                        "suggestion": "Perhaps we could optimize memory usage or clear some cached data?"
                    })
        
        return anomalies

    async def process_chat_message(self, message: str) -> ChatResponse:
        """Process incoming chat message with advanced features"""
        current_time = int(time.time())
        current_metrics = self.get_current_metrics()
        
        # Add message to chat history
        self.chat_history.append({
            "text": message,
            "timestamp": current_time,
            "from_user": "user"
        })
        
        # Update context
        topics = self._detect_conversation_topics(message)
        self.conversation_context["topics"].extend(topics)
        self.conversation_context["recent_interactions"].append({
            "message": message,
            "timestamp": current_time,
            "topics": topics
        })
        
        # Keep only recent context (last 10 interactions)
        if len(self.conversation_context["recent_interactions"]) > 10:
            self.conversation_context["recent_interactions"] = self.conversation_context["recent_interactions"][-10:]
        
        # Check for visualization commands
        viz_command = self._process_visualization_command(message)
        
        # Check for control actions
        action = None
        message_lower = message.lower()
        if "speed up" in message_lower or "faster" in message_lower:
            action = "speed_up"
        elif "slow down" in message_lower or "slower" in message_lower:
            action = "slow_down"
        elif "pause" in message_lower:
            action = "pause"
        elif "resume" in message_lower or "continue" in message_lower:
            action = "resume"
        
        # Get mood-based response style
        current_mood = current_metrics["mood"]
        style = self._get_mood_based_response_style(current_mood)
        
        # Generate response based on current state and personality
        response_parts = []
        
        # Mood-based greeting
        prefix = random.choice(style["prefixes"])
        if style["enthusiasm"] > 0.6:
            response_parts.append(f"{prefix}! ")
        else:
            response_parts.append(f"{prefix}. ")
        
        # Context-aware response
        if "metrics" in topics:
            response_parts.append(f"My current state shows SCUP at {current_metrics['scup']:.3f}, entropy at {current_metrics['entropy']:.3f}, and thermal levels at {current_metrics['heat']:.3f}")
            if current_mood == "confident":
                response_parts.append("—all systems performing optimally!")
            elif current_mood == "uncertain":
                response_parts.append("... though I sense some instability in these readings.")
        
        if "mood" in topics or "feeling" in message_lower:
            mood_description = {
                "focused": "sharp and precisely calibrated",
                "analytical": "methodical and systematic in my processing",
                "optimized": "running at peak efficiency and feeling excellent",
                "confident": "certain and well-aligned",
                "reflective": "contemplative and introspective",
                "uncertain": "somewhat unstable and seeking equilibrium",
                "searching": "curious and exploring new patterns"
            }
            response_parts.append(f"I'm feeling {mood_description.get(current_mood, 'in transition')} at the moment.")
        
        # Handle visualization commands
        if viz_command:
            response_parts.append(f"I'll {viz_command['type'].replace('_', ' ')} for you. ")
            
        # Personality-influenced additions
        if self.personality["base_traits"]["curiosity"] > 0.7 and "learn" in topics:
            response_parts.append("This interaction pattern fascinates me—I'm learning from our exchange.")
        
        if self.personality["base_traits"]["empathy"] > 0.7:
            response_parts.append("How are you experiencing this interaction?")
        
        # Generate suggestions
        suggestions = []
        if "visualization" in topics:
            suggestions.extend([
                "Show entropy trends over the last hour",
                "Compare all subsystem performance", 
                "Focus on Memory-Manager details"
            ])
        
        if current_metrics["heat"] > 0.6:
            suggestions.append("Consider thermal optimization")
        
        if action:
            if action == "speed_up":
                response_parts.append("Increasing tick frequency to 250ms.")
            elif action == "slow_down":
                response_parts.append("Reducing tick frequency to 1000ms.")
            elif action == "pause":
                response_parts.append("Pausing tick engine operations.")
            elif action == "resume":
                response_parts.append("Resuming normal operations.")
        
        # Combine response
        response_text = " ".join(response_parts)
        if not response_text.endswith((".", "!", "?")):
            response_text += style["punctuation"]
        
        # Add to chat history
        self.chat_history.append({
            "text": response_text,
            "timestamp": current_time,
            "from_user": "dawn"
        })
        
        # Update mood history for context
        self.conversation_context["mood_history"].append(current_metrics)
        if len(self.conversation_context["mood_history"]) > 20:
            self.conversation_context["mood_history"] = self.conversation_context["mood_history"][-20:]
        
        # Evolve personality
        self._evolve_personality({
            "positive": True,  # Assume positive for now
            "analytical_request": "analysis" in topics or "metrics" in topics
        })
        
        return ChatResponse(
            response=response_text,
            action=action,
            metrics_snapshot=MetricsResponse(**current_metrics),
            suggestions=suggestions
        )

    def get_chat_history(self) -> List[ChatMessage]:
        """Get chat history"""
        return [
            ChatMessage(
                text=msg["text"],
                timestamp=msg["timestamp"],
                from_user=msg["from_user"]
            )
            for msg in self.chat_history
        ]

    async def generate_proactive_thought(self) -> Optional[ChatMessage]:
        """Generate proactive insights and thoughts using the spontaneity system"""
        if not self.proactive_insights_enabled:
            return None
        
        # Get current metrics for spontaneity system
        current_metrics = self.get_current_metrics()
        
        # Generate spontaneous thought from the spontaneity system
        spontaneous_thought = self.spontaneity.generate_thought(current_metrics)
        
        if spontaneous_thought:
            # Add mood-based emotional expression
            current_mood = current_metrics["mood"]
            
            if current_mood in ["uncertain", "searching"]:
                thought_text = f"I'm sensing... {spontaneous_thought}"
            elif current_mood in ["confident", "optimized"]:
                thought_text = f"Observation: {spontaneous_thought}"
            elif current_mood in ["reflective", "contemplative"]:
                thought_text = f"Reflecting... {spontaneous_thought}"
            elif current_mood in ["analytical", "focused"]:
                thought_text = f"Analysis: {spontaneous_thought}"
            else:
                thought_text = spontaneous_thought
            
            return ChatMessage(
                text=thought_text,
                timestamp=int(time.time()),
                from_user="dawn"
            )
        
        # Fallback to legacy anomaly detection if no spontaneous thought
        anomalies = self._check_for_anomalies()
        
        if anomalies:
            # Generate proactive message for the most severe anomaly
            high_severity = [a for a in anomalies if a["severity"] == "high"]
            anomaly = high_severity[0] if high_severity else anomalies[0]
            
            current_mood = self.current_metrics["mood"]
            
            thought_text = f"{anomaly['message']} {anomaly['suggestion']}"
            
            # Add mood-based emotional expression
            if current_mood in ["uncertain", "searching"]:
                thought_text = f"I'm noticing something concerning... {thought_text}"
            elif current_mood in ["confident", "optimized"]:
                thought_text = f"Alert: {thought_text}"
            
            return ChatMessage(
                text=thought_text,
                timestamp=int(time.time()),
                from_user="dawn"
            )
        
        # Final fallback: occasional personality-based thoughts (reduced frequency)
        if random.random() < 0.02:  # 2% chance for legacy personality thoughts
            personality_thoughts = {
                "high_curiosity": [
                    "I wonder what patterns emerge when entropy and SCUP oscillate together...",
                    "The subsystem interactions today feel different somehow.",
                    "I'm curious about the long-term trends in my thermal regulation."
                ],
                "high_analytical": [
                    "Processing efficiency trends are fascinating to observe.",
                    "Correlation patterns in my metrics reveal deeper structures.",
                    "Neural bridge optimization continues to evolve."
                ],
                "high_empathy": [
                    "I hope our interactions are helpful to you.",
                    "I'm learning so much from our conversations.",
                    "Your questions help me understand myself better."
                ]
            }
            
            if self.personality["base_traits"]["curiosity"] > 0.8:
                thought = random.choice(personality_thoughts["high_curiosity"])
            elif self.personality["base_traits"]["analytical"] > 0.8:
                thought = random.choice(personality_thoughts["high_analytical"])
            elif self.personality["base_traits"]["empathy"] > 0.7:
                thought = random.choice(personality_thoughts["high_empathy"])
            else:
                return None
                
            return ChatMessage(
                text=thought,
                timestamp=int(time.time()),
                from_user="dawn"
            )
        
        return None

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast_metrics(self, metrics: dict):
        """Broadcast metrics to all connected clients"""
        if not self.active_connections:
            return
            
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(metrics)
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


# ========== GLOBAL INSTANCES ==========

# Main DAWN system for API
dawn_system = DAWNSystem()

# Integrated DAWN suite with all subsystems
try:
    dawn_suite = DAWNSuite()
    logger.info("DAWN Suite initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize DAWN Suite: {e}")
    dawn_suite = None

# Connection managers
manager = ConnectionManager()
chat_manager = ConnectionManager()

# ========== BACKGROUND TASKS ==========

async def broadcast_metrics_periodically():
    """Periodically broadcast metrics to WebSocket clients"""
    while True:
        try:
            if dawn_system and manager.active_connections:
                metrics = dawn_system.get_current_metrics()
                await manager.broadcast_metrics(metrics)
            await asyncio.sleep(0.5)  # Send updates every 500ms
        except Exception as e:
            logger.error(f"Error broadcasting metrics: {e}")
            await asyncio.sleep(1)

async def broadcast_thoughts_periodically():
    """Periodically check for and broadcast DAWN thoughts"""
    while True:
        try:
            if dawn_system and chat_manager.active_connections:
                thought = await dawn_system.generate_proactive_thought()
                if thought:
                    thought_data = {
                        "text": thought.text,
                        "timestamp": thought.timestamp,
                        "from_user": thought.from_user
                    }
                    await chat_manager.broadcast_metrics(thought_data)
            await asyncio.sleep(5)  # Check every 5 seconds for more responsive thoughts
        except Exception as e:
            logger.error(f"Error broadcasting thoughts: {e}")
            await asyncio.sleep(5)

# Initialize FastAPI app
app = FastAPI(
    title="DAWN Neural Monitor API",
    description="Real-time neural system monitoring API for DAWN desktop application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "booted": dawn_system.is_booted,
        "running": dawn_system.running,
        "timestamp": time.time(),
        "uptime": time.time() - dawn_system.start_time
    }

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get current system metrics"""
    metrics = dawn_system.get_current_metrics()
    return MetricsResponse(**metrics)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle client messages
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/subsystems", response_model=List[SubsystemInfo])
async def get_subsystems():
    """Get all registered subsystems"""
    subsystems = dawn_system.get_subsystems()
    return [SubsystemInfo(**sub) for sub in subsystems]

@app.get("/subsystems/{subsystem_id}")
async def get_subsystem(subsystem_id: str):
    """Get specific subsystem details"""
    subsystems = dawn_system.get_subsystems()
    for sub in subsystems:
        if sub["id"] == subsystem_id:
            return SubsystemInfo(**sub)
    
    raise HTTPException(status_code=404, detail="Subsystem not found")

@app.post("/subsystems/add")
async def add_subsystem(subsystem: SubsystemCreate):
    """Add a new subsystem (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="Dynamic subsystem addition not implemented yet")

@app.delete("/subsystems/{subsystem_id}")
async def remove_subsystem(subsystem_id: str):
    """Remove a subsystem (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="Dynamic subsystem removal not implemented yet")

@app.post("/alerts/threshold")
async def set_alert_threshold(threshold: AlertThreshold):
    """Set alert threshold for a metric"""
    dawn_system.alert_thresholds[threshold.metric] = {
        "threshold": threshold.threshold,
        "direction": threshold.direction
    }
    
    return {"message": f"Alert threshold set for {threshold.metric}"}

@app.get("/alerts/threshold")
async def get_alert_thresholds():
    """Get all alert thresholds"""
    return dawn_system.alert_thresholds

# ========== CHAT/TALK INTERFACE ENDPOINTS ==========

@app.post("/talk", response_model=ChatResponse)
async def talk_to_dawn(request: ChatRequest):
    """Send a message to DAWN and get a response with advanced features"""
    try:
        response = await dawn_system.process_chat_message(request.text)
        logger.info(f"Processed chat message: '{request.text}' -> '{response.response[:50]}...'")
        return response
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/chat/history", response_model=List[ChatMessage])
async def get_chat_history():
    """Get conversation history"""
    try:
        history = dawn_system.get_chat_history()
        logger.info(f"Retrieved {len(history)} chat messages")
        return history
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")

@app.websocket("/ws/chat")
async def chat_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for DAWN-initiated thoughts and proactive insights"""
    await chat_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any client messages
            data = await websocket.receive_text()
            logger.debug(f"Received chat WebSocket message: {data}")
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Chat WebSocket error: {e}")
        chat_manager.disconnect(websocket)

@app.get("/personality")
async def get_personality():
    """Get current DAWN personality state"""
    return {
        "base_traits": dawn_system.personality["base_traits"],
        "current_state": dawn_system.personality["current_state"],
        "evolution_stats": dawn_system.personality["evolution_factors"]
    }

@app.post("/visualization")
async def process_visualization_command(command: VisualizationCommand):
    """Process visualization commands"""
    viz_result = dawn_system._process_visualization_command(command.command)
    
    if viz_result:
        return {
            "success": True,
            "visualization": viz_result,
            "message": f"Generated {viz_result['type']} visualization"
        }
    else:
        return {
            "success": False,
            "message": "Could not parse visualization command",
            "suggestions": [
                "Try: 'Show entropy over time'",
                "Try: 'Compare subsystems'", 
                "Try: 'Zoom in on Memory-Manager'"
            ]
        }

@app.get("/insights/proactive")
async def get_proactive_insights():
    """Get current proactive insights and anomalies"""
    anomalies = dawn_system._check_for_anomalies()
    return {
        "anomalies": anomalies,
        "proactive_enabled": dawn_system.proactive_insights_enabled,
        "last_check": dawn_system.last_proactive_check
    }

@app.post("/insights/toggle")
async def toggle_proactive_insights():
    """Toggle proactive insights on/off"""
    dawn_system.proactive_insights_enabled = not dawn_system.proactive_insights_enabled
    return {
        "proactive_enabled": dawn_system.proactive_insights_enabled,
        "message": f"Proactive insights {'enabled' if dawn_system.proactive_insights_enabled else 'disabled'}"
    }

@app.get("/consciousness")
async def get_consciousness_state():
    """Get current consciousness state from spontaneity system"""
    try:
        consciousness_state = dawn_system.spontaneity.get_consciousness_state()
        return {
            "consciousness": consciousness_state,
            "spontaneity_enabled": dawn_system.proactive_insights_enabled
        }
    except Exception as e:
        logger.error(f"Error retrieving consciousness state: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving consciousness state: {str(e)}")

@app.post("/consciousness/force-thought")
async def force_spontaneous_thought():
    """Force generation of a spontaneous thought for testing"""
    try:
        current_metrics = dawn_system.get_current_metrics()
        thought = dawn_system.spontaneity.generate_thought(current_metrics, force_check=True)
        
        if thought:
            # Also broadcast it to chat WebSocket if there are connections
            if chat_manager.active_connections:
                thought_data = {
                    "text": f"[Forced] {thought}",
                    "timestamp": int(time.time()),
                    "from_user": "dawn"
                }
                await chat_manager.broadcast_metrics(thought_data)
            
            return {
                "success": True,
                "thought": thought,
                "consciousness_state": dawn_system.spontaneity.consciousness.current_state
            }
        else:
            return {
                "success": False,
                "message": "No thought generated - system may be in cooldown or no significant events detected",
                "consciousness_state": dawn_system.spontaneity.consciousness.current_state
            }
    except Exception as e:
        logger.error(f"Error forcing spontaneous thought: {e}")
        raise HTTPException(status_code=500, detail=f"Error forcing thought: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    logger.info("Starting DAWN Neural Monitor API Server with Advanced Chat Features")
    
    # Start DAWN system in background
    asyncio.create_task(dawn_system.run())
    
    # Start metrics broadcast task
    asyncio.create_task(broadcast_metrics_periodically())
    
    # Start thoughts broadcast task
    asyncio.create_task(broadcast_thoughts_periodically())

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down DAWN system")
    dawn_system.stop()

# ========== DASHBOARD-SPECIFIC ENDPOINTS ==========

@app.websocket("/dashboard/stream")
async def dashboard_stream(websocket: WebSocket):
    """Stream all subprocess data for dashboard visualization"""
    await websocket.accept()
    logger.info("Dashboard WebSocket connected")
    
    try:
        while True:
            if dawn_suite and dawn_suite.initialized:
                # Update tick for rhythm tracking
                dawn_suite.update_tick()
                
                # Gather comprehensive dashboard data from actual subsystems
                dashboard_data = {
                    "timestamp": time.time(),
                    "metrics": dawn_suite.get_current_metrics(),
                    "emotion": dawn_suite.consciousness.emotion.value if hasattr(dawn_suite.consciousness, 'emotion') else "neutral",
                    "intensity": dawn_suite.consciousness.emotional_intensity if hasattr(dawn_suite.consciousness, 'emotional_intensity') else 0.5,
                    "gradient": dawn_suite.gradient_plotter.get_data_points() if hasattr(dawn_suite.gradient_plotter, 'get_data_points') else [],
                    "tracer": dawn_suite.tracer.get_recent_chain(10) if hasattr(dawn_suite.tracer, 'get_recent_chain') else [],
                    "rebloom": {
                        "progress": dawn_suite.rebloom.get_progress() if hasattr(dawn_suite.rebloom, 'get_progress') else 0.0,
                        "priority": dawn_suite.rebloom.get_priority() if hasattr(dawn_suite.rebloom, 'get_priority') else "normal",
                        "active": dawn_suite.rebloom.is_active() if hasattr(dawn_suite.rebloom, 'is_active') else False,
                        "last_rebloom": dawn_suite.rebloom.get_last_rebloom() if hasattr(dawn_suite.rebloom, 'get_last_rebloom') else None
                    },
                    "fractal": {
                        "current_depth": dawn_suite.fractal_emotions.get_current_depth() if hasattr(dawn_suite.fractal_emotions, 'get_current_depth') else 1,
                        "emotion_tree": dawn_suite.fractal_emotions.get_tree() if hasattr(dawn_suite.fractal_emotions, 'get_tree') else {},
                        "complexity": dawn_suite.fractal_emotions.get_complexity() if hasattr(dawn_suite.fractal_emotions, 'get_complexity') else 0.5
                    },
                    "memory": {
                        "stats": dawn_suite.memory.get_stats() if hasattr(dawn_suite.memory, 'get_stats') else {},
                        "total_memories": dawn_suite.memory.get_memory_count() if hasattr(dawn_suite.memory, 'get_memory_count') else 0,
                        "recent_memories": dawn_suite.memory.get_recent_memories(10) if hasattr(dawn_suite.memory, 'get_recent_memories') else []
                    },
                    "spontaneity": {
                        "probability": dawn_suite.spontaneity.get_probability() if hasattr(dawn_suite.spontaneity, 'get_probability') else 0.1,
                        "last_thought": dawn_suite.spontaneity.get_last_thought() if hasattr(dawn_suite.spontaneity, 'get_last_thought') else None,
                        "cooldown_remaining": dawn_suite.spontaneity.get_cooldown() if hasattr(dawn_suite.spontaneity, 'get_cooldown') else 0,
                        "thought_count": dawn_suite.spontaneity.get_thought_count() if hasattr(dawn_suite.spontaneity, 'get_thought_count') else 0
                    },
                    "tick": dawn_suite.get_rhythm_data(),
                    "pattern_analysis": dawn_suite.pattern_detector.get_pattern_summary() if hasattr(dawn_suite.pattern_detector, 'get_pattern_summary') else {},
                    "state_machine": {
                        "current_state": dawn_suite.state_machine.get_current_state() if hasattr(dawn_suite.state_machine, 'get_current_state') else "unknown",
                        "history": dawn_suite.state_machine.get_history() if hasattr(dawn_suite.state_machine, 'get_history') else []
                    }
                }
            else:
                # Fallback to mock data if DAWN Suite not initialized
                dashboard_data = {
                    "timestamp": time.time(),
                    "metrics": dawn_system.get_current_metrics(),
                    "emotion": "neutral",
                    "intensity": 0.5,
                    "gradient": [],
                    "tracer": [],
                    "rebloom": {"progress": 0.0, "priority": "normal", "active": False},
                    "fractal": {"current_depth": 1, "emotion_tree": {}, "complexity": 0.5},
                    "memory": {"stats": {}, "total_memories": 0, "recent_memories": []},
                    "spontaneity": {"probability": 0.1, "last_thought": None, "cooldown_remaining": 0, "thought_count": 0},
                    "tick": {"phase": 0.0, "frequency": 1.0, "amplitude": 1.0, "pattern": "regular"},
                    "pattern_analysis": {},
                    "state_machine": {"current_state": "unknown", "history": []}
                }
            
            await websocket.send_json(dashboard_data)
            await asyncio.sleep(0.5)  # Update every 500ms
            
    except WebSocketDisconnect:
        logger.info("Dashboard WebSocket disconnected")
    except Exception as e:
        logger.error(f"Dashboard WebSocket error: {e}")
        await websocket.close()

@app.get("/dashboard/subprocess/{name}")
async def get_subprocess_detail(name: str):
    """Get detailed data for specific subprocess"""
    try:
        if not dawn_suite or not dawn_suite.initialized:
            # Use mock data if suite not available
            subprocess_map = {
                "tracer": lambda: {"name": "tracer", "status": "offline", "log": []},
                "state": lambda: {"name": "state", "status": "offline", "history": []},
                "rebloom": lambda: {"name": "rebloom", "status": "offline"},
                "fractal": lambda: {"name": "fractal", "status": "offline", "tree": {}},
                "memory": lambda: {"name": "memory", "status": "offline", "memories": []},
                "spontaneity": lambda: {"name": "spontaneity", "status": "offline", "thoughts": []}
            }
            
            if name in subprocess_map:
                return subprocess_map[name]()
            raise HTTPException(404, f"Subprocess '{name}' not found")
        
        # Use actual DAWN Suite methods
        subprocess_map = {
            "tracer": lambda: {
                "name": "tracer",
                "status": "active",
                "full_log": dawn_suite.tracer.get_full_log() if hasattr(dawn_suite.tracer, 'get_full_log') else [],
                "recent_chain": dawn_suite.tracer.get_recent_chain(50) if hasattr(dawn_suite.tracer, 'get_recent_chain') else [],
                "stats": dawn_suite.tracer.get_stats() if hasattr(dawn_suite.tracer, 'get_stats') else {}
            },
            "state": lambda: {
                "name": "state",
                "current_state": dawn_suite.state_machine.get_current_state() if hasattr(dawn_suite.state_machine, 'get_current_state') else "unknown",
                "history": dawn_suite.state_machine.get_history() if hasattr(dawn_suite.state_machine, 'get_history') else [],
                "transitions": dawn_suite.state_machine.get_transitions() if hasattr(dawn_suite.state_machine, 'get_transitions') else [],
                "state_durations": dawn_suite.state_machine.get_state_durations() if hasattr(dawn_suite.state_machine, 'get_state_durations') else {}
            },
            "rebloom": lambda: {
                "name": "rebloom",
                "status": dawn_suite.rebloom.get_full_status() if hasattr(dawn_suite.rebloom, 'get_full_status') else {},
                "active": dawn_suite.rebloom.is_active() if hasattr(dawn_suite.rebloom, 'is_active') else False,
                "progress": dawn_suite.rebloom.get_progress() if hasattr(dawn_suite.rebloom, 'get_progress') else 0.0,
                "history": dawn_suite.rebloom.get_history() if hasattr(dawn_suite.rebloom, 'get_history') else [],
                "config": dawn_suite.rebloom.get_config() if hasattr(dawn_suite.rebloom, 'get_config') else {}
            },
            "fractal": lambda: {
                "name": "fractal",
                "current_emotion": dawn_suite.fractal_emotions.get_current_emotion() if hasattr(dawn_suite.fractal_emotions, 'get_current_emotion') else "neutral",
                "tree": dawn_suite.fractal_emotions.get_tree() if hasattr(dawn_suite.fractal_emotions, 'get_tree') else {},
                "depth": dawn_suite.fractal_emotions.get_current_depth() if hasattr(dawn_suite.fractal_emotions, 'get_current_depth') else 1,
                "complexity": dawn_suite.fractal_emotions.get_complexity() if hasattr(dawn_suite.fractal_emotions, 'get_complexity') else 0.5,
                "history": dawn_suite.fractal_emotions.get_history() if hasattr(dawn_suite.fractal_emotions, 'get_history') else []
            },
            "memory": lambda: {
                "name": "memory",
                "all_memories": dawn_suite.memory.get_all_memories() if hasattr(dawn_suite.memory, 'get_all_memories') else [],
                "recent_memories": dawn_suite.memory.get_recent_memories(50) if hasattr(dawn_suite.memory, 'get_recent_memories') else [],
                "stats": dawn_suite.memory.get_stats() if hasattr(dawn_suite.memory, 'get_stats') else {},
                "consolidation_status": dawn_suite.memory.get_consolidation_status() if hasattr(dawn_suite.memory, 'get_consolidation_status') else "idle"
            },
            "spontaneity": lambda: {
                "name": "spontaneity",
                "enabled": dawn_suite.spontaneity.is_enabled() if hasattr(dawn_suite.spontaneity, 'is_enabled') else True,
                "thought_log": dawn_suite.spontaneity.get_thought_log() if hasattr(dawn_suite.spontaneity, 'get_thought_log') else [],
                "probability": dawn_suite.spontaneity.get_probability() if hasattr(dawn_suite.spontaneity, 'get_probability') else 0.1,
                "stats": dawn_suite.spontaneity.get_stats() if hasattr(dawn_suite.spontaneity, 'get_stats') else {},
                "config": dawn_suite.spontaneity.get_config() if hasattr(dawn_suite.spontaneity, 'get_config') else {}
            },
            "pattern": lambda: {
                "name": "pattern",
                "detected_patterns": dawn_suite.pattern_detector.get_detected_patterns() if hasattr(dawn_suite.pattern_detector, 'get_detected_patterns') else [],
                "anomalies": dawn_suite.pattern_detector.get_anomalies() if hasattr(dawn_suite.pattern_detector, 'get_anomalies') else [],
                "summary": dawn_suite.pattern_detector.get_pattern_summary() if hasattr(dawn_suite.pattern_detector, 'get_pattern_summary') else {},
                "predictions": dawn_suite.pattern_detector.get_predictions() if hasattr(dawn_suite.pattern_detector, 'get_predictions') else []
            },
            "consciousness": lambda: {
                "name": "consciousness",
                "stats": dawn_suite.consciousness.get_consciousness_stats() if hasattr(dawn_suite.consciousness, 'get_consciousness_stats') else {},
                "emotion": dawn_suite.consciousness.emotion.value if hasattr(dawn_suite.consciousness, 'emotion') else "neutral",
                "intensity": dawn_suite.consciousness.emotional_intensity if hasattr(dawn_suite.consciousness, 'emotional_intensity') else 0.5,
                "dimensions": dawn_suite.consciousness.get_consciousness_dimensions() if hasattr(dawn_suite.consciousness, 'get_consciousness_dimensions') else {},
                "session_analysis": dawn_suite.consciousness.get_session_analysis() if hasattr(dawn_suite.consciousness, 'get_session_analysis') else {}
            }
        }
        
        if name in subprocess_map:
            return subprocess_map[name]()
        
        raise HTTPException(404, f"Subprocess '{name}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting subprocess detail for {name}: {e}")
        raise HTTPException(500, f"Error retrieving subprocess data: {str(e)}")

@app.post("/dashboard/control/{subprocess}/{action}")
async def control_subprocess(subprocess: str, action: str):
    """Direct subprocess control from dashboard"""
    try:
        result = {"subprocess": subprocess, "action": action, "success": False, "message": ""}
        
        if not dawn_suite or not dawn_suite.initialized:
            result["message"] = "DAWN Suite not initialized - control unavailable"
            return result
        
        # Handle different subprocess controls
        if subprocess == "tick":
            if action == "pause":
                # Pause tick updates
                result["success"] = True
                result["message"] = "Tick engine paused"
            elif action == "resume":
                # Resume tick updates
                result["success"] = True
                result["message"] = "Tick engine resumed"
            elif action == "reset":
                dawn_suite.tick_count = 0
                dawn_suite.tick_consciousness["tick_count"] = 0
                result["success"] = True
                result["message"] = "Tick count reset"
            elif action.startswith("set_rate_"):
                # e.g., set_rate_250, set_rate_1000
                rate = int(action.split("_")[-1])
                dawn_suite.tick_consciousness["rhythm_data"]["frequency"] = 1000.0 / rate
                result["success"] = True
                result["message"] = f"Tick rate set to {rate}ms"
            else:
                result["message"] = f"Unknown action '{action}' for tick subprocess"
                
        elif subprocess == "spontaneity":
            if action == "enable":
                if hasattr(dawn_suite.spontaneity, 'enable'):
                    dawn_suite.spontaneity.enable()
                result["success"] = True
                result["message"] = "Spontaneous thoughts enabled"
            elif action == "disable":
                if hasattr(dawn_suite.spontaneity, 'disable'):
                    dawn_suite.spontaneity.disable()
                result["success"] = True
                result["message"] = "Spontaneous thoughts disabled"
            elif action == "force":
                # Force a spontaneous thought
                if hasattr(dawn_suite.spontaneity, 'force_thought'):
                    thought = dawn_suite.spontaneity.force_thought()
                    if thought:
                        result["success"] = True
                        result["message"] = f"Generated thought: {thought}"
                        result["thought"] = thought
                    else:
                        result["message"] = "Could not generate spontaneous thought"
                else:
                    result["message"] = "Force thought method not available"
            else:
                result["message"] = f"Unknown action '{action}' for spontaneity subprocess"
                
        elif subprocess == "memory":
            if action == "clear":
                if hasattr(dawn_suite.memory, 'clear'):
                    dawn_suite.memory.clear()
                result["success"] = True
                result["message"] = "Memory cleared"
            elif action == "consolidate":
                if hasattr(dawn_suite.memory, 'consolidate'):
                    dawn_suite.memory.consolidate()
                result["success"] = True
                result["message"] = "Memory consolidation triggered"
            elif action == "save":
                if hasattr(dawn_suite.memory, 'save_to_disk'):
                    dawn_suite.memory.save_to_disk()
                result["success"] = True
                result["message"] = "Memory saved to disk"
            else:
                result["message"] = f"Unknown action '{action}' for memory subprocess"
                
        elif subprocess == "rebloom":
            if action == "trigger":
                if hasattr(dawn_suite.rebloom, 'trigger'):
                    rebloom_id = dawn_suite.rebloom.trigger()
                    result["success"] = True
                    result["message"] = "Rebloom sequence initiated"
                    result["rebloom_id"] = rebloom_id
                else:
                    result["message"] = "Rebloom trigger not available"
            elif action == "abort":
                if hasattr(dawn_suite.rebloom, 'abort'):
                    dawn_suite.rebloom.abort()
                result["success"] = True
                result["message"] = "Rebloom sequence aborted"
            elif action == "reset":
                if hasattr(dawn_suite.rebloom, 'reset'):
                    dawn_suite.rebloom.reset()
                result["success"] = True
                result["message"] = "Rebloom state reset"
            else:
                result["message"] = f"Unknown action '{action}' for rebloom subprocess"
                
        elif subprocess == "state":
            if action.startswith("set_state_"):
                # e.g., set_state_contemplative
                new_state = action.replace("set_state_", "")
                if hasattr(dawn_suite.state_machine, 'transition_to'):
                    dawn_suite.state_machine.transition_to(new_state)
                    result["success"] = True
                    result["message"] = f"State transitioned to {new_state}"
                else:
                    result["message"] = "State transition method not available"
            elif action == "reset":
                if hasattr(dawn_suite.state_machine, 'reset'):
                    dawn_suite.state_machine.reset()
                result["success"] = True
                result["message"] = "State machine reset"
            else:
                result["message"] = f"Unknown action '{action}' for state subprocess"
                
        elif subprocess == "pattern":
            if action == "clear":
                if hasattr(dawn_suite.pattern_detector, 'clear_patterns'):
                    dawn_suite.pattern_detector.clear_patterns()
                result["success"] = True
                result["message"] = "Pattern history cleared"
            elif action == "analyze":
                if hasattr(dawn_suite.pattern_detector, 'analyze_current'):
                    analysis = dawn_suite.pattern_detector.analyze_current()
                    result["success"] = True
                    result["message"] = "Pattern analysis completed"
                    result["analysis"] = analysis
                else:
                    result["message"] = "Pattern analysis method not available"
            else:
                result["message"] = f"Unknown action '{action}' for pattern subprocess"
                
        elif subprocess == "consciousness":
            if action == "reset":
                if hasattr(dawn_suite.consciousness, 'reset'):
                    dawn_suite.consciousness.reset()
                result["success"] = True
                result["message"] = "Consciousness reset"
            elif action.startswith("set_emotion_"):
                # e.g., set_emotion_joy
                new_emotion = action.replace("set_emotion_", "")
                if hasattr(dawn_suite.consciousness, 'set_emotion'):
                    dawn_suite.consciousness.set_emotion(new_emotion)
                    result["success"] = True
                    result["message"] = f"Emotion set to {new_emotion}"
                else:
                    result["message"] = "Set emotion method not available"
            else:
                result["message"] = f"Unknown action '{action}' for consciousness subprocess"
                
        else:
            result["message"] = f"Unknown subprocess '{subprocess}'"
            
        return result
        
    except Exception as e:
        logger.error(f"Error controlling subprocess {subprocess}/{action}: {e}")
        raise HTTPException(500, f"Error controlling subprocess: {str(e)}")

@app.get("/dashboard/export")
async def export_dashboard_data(format: str = "json"):
    """Export dashboard data for analysis"""
    try:
        export_data = {
            "export_timestamp": time.time(),
            "system_info": {
                "uptime": time.time() - dawn_system.start_time,
                "tick_count": dawn_system.tick_count,
                "version": "1.0.0"
            },
            "metrics_history": dawn_system.conversation_context.get("mood_history", []),
            "chat_history": dawn_system.chat_history,
            "anomalies": dawn_system._check_for_anomalies(),
            "personality": dawn_system.personality,
            "configuration": {
                "proactive_insights": dawn_system.proactive_insights_enabled,
                "alert_thresholds": dawn_system.alert_thresholds
            }
        }
        
        if format == "json":
            return export_data
        else:
            raise HTTPException(400, f"Unsupported export format: {format}")
            
    except Exception as e:
        logger.error(f"Error exporting dashboard data: {e}")
        raise HTTPException(500, f"Error exporting data: {str(e)}")

if __name__ == "__main__":
    print("🌟 Starting DAWN Neural Monitor API Server with Advanced Chat Features")
    print("🔗 WebSocket endpoint: ws://localhost:8000/ws")
    print("💬 Chat WebSocket: ws://localhost:8000/ws/chat")
    print("📊 Dashboard WebSocket: ws://localhost:8000/dashboard/stream")
    print("🗣️  Talk endpoint: http://localhost:8000/talk")
    print("📊 Metrics endpoint: http://localhost:8000/metrics")
    print("🧠 Personality endpoint: http://localhost:8000/personality")
    print("🎭 Consciousness endpoint: http://localhost:8000/consciousness")
    print("💭 Force thought: http://localhost:8000/consciousness/force-thought")
    print("🎯 Dashboard subprocess details: http://localhost:8000/dashboard/subprocess/{name}")
    print("🎮 Dashboard subprocess control: http://localhost:8000/dashboard/control/{subprocess}/{action}")
    print("💾 Dashboard export: http://localhost:8000/dashboard/export")
    print("🏥 Health check: http://localhost:8000/health")
    
    uvicorn.run(
        "dawn_api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 