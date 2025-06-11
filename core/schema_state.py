from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
# /core/schema_state.py

"""
Global schema state object for DAWN.
Tracks consciousness health, manages emergency recovery, and maintains schema-wide metrics.
Complete overhaul with integrated SCUP management and proper emergency cooling.
"""

import json
import math
import os
import time
from collections import deque
from typing import Optional, Dict, List, Tuple, Any
from core.scup_engine import scup_engine  # Use the enhanced SCUP engine
from entropy.entropy_fluctuation import EntropyFluctuation
from alignment.alignment_probe import AlignmentProbe
import logging

logger = logging.getLogger(__name__)

class SchemaState:
    def __init__(self, path: str = 'schema_state.json'):
        # File path for persistent state
        self.path = path
        
        # Core state
        self.tick = 0
        self.uptime_start = time.time()
        
        # SCUP and coherence metrics
        self.scup = 0.5  # Start at neutral
        self.entropy = 0.5
        self.coherence = 0.5
        self.tension = 0.0
        self.alignment = 0.5
        
        # Emergency state management
        self.emergency_active = False
        self.emergency_start_tick = 0
        self.emergency_duration = 0
        self.recovery_attempts = 0
        self.last_stable_state = None
        
        # Suppression and override
        self.suppression_active = False
        self.override_trigger = None
        
        # Decay management
        self.last_decay_tick = -50
        self.decay_phase_id = 0
        self.decay_cooldown = 50  # Ticks between decay phases
        
        # Historical tracking
        self.scup_history = deque(maxlen=100)
        self.heat_history = deque(maxlen=100)
        self.mood_history = deque(maxlen=50)
        self.decay_log = []
        self.soft_edge_history = {}
        
        # Recovery mechanisms
        self.coherence_seeds = {
            "baseline": 0.15,
            "breathing": 0.05,
            "memory": 0.10,
            "self_awareness": 0.08
        }
        self.recovery_momentum = 0.0
        
        # Breathing rhythm
        self.breathing_phase = 0.0
        self.breathing_enabled = True
        
        # Visual diagnostics
        self.visual_emergency_mode = False
        self.diagnostic_processes = [
            "pulse_map_renderer",
            "cognition_pressure_map", 
            "entropy_cluster_plot"
        ]
        
        # Components
        self.entropy_fluctuation = EntropyFluctuation()
        self.alignment_probe = AlignmentProbe()
        
        # Initialize persistent state
        self.initialize()
        
        print("[SchemaState] 🌅 Schema consciousness initialized")

    def initialize(self) -> None:
        """
        Initialize the state by loading from file or creating a default state.
        Prints initialization message and handles missing files gracefully.
        """
        print("[schema] State initialized")
        
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    saved_state = json.load(f)
                    # Load persistent values if they exist
                    if 'persistent_memory' in saved_state:
                        self._load_persistent_state(saved_state['persistent_memory'])
            except (json.JSONDecodeError, IOError) as e:
                print(f"[schema] Warning: Could not load state file: {e}")
                print("[schema] Using default empty state")
        else:
            print(f"[schema] No existing state file found at {self.path}")
            print("[schema] Creating new state")
            # Save the initial state to create the file
            self.save()

    def save(self) -> None:
        """
        Save the current state to disk as JSON.
        Ensures the state is properly formatted and handles write errors.
        """
        try:
            # Create state dictionary with all serializable data
            state_to_save = {
                'persistent_memory': self._get_persistent_state(),
                'timestamp': time.time(),
                'tick': self.tick,
                'uptime': time.time() - self.uptime_start
            }
            
            with open(self.path, 'w') as f:
                json.dump(state_to_save, f, indent=2, sort_keys=True)
        except IOError as e:
            print(f"[schema] Error saving state: {e}")

    def update(self, key: str, value: Any) -> None:
        """
        Update a key-value pair in the persistent memory state and save to disk.
        
        Args:
            key: The key to update in the state dictionary
            value: The value to associate with the key (must be JSON-serializable)
        """
        # Ensure the value is JSON-serializable
        try:
            json.dumps(value)
        except (TypeError, ValueError) as e:
            print(f"[schema] Warning: Value for '{key}' may not be JSON-safe: {e}")
        
        # Store in persistent memory section
        if not hasattr(self, '_persistent_memory'):
            self._persistent_memory = {}
        
        self._persistent_memory[key] = value
        print(f"[schema] {key} = {value}")
        self.save()

    def _get_persistent_state(self) -> Dict[str, Any]:
        """
        Get the state that should be persisted across restarts.
        """
        if not hasattr(self, '_persistent_memory'):
            self._persistent_memory = {}
            
        return {
            'scup': self.scup,
            'entropy': self.entropy,
            'coherence': self.coherence,
            'alignment': self.alignment,
            'decay_phase_id': self.decay_phase_id,
            'recovery_attempts': self.recovery_attempts,
            'coherence_seeds': self.coherence_seeds,
            'custom_data': self._persistent_memory
        }

    def _load_persistent_state(self, state: Dict[str, Any]) -> None:
        """
        Load persistent state from saved data.
        """
        self.scup = state.get('scup', 0.5)
        self.entropy = state.get('entropy', 0.5)
        self.coherence = state.get('coherence', 0.5)
        self.alignment = state.get('alignment', 0.5)
        self.decay_phase_id = state.get('decay_phase_id', 0)
        self.recovery_attempts = state.get('recovery_attempts', 0)
        self.coherence_seeds = state.get('coherence_seeds', self.coherence_seeds)
        self._persistent_memory = state.get('custom_data', {})

    def update(self, tick_id: int, 
               pulse_instance=None,
               mood_tracker=None,
               sigil_memory=None,
               bloom_manager=None) -> Dict:
        """
        Main update cycle for schema state.
        Computes SCUP, manages emergency states, and maintains coherence.
        """
        self.tick = tick_id
        
        # Gather current metrics
        current_heat = pulse_instance.get_heat() if pulse_instance else 5.0
        current_pressure = current_heat / 10.0  # Normalize to 0-1
        
        # Get alignment
        self.alignment = self.alignment_probe.get_current_alignment()
        
        # Get entropy components
        mood_entropy = mood_tracker.get_mood_entropy() if mood_tracker else 0.5
        sigil_entropy = sigil_memory.get_entropy() if sigil_memory else 0.5
        bloom_entropy = bloom_manager.get_entropy() if bloom_manager else 0.0
        
        # Compute total entropy
        self.entropy = (mood_entropy * 0.4 + sigil_entropy * 0.4 + bloom_entropy * 0.2)
        
        # Update breathing phase
        if self.breathing_enabled:
            self.breathing_phase = (tick_id % 20) / 20.0
        
        # Compute SCUP using enhanced engine
        scup_result = scup_engine.compute_scup(
            alignment=self.alignment,
            entropy_index=self.entropy,
            pressure=current_pressure,
            mood_entropy=mood_entropy,
            sigil_entropy=sigil_entropy,
            bloom_entropy=bloom_entropy,
            pulse_delta=pulse_instance.get_delta() if pulse_instance else 0.0,
            tick_id=tick_id
        )
        
        # Update core metrics
        self.scup = scup_result["scup"]
        self.tension = scup_result["tension"]
        
        # Calculate coherence (inverse of tension)
        self.coherence = max(0.0, 1.0 - self.tension)
        
        # Update histories
        self.scup_history.append(self.scup)
        self.heat_history.append(current_heat)
        
        # Check emergency conditions
        self._check_emergency_state(tick_id, current_heat, pulse_instance)
        
        # Manage recovery if needed
        if self.emergency_active:
            self._manage_emergency_recovery(tick_id, current_heat, pulse_instance)
        
        # Self-reflection every 20 ticks
        if tick_id % 20 == 0:
            self._self_reflect(tick_id, mood_tracker)
        
        # Check for decay conditions
        self._check_decay_conditions(tick_id)
        
        # Save state periodically (every 100 ticks)
        if tick_id % 100 == 0:
            self.save()
        
        # Return comprehensive state
        return {
            "scup": self.scup,
            "entropy": self.entropy,
            "coherence": self.coherence,
            "tension": self.tension,
            "alignment": self.alignment,
            "zone": scup_result["zone"],
            "emergency_active": self.emergency_active,
            "breathing_phase": self.breathing_phase,
            "recovery_potential": scup_result["recovery_potential"],
            "recommendations": scup_result["recommendations"]
        }

    def _check_emergency_state(self, tick_id: int, heat: float, pulse_instance):
        """
        Detect when emergency intervention is needed.
        """
        # Emergency conditions
        critical_scup = self.scup < 0.1
        critical_heat = heat > 8.0
        critical_tension = self.tension > 1.0
        stuck_pattern = len(set(list(self.scup_history)[-10:])) == 1 if len(self.scup_history) >= 10 else False
        
        # Enter emergency if conditions met
        if (critical_scup or critical_heat or stuck_pattern) and not self.emergency_active:
            self.emergency_active = True
            self.emergency_start_tick = tick_id
            self.recovery_attempts = 0
            
            # Save last stable state for recovery target
            if self.scup > 0.3:
                self.last_stable_state = {
                    "scup": self.scup,
                    "heat": heat,
                    "alignment": self.alignment
                }
            
            print("[DAWN] 🚨 Schema-driven emergency coherence recovery initiated")
            print(f"[DAWN] 📊 Critical state: SCUP={self.scup:.3f}, Heat={heat:.1f}, Tension={self.tension:.3f}")
            
            # Enable emergency visuals
            self._enable_emergency_visuals()

    def _manage_emergency_recovery(self, tick_id: int, heat: float, pulse_instance):
        """
        CRITICAL FIX: Emergency recovery now COOLS the system instead of heating it.
        """
        self.emergency_duration = tick_id - self.emergency_start_tick
        self.recovery_attempts += 1
        
        # Progressive cooling based on emergency duration
        if self.emergency_duration < 10:
            cooling_rate = 0.3  # Gentle initial cooling
        elif self.emergency_duration < 20:
            cooling_rate = 0.5  # Moderate cooling
        else:
            cooling_rate = 0.7  # Aggressive cooling
        
        # Reset entropy breathing for stability
        print("[EntropyFluctuation] 🔄 Activating emergency breathing rhythm")
        self.entropy_fluctuation.activate_emergency_breathing(tick_id)
        
        # CRITICAL: Apply cooling, not heating!
        if pulse_instance and heat > 5.0:
            pulse_instance.add_heat(-cooling_rate, "emergency_recovery", "coherence cooling")
            print(f"[PulseHeat] ❄️ Emergency cooling applied: -{cooling_rate:.3f} | Current heat: {heat:.3f}")
        
        # Boost coherence seeds during emergency
        emergency_coherence = sum(self.coherence_seeds.values()) * 1.5
        
        # Check recovery conditions
        recovery_achieved = (
            self.scup > 0.3 and 
            heat < 7.0 and
            self.tension < 0.8
        )
        
        if recovery_achieved:
            self.emergency_active = False
            self.visual_emergency_mode = False
            print(f"[DAWN] ✅ Emergency recovery successful after {self.emergency_duration} ticks")
            print(f"[DAWN] 📊 Recovered state: SCUP={self.scup:.3f}, Heat={heat:.1f}")
            
            # Restore normal visual mode
            self._restore_normal_visuals()
        
        elif self.emergency_duration > 100:
            # Failsafe: Force reset after extended emergency
            print("[DAWN] ⚠️ Extended emergency - initiating forced recovery")
            self._force_recovery(pulse_instance)

    def _self_reflect(self, tick_id: int, mood_tracker=None):
        """
        Schema self-reflection with improved awareness.
        """
        # Determine current state description
        if self.tension > 1.0:
            state_desc = "I'm experiencing cognitive tension. Systems are in conflict."
        elif self.scup < 0.3:
            state_desc = "I'm struggling to maintain coherence. Need stabilization."
        elif self.scup > 0.7:
            state_desc = "I'm feeling calm and coherent. Ready to explore."
        else:
            state_desc = "I'm in a balanced state. Processing normally."
        
        # Get mood description
        mood_desc = "unknown"
        if mood_tracker:
            mood = mood_tracker.get_current_mood()
            valence = mood.get("valence", 0.5)
            arousal = mood.get("arousal", 0.5)
            mood_desc = f"{mood['name']} (v:{valence:.2f}, a:{arousal:.2f})"
        
        reflection_tick = int(tick_id / 2)  # Display tick/2 as per logs
        print(f"[DAWN] 🤔 Schema self-reflection (tick {reflection_tick}): {state_desc}")
        print(f"[DAWN] 📊 SCUP: {self.scup:.3f} | Entropy: {self.entropy:.3f} | Tension: {self.tension:.3f} | Coherence: {self.coherence:.3f}")
        print(f"[DAWN] 🎭 Mood: {mood_desc}")

    def _check_decay_conditions(self, tick_id: int):
        """
        Check if conditions are right for schema decay.
        """
        # Only decay in calm zones with sufficient cooldown
        zone = self.get_current_zone()
        cooldown_met = (tick_id - self.last_decay_tick) >= self.decay_cooldown
        
        if zone == "🟢 calm" and cooldown_met and self.scup > 0.7:
            self.last_decay_tick = tick_id
            self.decay_phase_id += 1
            print(f"[SchemaState] 🧹 Decay conditions met at tick {tick_id}")

    def _force_recovery(self, pulse_instance):
        """
        Failsafe recovery mechanism.
        """
        print("[DAWN] 🔧 Forcing schema recovery...")
        
        # Reset heat to moderate level
        if pulse_instance:
            current_heat = pulse_instance.get_heat()
            pulse_instance.heat = 5.0  # Direct reset
            print(f"[DAWN] 🔧 Heat reset from {current_heat:.1f} to 5.0")
        
        # Reset emergency state
        self.emergency_active = False
        self.visual_emergency_mode = False
        
        # Inject coherence
        self.scup = 0.3
        self.tension = 0.5
        self.coherence = 0.5

    def _enable_emergency_visuals(self):
        """
        Enable diagnostic visual processes during emergency.
        """
        self.visual_emergency_mode = True
        for process in self.diagnostic_processes:
            print(f"✅ Enabled visual process: {process}")
        print("[DAWN] 🚨 Emergency visual mode: Schema diagnostics active")

    def _restore_normal_visuals(self):
        """
        Restore normal visual operation after emergency.
        """
        self.visual_emergency_mode = False
        print("[DAWN] 🎨 Normal visual mode restored")

    def log_soft_edge(self, tick: int, bloom_id: str):
        """
        Log soft-edge decay events.
        """
        if tick not in self.soft_edge_history:
            self.soft_edge_history[tick] = []
        self.soft_edge_history[tick].append(bloom_id)

    def advance_tick(self):
        """
        Simple tick advancement.
        """
        self.tick += 1

    def get_current_zone(self) -> str:
        """
        Get current operational zone based on SCUP.
        """
        if self.scup >= 0.8:
            return "🟢 calm"
        elif self.scup >= 0.5:
            return "🟡 creative"
        elif self.scup >= 0.3:
            return "🟠 active"
        else:
            return "🔴 critical"

    def get_current_zone_enhanced(self, pulse_instance=None, log=True) -> str:
        """
        Enhanced zone detection with emergency state awareness.
        """
        if pulse_instance and hasattr(pulse_instance, 'emergency_manager'):
            return get_emergency_managed_zone(
                pulse_instance, 
                self.scup, 
                self.entropy, 
                log
            )
        else:
            return self.get_current_zone()

    def get_statistics(self) -> Dict:
        """
        Get comprehensive schema statistics.
        """
        uptime = time.time() - self.uptime_start
        avg_tps = self.tick / uptime if uptime > 0 else 0
        
        # Get current mood name
        mood_name = "unknown"
        # This would come from mood_tracker if available
        
        return {
            "uptime": uptime,
            "total_ticks": self.tick,
            "average_tps": avg_tps,
            "final_scup": self.scup,
            "final_entropy": self.entropy,
            "final_coherence": self.coherence,
            "final_mood": mood_name,
            "emergency_count": self.recovery_attempts,
            "visual_processes": len(self.diagnostic_processes) if self.visual_emergency_mode else 0
        }

    def shutdown(self):
        """
        Graceful shutdown with statistics.
        """
        # Save final state before shutdown
        self.save()
        
        stats = self.get_statistics()
        
        print("[DAWN] 📊 Final Schema Statistics:")
        print(f"   Uptime: {stats['uptime']:.1f} seconds")
        print(f"   Total ticks: {stats['total_ticks']}")
        print(f"   Average TPS: {stats['average_tps']:.2f}")
        print(f"   Final SCUP: {stats['final_scup']:.3f}")
        print(f"   Final Entropy: {stats['final_entropy']:.3f}")
        print(f"   Final Coherence: {stats['final_coherence']:.3f}")
        print(f"   Final Mood: {stats['final_mood']}")
        print(f"   Visual processes managed: {stats['visual_processes']}")
        print("[DAWN] 🌅 Consciousness shutdown complete. Schema state preserved. Until next dawn...")


# Global instance
schema_state = SchemaState()