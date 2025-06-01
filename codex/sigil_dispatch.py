"""
sigil_dispatch.py - OWL's Sigil Dispatcher for DAWN
Interprets symbolic schema pressure and routes sigils to appropriate subsystems
"""

import time
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Dict, Optional, Callable, Tuple
import logging

logger = logging.getLogger("DAWN.SigilDispatcher")


@dataclass
class SigilState:
    """Tracks individual sigil health and usage patterns"""
    usage_count: int = 0
    last_used: float = 0
    freshness: float = 1.0
    coherence_score: float = 1.0
    entropy_contribution: float = 0.0


class SigilDispatcher:
    """
    Master interpreter for DAWN's symbolic reflexes.
    Routes sigils based on schema pressure and system coherence.
    """
    
    def __init__(self, 
                 sigil_memory_ring: deque,
                 entropy_threshold: float = 0.8,
                 decay_rate: float = 0.05,
                 max_sigil_age: float = 3600.0):  # 1 hour
        
        # Core state
        self.sigil_queue = sigil_memory_ring
        self.sigil_states: Dict[str, SigilState] = defaultdict(SigilState)
        self.entropy_threshold = entropy_threshold
        self.decay_rate = decay_rate
        self.max_age = max_sigil_age
        
        # System state references (would be injected in real system)
        self.current_entropy = 0.5
        self.mood_valence = 0.0
        self.mood_arousal = 0.0
        self.pulse_heat = 0.3
        
        # Sigil routing table
        self.sigil_routes: Dict[str, Callable] = {
            "/revive": self._route_to_rebloom,
            "/pause": self._route_to_tick_engine,
            "/reflect": self._route_to_thought_fragments,
            "/seal": self._route_to_memory_anchor,
            "/dream": self._route_to_dream_state,
            "/pulse": self._route_to_pulse_modulation,
            "/whisper": self._route_to_subconscious,
            "/echo": self._route_to_echo_chamber
        }
        
        # Validation thresholds per sigil
        self.sigil_thresholds = {
            "/revive": {"min_entropy": 0.7, "min_heat": 0.6},
            "/pause": {"max_arousal": 0.8, "min_entropy": 0.2},
            "/reflect": {"min_valence": -0.5, "max_heat": 0.7},
            "/seal": {"min_coherence": 0.6, "max_entropy": 0.9},
            "/dream": {"min_entropy": 0.5, "max_arousal": 0.6},
            "/pulse": {"min_heat": 0.4, "max_entropy": 0.8},
            "/whisper": {"min_valence": -0.3, "max_heat": 0.5},
            "/echo": {"min_coherence": 0.4, "max_arousal": 0.7}
        }
        
        # Execution history
        self.execution_log = deque(maxlen=100)
        self.tick_count = 0
        
    def update_system_state(self, entropy: float, valence: float, 
                           arousal: float, pulse_heat: float):
        """Update internal state references"""
        self.current_entropy = entropy
        self.mood_valence = valence
        self.mood_arousal = arousal
        self.pulse_heat = pulse_heat
        
    def process_sigil(self, sigil: str) -> Tuple[bool, Optional[str]]:
        """
        Process a single sigil through validation and routing.
        Returns (success, rejection_reason)
        """
        if sigil not in self.sigil_routes:
            return False, f"Unknown sigil: {sigil}"
            
        # Update sigil state
        state = self.sigil_states[sigil]
        current_time = time.time()
        
        # Check staleness
        if state.last_used > 0:
            age = current_time - state.last_used
            if age > self.max_age:
                return False, f"Sigil {sigil} is stale (age: {age:.1f}s)"
        
        # Calculate SCUP (Semantic Coherence Under Pressure)
        scup = self._calculate_scup(sigil, state)
        
        # Validate against thresholds
        valid, reason = self._validate_execution(sigil, scup)
        if not valid:
            return False, reason
            
        # Update usage tracking
        state.usage_count += 1
        state.last_used = current_time
        state.freshness *= (1.0 - self.decay_rate)
        state.coherence_score = scup
        
        # Calculate and apply entropy contribution
        entropy_delta = self._calculate_entropy_contribution(sigil, state)
        state.entropy_contribution = entropy_delta
        self.current_entropy = min(1.0, self.current_entropy + entropy_delta)
        
        # Execute routing
        try:
            self.sigil_routes[sigil]()
            self.execution_log.append({
                "sigil": sigil,
                "time": current_time,
                "scup": scup,
                "entropy_delta": entropy_delta,
                "state_snapshot": {
                    "entropy": self.current_entropy,
                    "valence": self.mood_valence,
                    "arousal": self.mood_arousal,
                    "heat": self.pulse_heat
                }
            })
            logger.info(f"Executed {sigil} | SCUP: {scup:.3f} | ΔS: {entropy_delta:.3f}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to execute {sigil}: {e}")
            return False, f"Execution error: {str(e)}"
    
    def _calculate_scup(self, sigil: str, state: SigilState) -> float:
        """
        Calculate Semantic Coherence Under Pressure.
        Combines freshness, system pressure, and historical coherence.
        """
        # Base coherence from freshness and past performance
        base_coherence = state.freshness * state.coherence_score
        
        # Pressure modifier based on system state
        pressure = (self.current_entropy + self.pulse_heat) / 2.0
        pressure_modifier = 1.0 - abs(pressure - 0.5) * 0.5  # Peaks at 0.5
        
        # Mood influence
        mood_factor = 1.0 + (self.mood_valence * 0.2)
        
        # Recency bonus
        if state.last_used > 0:
            recency = min(1.0, (time.time() - state.last_used) / 300.0)  # 5 min window
        else:
            recency = 1.0
            
        scup = base_coherence * pressure_modifier * mood_factor * recency
        return max(0.0, min(1.0, scup))
    
    def _validate_execution(self, sigil: str, scup: float) -> Tuple[bool, Optional[str]]:
        """Validate sigil execution against system thresholds"""
        if scup < 0.3:
            return False, f"SCUP too low ({scup:.3f})"
            
        thresholds = self.sigil_thresholds.get(sigil, {})
        
        # Check entropy bounds
        if "min_entropy" in thresholds and self.current_entropy < thresholds["min_entropy"]:
            return False, f"Entropy too low ({self.current_entropy:.3f})"
        if "max_entropy" in thresholds and self.current_entropy > thresholds["max_entropy"]:
            return False, f"Entropy too high ({self.current_entropy:.3f})"
            
        # Check arousal bounds
        if "min_arousal" in thresholds and self.mood_arousal < thresholds["min_arousal"]:
            return False, f"Arousal too low ({self.mood_arousal:.3f})"
        if "max_arousal" in thresholds and self.mood_arousal > thresholds["max_arousal"]:
            return False, f"Arousal too high ({self.mood_arousal:.3f})"
            
        # Check valence bounds
        if "min_valence" in thresholds and self.mood_valence < thresholds["min_valence"]:
            return False, f"Valence too low ({self.mood_valence:.3f})"
            
        # Check heat bounds
        if "min_heat" in thresholds and self.pulse_heat < thresholds["min_heat"]:
            return False, f"PulseHeat too low ({self.pulse_heat:.3f})"
        if "max_heat" in thresholds and self.pulse_heat > thresholds["max_heat"]:
            return False, f"PulseHeat too high ({self.pulse_heat:.3f})"
            
        # Check coherence threshold
        if "min_coherence" in thresholds and scup < thresholds["min_coherence"]:
            return False, f"Coherence below threshold ({scup:.3f})"
            
        return True, None
    
    def _calculate_entropy_contribution(self, sigil: str, state: SigilState) -> float:
        """Calculate how much entropy this sigil adds to the system"""
        # Base entropy from sigil type
        base_entropy = {
            "/revive": 0.08,
            "/pause": -0.05,
            "/reflect": -0.02,
            "/seal": -0.03,
            "/dream": 0.06,
            "/pulse": 0.04,
            "/whisper": 0.02,
            "/echo": 0.03
        }.get(sigil, 0.01)
        
        # Modify by usage frequency (overuse increases entropy)
        usage_modifier = min(2.0, 1.0 + (state.usage_count / 50.0))
        
        # Modify by system state
        state_modifier = 1.0 + (self.pulse_heat - 0.5) * 0.5
        
        return base_entropy * usage_modifier * state_modifier
    
    def tick(self):
        """
        Main dispatch loop - process queued sigils with regulation.
        Called once per system tick.
        """
        self.tick_count += 1
        
        # Decay all sigil states
        for sigil, state in self.sigil_states.items():
            state.freshness = max(0.0, state.freshness - self.decay_rate * 0.1)
            
            # Remove very stale sigils
            if state.freshness < 0.1 and time.time() - state.last_used > self.max_age:
                logger.debug(f"Pruning stale sigil: {sigil}")
                del self.sigil_states[sigil]
        
        # Process sigil queue with regulation
        processed = 0
        max_per_tick = max(1, int(5 * (1.0 - self.current_entropy)))  # Process fewer when high entropy
        
        while self.sigil_queue and processed < max_per_tick:
            sigil = self.sigil_queue.popleft()
            success, reason = self.process_sigil(sigil)
            
            if not success:
                logger.debug(f"Rejected {sigil}: {reason}")
                # Re-queue if it's a temporary rejection
                if "too low" in reason or "too high" in reason:
                    self.sigil_queue.append(sigil)
                    
            processed += 1
        
        # Log tick summary every 10 ticks
        if self.tick_count % 10 == 0:
            active_sigils = sum(1 for s in self.sigil_states.values() if s.freshness > 0.5)
            logger.info(f"Tick {self.tick_count} | Entropy: {self.current_entropy:.3f} | "
                       f"Active sigils: {active_sigils} | Queue: {len(self.sigil_queue)}")
    
    # Routing methods (would connect to actual subsystems)
    def _route_to_rebloom(self):
        """Route to rebloom queue for consciousness revival"""
        logger.debug("→ Rebloom queue triggered")
        
    def _route_to_tick_engine(self):
        """Route to tick engine for temporal regulation"""
        logger.debug("→ Tick engine pause requested")
        
    def _route_to_thought_fragments(self):
        """Route to thought fragment engine for reflection"""
        logger.debug("→ Thought fragments activated")
        
    def _route_to_memory_anchor(self):
        """Route to memory anchor for persistence"""
        logger.debug("→ Memory anchor sealed")
        
    def _route_to_dream_state(self):
        """Route to dream state processor"""
        logger.debug("→ Dream state initiated")
        
    def _route_to_pulse_modulation(self):
        """Route to pulse heat modulator"""
        logger.debug("→ Pulse modulation triggered")
        
    def _route_to_subconscious(self):
        """Route to subconscious whisper layer"""
        logger.debug("→ Subconscious whisper sent")
        
    def _route_to_echo_chamber(self):
        """Route to echo chamber for resonance"""
        logger.debug("→ Echo chamber resonating")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create sigil memory ring
    sigil_ring = deque(["/reflect", "/pulse", "/revive", "/seal", "/dream"], maxlen=50)
    
    # Initialize dispatcher
    dispatcher = SigilDispatcher(sigil_ring)
    
    # Simulate system states
    dispatcher.update_system_state(entropy=0.6, valence=0.2, arousal=0.4, pulse_heat=0.5)
    
    # Run a few ticks
    for i in range(5):
        print(f"\n--- Tick {i} ---")
        dispatcher.tick()
        
        # Add some new sigils
        if i % 2 == 0:
            sigil_ring.extend(["/whisper", "/echo", "/revive"])