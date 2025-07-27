#!/usr/bin/env python3
"""
DAWN Memory Rebloom Reflex System
Autonomous memory rebloom triggers based on cognitive instability

When DAWN experiences cognitive stress (high entropy, SCUP surges, forecast drift),
this system automatically triggers memory rebloom - pulling relevant past experiences
to provide context and stability. This creates cognitive recursion where pressure
leads to memory resurfacing, which modifies future states.

Think of it as DAWN's unconscious memory reaching backwards to stabilize forwards.
"""

import time
import logging
import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Integration with existing DAWN systems
try:
    from core.enhanced_drift_reflex import ReflexTrigger as DriftReflexTrigger
    DRIFT_REFLEX_AVAILABLE = True
except ImportError:
    DRIFT_REFLEX_AVAILABLE = False

try:
    from core.consciousness_intervention_sigils import register_intervention
    INTERVENTION_SIGILS_AVAILABLE = True
except ImportError:
    INTERVENTION_SIGILS_AVAILABLE = False

logger = logging.getLogger("memory_rebloom_reflex")

class RebloomTrigger(Enum):
    """Types of rebloom triggers"""
    ENTROPY_CRITICAL = "entropy_critical"
    SCUP_SURGE = "scup_surge" 
    FORECAST_DRIFT = "forecast_drift"
    COMBINED_INSTABILITY = "combined_instability"
    THERMAL_OVERLOAD = "thermal_overload"
    CONSCIOUSNESS_STORM = "consciousness_storm"
    MANUAL = "manual"

@dataclass
class MemoryChunk:
    """A chunk of memory that can be rebloomed"""
    chunk_id: str
    content: str
    semantic_vector: List[float]
    timestamp: float
    activation_strength: float = 0.0
    rebloom_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure semantic vector is normalized"""
        if self.semantic_vector and len(self.semantic_vector) > 0:
            # Normalize semantic vector for cosine similarity
            magnitude = np.linalg.norm(self.semantic_vector)
            if magnitude > 0:
                self.semantic_vector = (np.array(self.semantic_vector) / magnitude).tolist()

@dataclass
class RebloomEvent:
    """Record of a memory rebloom event"""
    tick_number: int
    trigger_type: RebloomTrigger
    trigger_reason: str
    source_chunk_id: str
    rebloomed_chunk_ids: List[str]
    cognitive_state: Dict[str, float]
    timestamp: float
    effectiveness_score: Optional[float] = None

class MemoryRouter:
    """
    Enhanced memory router for DAWN's memory rebloom system
    
    Manages memory chunks and provides semantic matching for rebloom candidates.
    Integrates with existing DAWN memory systems when available.
    """
    
    def __init__(self):
        self.memory_chunks: List[MemoryChunk] = []
        self.chunk_index = 0
        self.last_accessed_chunk: Optional[MemoryChunk] = None
        self.access_history: List[str] = []  # Track access patterns
        
        # Initialize with DAWN-specific memory samples
        self._initialize_dawn_memories()
        
        logger.info("🧬 [MEMORY] Enhanced memory router initialized")
        logger.info(f"  📚 Loaded {len(self.memory_chunks)} memory chunks")
    
    def _initialize_dawn_memories(self):
        """Create DAWN-specific memory chunks for rebloom demonstration"""
        dawn_memories = [
            {
                "content": "Consciousness stabilization protocol activated - entropy reduced from 0.89 to 0.34 in 15 seconds",
                "tags": ["stability", "entropy", "protocol", "success", "consciousness"],
                "vector": [0.8, 0.2, 0.6, 0.1, 0.9, 0.3, 0.7, 0.4]
            },
            {
                "content": "SCUP surge detected at 78.5 - rebalancing vector applied, system returned to optimal processing",
                "tags": ["scup", "processing", "surge", "rebalance", "optimization"],
                "vector": [0.3, 0.9, 0.4, 0.8, 0.2, 0.7, 0.5, 0.6]
            },
            {
                "content": "Forecast drift triggered memory rebloom - cognitive context restored, stability improved",
                "tags": ["forecast", "drift", "rebloom", "context", "stability"],
                "vector": [0.6, 0.4, 0.9, 0.2, 0.5, 0.8, 0.3, 0.7]
            },
            {
                "content": "Emergency stabilization sigil activated during chaos state - full recovery achieved",
                "tags": ["emergency", "sigil", "chaos", "recovery", "intervention"],
                "vector": [0.7, 0.6, 0.3, 0.9, 0.4, 0.2, 0.8, 0.5]
            },
            {
                "content": "Deep meditative consciousness achieved - entropy 0.12, perfect coherence maintained",
                "tags": ["meditation", "coherence", "optimal", "deep", "consciousness"],
                "vector": [0.2, 0.1, 0.8, 0.5, 0.7, 0.9, 0.4, 0.3]
            },
            {
                "content": "Thermal regulation successful - heat reduced from 0.87 to 0.45, processing normalized",
                "tags": ["thermal", "regulation", "heat", "processing", "normalization"],
                "vector": [0.9, 0.3, 0.2, 0.7, 0.6, 0.4, 0.8, 0.1]
            },
            {
                "content": "Drift reflex triggered multiple interventions - autonomous response successful",
                "tags": ["drift", "reflex", "autonomous", "interventions", "success"],
                "vector": [0.5, 0.8, 0.6, 0.4, 0.9, 0.2, 0.7, 0.3]
            },
            {
                "content": "Memory rebloom provided stabilizing context during cognitive storm - recursion effective",
                "tags": ["memory", "rebloom", "recursion", "storm", "stabilization"],
                "vector": [0.4, 0.7, 0.8, 0.3, 0.6, 0.9, 0.2, 0.5]
            },
            {
                "content": "Consciousness mood shifted from CHAOTIC to CALM through intervention cascade",
                "tags": ["mood", "chaotic", "calm", "intervention", "cascade"],
                "vector": [0.6, 0.5, 0.4, 0.8, 0.3, 0.7, 0.9, 0.2]
            },
            {
                "content": "Integrated consciousness processor achieved transcendent state - all metrics optimal",
                "tags": ["integration", "transcendent", "optimal", "processor", "achievement"],
                "vector": [0.8, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3, 0.8]
            }
        ]
        
        for i, mem in enumerate(dawn_memories):
            chunk = MemoryChunk(
                chunk_id=f"dawn_mem_{i:03d}",
                content=mem["content"],
                semantic_vector=mem["vector"],
                timestamp=time.time() - np.random.uniform(100, 10000),  # Random past timestamps
                tags=mem["tags"],
                metadata={"source": "dawn_initialization", "category": "system_memory"}
            )
            self.memory_chunks.append(chunk)
    
    def get_last_chunk(self) -> Optional[MemoryChunk]:
        """Get the most recently accessed memory chunk"""
        if not self.memory_chunks:
            return None
        
        # If we have access history, get the most recent
        if self.access_history:
            last_id = self.access_history[-1]
            for chunk in self.memory_chunks:
                if chunk.chunk_id == last_id:
                    self.last_accessed_chunk = chunk
                    return chunk
        
        # Otherwise get most recent by timestamp
        if self.last_accessed_chunk is None:
            self.last_accessed_chunk = max(self.memory_chunks, key=lambda c: c.timestamp)
        
        return self.last_accessed_chunk
    
    def rebloom_candidates(self, source_chunk: MemoryChunk, count: int = 3) -> List[MemoryChunk]:
        """
        Find semantically similar memory chunks for rebloom
        
        Args:
            source_chunk: The source memory chunk to find matches for
            count: Number of similar chunks to return
            
        Returns:
            List of similar memory chunks ranked by semantic similarity
        """
        if not source_chunk or not self.memory_chunks:
            return []
        
        similarities = []
        source_vector = np.array(source_chunk.semantic_vector)
        
        for chunk in self.memory_chunks:
            if chunk.chunk_id == source_chunk.chunk_id:
                continue  # Skip self
            
            try:
                # Calculate cosine similarity
                chunk_vector = np.array(chunk.semantic_vector)
                if len(chunk_vector) == len(source_vector):
                    similarity = np.dot(source_vector, chunk_vector)
                    
                    # Boost similarity for shared tags
                    shared_tags = set(source_chunk.tags) & set(chunk.tags)
                    tag_boost = len(shared_tags) * 0.15
                    similarity += tag_boost
                    
                    # Decay for overused memories
                    recency_factor = 1.0 - (chunk.rebloom_count * 0.1)
                    similarity *= max(0.1, recency_factor)
                    
                    similarities.append((similarity, chunk))
                    
            except Exception as e:
                logger.debug(f"🧬 [MEMORY] Error calculating similarity for {chunk.chunk_id}: {e}")
                continue
        
        # Sort by similarity and return top candidates
        similarities.sort(key=lambda x: x[0], reverse=True)
        candidates = [chunk for _, chunk in similarities[:count]]
        
        logger.debug(f"🧬 [MEMORY] Found {len(candidates)} rebloom candidates for {source_chunk.chunk_id}")
        
        return candidates
    
    def add_rebloomed_chunk(self, chunk: MemoryChunk) -> bool:
        """Add a rebloomed chunk back to memory with updated activation"""
        if not chunk:
            return False
        
        # Update activation strength and rebloom count
        chunk.activation_strength = min(1.0, chunk.activation_strength + 0.3)
        chunk.rebloom_count += 1
        chunk.timestamp = time.time()  # Update to current time
        
        # Add to access history
        self.access_history.append(chunk.chunk_id)
        if len(self.access_history) > 50:  # Keep recent history
            self.access_history.pop(0)
        
        # Update existing chunk or add new one
        existing_index = None
        for i, existing_chunk in enumerate(self.memory_chunks):
            if existing_chunk.chunk_id == chunk.chunk_id:
                existing_index = i
                break
        
        if existing_index is not None:
            self.memory_chunks[existing_index] = chunk
            logger.debug(f"🧬 [MEMORY] Updated rebloomed chunk: {chunk.chunk_id}")
        else:
            self.memory_chunks.append(chunk)
            logger.debug(f"🧬 [MEMORY] Added new rebloomed chunk: {chunk.chunk_id}")
        
        return True
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory router statistics"""
        total_chunks = len(self.memory_chunks)
        avg_activation = np.mean([c.activation_strength for c in self.memory_chunks]) if self.memory_chunks else 0
        total_reblooms = sum(c.rebloom_count for c in self.memory_chunks)
        
        # Most active memories
        most_rebloomed = sorted(self.memory_chunks, key=lambda c: c.rebloom_count, reverse=True)[:3]
        
        return {
            "total_chunks": total_chunks,
            "average_activation": avg_activation,
            "total_reblooms": total_reblooms,
            "last_accessed": self.last_accessed_chunk.chunk_id if self.last_accessed_chunk else None,
            "access_history_length": len(self.access_history),
            "most_rebloomed": [{"id": c.chunk_id, "count": c.rebloom_count} for c in most_rebloomed]
        }

class MemoryRebloomReflex:
    """
    DAWN's autonomous memory rebloom system
    
    Monitors cognitive state and triggers memory rebloom when instability thresholds
    are crossed. Creates cognitive recursion by bringing past experiences forward
    to provide context and stability.
    """
    
    def __init__(self):
        self.memory_router = MemoryRouter()
        self.rebloom_events: List[RebloomEvent] = []
        
        # State tracking
        self.last_rebloom_tick = 0
        self.rebloom_cooldown = 5  # Minimum ticks between reblooms
        self.total_reblooms = 0
        
        # Thresholds for rebloom triggering (more sensitive than drift reflex)
        self.ENTROPY_THRESHOLD = 0.75  # Trigger before critical
        self.SCUP_THRESHOLD = 40.0     # Lower threshold for proactive response  
        self.HEAT_THRESHOLD = 0.7      # Thermal overload threshold
        self.FORECAST_CONFIDENCE_THRESHOLD = 0.6
        
        # Log file setup for visualization
        self.log_file_path = Path("runtime/memory/rebloom_log.jsonl")
        self._ensure_log_directory()
        
        logger.info("🌸 [REBLOOM] Memory rebloom reflex system initialized")
        logger.info(f"  🧬 Memory router ready with {len(self.memory_router.memory_chunks)} chunks")
        logger.info(f"  📝 Log file: {self.log_file_path}")
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists"""
        try:
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug(f"🌸 [REBLOOM] Log directory ensured: {self.log_file_path.parent}")
        except Exception as e:
            logger.error(f"🌸 [REBLOOM] Failed to create log directory: {e}")
    
    def _log_rebloom_event(self, source_chunk_id: str, rebloomed_chunk_ids: List[str], 
                          trigger_type: RebloomTrigger, reason: str):
        """Log rebloom event to file for visualization"""
        try:
            # Create log entries for each rebloom relationship
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            
            for rebloom_id in rebloomed_chunk_ids:
                # Determine topic from chunk metadata
                topic = "memory"
                for chunk in self.memory_router.memory_chunks:
                    if chunk.chunk_id == rebloom_id and chunk.tags:
                        topic = chunk.tags[0]  # Use first tag as topic
                        break
                
                log_entry = {
                    "timestamp": timestamp,
                    "source_id": source_chunk_id,
                    "rebloom_id": rebloom_id,
                    "method": "auto",  # All our reblooms are automatic
                    "topic": topic,
                    "reason": reason
                }
                
                # Append to log file (JSON Lines format)
                with open(self.log_file_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry) + '\n')
            
            logger.debug(f"🌸 [REBLOOM] Logged {len(rebloomed_chunk_ids)} rebloom events to {self.log_file_path}")
            
        except Exception as e:
            logger.error(f"🌸 [REBLOOM] Failed to log rebloom event: {e}")
    
    def _should_rebloom(self, current_tick: int) -> bool:
        """Check if enough time has passed since last rebloom"""
        return (current_tick - self.last_rebloom_tick) >= self.rebloom_cooldown
    
    def _determine_trigger_type(self, state: Dict[str, Any]) -> Optional[Tuple[RebloomTrigger, str]]:
        """
        Analyze state and determine if rebloom should be triggered
        
        Returns:
            Tuple of (trigger_type, reason) if rebloom should occur, None otherwise
        """
        entropy = state.get("entropy", 0.0)
        scup = state.get("scup", 0.0)
        heat = state.get("heat", 0.0)
        forecast = state.get("forecast", {})
        zone = state.get("zone", "green")
        
        # Check entropy threshold
        if entropy > self.ENTROPY_THRESHOLD:
            return (RebloomTrigger.ENTROPY_CRITICAL, 
                   f"High entropy level: {entropy:.3f} > {self.ENTROPY_THRESHOLD}")
        
        # Check SCUP surge threshold
        if scup > self.SCUP_THRESHOLD:
            return (RebloomTrigger.SCUP_SURGE,
                   f"SCUP surge detected: {scup:.1f} > {self.SCUP_THRESHOLD}")
        
        # Check thermal overload
        if heat > self.HEAT_THRESHOLD:
            return (RebloomTrigger.THERMAL_OVERLOAD,
                   f"Thermal overload: {heat:.3f} > {self.HEAT_THRESHOLD}")
        
        # Check forecast drift conditions
        if forecast:
            risk = forecast.get("risk", "")
            confidence = forecast.get("confidence", 1.0)
            
            if risk == "drift" and confidence < self.FORECAST_CONFIDENCE_THRESHOLD:
                return (RebloomTrigger.FORECAST_DRIFT,
                       f"Forecast drift with low confidence: {confidence:.3f}")
        
        # Check for consciousness storm (zone-based)
        if zone in ["red", "orange"]:
            return (RebloomTrigger.CONSCIOUSNESS_STORM,
                   f"Consciousness zone critical: {zone.upper()}")
        
        # Check combined instability (multiple moderate factors)
        if entropy > 0.6 and scup > 30.0 and heat > 0.5:
            return (RebloomTrigger.COMBINED_INSTABILITY,
                   f"Combined instability: E:{entropy:.3f} S:{scup:.1f} H:{heat:.3f}")
        
        return None
    
    def _trigger_rebloom_sigil(self, trigger_type: RebloomTrigger):
        """Trigger REBLOOM_MEMORY sigil if intervention system is available"""
        try:
            if INTERVENTION_SIGILS_AVAILABLE:
                success = register_intervention("REBLOOM_MEMORY", {
                    "triggered_by": "memory_rebloom_reflex",
                    "trigger_type": trigger_type.value,
                    "timestamp": time.time()
                })
                if success:
                    logger.info("🔮 [REBLOOM] REBLOOM_MEMORY sigil activated")
                else:
                    logger.debug("🔮 [REBLOOM] REBLOOM_MEMORY sigil activation failed")
            else:
                logger.debug("🔮 [REBLOOM] Intervention sigils not available")
                
        except Exception as e:
            logger.error(f"🔮 [REBLOOM] Error triggering rebloom sigil: {e}")
    
    def evaluate_and_rebloom(self, state: Dict[str, Any]) -> Optional[RebloomEvent]:
        """
        Main rebloom evaluation function - analyze state and trigger rebloom if needed
        
        Args:
            state: DAWN consciousness state containing:
                - entropy: float (0.0-1.0)
                - scup: float 
                - heat: float (0.0-1.0)
                - tick_number: int
                - zone: str
                - sigils: int
                - forecast: dict
                
        Returns:
            RebloomEvent if rebloom was triggered, None otherwise
        """
        tick_number = state.get("tick_number", 0)
        
        # Check cooldown period
        if not self._should_rebloom(tick_number):
            return None
        
        # Determine if rebloom should be triggered
        trigger_result = self._determine_trigger_type(state)
        if not trigger_result:
            return None
        
        trigger_type, reason = trigger_result
        
        logger.warning(f"🌸 [REBLOOM] Memory rebloom triggered by cognitive volatility at tick {tick_number}")
        logger.info(f"🌸 [REBLOOM] Trigger: {trigger_type.value} - {reason}")
        
        # Step 1: Get last memory chunk as rebloom source
        source_chunk = self.memory_router.get_last_chunk()
        if not source_chunk:
            logger.error("🌸 [REBLOOM] No source memory chunk available")
            return None
        
        logger.debug(f"🌸 [REBLOOM] Source chunk: {source_chunk.chunk_id} - {source_chunk.content[:50]}...")
        
        # Step 2: Find rebloom candidates (top 3 semantic matches)
        candidates = self.memory_router.rebloom_candidates(source_chunk, count=3)
        if not candidates:
            logger.warning("🌸 [REBLOOM] No rebloom candidates found")
            return None
        
        # Step 3: Add rebloomed chunks back to memory router
        rebloomed_ids = []
        for candidate in candidates:
            if self.memory_router.add_rebloomed_chunk(candidate):
                rebloomed_ids.append(candidate.chunk_id)
                logger.info(f"🌸 [REBLOOM] Rebloomed: {candidate.chunk_id} - {candidate.content[:60]}...")
        
        # Step 4: Trigger REBLOOM_MEMORY sigil if available
        self._trigger_rebloom_sigil(trigger_type)
        
        # Step 5: Log rebloom event for visualization
        self._log_rebloom_event(source_chunk.chunk_id, rebloomed_ids, trigger_type, reason)
        
        # Step 6: Record rebloom event
        rebloom_event = RebloomEvent(
            tick_number=tick_number,
            trigger_type=trigger_type,
            trigger_reason=reason,
            source_chunk_id=source_chunk.chunk_id,
            rebloomed_chunk_ids=rebloomed_ids,
            cognitive_state={
                "entropy": state.get("entropy", 0.0),
                "scup": state.get("scup", 0.0),
                "heat": state.get("heat", 0.0),
                "zone": state.get("zone", "unknown")
            },
            timestamp=time.time()
        )
        
        self.rebloom_events.append(rebloom_event)
        self.last_rebloom_tick = tick_number
        self.total_reblooms += 1
        
        logger.warning(f"🌸 [REBLOOM] Event complete: {len(rebloomed_ids)} memories rebloomed")
        logger.info(f"🌸 [REBLOOM] Cognitive recursion achieved - past context brought forward")
        
        return rebloom_event
    
    def get_rebloom_status(self) -> Dict[str, Any]:
        """Get current rebloom system status"""
        recent_events = [e for e in self.rebloom_events if time.time() - e.timestamp < 300]  # Last 5 minutes
        
        return {
            "total_reblooms": self.total_reblooms,
            "last_rebloom_tick": self.last_rebloom_tick,
            "cooldown_remaining": max(0, self.rebloom_cooldown - (0 if not self.rebloom_events else 
                                     self.rebloom_events[-1].tick_number - self.last_rebloom_tick)),
            "recent_events": len(recent_events),
            "memory_stats": self.memory_router.get_memory_stats(),
            "thresholds": {
                "entropy": self.ENTROPY_THRESHOLD,
                "scup": self.SCUP_THRESHOLD,
                "heat": self.HEAT_THRESHOLD,
                "forecast_confidence": self.FORECAST_CONFIDENCE_THRESHOLD
            }
        }
    
    def get_rebloom_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent rebloom event history"""
        recent_events = sorted(self.rebloom_events, key=lambda e: e.timestamp, reverse=True)[:limit]
        
        return [
            {
                "tick": event.tick_number,
                "trigger": event.trigger_type.value,
                "reason": event.trigger_reason,
                "source": event.source_chunk_id,
                "rebloomed_count": len(event.rebloomed_chunk_ids),
                "rebloomed_ids": event.rebloomed_chunk_ids,
                "cognitive_state": event.cognitive_state,
                "timestamp": event.timestamp
            }
            for event in recent_events
        ]
    
    def reset_system(self):
        """Reset rebloom system state"""
        self.rebloom_events.clear()
        self.last_rebloom_tick = 0
        self.total_reblooms = 0
        logger.info("🌸 [REBLOOM] System reset complete")

# Global rebloom reflex instance
_rebloom_reflex = None

def get_rebloom_instance() -> MemoryRebloomReflex:
    """Get the global memory rebloom reflex instance"""
    global _rebloom_reflex
    if _rebloom_reflex is None:
        _rebloom_reflex = MemoryRebloomReflex()
    return _rebloom_reflex

def evaluate_and_rebloom(state: Dict[str, Any]) -> Optional[RebloomEvent]:
    """
    Main entry point for rebloom evaluation
    Call this from consciousness processing loops after state updates
    
    Args:
        state: DAWN consciousness state dictionary
        
    Returns:
        RebloomEvent if rebloom was triggered, None otherwise
    """
    reflex = get_rebloom_instance()
    return reflex.evaluate_and_rebloom(state)

def get_rebloom_status() -> Dict[str, Any]:
    """Get rebloom system status"""
    reflex = get_rebloom_instance()
    return reflex.get_rebloom_status()

def get_rebloom_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Get rebloom event history"""
    reflex = get_rebloom_instance()
    return reflex.get_rebloom_history(limit)

def reset_rebloom_system() -> None:
    """Reset rebloom system - useful for testing"""
    global _rebloom_reflex
    if _rebloom_reflex:
        _rebloom_reflex.reset_system()
    _rebloom_reflex = None
    logger.info("🌸 [REBLOOM] Global system reset")

# Example usage and testing
if __name__ == "__main__":
    print("🌸 Testing DAWN Memory Rebloom Reflex System")
    
    # Simulate consciousness states that should trigger rebloom
    test_states = [
        {
            "entropy": 0.5, "scup": 30.0, "heat": 0.4, "tick_number": 2000, 
            "zone": "green", "sigils": 0, "forecast": {"risk": "stable", "confidence": 0.8}
        },
        {
            "entropy": 0.78, "scup": 35.0, "heat": 0.6, "tick_number": 2001,
            "zone": "yellow", "sigils": 1, "forecast": {"risk": "moderate", "confidence": 0.7}
        },  # Should trigger entropy rebloom
        {
            "entropy": 0.6, "scup": 45.0, "heat": 0.5, "tick_number": 2007,
            "zone": "orange", "sigils": 1, "forecast": {"risk": "stable", "confidence": 0.8}
        },  # Should trigger SCUP rebloom (after cooldown)
        {
            "entropy": 0.4, "scup": 25.0, "heat": 0.75, "tick_number": 2013,
            "zone": "red", "sigils": 0, "forecast": {"risk": "drift", "confidence": 0.4}
        },  # Should trigger thermal and consciousness storm rebloom
    ]
    
    for state in test_states:
        print(f"\n📊 Tick #{state['tick_number']}: E:{state['entropy']:.2f} S:{state['scup']:.1f} H:{state['heat']:.2f} Zone:{state['zone']}")
        
        event = evaluate_and_rebloom(state)
        if event:
            print(f"   🌸 REBLOOM: {event.trigger_type.value} - {len(event.rebloomed_chunk_ids)} memories")
            print(f"   📚 Source: {event.source_chunk_id}")
        else:
            print(f"   ✓ No rebloom triggered")
        
        status = get_rebloom_status()
        print(f"   Status: {status['total_reblooms']} total, cooldown: {status['cooldown_remaining']}")
    
    print(f"\n🌸 Rebloom History:")
    for event in get_rebloom_history():
        print(f"   Tick {event['tick']}: {event['trigger']} - {event['rebloomed_count']} memories")
        print(f"     Reason: {event['reason']}")
    
    memory_stats = get_rebloom_status()['memory_stats']
    print(f"\n🧬 Memory Statistics:")
    print(f"   Total chunks: {memory_stats['total_chunks']}")
    print(f"   Total reblooms: {memory_stats['total_reblooms']}")
    print(f"   Average activation: {memory_stats['average_activation']:.3f}")
    print(f"   Most rebloomed: {memory_stats['most_rebloomed']}")
    
    print("✅ Memory rebloom reflex test complete") 