"""
DAWN Consciousness State Persistence Module
Handles saving and loading of consciousness state for continuity across sessions.
Maintains emotional history, conversation memory, and thought patterns.
"""

import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import pickle
import gzip
from collections import deque, defaultdict

logger = logging.getLogger(__name__)

@dataclass
class EmotionalState:
    """Single emotional state record"""
    timestamp: float
    emotion: str
    intensity: float
    metrics: Dict[str, float]
    triggers: List[str]
    context: str

@dataclass
class ConversationExchange:
    """Single conversation exchange record"""
    timestamp: float
    user_message: str
    dawn_response: str
    emotion: str
    intent: str
    action: Optional[str]
    metrics_snapshot: Dict[str, Any]
    suggestions_given: List[str]
    response_time: float

@dataclass
class ThoughtPattern:
    """Thought pattern and trigger record"""
    pattern_id: str
    pattern_type: str  # 'spontaneous', 'reactive', 'reflective'
    triggers: List[str]
    frequency: int
    last_occurrence: float
    associated_emotions: List[str]
    context_keywords: List[str]
    effectiveness_score: float

@dataclass
class ConsciousnessSession:
    """Complete session record"""
    session_id: str
    start_time: float
    end_time: Optional[float]
    total_exchanges: int
    dominant_emotions: List[str]
    key_insights: List[str]
    avg_response_time: float
    system_health_summary: Dict[str, Any]

class ConsciousnessStatePersistence:
    """Advanced consciousness state persistence manager"""
    
    def __init__(self, base_directory: str = "state"):
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(exist_ok=True)
        
        # State directories
        self.emotional_history_dir = self.base_directory / "emotional_history"
        self.conversation_dir = self.base_directory / "conversations"
        self.patterns_dir = self.base_directory / "thought_patterns"
        self.sessions_dir = self.base_directory / "sessions"
        
        # Create subdirectories
        for directory in [self.emotional_history_dir, self.conversation_dir, 
                         self.patterns_dir, self.sessions_dir]:
            directory.mkdir(exist_ok=True)
        
        # In-memory state tracking
        self.emotional_history: deque = deque(maxlen=1000)  # Last 1000 emotional states
        self.conversation_memory: deque = deque(maxlen=100)  # Last 100 exchanges
        self.thought_patterns: Dict[str, ThoughtPattern] = {}
        self.current_session: Optional[ConsciousnessSession] = None
        self.state_changes_since_save = 0
        self.auto_save_threshold = 10  # Auto-save after 10 state changes
        
        # State tracking metadata
        self.last_save_time = time.time()
        self.total_sessions = 0
        self.consciousness_uptime = 0.0
        
        logger.info(f"Consciousness state persistence initialized in {self.base_directory}")
    
    def record_emotional_state(self, emotion: str, intensity: float, metrics: Dict[str, float],
                             triggers: List[str] = None, context: str = "") -> None:
        """Record a new emotional state"""
        
        emotional_state = EmotionalState(
            timestamp=time.time(),
            emotion=emotion,
            intensity=intensity,
            metrics=metrics.copy() if metrics else {},
            triggers=triggers or [],
            context=context
        )
        
        self.emotional_history.append(emotional_state)
        self._increment_state_changes()
        
        logger.debug(f"Recorded emotional state: {emotion} (intensity: {intensity:.2f})")
    
    def record_conversation_exchange(self, user_message: str, dawn_response: str, 
                                   emotion: str, intent: str, action: Optional[str],
                                   metrics_snapshot: Dict[str, Any], 
                                   suggestions_given: List[str], 
                                   response_time: float) -> None:
        """Record a conversation exchange"""
        
        exchange = ConversationExchange(
            timestamp=time.time(),
            user_message=user_message,
            dawn_response=dawn_response,
            emotion=emotion,
            intent=intent,
            action=action,
            metrics_snapshot=metrics_snapshot.copy() if metrics_snapshot else {},
            suggestions_given=suggestions_given.copy() if suggestions_given else [],
            response_time=response_time
        )
        
        self.conversation_memory.append(exchange)
        self._increment_state_changes()
        
        # Update current session if active
        if self.current_session:
            self.current_session.total_exchanges += 1
            
            # Update average response time
            total_time = (self.current_session.avg_response_time * 
                         (self.current_session.total_exchanges - 1) + response_time)
            self.current_session.avg_response_time = total_time / self.current_session.total_exchanges
        
        logger.debug(f"Recorded conversation exchange: {intent} -> {emotion}")
    
    def record_thought_pattern(self, pattern_type: str, triggers: List[str],
                             associated_emotions: List[str], context_keywords: List[str],
                             effectiveness_score: float = 0.5) -> str:
        """Record or update a thought pattern"""
        
        # Generate pattern ID from triggers and type
        pattern_content = f"{pattern_type}:{':'.join(sorted(triggers))}"
        pattern_id = hashlib.md5(pattern_content.encode()).hexdigest()[:12]
        
        if pattern_id in self.thought_patterns:
            # Update existing pattern
            pattern = self.thought_patterns[pattern_id]
            pattern.frequency += 1
            pattern.last_occurrence = time.time()
            pattern.effectiveness_score = (pattern.effectiveness_score + effectiveness_score) / 2
            
            # Merge new context keywords
            for keyword in context_keywords:
                if keyword not in pattern.context_keywords:
                    pattern.context_keywords.append(keyword)
                    
            # Merge new emotions
            for emotion in associated_emotions:
                if emotion not in pattern.associated_emotions:
                    pattern.associated_emotions.append(emotion)
        else:
            # Create new pattern
            pattern = ThoughtPattern(
                pattern_id=pattern_id,
                pattern_type=pattern_type,
                triggers=triggers.copy(),
                frequency=1,
                last_occurrence=time.time(),
                associated_emotions=associated_emotions.copy(),
                context_keywords=context_keywords.copy(),
                effectiveness_score=effectiveness_score
            )
            self.thought_patterns[pattern_id] = pattern
        
        self._increment_state_changes()
        logger.debug(f"Recorded thought pattern: {pattern_type} ({pattern_id})")
        return pattern_id
    
    def start_session(self, session_context: str = "") -> str:
        """Start a new consciousness session"""
        
        session_id = f"session_{int(time.time())}_{hashlib.md5(session_context.encode()).hexdigest()[:8]}"
        
        self.current_session = ConsciousnessSession(
            session_id=session_id,
            start_time=time.time(),
            end_time=None,
            total_exchanges=0,
            dominant_emotions=[],
            key_insights=[],
            avg_response_time=0.0,
            system_health_summary={}
        )
        
        self.total_sessions += 1
        logger.info(f"Started consciousness session: {session_id}")
        return session_id
    
    def end_session(self, key_insights: List[str] = None, 
                   system_health_summary: Dict[str, Any] = None) -> None:
        """End the current consciousness session"""
        
        if not self.current_session:
            logger.warning("No active session to end")
            return
        
        self.current_session.end_time = time.time()
        self.current_session.key_insights = key_insights or []
        self.current_session.system_health_summary = system_health_summary or {}
        
        # Calculate dominant emotions from recent conversation
        recent_emotions = [exchange.emotion for exchange in 
                          list(self.conversation_memory)[-20:]]  # Last 20 exchanges
        emotion_counts = defaultdict(int)
        for emotion in recent_emotions:
            emotion_counts[emotion] += 1
        
        self.current_session.dominant_emotions = sorted(
            emotion_counts.keys(), 
            key=lambda x: emotion_counts[x], 
            reverse=True
        )[:3]  # Top 3 emotions
        
        # Update total uptime
        session_duration = self.current_session.end_time - self.current_session.start_time
        self.consciousness_uptime += session_duration
        
        logger.info(f"Ended session {self.current_session.session_id} "
                   f"(duration: {session_duration:.1f}s, exchanges: {self.current_session.total_exchanges})")
        
        # Save session and reset
        self._save_session(self.current_session)
        self.current_session = None
    
    def save_state(self, filepath: str = None) -> bool:
        """Save complete consciousness state to file"""
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.base_directory / f"consciousness_state_{timestamp}.json"
        else:
            filepath = Path(filepath)
        
        try:
            # Prepare state data
            state_data = {
                "metadata": {
                    "save_time": time.time(),
                    "save_timestamp": datetime.now().isoformat(),
                    "total_sessions": self.total_sessions,
                    "consciousness_uptime": self.consciousness_uptime,
                    "version": "1.0"
                },
                "emotional_history": [asdict(state) for state in self.emotional_history],
                "conversation_memory": [asdict(exchange) for exchange in self.conversation_memory],
                "thought_patterns": {pid: asdict(pattern) for pid, pattern in self.thought_patterns.items()},
                "current_session": asdict(self.current_session) if self.current_session else None,
                "statistics": self._generate_statistics()
            }
            
            # Save with compression for large files
            if len(json.dumps(state_data, default=str)) > 1024 * 1024:  # > 1MB
                with gzip.open(f"{filepath}.gz", 'wt', encoding='utf-8') as f:
                    json.dump(state_data, f, indent=2, default=str)
                logger.info(f"Consciousness state saved (compressed): {filepath}.gz")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(state_data, f, indent=2, default=str)
                logger.info(f"Consciousness state saved: {filepath}")
            
            self.last_save_time = time.time()
            self.state_changes_since_save = 0
            return True
            
        except Exception as e:
            logger.error(f"Failed to save consciousness state: {e}")
            return False
    
    def load_state(self, filepath: str) -> bool:
        """Load consciousness state from file"""
        
        filepath = Path(filepath)
        
        # Try compressed version first
        if not filepath.exists() and Path(f"{filepath}.gz").exists():
            filepath = Path(f"{filepath}.gz")
        
        if not filepath.exists():
            logger.warning(f"State file not found: {filepath}")
            return False
        
        try:
            # Load data
            if filepath.suffix == '.gz':
                with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                    state_data = json.load(f)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
            
            # Restore emotional history
            self.emotional_history.clear()
            for state_dict in state_data.get("emotional_history", []):
                emotional_state = EmotionalState(**state_dict)
                self.emotional_history.append(emotional_state)
            
            # Restore conversation memory
            self.conversation_memory.clear()
            for exchange_dict in state_data.get("conversation_memory", []):
                exchange = ConversationExchange(**exchange_dict)
                self.conversation_memory.append(exchange)
            
            # Restore thought patterns
            self.thought_patterns.clear()
            for pattern_id, pattern_dict in state_data.get("thought_patterns", {}).items():
                pattern = ThoughtPattern(**pattern_dict)
                self.thought_patterns[pattern_id] = pattern
            
            # Restore session if active
            current_session_data = state_data.get("current_session")
            if current_session_data:
                self.current_session = ConsciousnessSession(**current_session_data)
            
            # Restore metadata
            metadata = state_data.get("metadata", {})
            self.total_sessions = metadata.get("total_sessions", 0)
            self.consciousness_uptime = metadata.get("consciousness_uptime", 0.0)
            
            self.state_changes_since_save = 0
            logger.info(f"Consciousness state loaded from: {filepath}")
            logger.info(f"Restored {len(self.emotional_history)} emotional states, "
                       f"{len(self.conversation_memory)} conversation exchanges, "
                       f"{len(self.thought_patterns)} thought patterns")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load consciousness state: {e}")
            return False
    
    def get_conversation_summary(self) -> str:
        """Generate a comprehensive conversation summary"""
        
        if not self.conversation_memory:
            return "No conversation history available."
        
        # Analyze conversation patterns
        total_exchanges = len(self.conversation_memory)
        recent_exchanges = list(self.conversation_memory)[-20:]  # Last 20
        
        # Emotion analysis
        emotion_counts = defaultdict(int)
        intent_counts = defaultdict(int)
        actions_taken = []
        
        for exchange in self.conversation_memory:
            emotion_counts[exchange.emotion] += 1
            intent_counts[exchange.intent] += 1
            if exchange.action:
                actions_taken.append(exchange.action)
        
        # Calculate average response time
        avg_response_time = sum(ex.response_time for ex in self.conversation_memory) / total_exchanges
        
        # Find dominant patterns
        top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Recent conversation flow
        recent_flow = " → ".join([
            f"{ex.intent}({ex.emotion})" for ex in recent_exchanges[-5:]
        ])
        
        # Time span analysis
        if total_exchanges > 1:
            first_time = self.conversation_memory[0].timestamp
            last_time = self.conversation_memory[-1].timestamp
            conversation_span = last_time - first_time
            span_str = f"{conversation_span / 3600:.1f} hours" if conversation_span > 3600 else f"{conversation_span / 60:.1f} minutes"
        else:
            span_str = "single exchange"
        
        # Build summary
        summary_parts = [
            f"📊 Conversation Summary ({total_exchanges} exchanges over {span_str})",
            "",
            f"🎭 Emotional Profile:",
            f"   • Primary emotions: {', '.join([f'{emotion} ({count})' for emotion, count in top_emotions])}",
            f"   • Emotional stability: {'High' if len(emotion_counts) <= 3 else 'Moderate' if len(emotion_counts) <= 5 else 'Variable'}",
            "",
            f"💬 Interaction Patterns:",
            f"   • Common intents: {', '.join([f'{intent} ({count})' for intent, count in top_intents])}",
            f"   • Average response time: {avg_response_time:.2f}s",
            f"   • Actions executed: {len(actions_taken)} ({', '.join(set(actions_taken)[:5])})",
            "",
            f"🔄 Recent Flow: {recent_flow}",
            "",
            f"🧠 Thought Patterns: {len(self.thought_patterns)} patterns identified",
            f"⏱️ Session Info: {self.total_sessions} total sessions, {self.consciousness_uptime / 3600:.1f}h uptime"
        ]
        
        return "\n".join(summary_parts)
    
    def get_emotional_insights(self) -> Dict[str, Any]:
        """Generate insights from emotional history"""
        
        if not self.emotional_history:
            return {"status": "no_data"}
        
        # Analyze emotional patterns
        emotions = [state.emotion for state in self.emotional_history]
        intensities = [state.intensity for state in self.emotional_history]
        
        # Recent vs historical comparison
        recent_emotions = emotions[-20:] if len(emotions) >= 20 else emotions
        historical_emotions = emotions[:-20] if len(emotions) >= 40 else []
        
        emotion_counts = defaultdict(int)
        for emotion in emotions:
            emotion_counts[emotion] += 1
        
        # Intensity analysis
        avg_intensity = sum(intensities) / len(intensities)
        recent_avg_intensity = sum(intensities[-10:]) / min(10, len(intensities))
        
        # Emotional stability
        unique_emotions = len(set(emotions))
        stability_score = max(0, 1 - (unique_emotions / len(emotions)))
        
        # Trigger analysis
        trigger_counts = defaultdict(int)
        for state in self.emotional_history:
            for trigger in state.triggers:
                trigger_counts[trigger] += 1
        
        return {
            "emotional_diversity": unique_emotions,
            "dominant_emotion": max(emotion_counts, key=emotion_counts.get),
            "average_intensity": avg_intensity,
            "recent_intensity": recent_avg_intensity,
            "stability_score": stability_score,
            "common_triggers": dict(sorted(trigger_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            "emotional_trend": "increasing" if recent_avg_intensity > avg_intensity else "stable" if abs(recent_avg_intensity - avg_intensity) < 0.1 else "decreasing"
        }
    
    def get_thought_pattern_analysis(self) -> Dict[str, Any]:
        """Analyze thought patterns for insights"""
        
        if not self.thought_patterns:
            return {"status": "no_patterns"}
        
        patterns = list(self.thought_patterns.values())
        
        # Pattern effectiveness
        avg_effectiveness = sum(p.effectiveness_score for p in patterns) / len(patterns)
        most_effective = max(patterns, key=lambda p: p.effectiveness_score)
        
        # Pattern frequency
        total_occurrences = sum(p.frequency for p in patterns)
        most_frequent = max(patterns, key=lambda p: p.frequency)
        
        # Pattern types
        type_counts = defaultdict(int)
        for pattern in patterns:
            type_counts[pattern.pattern_type] += 1
        
        # Recent activity
        now = time.time()
        recent_patterns = [p for p in patterns if now - p.last_occurrence < 3600]  # Last hour
        
        return {
            "total_patterns": len(patterns),
            "average_effectiveness": avg_effectiveness,
            "most_effective_pattern": {
                "id": most_effective.pattern_id,
                "type": most_effective.pattern_type,
                "effectiveness": most_effective.effectiveness_score
            },
            "most_frequent_pattern": {
                "id": most_frequent.pattern_id,
                "type": most_frequent.pattern_type,
                "frequency": most_frequent.frequency
            },
            "pattern_distribution": dict(type_counts),
            "recent_activity": len(recent_patterns),
            "total_occurrences": total_occurrences
        }
    
    def auto_save_check(self) -> bool:
        """Check if auto-save should be triggered"""
        
        if self.state_changes_since_save >= self.auto_save_threshold:
            return self.save_state()
        return True
    
    def _increment_state_changes(self) -> None:
        """Increment state change counter and check for auto-save"""
        self.state_changes_since_save += 1
        
        # Auto-save check
        if self.state_changes_since_save >= self.auto_save_threshold:
            try:
                self.auto_save_check()
            except Exception as e:
                logger.warning(f"Auto-save failed: {e}")
    
    def _save_session(self, session: ConsciousnessSession) -> None:
        """Save individual session data"""
        
        try:
            session_file = self.sessions_dir / f"{session.session_id}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(session), f, indent=2, default=str)
            logger.debug(f"Session saved: {session.session_id}")
        except Exception as e:
            logger.error(f"Failed to save session {session.session_id}: {e}")
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive statistics"""
        
        return {
            "emotional_states_recorded": len(self.emotional_history),
            "conversations_recorded": len(self.conversation_memory),
            "thought_patterns_identified": len(self.thought_patterns),
            "total_sessions": self.total_sessions,
            "total_uptime_hours": self.consciousness_uptime / 3600,
            "state_changes_since_save": self.state_changes_since_save,
            "last_save_time": self.last_save_time,
            "memory_usage": {
                "emotional_history_size": len(self.emotional_history),
                "conversation_memory_size": len(self.conversation_memory),
                "thought_patterns_count": len(self.thought_patterns)
            }
        }
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> None:
        """Clean up old data beyond retention period"""
        
        cutoff_time = time.time() - (days_to_keep * 24 * 3600)
        
        # Clean emotional history
        self.emotional_history = deque([
            state for state in self.emotional_history 
            if state.timestamp > cutoff_time
        ], maxlen=1000)
        
        # Clean conversation memory
        self.conversation_memory = deque([
            exchange for exchange in self.conversation_memory
            if exchange.timestamp > cutoff_time
        ], maxlen=100)
        
        # Clean old thought patterns (keep if used recently)
        patterns_to_remove = [
            pid for pid, pattern in self.thought_patterns.items()
            if pattern.last_occurrence < cutoff_time
        ]
        
        for pid in patterns_to_remove:
            del self.thought_patterns[pid]
        
        logger.info(f"Cleaned up data older than {days_to_keep} days. "
                   f"Removed {len(patterns_to_remove)} old thought patterns.")


# Global instance for easy access
consciousness_state = ConsciousnessStatePersistence()


def initialize_consciousness_persistence(base_directory: str = "state") -> ConsciousnessStatePersistence:
    """Initialize consciousness state persistence system"""
    global consciousness_state
    consciousness_state = ConsciousnessStatePersistence(base_directory)
    return consciousness_state


def get_consciousness_state() -> ConsciousnessStatePersistence:
    """Get the global consciousness state persistence instance"""
    return consciousness_state 