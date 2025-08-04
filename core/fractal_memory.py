#!/usr/bin/env python3
"""
DAWN Fractal Memory System - Shimmer Decay & Crystallization
===========================================================

Implements fractal memory management with shimmer decay mathematics:
Shimmer = A * exp(-λt)

Where:
- A: Initial shimmer amplitude (memory vividness)
- λ: Decay constant (memory fade rate)
- t: Time since memory creation

Features:
- Memory shimmer decay tracking
- Automatic crystallization when shimmer < threshold + age > limit
- Juliet signatures (UUID + fragment hash) for memory identity
- Fractal memory pattern analysis
- Memory consolidation and rebloom management
- Visual shimmer representation for GUI

The system maintains DAWN's memory ecology, ensuring important memories
crystallize into stable long-term storage while transient memories
fade naturally through shimmer decay.
"""

import time
import math
import logging
import hashlib
import uuid
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable, Set
from datetime import datetime, timezone
from collections import deque, defaultdict
from enum import Enum
from pathlib import Path
import json

logger = logging.getLogger("fractal_memory")

class MemoryType(Enum):
    """Types of memories in the fractal system"""
    EXPERIENCE = "experience"           # Direct experiential memories
    REFLECTION = "reflection"           # Reflective thoughts and insights
    KNOWLEDGE = "knowledge"             # Factual or learned information
    EMOTION = "emotion"                 # Emotional associations
    PATTERN = "pattern"                 # Recognized patterns or relationships
    INTENTION = "intention"             # Goals, plans, and intentions
    DREAM = "dream"                     # Dream-state or imaginative content
    CRYSTALLIZED = "crystallized"       # Stable, long-term memories

class MemoryState(Enum):
    """Current state of a memory"""
    FRESH = "fresh"                     # Recently created, high shimmer
    ACTIVE = "active"                   # Being accessed/reinforced
    FADING = "fading"                   # Natural decay in progress
    CONSOLIDATING = "consolidating"     # Being prepared for crystallization
    CRYSTALLIZED = "crystallized"       # Stable, long-term storage
    ARCHIVED = "archived"               # Dormant but preserved

@dataclass
class JulietSignature:
    """Unique identifier for memory fragments"""
    uuid: str                           # Unique identifier
    content_hash: str                   # Hash of fragment content
    creation_timestamp: float           # When signature was created
    fragment_essence: str               # Core essence of the fragment
    pattern_signature: str              # Fractal pattern identifier

@dataclass
class MemoryShimmer:
    """Shimmer state of a memory"""
    amplitude: float                    # A: Initial shimmer amplitude
    decay_constant: float               # λ: Decay rate
    current_shimmer: float              # Current shimmer value
    shimmer_history: List[float] = field(default_factory=list)
    last_calculation: float = 0.0
    reinforcement_count: int = 0        # Times memory was accessed/reinforced

@dataclass
class FractalMemory:
    """Individual memory in the fractal system"""
    juliet_signature: JulietSignature
    memory_type: MemoryType
    memory_state: MemoryState
    content: str                        # Memory content
    shimmer: MemoryShimmer
    
    # Temporal properties
    creation_time: float
    last_access_time: float
    age_hours: float = 0.0
    
    # Fractal properties
    complexity_score: float = 0.5       # How complex/rich the memory is
    connection_strength: float = 0.5    # How connected to other memories
    emotional_resonance: float = 0.5    # Emotional significance
    
    # Crystallization tracking
    crystallization_threshold: float = 0.1
    age_threshold_hours: float = 100.0
    crystallization_score: float = 0.0
    
    # Metadata
    tags: Set[str] = field(default_factory=set)
    related_memories: Set[str] = field(default_factory=set)  # UUIDs
    access_count: int = 0
    rebloom_eligible: bool = True

@dataclass
class CrystallizationEvent:
    """Record of a memory crystallization"""
    timestamp: float
    memory_uuid: str
    memory_type: MemoryType
    final_shimmer: float
    age_hours: float
    crystallization_reason: str
    preservation_quality: float         # How well the memory was preserved

class MemoryFractalManager:
    """
    Fractal Memory Management System
    
    Manages memory lifecycle through shimmer decay, crystallization,
    and fractal pattern analysis. Maintains the temporal ecology
    of DAWN's memory system.
    """
    
    def __init__(self):
        """Initialize the Memory Fractal Manager"""
        
        # Memory storage
        self.active_memories: Dict[str, FractalMemory] = {}
        self.crystallized_memories: Dict[str, FractalMemory] = {}
        self.memory_index: Dict[str, str] = {}  # content_hash -> uuid
        
        # Shimmer decay configuration
        self.DEFAULT_SHIMMER_AMPLITUDE = 1.0
        self.DEFAULT_DECAY_CONSTANT = 0.01      # λ for moderate decay
        self.SHIMMER_CALCULATION_INTERVAL = 300  # 5 minutes
        self.CRYSTALLIZATION_THRESHOLD = 0.1
        self.AGE_THRESHOLD_HOURS = 100.0
        
        # Memory type configurations
        self.MEMORY_TYPE_CONFIGS = {
            MemoryType.EXPERIENCE: {
                "default_amplitude": 1.2,
                "decay_constant": 0.008,  # Slower decay for experiences
                "age_threshold": 120.0,
                "complexity_weight": 1.2
            },
            MemoryType.REFLECTION: {
                "default_amplitude": 1.0,
                "decay_constant": 0.01,
                "age_threshold": 80.0,
                "complexity_weight": 1.4
            },
            MemoryType.KNOWLEDGE: {
                "default_amplitude": 0.8,
                "decay_constant": 0.005,  # Very slow decay for knowledge
                "age_threshold": 200.0,
                "complexity_weight": 1.0
            },
            MemoryType.EMOTION: {
                "default_amplitude": 1.5,
                "decay_constant": 0.015,  # Faster initial decay
                "age_threshold": 60.0,
                "complexity_weight": 1.3
            },
            MemoryType.PATTERN: {
                "default_amplitude": 1.1,
                "decay_constant": 0.007,
                "age_threshold": 150.0,
                "complexity_weight": 1.5
            },
            MemoryType.INTENTION: {
                "default_amplitude": 1.3,
                "decay_constant": 0.012,
                "age_threshold": 48.0,    # Shorter threshold for intentions
                "complexity_weight": 1.1
            },
            MemoryType.DREAM: {
                "default_amplitude": 0.9,
                "decay_constant": 0.02,   # Dreams fade quickly
                "age_threshold": 24.0,    # Very short threshold
                "complexity_weight": 0.8
            }
        }
        
        # Performance tracking
        self.memories_created = 0
        self.memories_crystallized = 0
        self.shimmer_calculations = 0
        self.rebloom_events = 0
        
        # Event history
        self.crystallization_history: deque = deque(maxlen=100)
        self.shimmer_update_history: deque = deque(maxlen=50)
        
        # Callback system
        self.crystallization_callbacks: List[Callable] = []
        self.shimmer_update_callbacks: List[Callable] = []
        self.rebloom_callbacks: List[Callable] = []
        
        # System state
        self.last_maintenance_time = 0.0
        self.maintenance_interval = 1800  # 30 minutes
        
        logger.info("🔮 [FRACTAL] Memory Fractal Manager initialized")
        logger.info(f"🔮 [FRACTAL] Memory types configured: {len(self.MEMORY_TYPE_CONFIGS)}")
        logger.info(f"🔮 [FRACTAL] Crystallization threshold: {self.CRYSTALLIZATION_THRESHOLD}")
    
    def create_memory(self, content: str, memory_type: MemoryType = MemoryType.EXPERIENCE, 
                     initial_shimmer: Optional[float] = None, tags: Set[str] = None) -> FractalMemory:
        """
        Create a new fractal memory with shimmer tracking
        
        Args:
            content: Memory content
            memory_type: Type of memory
            initial_shimmer: Override default shimmer amplitude
            tags: Optional tags for the memory
            
        Returns:
            Created FractalMemory
        """
        
        try:
            current_time = time.time()
            
            # Generate Juliet signature
            juliet_signature = self._generate_juliet_signature(content, current_time)
            
            # Check for duplicate content
            if juliet_signature.content_hash in self.memory_index:
                existing_uuid = self.memory_index[juliet_signature.content_hash]
                logger.debug(f"🔮 [FRACTAL] Reinforcing existing memory: {existing_uuid[:8]}...")
                return self._reinforce_memory(existing_uuid)
            
            # Get configuration for memory type
            config = self.MEMORY_TYPE_CONFIGS.get(memory_type, self.MEMORY_TYPE_CONFIGS[MemoryType.EXPERIENCE])
            
            # Create shimmer with appropriate parameters
            amplitude = initial_shimmer if initial_shimmer is not None else config["default_amplitude"]
            decay_constant = config["decay_constant"]
            
            shimmer = MemoryShimmer(
                amplitude=amplitude,
                decay_constant=decay_constant,
                current_shimmer=amplitude,
                last_calculation=current_time
            )
            
            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(content, memory_type)
            
            # Create memory
            memory = FractalMemory(
                juliet_signature=juliet_signature,
                memory_type=memory_type,
                memory_state=MemoryState.FRESH,
                content=content,
                shimmer=shimmer,
                creation_time=current_time,
                last_access_time=current_time,
                complexity_score=complexity_score,
                crystallization_threshold=self.CRYSTALLIZATION_THRESHOLD,
                age_threshold_hours=config["age_threshold"],
                tags=tags or set()
            )
            
            # Store memory
            self.active_memories[juliet_signature.uuid] = memory
            self.memory_index[juliet_signature.content_hash] = juliet_signature.uuid
            self.memories_created += 1
            
            logger.info(f"🔮 [FRACTAL] Created {memory_type.value} memory: {juliet_signature.uuid[:8]}... (shimmer={amplitude:.2f})")
            
            return memory
            
        except Exception as e:
            logger.error(f"🔮 [FRACTAL] Memory creation error: {e}")
            raise
    
    def _generate_juliet_signature(self, content: str, creation_time: float) -> JulietSignature:
        """Generate unique Juliet signature for memory"""
        
        # Create UUID
        memory_uuid = str(uuid.uuid4())
        
        # Hash content for deduplication
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
        
        # Extract essence (first meaningful words)
        words = content.split()
        essence = ' '.join(words[:5]) if len(words) >= 5 else content
        
        # Generate pattern signature based on content structure
        pattern_elements = [
            str(len(content)),
            str(len(words)),
            str(content.count('.')),
            str(content.count('?')),
            str(content.count('!')),
            str(hash(content) % 1000)  # Structural hash
        ]
        pattern_signature = '-'.join(pattern_elements)
        
        return JulietSignature(
            uuid=memory_uuid,
            content_hash=content_hash,
            creation_timestamp=creation_time,
            fragment_essence=essence,
            pattern_signature=pattern_signature
        )
    
    def _calculate_complexity_score(self, content: str, memory_type: MemoryType) -> float:
        """Calculate complexity score for a memory"""
        
        # Base complexity factors
        length_factor = min(1.0, len(content) / 200.0)  # Longer = more complex
        word_count_factor = min(1.0, len(content.split()) / 50.0)
        punctuation_factor = min(1.0, (content.count('.') + content.count('?') + content.count('!')) / 10.0)
        
        # Memory type weight
        type_weight = self.MEMORY_TYPE_CONFIGS[memory_type]["complexity_weight"]
        
        # Calculate base complexity
        base_complexity = (length_factor * 0.4 + word_count_factor * 0.4 + punctuation_factor * 0.2)
        
        # Apply type weight and normalize
        complexity = base_complexity * type_weight
        return max(0.1, min(1.0, complexity))
    
    def _reinforce_memory(self, memory_uuid: str) -> FractalMemory:
        """Reinforce an existing memory (boost shimmer, reset access time)"""
        
        if memory_uuid not in self.active_memories:
            raise ValueError(f"Memory {memory_uuid} not found in active memories")
        
        memory = self.active_memories[memory_uuid]
        current_time = time.time()
        
        # Update shimmer (reinforcement effect)
        reinforcement_boost = 0.2 * (1.0 - memory.shimmer.current_shimmer)  # Boost scales with decay
        memory.shimmer.current_shimmer = min(memory.shimmer.amplitude, 
                                           memory.shimmer.current_shimmer + reinforcement_boost)
        memory.shimmer.reinforcement_count += 1
        
        # Update access tracking
        memory.last_access_time = current_time
        memory.access_count += 1
        memory.memory_state = MemoryState.ACTIVE
        
        logger.debug(f"🔮 [FRACTAL] Reinforced memory: {memory_uuid[:8]}... (shimmer={memory.shimmer.current_shimmer:.2f})")
        
        return memory
    
    def tick_shimmer_decay(self) -> Dict[str, Any]:
        """
        Update shimmer values for all active memories using A * exp(-λt)
        
        Returns:
            Summary of shimmer updates and crystallizations
        """
        
        tick_start = time.time()
        current_time = time.time()
        
        # Check if it's time for shimmer calculation
        if current_time - self.last_maintenance_time < self.SHIMMER_CALCULATION_INTERVAL:
            return {"status": "skipped", "reason": "interval_not_reached"}
        
        updated_memories = 0
        crystallized_memories = 0
        total_shimmer = 0.0
        
        memories_to_crystallize = []
        
        try:
            # Update shimmer for all active memories
            for memory_uuid, memory in list(self.active_memories.items()):
                
                # Calculate time elapsed since last calculation
                time_elapsed = current_time - memory.shimmer.last_calculation
                
                # Apply shimmer decay formula: A * exp(-λt)
                decay_factor = math.exp(-memory.shimmer.decay_constant * time_elapsed)
                new_shimmer = memory.shimmer.current_shimmer * decay_factor
                
                # Update memory shimmer
                memory.shimmer.current_shimmer = max(0.0, new_shimmer)
                memory.shimmer.last_calculation = current_time
                memory.shimmer.shimmer_history.append(new_shimmer)
                
                # Limit shimmer history
                if len(memory.shimmer.shimmer_history) > 20:
                    memory.shimmer.shimmer_history = memory.shimmer.shimmer_history[-20:]
                
                # Update memory age
                memory.age_hours = (current_time - memory.creation_time) / 3600.0
                
                # Check for crystallization conditions
                crystallization_score = self._calculate_crystallization_score(memory)
                memory.crystallization_score = crystallization_score
                
                if self._should_crystallize(memory):
                    memories_to_crystallize.append(memory_uuid)
                
                updated_memories += 1
                total_shimmer += memory.shimmer.current_shimmer
                
                # Update memory state based on shimmer
                if memory.shimmer.current_shimmer < 0.3:
                    memory.memory_state = MemoryState.FADING
                elif crystallization_score > 0.8:
                    memory.memory_state = MemoryState.CONSOLIDATING
            
            # Process crystallizations
            for memory_uuid in memories_to_crystallize:
                self._crystallize_memory(memory_uuid)
                crystallized_memories += 1
            
            # Update performance tracking
            self.shimmer_calculations += 1
            self.last_maintenance_time = current_time
            
            # Create summary
            summary = {
                "status": "completed",
                "updated_memories": updated_memories,
                "crystallized_memories": crystallized_memories,
                "average_shimmer": total_shimmer / max(1, updated_memories),
                "active_memory_count": len(self.active_memories),
                "crystallized_memory_count": len(self.crystallized_memories),
                "calculation_time_ms": (time.time() - tick_start) * 1000
            }
            
            # Store update history
            self.shimmer_update_history.append({
                "timestamp": current_time,
                "summary": summary
            })
            
            # Execute callbacks
            for callback in self.shimmer_update_callbacks:
                try:
                    callback(summary)
                except Exception as e:
                    logger.warning(f"🔮 [FRACTAL] Shimmer update callback failed: {e}")
            
            if crystallized_memories > 0:
                logger.info(f"🔮 [FRACTAL] Shimmer tick: {updated_memories} updated, {crystallized_memories} crystallized, avg shimmer: {summary['average_shimmer']:.3f}")
            else:
                logger.debug(f"🔮 [FRACTAL] Shimmer tick: {updated_memories} memories updated, avg shimmer: {summary['average_shimmer']:.3f}")
            
            return summary
            
        except Exception as e:
            logger.error(f"🔮 [FRACTAL] Shimmer tick error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _calculate_crystallization_score(self, memory: FractalMemory) -> float:
        """Calculate how ready a memory is for crystallization"""
        
        # Factors that promote crystallization
        age_factor = min(1.0, memory.age_hours / memory.age_threshold_hours)
        complexity_factor = memory.complexity_score
        access_factor = min(1.0, memory.access_count / 10.0)  # More access = more important
        connection_factor = memory.connection_strength
        emotional_factor = memory.emotional_resonance
        
        # Shimmer decay factor (low shimmer promotes crystallization)
        shimmer_factor = 1.0 - memory.shimmer.current_shimmer
        
        # Weight the factors
        crystallization_score = (
            age_factor * 0.3 +
            complexity_factor * 0.2 +
            access_factor * 0.2 +
            connection_factor * 0.1 +
            emotional_factor * 0.1 +
            shimmer_factor * 0.1
        )
        
        return max(0.0, min(1.0, crystallization_score))
    
    def _should_crystallize(self, memory: FractalMemory) -> bool:
        """Determine if a memory should be crystallized"""
        
        # Primary crystallization conditions
        shimmer_condition = memory.shimmer.current_shimmer < memory.crystallization_threshold
        age_condition = memory.age_hours > memory.age_threshold_hours
        score_condition = memory.crystallization_score > 0.85
        
        # Memory must meet shimmer threshold AND (age OR high score)
        return shimmer_condition and (age_condition or score_condition)
    
    def _crystallize_memory(self, memory_uuid: str):
        """Crystallize a memory into long-term storage"""
        
        if memory_uuid not in self.active_memories:
            logger.warning(f"🔮 [FRACTAL] Cannot crystallize non-existent memory: {memory_uuid}")
            return
        
        memory = self.active_memories[memory_uuid]
        current_time = time.time()
        
        try:
            # Calculate preservation quality based on final state
            preservation_quality = self._calculate_preservation_quality(memory)
            
            # Determine crystallization reason
            if memory.shimmer.current_shimmer < memory.crystallization_threshold:
                reason = "shimmer_decay"
            elif memory.age_hours > memory.age_threshold_hours:
                reason = "age_threshold"
            else:
                reason = "high_score"
            
            # Create crystallization event
            crystallization_event = CrystallizationEvent(
                timestamp=current_time,
                memory_uuid=memory_uuid,
                memory_type=memory.memory_type,
                final_shimmer=memory.shimmer.current_shimmer,
                age_hours=memory.age_hours,
                crystallization_reason=reason,
                preservation_quality=preservation_quality
            )
            
            # Update memory state
            memory.memory_state = MemoryState.CRYSTALLIZED
            memory.memory_type = MemoryType.CRYSTALLIZED  # Transform type
            
            # Move to crystallized storage
            self.crystallized_memories[memory_uuid] = memory
            del self.active_memories[memory_uuid]
            
            # Update performance tracking
            self.memories_crystallized += 1
            self.crystallization_history.append(crystallization_event)
            
            # Log crystallization to file
            self._log_crystallization_event(crystallization_event)
            
            # Execute callbacks
            for callback in self.crystallization_callbacks:
                try:
                    callback(crystallization_event)
                except Exception as e:
                    logger.warning(f"🔮 [FRACTAL] Crystallization callback failed: {e}")
            
            logger.info(f"💎 [FRACTAL] Crystallized memory: {memory_uuid[:8]}... ({reason}, quality={preservation_quality:.2f})")
            
        except Exception as e:
            logger.error(f"🔮 [FRACTAL] Crystallization error for {memory_uuid}: {e}")
    
    def _calculate_preservation_quality(self, memory: FractalMemory) -> float:
        """Calculate how well a memory is preserved during crystallization"""
        
        # Factors affecting preservation quality
        shimmer_factor = memory.shimmer.current_shimmer  # Higher shimmer = better preservation
        complexity_factor = memory.complexity_score
        access_factor = min(1.0, memory.access_count / 5.0)
        reinforcement_factor = min(1.0, memory.shimmer.reinforcement_count / 3.0)
        
        # Age penalty (very old memories may degrade)
        age_penalty = max(0.0, (memory.age_hours - memory.age_threshold_hours) / memory.age_threshold_hours * 0.3)
        
        # Calculate quality
        quality = (
            shimmer_factor * 0.4 +
            complexity_factor * 0.25 +
            access_factor * 0.2 +
            reinforcement_factor * 0.15
        ) - age_penalty
        
        return max(0.1, min(1.0, quality))
    
    def _log_crystallization_event(self, event: CrystallizationEvent):
        """Log crystallization event to rebloom log"""
        
        log_entry = {
            "timestamp": event.timestamp,
            "type": "crystallized",
            "memory_uuid": event.memory_uuid,
            "memory_type": event.memory_type.value,
            "final_shimmer": event.final_shimmer,
            "age_hours": event.age_hours,
            "reason": event.crystallization_reason,
            "preservation_quality": event.preservation_quality
        }
        
        try:
            log_path = Path("runtime/logs/rebloom_log.jsonl")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, "a") as f:
                f.write(f"{json.dumps(log_entry)}\n")
                
        except Exception as e:
            logger.error(f"🔮 [FRACTAL] Failed to log crystallization: {e}")
    
    def get_memory_by_uuid(self, memory_uuid: str) -> Optional[FractalMemory]:
        """Retrieve a memory by UUID from active or crystallized storage"""
        
        # Check active memories first
        if memory_uuid in self.active_memories:
            memory = self.active_memories[memory_uuid]
            # Update access tracking
            memory.last_access_time = time.time()
            memory.access_count += 1
            return memory
        
        # Check crystallized memories
        if memory_uuid in self.crystallized_memories:
            return self.crystallized_memories[memory_uuid]
        
        return None
    
    def search_memories(self, query: str, max_results: int = 10, 
                       include_crystallized: bool = False) -> List[FractalMemory]:
        """Search memories by content"""
        
        results = []
        query_lower = query.lower()
        
        # Search active memories
        for memory in self.active_memories.values():
            if query_lower in memory.content.lower() or query_lower in memory.juliet_signature.fragment_essence.lower():
                results.append(memory)
        
        # Search crystallized memories if requested
        if include_crystallized:
            for memory in self.crystallized_memories.values():
                if query_lower in memory.content.lower() or query_lower in memory.juliet_signature.fragment_essence.lower():
                    results.append(memory)
        
        # Sort by relevance (shimmer for active, preservation quality for crystallized)
        def relevance_score(memory):
            if memory.memory_state == MemoryState.CRYSTALLIZED:
                return memory.crystallization_score
            else:
                return memory.shimmer.current_shimmer
        
        results.sort(key=relevance_score, reverse=True)
        
        return results[:max_results]
    
    def get_rebloom_candidates(self, shimmer_threshold: float = 0.7) -> List[FractalMemory]:
        """Get memories eligible for reblooming"""
        
        candidates = []
        
        for memory in self.active_memories.values():
            if (memory.rebloom_eligible and 
                memory.shimmer.current_shimmer > shimmer_threshold and
                memory.access_count > 2):
                candidates.append(memory)
        
        # Sort by potential (shimmer * complexity * access count)
        def rebloom_potential(memory):
            return memory.shimmer.current_shimmer * memory.complexity_score * math.log(memory.access_count + 1)
        
        candidates.sort(key=rebloom_potential, reverse=True)
        
        return candidates
    
    def trigger_rebloom(self, memory_uuid: str) -> bool:
        """Trigger a rebloom event for a memory"""
        
        memory = self.get_memory_by_uuid(memory_uuid)
        if not memory or not memory.rebloom_eligible:
            return False
        
        try:
            # Boost shimmer significantly
            memory.shimmer.current_shimmer = min(memory.shimmer.amplitude * 1.2, 
                                               memory.shimmer.current_shimmer + 0.5)
            memory.shimmer.reinforcement_count += 1
            
            # Update state
            memory.memory_state = MemoryState.ACTIVE
            memory.last_access_time = time.time()
            memory.access_count += 1
            
            # Log rebloom event
            self._log_rebloom_event(memory)
            
            # Execute callbacks
            for callback in self.rebloom_callbacks:
                try:
                    callback(memory)
                except Exception as e:
                    logger.warning(f"🔮 [FRACTAL] Rebloom callback failed: {e}")
            
            self.rebloom_events += 1
            logger.info(f"🌸 [FRACTAL] Rebloomed memory: {memory_uuid[:8]}... (shimmer={memory.shimmer.current_shimmer:.2f})")
            
            return True
            
        except Exception as e:
            logger.error(f"🔮 [FRACTAL] Rebloom error for {memory_uuid}: {e}")
            return False
    
    def _log_rebloom_event(self, memory: FractalMemory):
        """Log rebloom event"""
        
        log_entry = {
            "timestamp": time.time(),
            "type": "rebloom",
            "memory_uuid": memory.juliet_signature.uuid,
            "memory_type": memory.memory_type.value,
            "shimmer_boost": memory.shimmer.current_shimmer,
            "complexity_score": memory.complexity_score,
            "access_count": memory.access_count
        }
        
        try:
            log_path = Path("runtime/logs/rebloom_log.jsonl")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, "a") as f:
                f.write(f"{json.dumps(log_entry)}\n")
                
        except Exception as e:
            logger.error(f"🔮 [FRACTAL] Failed to log rebloom: {e}")
    
    def get_memory_shimmer_data(self) -> Dict[str, Any]:
        """Get memory shimmer data for visualization"""
        
        shimmer_data = []
        
        for memory in self.active_memories.values():
            shimmer_data.append({
                "uuid": memory.juliet_signature.uuid,
                "essence": memory.juliet_signature.fragment_essence,
                "type": memory.memory_type.value,
                "state": memory.memory_state.value,
                "shimmer": memory.shimmer.current_shimmer,
                "age_hours": memory.age_hours,
                "complexity": memory.complexity_score,
                "crystallization_score": memory.crystallization_score,
                "shimmer_history": memory.shimmer.shimmer_history[-10:]  # Last 10 readings
            })
        
        return {
            "active_memories": shimmer_data,
            "total_active": len(self.active_memories),
            "total_crystallized": len(self.crystallized_memories),
            "average_shimmer": sum(m.shimmer.current_shimmer for m in self.active_memories.values()) / max(1, len(self.active_memories)),
            "shimmer_range": {
                "min": min((m.shimmer.current_shimmer for m in self.active_memories.values()), default=0),
                "max": max((m.shimmer.current_shimmer for m in self.active_memories.values()), default=0)
            }
        }
    
    def register_crystallization_callback(self, callback: Callable[[CrystallizationEvent], None]):
        """Register callback for crystallization events"""
        self.crystallization_callbacks.append(callback)
        logger.info(f"🔮 [FRACTAL] Registered crystallization callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def register_shimmer_update_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Register callback for shimmer updates"""
        self.shimmer_update_callbacks.append(callback)
        logger.info(f"🔮 [FRACTAL] Registered shimmer update callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def register_rebloom_callback(self, callback: Callable[[FractalMemory], None]):
        """Register callback for rebloom events"""
        self.rebloom_callbacks.append(callback)
        logger.info(f"🔮 [FRACTAL] Registered rebloom callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get comprehensive fractal memory system state"""
        
        # Calculate memory statistics
        active_by_type = defaultdict(int)
        crystallized_by_type = defaultdict(int)
        
        for memory in self.active_memories.values():
            active_by_type[memory.memory_type.value] += 1
        
        for memory in self.crystallized_memories.values():
            crystallized_by_type[memory.memory_type.value] += 1
        
        return {
            "memory_counts": {
                "active_memories": len(self.active_memories),
                "crystallized_memories": len(self.crystallized_memories),
                "total_memories": len(self.active_memories) + len(self.crystallized_memories)
            },
            "memory_distribution": {
                "active_by_type": dict(active_by_type),
                "crystallized_by_type": dict(crystallized_by_type)
            },
            "performance_metrics": {
                "memories_created": self.memories_created,
                "memories_crystallized": self.memories_crystallized,
                "shimmer_calculations": self.shimmer_calculations,
                "rebloom_events": self.rebloom_events,
                "crystallization_rate": self.memories_crystallized / max(1, self.memories_created)
            },
            "recent_activity": {
                "recent_crystallizations": len([e for e in self.crystallization_history if time.time() - e.timestamp < 3600]),
                "last_maintenance": self.last_maintenance_time,
                "next_maintenance": self.last_maintenance_time + self.maintenance_interval
            },
            "configuration": {
                "crystallization_threshold": self.CRYSTALLIZATION_THRESHOLD,
                "age_threshold_hours": self.AGE_THRESHOLD_HOURS,
                "shimmer_interval": self.SHIMMER_CALCULATION_INTERVAL,
                "memory_type_configs": len(self.MEMORY_TYPE_CONFIGS)
            }
        }

# Global fractal memory manager instance
_global_fractal_manager: Optional[MemoryFractalManager] = None

def get_memory_fractal_manager() -> MemoryFractalManager:
    """Get global memory fractal manager instance"""
    global _global_fractal_manager
    if _global_fractal_manager is None:
        _global_fractal_manager = MemoryFractalManager()
    return _global_fractal_manager

def create_fractal_memory(content: str, memory_type: MemoryType = MemoryType.EXPERIENCE, 
                         initial_shimmer: Optional[float] = None, tags: Set[str] = None) -> FractalMemory:
    """Convenience function to create a fractal memory"""
    manager = get_memory_fractal_manager()
    return manager.create_memory(content, memory_type, initial_shimmer, tags)

def update_memory_shimmer() -> Dict[str, Any]:
    """Convenience function to update memory shimmer"""
    manager = get_memory_fractal_manager()
    return manager.tick_shimmer_decay()

def get_memory_shimmer_visualization() -> Dict[str, Any]:
    """Convenience function to get shimmer data for visualization"""
    manager = get_memory_fractal_manager()
    return manager.get_memory_shimmer_data()

# Export key classes and functions
__all__ = [
    'MemoryFractalManager',
    'FractalMemory',
    'MemoryShimmer',
    'JulietSignature',
    'CrystallizationEvent',
    'MemoryType',
    'MemoryState',
    'get_memory_fractal_manager',
    'create_fractal_memory',
    'update_memory_shimmer',
    'get_memory_shimmer_visualization'
] 