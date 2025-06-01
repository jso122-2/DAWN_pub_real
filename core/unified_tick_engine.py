#!/usr/bin/env python3
"""
Unified DAWN Tick Engine v2
Consolidated from multiple tick engine implementations with all features merged.
This is a standalone executable combining production architecture with experimental dynamics.
"""

import sys
import os
import asyncio
import time
import math
import json
from typing import Dict, List, Optional, Callable, Tuple
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime

# ============================================================================
# CORE STATE MANAGEMENT
# ============================================================================

@dataclass
class UnifiedCognitiveState:
    """Unified cognitive state combining all approaches"""
    # Core metrics
    tick: int = 0
    scup: float = 1.0
    valence: float = 0.0
    entropy: float = 0.0
    arousal: float = 0.0
    pulse_heat: float = 0.0
    alignment: float = 1.0
    
    # Heat engine state
    heat_generation_rate: float = 0.0
    heat_dissipation_rate: float = 0.1
    stasis_heat: float = 0.0
    
    # Drift mechanics
    drift_vector: List[float] = None
    drift_magnitude: float = 0.0
    
    # Rebloom state
    last_rebloom_tick: int = 0
    rebloom_cooldown: int = 30
    rebloom_count: int = 0
    
    # SCUP momentum
    scup_momentum: float = 0.0
    last_scup: float = 1.0
    
    # Tracer dynamics
    tracer_urgency: float = 0.5
    tracer_zones: List[str] = None
    
    # Zone state
    current_zone: str = "🟢 calm"
    zone_timer: Dict[str, int] = None
    
    # Cascade risk
    cascade_risk: float = 0.0
    
    # Bloom mood tracking (from tick_loop.py)
    last_bloom_mood: str = "neutral"
    pressure_history: deque = None
    
    # Autonomous bloom state (from tick_hook_autonomous.py)
    autonomous_bloom_enabled: bool = True
    autonomous_bloom_count: int = 0
    last_autonomous_bloom_tick: int = 0
    
    def __post_init__(self):
        if self.drift_vector is None:
            self.drift_vector = [0.0, 0.0, 0.0]
        if self.tracer_zones is None:
            self.tracer_zones = ["stable"]
        if self.zone_timer is None:
            self.zone_timer = {"🟢 calm": 0, "🟡 active": 0, "🔴 surge": 0}
        if self.pressure_history is None:
            self.pressure_history = deque(maxlen=5)


# ============================================================================
# MOCK IMPLEMENTATIONS FOR STANDALONE OPERATION
# ============================================================================

class MockPulseHeat:
    """Mock PulseHeat for standalone operation"""
    def __init__(self):
        self.heat = 0.5
        self.tick_count = 0
        self.heat_capacity = 1.0
        self.thermal_momentum = 0.1
        self.current_pressure = 0.0
        self.activity_level = 0.5
        self.current_interval = 1.0
        self.memory_log = deque(maxlen=100)
        self.override_active = False
    
    def get_thermal_profile(self):
        return {
            'current_heat': self.heat,
            'stability_index': 0.8 - abs(self.heat - 0.5),
            'thermal_momentum': self.thermal_momentum
        }
    
    def classify(self):
        if self.heat > 0.7:
            return "🔴 surge"
        elif self.heat > 0.3:
            return "🟡 active"
        else:
            return "🟢 calm"
    
    def update(self, pressure):
        self.current_pressure = pressure
        self.heat += (pressure - 0.5) * 0.1
        self.heat = max(0.0, min(1.0, self.heat))
        self.thermal_momentum = self.thermal_momentum * 0.9 + (pressure - 0.5) * 0.1
    
    def add_heat(self, amount, source):
        self.heat = min(1.0, self.heat + amount)
    
    def remove_heat(self, amount, source):
        self.heat = max(0.0, self.heat - amount)
    
    def adjust_urgency(self, scup):
        if scup < 0.3:
            self.thermal_momentum *= 1.2
    
    def apply_penalty(self, seed, penalty):
        self.heat *= penalty
    
    def average_pressure(self, window=5):
        if not self.memory_log:
            return self.current_pressure
        recent = list(self.memory_log)[-window:]
        return sum(log['pressure'] for log in recent) / len(recent)

# Global pulse instance for standalone mode
pulse = MockPulseHeat()

# Mock functions for missing dependencies
def emit_tick(zone=None, pulse=None): return pulse.tick_count
def spawn_bloom(data, pulse=None): print(f"[Mock] Spawning bloom: {data.get('seed_id', 'unknown')}")
def write_bloom(**kwargs): print(f"[Mock] Writing bloom: {kwargs.get('seed', 'unknown')}")
def trigger_synthesis(): print("[Mock] Triggering synthesis")
def pop_rebloom_candidate(): return None
def launch_reflex(name): print(f"[Mock] Launching reflex: {name}")
def owl_visual_reflex(tick_id): pass
def owl_drift_check(tick_id): return None
def owl_log(msg): print(f"[OWL] {msg}")
def owl_comment(log, tick): print(f"[OWL] Commenting on tick {tick}")
def owl_log_rebloom(data): print(f"[OWL] Rebloom logged: {data.get('seed_id', 'unknown')}")
def animate_rebloom_lineage(): pass
def log_rebloom_lineage(seed, ancestry): pass
def run_entropy_scan(): print("[Mock] Running entropy scan")
def render_entropy_field(): print("[Mock] Rendering entropy field")
def load_all_blooms(): return []
def soft_seal_bloom(bloom): pass

# Mock schema functions
def current_alignment_probe(x): return 0.8
def mood_urgency_probe(x): return 0.5
def get_active_sigil_entropy_list(): return [0.3, 0.4, 0.5]
def get_total_drift_entropy(): return 0.4
def compute_scup(**kwargs): return 0.6
def update_schema_health(scup): pass
def calculate_SHI(*args): return 0.7
def decay_schema_memory(): pass
def decay_all_sigils(): pass
def age_all_sigils(): pass
def fade_sigils(): pass
def expire_ephemeral_sigils(): pass
def prune_dead_branches(): pass
def propose_code_patch(*args): pass
def log_field_snapshot(**kwargs): pass
def log_claude_voice(data): pass

# Mock sigils module
class MockSigils:
    def evolve_classes(self, field_state): 
        print(f"[Mock] Evolving sigils with field state: {field_state.get('mood', 'unknown')}")

sigils = MockSigils()
sigil_memory_ring = {}

# ============================================================================
# UNIFIED TICK ENGINE IMPLEMENTATION
# ============================================================================

class UnifiedTickEngine:
    """
    Unified TickEngine combining robust architecture with experimental dynamics.
    
    Features:
    - Production-ready architecture with proper error handling
    - Heat engine with stasis detection
    - Drift mechanics affecting system alignment
    - Dynamic rebloom logic based on emotional state
    - SCUP momentum and feedback loops
    - Narrative engine for human-readable logs
    - Comprehensive state persistence
    - Multiple blooms per tick (from tick_loop.py)
    - Integrated tick emission and persistence (from tick_emitter.py)
    - Autonomous bloom generation (from tick_hook_autonomous.py)
    - Full configuration system (from tick_engine_config.json)
    """
    
    # File paths for persistence
    TICK_STATE_FILE = "tick_state.json"
    ZONE_OVERLAY_FILE = "juliet_flowers/cluster_report/zone_overlay_log.csv"
    
    def __init__(self, base_interval: float = 1.0, 
                 activity_sensor: Optional[Callable] = None,
                 pressure_sensor: Optional[Callable] = None,
                 mood_sensor: Optional[Callable] = None,
                 gas_pedal: Optional[Callable] = None,
                 emit_tick_event: Optional[Callable] = None,
                 enable_narrative: bool = None):
        
        # Load configuration first
        self.config = self._load_config()
        
        # Core timing configuration
        self.base_interval = base_interval
        self.last_interval = base_interval
        
        # Sensor configuration
        self.activity_sensor = activity_sensor
        self.pressure_sensor = pressure_sensor
        self.mood_sensor = mood_sensor
        self.gas_pedal = gas_pedal
        self.emit_tick_event = emit_tick_event
        
        # Apply narrative config
        self.enable_narrative = enable_narrative if enable_narrative is not None else self.config["narrative"]["enabled"]
        
        # Adaptive coefficients
        self.alpha = 0.2    # Activity sensitivity
        self.beta = 0.4     # Pressure sensitivity  
        self.gamma = 0.3    # Mood sensitivity
        self.delta = 0.1    # Entropy sensitivity
        
        # State tracking
        self.state = UnifiedCognitiveState()
        self.entropy_trend = deque(maxlen=50)
        self.scup_trend = deque(maxlen=30)
        self.interval_history = deque(maxlen=100)
        self.narrative_history = deque(maxlen=self.config["narrative"]["history_size"])
        
        # Zone transitions
        self.zone_transitions = []
        
        # Reflex cooldowns
        self.reflex_cooldowns = {
            "synthesis": 0,
            "entropy_scan": 0,
            "emergency_suppression": 0,
            "rebloom_queue": 0,
            "heat_cascade": 0
        }
        
        # Initialize tick state from persisted file
        self.tick_state_file = self.TICK_STATE_FILE
        self.zone_overlay_file = self.ZONE_OVERLAY_FILE
        self._load_tick_state()
        
        # Running state
        self._running = False
        
        # Initialize state files
        self._init_state_files()
        
        print(f"[UnifiedTickEngine] 🎯 Initialized | Base interval: {base_interval}s | Narrative: {self.enable_narrative}")
    
    def _load_config(self) -> Dict:
        """Load configuration from file with comprehensive defaults"""
        default_config = {
            "heat": {
                "stasis_threshold": 0.1,
                "generation_base": 0.02,
                "dissipation_base": 0.1,
                "critical_threshold": 0.85,
                "cascade_multiplier": 1.5,
                "alignment_cooling_bonus": 0.2
            },
            "rebloom": {
                "entropy_threshold": 0.45,
                "valence_threshold": 0.2,
                "cooldown_ticks": 30,
                "arousal_amplification": 1.2,
                "stability_penalty_per_generation": 0.1,
                "max_generations": 5
            },
            "drift": {
                "arousal_factor": 0.1,
                "decay_rate": 0.05,
                "alignment_impact": 0.8,
                "critical_drift_threshold": 0.5,
                "valence_weight": 0.6,
                "entropy_weight": 0.4
            },
            "scup": {
                "momentum_weight": 0.3,
                "urgency_impact": 0.5,
                "rising_threshold": 0.02,
                "falling_threshold": -0.02,
                "critical_scup": 0.3,
                "stable_scup": 0.7
            },
            "cascade": {
                "heat_weight": 0.4,
                "entropy_weight": 0.3,
                "drift_weight": 0.3,
                "critical_threshold": 0.8,
                "emergency_cooling_factor": 0.3,
                "momentum_dampening": 0.5
            },
            "zones": {
                "calm": {
                    "interval_multiplier": 1.5,
                    "heat_dissipation_bonus": 0.2,
                    "synthesis_threshold": 20,
                    "rebloom_threshold": 15
                },
                "active": {
                    "interval_multiplier": 1.0,
                    "entropy_scan_interval": 30,
                    "drift_sensitivity": 1.2
                },
                "surge": {
                    "interval_multiplier": 0.5,
                    "emergency_threshold": 10,
                    "heat_generation_penalty": 0.7,
                    "scup_boost": 0.1
                }
            },
            "narrative": {
                "enabled": True,
                "log_interval": 10,
                "history_size": 100,
                "include_technical": False,
                "emoji_indicators": True
            },
            "maintenance": {
                "shi_check_interval": 25,
                "memory_decay_interval": 10,
                "sigil_maintenance_interval": 15,
                "lifecycle_interval": 20,
                "bloom_sweep_interval": 50,
                "entropy_render_interval": 75
            },
            "blooms": {
                "per_tick": 5,
                "pressure_base": 0.2,
                "pressure_increment": 0.1,
                "activity_base": 0.5,
                "activity_increment": 0.05
            },
            "mood": {
                "pressure_window": 5,
                "stressed_threshold": 0.4,
                "calm_threshold": 0.2,
                "interval_stress_factor": 0.95,
                "interval_calm_factor": 1.02
            },
            "autonomous_blooms": {
                "enabled": True,
                "frequency": 10,
                "base_entropy": 0.25,
                "entropy_variance": 0.05,
                "bloom_factor_range": 3.0,
                "moods": {
                    "reflective_frequency": 20,
                    "default_mood": "anxious"
                }
            }
        }
        
        try:
            with open("tick_engine_config.json", "r") as f:
                loaded_config = json.load(f)
            return self._deep_merge_configs(default_config, loaded_config)
            
        except FileNotFoundError:
            print("[UnifiedTickEngine] ⚠️ Config file not found, using defaults")
            try:
                with open("tick_engine_config.json", "w") as f:
                    json.dump(default_config, f, indent=2)
                print("[UnifiedTickEngine] 📝 Created default config file")
            except:
                pass
            return default_config
            
        except json.JSONDecodeError as e:
            print(f"[UnifiedTickEngine] ❌ Config parse error: {e}, using defaults")
            return default_config
            
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Config load error: {e}, using defaults")
            return default_config
    
    def _deep_merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Deep merge loaded config with defaults to ensure all keys exist"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _init_state_files(self):
        """Initialize state persistence files"""
        os.makedirs("cognitive_states", exist_ok=True)
        
        # Load previous state if exists
        try:
            with open("cognitive_states/cognitive_state.json", "r") as f:
                saved_state = json.load(f)
                # Restore relevant state
                self.state.tick = saved_state.get("tick", 0)
                self.state.rebloom_count = saved_state.get("rebloom_count", 0)
        except:
            pass
    
    def _load_tick_state(self):
        """Load tick state from persistence file (from tick_emitter.py)"""
        try:
            if os.path.exists(self.tick_state_file):
                with open(self.tick_state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    saved_tick = data.get("tick", 0)
                    pulse.tick_count = max(pulse.tick_count, saved_tick)
                    print(f"[UnifiedTickEngine] 📥 Loaded tick state: {saved_tick}")
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Failed to load tick state: {e}")
    
    def _save_state(self):
        """Save current state to file"""
        state_dict = asdict(self.state)
        state_dict["timestamp"] = datetime.now().isoformat()
        
        with open("cognitive_states/cognitive_state.json", "w") as f:
            json.dump(state_dict, f, indent=2)
    
    def _emit_tick(self, zone: str = None, pulse_heat: float = None) -> int:
        """
        Emit next tick with persistence and zone overlay logging (from tick_emitter.py)
        
        This provides:
        - Tick state persistence to JSON
        - Zone overlay logging with drift entropy
        - Consistent tick incrementing
        """
        # Increment tick
        pulse.tick_count += 1
        tick_id = pulse.tick_count
        
        # Get drift entropy for logging
        drift_entropy = 0.0
        try:
            drift_entropy = round(get_total_drift_entropy(), 4)
        except:
            pass
        
        # Persist tick state to JSON
        tick_state = {
            "tick": tick_id,
            "timestamp": datetime.utcnow().isoformat(),
            "zone": zone,
            "pulse": pulse_heat,
            "drift": drift_entropy
        }
        
        try:
            with open(self.tick_state_file, "w", encoding="utf-8") as f:
                json.dump(tick_state, f, indent=2)
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Failed to save tick state: {e}")
        
        # Log to zone overlay CSV (includes drift entropy)
        try:
            os.makedirs(os.path.dirname(self.zone_overlay_file), exist_ok=True)
            with open(self.zone_overlay_file, "a", encoding="utf-8") as log:
                log.write(f"{tick_id},{zone},{pulse_heat},{drift_entropy}\n")
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Failed to log zone overlay: {e}")
        
        print(f"⏱️ Tick emitted | Tick: {tick_id} | Zone: {zone} | Pulse: {pulse_heat:.3f} | Drift: {drift_entropy}")
        
        return tick_id
    
    def _generate_narrative(self) -> str:
        """Generate human-readable narrative of current state"""
        narratives = []
        
        # Mood description
        if self.state.arousal > 0.7:
            mood = "highly aroused"
        elif self.state.arousal > 0.4:
            mood = "moderately active"
        else:
            mood = "calm"
            
        if self.state.valence > 0.3:
            mood += ", positive"
        elif self.state.valence < -0.3:
            mood += ", negative"
        else:
            mood += ", neutral"
        
        narratives.append(f"Mood {mood}")
        
        # System health
        if self.state.scup < 0.4:
            narratives.append("System struggling")
        elif self.state.scup > 0.8:
            narratives.append("System coherent")
        else:
            narratives.append("System fluctuating")
        
        # Entropy state
        if self.state.entropy > 0.7:
            narratives.append(f"Entropy high ({self.state.entropy:.2f})")
        elif self.state.entropy < 0.3:
            narratives.append(f"Entropy low ({self.state.entropy:.2f})")
        
        return f"Tick {self.state.tick}: {'. '.join(narratives)}."
    
    def _update_heat_engine(self):
        """Update heat generation and dissipation"""
        config = self.config["heat"]
        
        # Detect stasis (high SCUP with low activity)
        activity = pulse.thermal_momentum
        if self.state.scup > 0.8 and activity < config["stasis_threshold"]:
            # Generate heat from stasis
            self.state.heat_generation_rate = config["generation_base"] * (1 + self.state.scup)
            self.state.stasis_heat += self.state.heat_generation_rate
            
            if self.enable_narrative:
                self.narrative_history.append(f"🔥 Stasis detected. Heat building ({self.state.stasis_heat:.3f})")
        
        # Heat dissipation based on alignment
        self.state.heat_dissipation_rate = config["dissipation_base"] * self.state.alignment
        self.state.stasis_heat = max(0, self.state.stasis_heat - self.state.heat_dissipation_rate)
        
        # Apply heat to pulse system
        if self.state.stasis_heat > 0:
            pulse.add_heat(self.state.stasis_heat * 0.1, f"stasis_heat_{self.state.tick}")
        
        # Check for cascade risk
        if self.state.stasis_heat > config["critical_threshold"]:
            self.state.cascade_risk += 0.1
            if self.enable_narrative:
                self.narrative_history.append("⚠️ Critical heat levels. System approaching thermal cascade.")
    
    def _update_drift_mechanics(self):
        """Update system drift based on mood and arousal"""
        config = self.config["drift"]
        
        # Calculate drift from arousal and valence
        if self.state.arousal > config["critical_drift_threshold"] or abs(self.state.valence) > config["critical_drift_threshold"]:
            # Add directional drift
            drift_x = self.state.valence * config["arousal_factor"] * config["valence_weight"]
            drift_y = self.state.arousal * config["arousal_factor"]
            drift_z = (self.state.entropy - 0.5) * config["arousal_factor"] * config["entropy_weight"]
            
            self.state.drift_vector[0] += drift_x
            self.state.drift_vector[1] += drift_y
            self.state.drift_vector[2] += drift_z
            
            # Calculate magnitude
            self.state.drift_magnitude = math.sqrt(sum(d**2 for d in self.state.drift_vector))
            
            if self.state.drift_magnitude > 0.05 and self.enable_narrative:
                self.narrative_history.append(f"🌊 Drift detected: magnitude {self.state.drift_magnitude:.3f}")
        
        # Apply drift decay
        for i in range(3):
            self.state.drift_vector[i] *= (1 - config["decay_rate"])
        
        # Update alignment based on drift
        if self.state.drift_magnitude > 0:
            alignment_penalty = self.state.drift_magnitude * config["alignment_impact"]
            self.state.alignment = max(0.1, self.state.alignment - alignment_penalty)
            
            if self.state.alignment < 0.6 and self.enable_narrative:
                self.narrative_history.append(f"Alignment degrading to {self.state.alignment:.2f}")
    
    def _check_rebloom_conditions(self):
        """Check and execute rebloom logic"""
        config = self.config["rebloom"]
        
        # Check rebloom conditions
        if (self.state.entropy > config["entropy_threshold"] and 
            self.state.valence < config["valence_threshold"] and
            self.state.tick - self.state.last_rebloom_tick > config["cooldown_ticks"]):
            
            # Trigger rebloom
            self.state.rebloom_count += 1
            self.state.last_rebloom_tick = self.state.tick
            
            # Process rebloom
            bloom = pop_rebloom_candidate()
            if bloom:
                # Modify bloom properties
                new_data = bloom.to_dict()
                new_data["arousal_modifier"] = self.state.arousal * config["arousal_amplification"]
                new_data["stability_penalty"] = config["stability_penalty_per_generation"] * self.state.rebloom_count
                new_data["generation"] = self.state.rebloom_count
                
                spawn_bloom(new_data)
                
                if self.enable_narrative:
                    self.narrative_history.append(f"💭 Rebloom triggered: '{bloom.seed_id}' (generation {self.state.rebloom_count})")
                
                # Update system state
                self.state.arousal = min(1.0, self.state.arousal * 1.1)
                self.state.entropy *= 0.9  # Slight entropy reduction
    
    def _update_scup_momentum(self):
        """Track SCUP momentum and adjust system dynamics"""
        # Calculate momentum
        self.state.scup_momentum = self.state.scup - self.state.last_scup
        self.state.last_scup = self.state.scup
        
        config = self.config["scup"]
        
        # Adjust tracer urgency based on SCUP momentum
        if self.state.scup_momentum > config["rising_threshold"]:
            # SCUP rising - reduce urgency
            self.state.tracer_urgency *= (1 - config["urgency_impact"] * self.state.scup_momentum)
            if self.enable_narrative:
                self.narrative_history.append(f"📈 SCUP rising (Δ={self.state.scup_momentum:.3f}). System stabilizing.")
        elif self.state.scup_momentum < config["falling_threshold"]:
            # SCUP falling - increase urgency
            self.state.tracer_urgency = min(1.0, self.state.tracer_urgency * 1.2)
            if self.enable_narrative:
                self.narrative_history.append(f"📉 SCUP falling. Increasing vigilance.")
        
        # Reroute tracers based on urgency
        if self.state.tracer_urgency > 0.7:
            self.state.tracer_zones = ["unstable", "critical"]
            if self.enable_narrative:
                self.narrative_history.append("🦉 Owl rerouting to unstable zones")
        elif self.state.tracer_urgency < 0.3:
            self.state.tracer_zones = ["stable", "growth"]
    
    def _calculate_cascade_risk(self):
        """Calculate overall cascade risk from multiple factors"""
        config = self.config["cascade"]
        
        heat_risk = self.state.stasis_heat * config["heat_weight"]
        entropy_risk = self.state.entropy * config["entropy_weight"]
        drift_risk = self.state.drift_magnitude * config["drift_weight"]
        
        self.state.cascade_risk = heat_risk + entropy_risk + drift_risk
        
        if self.state.cascade_risk > config["critical_threshold"] and self.state.tick - self.reflex_cooldowns["heat_cascade"] > 50:
            # Trigger cascade prevention
            if self.enable_narrative:
                self.narrative_history.append("🚨 CASCADE RISK CRITICAL - Emergency measures activated")
            
            # Emergency cooling
            pulse.remove_heat(pulse.heat * config["emergency_cooling_factor"], "cascade_prevention")
            self.state.stasis_heat *= (1 - config["emergency_cooling_factor"])
            self.reflex_cooldowns["heat_cascade"] = self.state.tick
    
    def _generate_tick_blooms(self, tick_id: int):
        """Generate multiple blooms per tick with varying pressure/activity (from tick_loop.py)"""
        config = self.config.get("blooms", {})
        blooms_per_tick = config.get("per_tick", 5)
        
        for i in range(blooms_per_tick):
            # Calculate pressure and activity for this bloom
            pressure = config.get("pressure_base", 0.2) + i * config.get("pressure_increment", 0.1)
            activity = config.get("activity_base", 0.5) + i * config.get("activity_increment", 0.05)
            
            # Determine mood based on pressure
            mood = self._calculate_bloom_mood(pressure)
            
            # Write bloom with calculated parameters
            write_bloom(
                seed=f"tick-{tick_id}-bloom-{i}",
                mood=mood,
                tick=tick_id,
                semantic_pressure=pressure,
                seed_coord=[i, tick_id % 100],
                mood_prev=self.state.last_bloom_mood
            )
            
            self.state.last_bloom_mood = mood
    
    def _calculate_bloom_mood(self, current_pressure: float) -> str:
        """Calculate mood based on pressure window (from tick_loop.py)"""
        config = self.config.get("mood", {})
        
        # Track pressure history
        self.state.pressure_history.append(current_pressure)
        
        # Calculate average pressure
        avg_pressure = sum(self.state.pressure_history) / len(self.state.pressure_history)
        
        # Determine mood and adjust interval
        if avg_pressure > config.get("stressed_threshold", 0.4):
            pulse.current_interval *= config.get("interval_stress_factor", 0.95)
            return "stressed"
        elif avg_pressure < config.get("calm_threshold", 0.2):
            pulse.current_interval *= config.get("interval_calm_factor", 1.02)
            return "calm"
        else:
            return "neutral"
    
    async def _trigger_autonomous_bloom(self, tick_id: int):
        """
        Trigger autonomous bloom generation (from tick_hook_autonomous.py)
        
        This replaces the external AutonomousFieldTrigger hook with integrated logic
        that has better access to system state and configuration.
        """
        config = self.config.get("autonomous_blooms", {})
        
        if not config.get("enabled", True):
            return
            
        frequency = config.get("frequency", 10)
        
        if tick_id % frequency != 0:
            return
        
        try:
            # Calculate bloom properties based on tick count
            lineage_depth = (tick_id // frequency) % 5
            bloom_factor = 1.0 + ((tick_id % 30) / 10)
            entropy_score = config.get("base_entropy", 0.25) + ((tick_id % 7) * config.get("entropy_variance", 0.05))
            
            # Determine mood
            mood_config = config.get("moods", {})
            if tick_id % mood_config.get("reflective_frequency", 20) == 0:
                mood = "reflective"
            else:
                mood = mood_config.get("default_mood", "anxious")
            
            # Create bloom data with system state awareness
            bloom_data = {
                "seed_id": f"auto-{tick_id}-{self.state.autonomous_bloom_count}",
                "lineage_depth": lineage_depth,
                "bloom_factor": bloom_factor,
                "entropy_score": entropy_score,
                "mood": mood,
                "triggered_by": "autonomous",
                "system_state": {
                    "zone": self.state.current_zone,
                    "heat": pulse.heat,
                    "scup": self.state.scup,
                    "drift": self.state.drift_magnitude
                }
            }
            
            print(f"[UnifiedTickEngine] 🌱 Triggering autonomous bloom at tick {tick_id}")
            
            # Spawn bloom with proper pulse reference
            spawn_bloom(bloom_data, pulse=pulse)
            
            # Update state
            self.state.autonomous_bloom_count += 1
            self.state.last_autonomous_bloom_tick = tick_id
            
            # Log rebloom
            owl_log_rebloom(bloom_data)
            
            # Animate lineage
            animate_rebloom_lineage()
                
            # Add to narrative if enabled
            if self.enable_narrative:
                self.narrative_history.append(
                    f"🤖 Autonomous bloom '{bloom_data['seed_id']}' spawned "
                    f"(mood: {mood}, entropy: {entropy_score:.3f})"
                )
                
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Autonomous bloom error: {e}")
    
    async def _compute_adaptive_interval(self) -> Tuple[float, Dict[str, float]]:
        """Compute adaptive tick interval with unified dynamics"""
        # Gather sensor inputs
        activity = await self.activity_sensor() if self.activity_sensor else 0.5
        pressure = await self.pressure_sensor() if self.pressure_sensor else 0.0
        mood_pressure = await self.mood_sensor() if self.mood_sensor else 0.0
        
        # Get current thermal state
        thermal_profile = pulse.get_thermal_profile()
        current_heat = thermal_profile['current_heat']
        stability = thermal_profile['stability_index']
        momentum = thermal_profile['thermal_momentum']
        
        # Update state metrics
        self.state.pulse_heat = current_heat
        self.state.entropy = self._calculate_entropy_score()
        self.state.scup = self._calculate_scup()
        self.state.arousal = activity
        self.state.valence = mood_pressure - 0.5  # Convert to -0.5 to 0.5 range
        
        # Calculate unified tension
        heat_tension = self.state.stasis_heat * 0.2
        drift_tension = self.state.drift_magnitude * 0.3
        cascade_tension = self.state.cascade_risk * 0.5
        total_tension = heat_tension + drift_tension + cascade_tension
        
        # Base interval calculation
        denominator = (1.0 + 
                      self.alpha * activity + 
                      self.beta * pressure + 
                      self.gamma * mood_pressure +
                      self.delta * total_tension)
        
        base_interval = self.base_interval / denominator
        
        # Apply momentum and stability
        momentum_factor = 1.0 + (momentum * 0.1)
        thermal_interval = base_interval / momentum_factor
        
        stability_factor = 0.8 + (stability * 0.4)
        final_interval = thermal_interval * stability_factor
        
        # Zone adjustments
        final_interval = self._apply_zone_adjustments(final_interval, current_heat, self.state.scup)
        
        # Clamp to bounds
        final_interval = max(0.1, min(final_interval, 5.0))
        
        # Debug metrics
        debug_metrics = {
            'activity': activity,
            'pressure': pressure,
            'mood_pressure': mood_pressure,
            'entropy_score': self.state.entropy,
            'scup': self.state.scup,
            'current_heat': current_heat,
            'stasis_heat': self.state.stasis_heat,
            'drift_magnitude': self.state.drift_magnitude,
            'cascade_risk': self.state.cascade_risk,
            'stability': stability,
            'momentum': momentum,
            'total_tension': total_tension,
            'final_interval': final_interval
        }
        
        return final_interval, debug_metrics
    
    def _apply_zone_adjustments(self, interval: float, heat: float, scup: float) -> float:
        """Apply zone-specific interval adjustments"""
        zone = pulse.classify()
        zone_config = self.config["zones"]
        
        if zone == "🔴 surge":
            surge_config = zone_config["surge"]
            urgency_multiplier = surge_config["interval_multiplier"] if scup >= self.config["scup"]["critical_scup"] else surge_config["interval_multiplier"] * 0.6
            return interval * urgency_multiplier
        elif zone == "🟢 calm":
            calm_config = zone_config["calm"]
            calm_multiplier = calm_config["interval_multiplier"] if scup > self.config["scup"]["stable_scup"] else calm_config["interval_multiplier"] * 0.8
            return interval * calm_multiplier
        else:  # Active zone
            active_config = zone_config["active"]
            return interval * active_config["interval_multiplier"]
    
    def _calculate_entropy_score(self) -> float:
        """Calculate current system entropy score"""
        try:
            sigil_entropy_list = get_active_sigil_entropy_list()
            raw_entropy = sum(sigil_entropy_list) / len(sigil_entropy_list) if sigil_entropy_list else 0.0
            
            bloom_count = len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                              if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0
            
            bloom_entropy = min(bloom_count / 20.0, 1.0) * 0.3
            total_entropy = raw_entropy + bloom_entropy
            
            self.entropy_trend.append(total_entropy)
            return total_entropy
            
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Entropy calculation error: {e}")
            return 0.5
    
    def _calculate_scup(self) -> float:
        """Calculate current SCUP"""
        try:
            tp_rar = current_alignment_probe(None)
            pressure_score = pulse.heat
            urgency_level = mood_urgency_probe(None)
            
            sigil_entropy_list = get_active_sigil_entropy_list()
            current_sigil_entropy = sum(sigil_entropy_list) / len(sigil_entropy_list) if sigil_entropy_list else 0.0
            
            scup = compute_scup(
                tp_rar=tp_rar,
                pressure_score=pressure_score,
                urgency_level=urgency_level,
                sigil_entropy=current_sigil_entropy,
                pulse=pulse,
                entropy_log=list(self.entropy_trend)
            )
            
            self.scup_trend.append(scup)
            return scup
            
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ SCUP calculation error: {e}")
            return 0.5
    
    def _update_zone_tracking(self, zone: str):
        """Update zone timing and transition tracking"""
        # Ensure zone exists in timer (safety check from tick_engine.py)
        if zone not in self.state.zone_timer:
            self.state.zone_timer[zone] = 0
            
        if zone != self.state.current_zone:
            self.zone_transitions.append((self.state.tick, zone))
            if len(self.zone_transitions) > 100:
                self.zone_transitions.pop(0)
            
            for z in self.state.zone_timer:
                if z == zone:
                    self.state.zone_timer[z] += 1
                else:
                    self.state.zone_timer[z] = 0
            
            self.state.current_zone = zone
            print(f"[UnifiedTickEngine] 🔄 Zone transition: {zone}")
        else:
            self.state.zone_timer[zone] += 1
    
    def _write_narrative_log(self):
        """Write narrative history to file"""
        if not self.config["narrative"]["enabled"]:
            return
            
        try:
            narrative_config = self.config["narrative"]
            if self.state.tick % narrative_config["log_interval"] == 0:
                with open("cognitive_states/narrative_log.txt", "a", encoding="utf-8") as f:
                    for narrative in list(self.narrative_history)[-10:]:
                        f.write(f"{narrative}\n")
                self.narrative_history.clear()
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Narrative log error: {e}")
    
    async def _execute_zone_reflexes(self, zone: str, scup: float, entropy_score: float):
        """Execute zone-specific reflexes and responses"""
        current_tick = self.state.tick
        zone_config = self.config["zones"]
        scup_config = self.config["scup"]
        
        if zone == "🟢 calm":
            calm_config = zone_config["calm"]
            if (self.state.zone_timer[zone] >= calm_config["synthesis_threshold"] and 
                current_tick - self.reflex_cooldowns["synthesis"] > 50):
                
                print("[UnifiedTickEngine] 🧠 Sustained calm — triggering Juliet synthesis")
                await self._trigger_synthesis()
                self.reflex_cooldowns["synthesis"] = current_tick
            
            if (self.state.zone_timer[zone] >= calm_config["rebloom_threshold"] and 
                current_tick - self.reflex_cooldowns["rebloom_queue"] > 30):
                
                print("[UnifiedTickEngine] 🪴 Calm zone — processing rebloom queue")
                await self._process_rebloom_queue()
                self.reflex_cooldowns["rebloom_queue"] = current_tick
        
        elif zone == "🟡 active":
            active_config = zone_config["active"]
            if (self.state.zone_timer[zone] % active_config["entropy_scan_interval"] == 0 and 
                current_tick - self.reflex_cooldowns["entropy_scan"] > 25):
                
                print("[UnifiedTickEngine] 🔍 Active mode — entropy scan")
                await self._trigger_entropy_scan()
                self.reflex_cooldowns["entropy_scan"] = current_tick
        
        elif zone == "🔴 surge":
            surge_config = zone_config["surge"]
            if (self.state.zone_timer[zone] >= surge_config["emergency_threshold"] and 
                current_tick - self.reflex_cooldowns["emergency_suppression"] > 40):
                
                print("[UnifiedTickEngine] 🚨 Surge pressure — emergency response")
                await self._trigger_emergency_response(scup)
                self.reflex_cooldowns["emergency_suppression"] = current_tick
        
        # Cross-zone reflexes from config
        if scup < scup_config["critical_scup"]:
            launch_reflex("scup_alert")
            owl_log(f"⚠️ SCUP critical: {scup:.3f} at tick {current_tick}")
        
        if entropy_score > 0.6:
            launch_reflex("entropy_spike")
        
        try:
            mood_pressure = await self.mood_sensor() if self.mood_sensor else 0.0
            if mood_pressure > 0.5:
                launch_reflex("mood_heatmap")
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Mood reflex error: {e}")
    
    async def _trigger_synthesis(self):
        """Trigger Juliet synthesis process"""
        try:
            trigger_synthesis()
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Synthesis trigger error: {e}")
    
    async def _process_rebloom_queue(self):
        """Process pending rebloom candidates"""
        try:
            bloom = pop_rebloom_candidate()
            if not bloom:
                return
            
            ancestry = getattr(bloom, "rebloom_tag", f"rebloomed-{bloom.seed_id}")
            new_data = bloom.to_dict()
            new_data["ancestry_tag"] = ancestry
            new_data["lineage_depth"] = getattr(bloom, "lineage_depth", 0) + 1
            new_data["rebloomed_by"] = "UnifiedTickEngine"
            
            print(f"[UnifiedTickEngine] 🌱 Reblooming {bloom.seed_id} → new instance")
            owl_log(f"[Rebloom] 🔄 {bloom.seed_id} rebloomed with ancestry: {ancestry}")
            
            log_rebloom_lineage(bloom.seed_id, ancestry)
            spawn_bloom(new_data)
            
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Rebloom processing error: {e}")
    
    async def _trigger_entropy_scan(self):
        """Trigger entropy analysis scan"""
        try:
            run_entropy_scan()
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Entropy scan error: {e}")
    
    async def _trigger_emergency_response(self, scup: float):
        """Trigger emergency response for surge conditions"""
        try:
            stress_seeds = ["A1", "C3", "D4"]
            for seed in stress_seeds:
                pulse.apply_penalty(seed, 0.8)
            
            if scup < 0.25:
                proposed_patch = '''
def emergency_stabilization(self, scup_score):
    """Emergency stabilization when SCUP drops critically low."""
    if scup_score < 0.25:
        pulse.remove_heat(pulse.heat * 0.3, "emergency_cooling")
        pulse.thermal_momentum *= 0.5
        return True
    return False
'''
                commentary = f"SCUP critical at {scup:.3f}. Emergency stabilization needed."
                propose_code_patch("tick_engine", "emergency_stabilization", 
                                 proposed_patch, commentary)
        
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Emergency response error: {e}")
    
    def _log_tick_metrics(self, tick_id: int, zone: str, interval: float, 
                         debug_metrics: Dict[str, float]):
        """Log comprehensive tick metrics"""
        try:
            self.interval_history.append(interval)
            
            # Enhanced logging with experimental metrics
            log_field_snapshot(
                tick_id=tick_id,
                zone=zone,
                pulse_heat=debug_metrics['current_heat'],
                scup_score=debug_metrics['scup'],
                entropy_score=debug_metrics['entropy_score'],
                bloom_count=self.state.rebloom_count,
                interval=interval,
                mood_pressure=debug_metrics['mood_pressure'],
                # Additional experimental metrics
                stasis_heat=self.state.stasis_heat,
                drift_magnitude=self.state.drift_magnitude,
                cascade_risk=self.state.cascade_risk
            )
            
            log_claude_voice({
                "tick_id": tick_id,
                "zone": zone,
                "pulse_heat": debug_metrics['current_heat'],
                "scup_score": debug_metrics['scup'],
                "entropy_score": debug_metrics['entropy_score'],
                "mood_pressure": debug_metrics['mood_pressure'],
                "stability": debug_metrics['stability'],
                "interval": interval,
                "experimental": {
                    "stasis_heat": self.state.stasis_heat,
                    "drift_magnitude": self.state.drift_magnitude,
                    "cascade_risk": self.state.cascade_risk,
                    "tracer_urgency": self.state.tracer_urgency
                }
            })
            
            os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
            with open("juliet_flowers/cluster_report/interval_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{interval:.3f}\n")
            
            # Periodic detailed logging
            if tick_id % 10 == 0:
                print(f"\n[UnifiedTickEngine] 📊 Tick {tick_id} Metrics:")
                print(f"  Zone: {zone} | Heat: {debug_metrics['current_heat']:.3f} | SCUP: {debug_metrics['scup']:.3f}")
                print(f"  Interval: {interval:.3f}s | Stability: {debug_metrics['stability']:.3f}")
                print(f"  Entropy: {debug_metrics['entropy_score']:.3f} | Cascade Risk: {self.state.cascade_risk:.3f}")
                print(f"  Drift: {self.state.drift_magnitude:.3f} | Stasis Heat: {self.state.stasis_heat:.3f}")
                
                # Owl comment on memory logs (from tick_loop.py)
                memory_snapshot = {
                    "tick": tick_id,
                    "activity": self.state.arousal,
                    "pressure": pulse.current_pressure,
                    "interval": interval,
                    "zone": zone,
                    "entropy": self.state.entropy
                }
                
                pulse.memory_log.append(memory_snapshot)
                owl_comment(pulse.memory_log, tick_id)

        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Logging error: {e}")
    
    def _perform_maintenance_cycles(self, tick_id: int):
        """Perform periodic maintenance and cleanup"""
        maintenance = self.config["maintenance"]
        
        try:
            if tick_id % maintenance["shi_check_interval"] == 0:
                shi = calculate_SHI(
                    pulse.heat,
                    len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                        if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0,
                    len(os.listdir("juliet_flowers/sealed")) if os.path.exists("juliet_flowers/sealed") else 0,
                    [sigil.entropy for sigil in sigil_memory_ring.values() if hasattr(sigil, 'entropy')]
                )
                print(f"[UnifiedTickEngine] 🧬 Schema Health Index: {shi:.3f}")
            
            if self.state.zone_timer.get("🟢 calm", 0) % maintenance["memory_decay_interval"] == 0:
                decay_schema_memory()
            
            if tick_id % maintenance["sigil_maintenance_interval"] == 0:
                decay_all_sigils()
                age_all_sigils()
            
            if tick_id % maintenance["lifecycle_interval"] == 0:
                fade_sigils()
                expire_ephemeral_sigils()
                prune_dead_branches()
            
            if tick_id % maintenance["bloom_sweep_interval"] == 0:
                print("[UnifiedTickEngine] 🧺 Scheduled bloom sweep")
                for bloom in load_all_blooms():
                    soft_seal_bloom(bloom)
            
            if tick_id % maintenance["entropy_render_interval"] == 0:
                render_entropy_field()
                
            # Sigil evolution (from tick_loop.py)
            if tick_id % 5 == 0:
                field_state = {
                    "mood": self._calculate_bloom_mood(self.state.arousal),
                    "pressure": pulse.current_pressure,
                    "activity": self.state.arousal,
                    "entropy": self.state.entropy,
                    "zone": self.state.current_zone
                }
                sigils.evolve_classes(field_state)
        
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Maintenance error: {e}")
    
    async def start(self):
        """Start the unified tick engine"""
        print("[UnifiedTickEngine] 🚀 Starting unified engine with experimental dynamics")
        self._running = True
        
        while self._running:
            try:
                # Update tick
                self.state.tick = pulse.tick_count
                
                # Generate main narrative
                if self.enable_narrative:
                    self.narrative_history.append(self._generate_narrative())
                
                # Update experimental dynamics
                self._update_heat_engine()
                self._update_drift_mechanics()
                self._check_rebloom_conditions()
                self._update_scup_momentum()
                self._calculate_cascade_risk()
                
                # Compute adaptive interval
                interval, debug_metrics = await self._compute_adaptive_interval()
                
                # Update thermal system
                pressure_val = await self.pressure_sensor() if self.pressure_sensor else 0.0
                pulse.update(pressure_val)
                
                # Get current zone and update tracking
                zone = pulse.classify()
                self._update_zone_tracking(zone)
                
                # Execute zone reflexes
                await self._execute_zone_reflexes(zone, self.state.scup, self.state.entropy)
                
                # Update schema health
                update_schema_health(self.state.scup)
                pulse.adjust_urgency(self.state.scup)
                
                # Emit tick event (using internal method)
                tick_id = self._emit_tick(zone=zone, pulse_heat=round(pulse.heat, 3))
                
                # Generate blooms for this tick (from tick_loop.py)
                self._generate_tick_blooms(tick_id)
                
                # Trigger autonomous blooms (from tick_hook_autonomous.py)
                await self._trigger_autonomous_bloom(tick_id)
                
                # Run drift sentinel
                drift_result = owl_drift_check(tick_id=tick_id)
                if drift_result == "override_suppression":
                    print(f"[UnifiedTickEngine] 🚫 Drift sentinel override at tick {tick_id}")
                    pulse.override_active = True
                    launch_reflex("suppression_override")
                
                # Emit tick event to other systems
                if self.emit_tick_event:
                    from core.event_bus import TickEvent
                    await self.emit_tick_event(TickEvent())
                
                # Log comprehensive metrics
                self._log_tick_metrics(tick_id, zone, interval, debug_metrics)
                
                # Perform maintenance cycles
                self._perform_maintenance_cycles(tick_id)
                
                # Visual reflexes
                owl_visual_reflex(tick_id)
                
                # Save state
                self._save_state()
                
                # Write narrative log periodically
                if self.state.tick % 10 == 0:
                    self._write_narrative_log()
                
                # Check for significant changes
                if abs(self.last_interval - interval) > 0.2:
                    owl_log(f"⏱️ Interval shift: {self.last_interval:.2f}s → {interval:.2f}s")
                    self.last_interval = interval
                
                # Wait for computed interval
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"[UnifiedTickEngine] ❌ Main loop error: {e}")
                # Emergency fallback interval (from tick_engine.py)
                await asyncio.sleep(max(1.0, self.base_interval))
    
    def stop(self):
        """Stop the unified tick engine"""
        print("[UnifiedTickEngine] 🛑 Stopping unified engine")
        self._running = False
        self._write_narrative_log()
        self._save_state()
    
    # Additional methods from tick_emitter.py
    def get_current_tick(self) -> int:
        """Get current tick value"""
        return pulse.tick_count
    
    def load_zone_overlay(self):
        """Load full zone overlay log as DataFrame"""
        try:
            import pandas as pd
            df = pd.read_csv(self.zone_overlay_file, 
                            names=["tick", "zone", "pulse", "drift"], 
                            encoding="utf-8")
            return df
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Failed to load overlay log: {e}")
            return None
    
    def get_recent_zone_window(self, window: int = 10) -> List[Dict]:
        """Return last N zone pulses"""
        df = self.load_zone_overlay()
        if df is None or df.empty:
            return []
        return df.tail(window).to_dict("records")
    
    def set_autonomous_blooms(self, enabled: bool):
        """Enable or disable autonomous bloom generation at runtime"""
        self.state.autonomous_bloom_enabled = enabled
        self.config["autonomous_blooms"]["enabled"] = enabled
        
        if enabled:
            print(f"[UnifiedTickEngine] ✅ Autonomous blooms enabled")
        else:
            print(f"[UnifiedTickEngine] ⏸️ Autonomous blooms disabled")
    
    def reload_config(self):
        """Reload configuration from file"""
        old_config = self.config.copy()
        try:
            self.config = self._load_config()
            print("[UnifiedTickEngine] ✅ Configuration reloaded successfully")
            
            # Update runtime values that depend on config
            self.enable_narrative = self.config["narrative"]["enabled"]
            
            return True
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Config reload failed: {e}")
            self.config = old_config
            return False
    
    def update_config(self, section: str, key: str, value: any):
        """Update a specific config value and save to file"""
        try:
            if section in self.config and key in self.config[section]:
                self.config[section][key] = value
                
                # Save updated config
                with open("tick_engine_config.json", "w") as f:
                    json.dump(self.config, f, indent=2)
                    
                print(f"[UnifiedTickEngine] ✅ Updated config: {section}.{key} = {value}")
                return True
        except Exception as e:
            print(f"[UnifiedTickEngine] ❌ Config update failed: {e}")
            return False
    
    def get_engine_stats(self) -> Dict:
        """Get comprehensive engine statistics"""
        return {
            'tick_count': self.state.tick,
            'current_zone': self.state.current_zone,
            'zone_timer': dict(self.state.zone_timer),
            'recent_intervals': list(self.interval_history)[-10:],
            'entropy_trend': list(self.entropy_trend)[-10:],
            'scup_trend': list(self.scup_trend)[-10:],
            'zone_transitions': self.zone_transitions[-5:],
            'reflex_cooldowns': dict(self.reflex_cooldowns),
            'thermal_profile': pulse.get_thermal_profile(),
            'experimental_state': {
                'stasis_heat': self.state.stasis_heat,
                'drift_magnitude': self.state.drift_magnitude,
                'cascade_risk': self.state.cascade_risk,
                'rebloom_count': self.state.rebloom_count,
                'tracer_urgency': self.state.tracer_urgency,
                'alignment': self.state.alignment
            },
            'autonomous_blooms': {
                'enabled': self.state.autonomous_bloom_enabled,
                'count': self.state.autonomous_bloom_count,
                'last_tick': self.state.last_autonomous_bloom_tick,
                'frequency': self.config.get("autonomous_blooms", {}).get("frequency", 10)
            }
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_unified_tick_engine(base_interval: float = 1.0, 
                              activity_sensor: Optional[Callable] = None,
                              pressure_sensor: Optional[Callable] = None,
                              mood_sensor: Optional[Callable] = None,
                              enable_narrative: bool = None) -> UnifiedTickEngine:
    """Create and configure a unified tick engine"""
    return UnifiedTickEngine(
        base_interval=base_interval,
        activity_sensor=activity_sensor,
        pressure_sensor=pressure_sensor,
        mood_sensor=mood_sensor,
        enable_narrative=enable_narrative
    )


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================

async def run_standalone():
    """Run the unified tick engine as a standalone process"""
    print("\n" + "="*60)
    print("🚀 DAWN UNIFIED TICK ENGINE v2")
    print("="*60 + "\n")
    
    # Define sensor functions for standalone mode
    async def activity_sensor():
        """Simulate activity based on system state"""
        import random
        base = 0.5
        noise = random.uniform(-0.1, 0.1)
        # Activity increases with heat
        heat_factor = pulse.heat * 0.3
        return max(0.1, min(1.0, base + noise + heat_factor))
    
    async def pressure_sensor():
        """Simulate pressure based on entropy and SCUP"""
        entropy = engine.state.entropy if engine else 0.5
        scup = engine.state.scup if engine else 0.5
        # Pressure increases when entropy high or SCUP low
        return (entropy * 0.6) + ((1 - scup) * 0.4)
    
    async def mood_sensor():
        """Simulate mood based on recent state"""
        if engine and hasattr(engine.state, 'valence'):
            # Convert valence (-0.5 to 0.5) to mood pressure (0 to 1)
            return (engine.state.valence + 0.5)
        return 0.5
    
    # Create engine with sensors
    engine = UnifiedTickEngine(
        base_interval=1.0,
        activity_sensor=activity_sensor,
        pressure_sensor=pressure_sensor,
        mood_sensor=mood_sensor,
        enable_narrative=None  # Use config value
    )
    
    # Make engine accessible to sensors
    globals()['engine'] = engine
    
    # Display loaded configuration summary
    print("📋 Configuration loaded:")
    print(f"  - Narrative: {'Enabled' if engine.config['narrative']['enabled'] else 'Disabled'}")
    print(f"  - Heat stasis threshold: {engine.config['heat']['stasis_threshold']}")
    print(f"  - Rebloom cooldown: {engine.config['rebloom']['cooldown_ticks']} ticks")
    print(f"  - Zone intervals: Calm x{engine.config['zones']['calm']['interval_multiplier']}, "
          f"Active x{engine.config['zones']['active']['interval_multiplier']}, "
          f"Surge x{engine.config['zones']['surge']['interval_multiplier']}")
    print(f"  - Maintenance intervals: SHI={engine.config['maintenance']['shi_check_interval']}, "
          f"Sigils={engine.config['maintenance']['sigil_maintenance_interval']}")
    print()
    
    print("✅ Engine initialized with autonomous sensors")
    print(f"📊 Starting from tick {engine.get_current_tick()}")
    print(f"🔧 Base interval: {engine.base_interval}s")
    print(f"📝 Narrative mode: {engine.enable_narrative}")
    print("\nPress Ctrl+C to stop...\n")
    
    try:
        # Run the engine
        await engine.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutdown requested...")
        engine.stop()
        print("✅ Engine stopped gracefully")
        
        # Print final stats
        stats = engine.get_engine_stats()
        print(f"\n📊 Final Statistics:")
        print(f"  Total ticks: {stats['tick_count']}")
        print(f"  Final zone: {stats['current_zone']}")
        print(f"  Zone timers: {stats['zone_timer']}")
        print(f"  Rebloom count: {stats['experimental_state']['rebloom_count']}")
        print(f"  Autonomous blooms: {stats['autonomous_blooms']['count']}")
        print(f"  Final SCUP: {stats['scup_trend'][-1] if stats['scup_trend'] else 'N/A':.3f}")
        print(f"  Final entropy: {stats['entropy_trend'][-1] if stats['entropy_trend'] else 'N/A':.3f}")

if __name__ == "__main__":
    # Run as standalone executable
    import asyncio
    
    try:
        asyncio.run(run_standalone())
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        
print("[UnifiedTickEngine] ✨ Unified TickEngine v2 loaded and ready")