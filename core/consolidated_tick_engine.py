#!/usr/bin/env python3
"""
DAWN Consolidated Tick Engine v3.0
Unified tick engine combining all tick-related functionality into a single module.
Can be run standalone or imported as a module.
"""

import sys
import os
import asyncio
import time
import math
import json
import argparse
import pandas as pd
from typing import Dict, List, Optional, Callable, Tuple, Any
from collections import deque
from dataclasses import dataclass, asdict, field
from datetime import datetime
from abc import ABC, abstractmethod
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(name)s] %(message)s')
logger = logging.getLogger("TickEngine")

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class CognitiveState:
    """Unified cognitive state tracking all system metrics"""
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
    drift_vector: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
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
    tracer_zones: List[str] = field(default_factory=lambda: ["stable"])
    
    # Zone state
    current_zone: str = "🟢 calm"
    zone_timer: Dict[str, int] = field(default_factory=lambda: {"🟢 calm": 0, "🟡 active": 0, "🔴 surge": 0})
    
    # Cascade risk
    cascade_risk: float = 0.0
    
    # Bloom mood tracking
    last_bloom_mood: str = "neutral"
    pressure_history: deque = field(default_factory=lambda: deque(maxlen=5))
    
    # Autonomous bloom state
    autonomous_bloom_enabled: bool = True
    autonomous_bloom_count: int = 0
    last_autonomous_bloom_tick: int = 0


@dataclass
class TickEvent:
    """Event emitted on each tick"""
    tick_id: int
    zone: str
    interval: float
    metrics: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BloomData:
    """Data structure for bloom generation"""
    seed_id: str
    mood: str
    tick: int
    entropy_score: float = 0.5
    lineage_depth: int = 0
    bloom_factor: float = 1.0
    triggered_by: str = "tick"
    semantic_pressure: float = 0.5
    seed_coord: List[int] = field(default_factory=lambda: [0, 0])
    mood_prev: Optional[str] = None
    system_state: Optional[Dict] = None


# ============================================================================
# INTERFACES FOR EXTERNAL SYSTEMS
# ============================================================================

class PulseInterface(ABC):
    """Interface for pulse/heat management system"""
    @abstractmethod
    def get_heat(self) -> float: pass
    @abstractmethod
    def add_heat(self, amount: float, source: str): pass
    @abstractmethod
    def remove_heat(self, amount: float, source: str): pass
    @abstractmethod
    def update(self, pressure: float): pass
    @abstractmethod
    def classify(self) -> str: pass
    @abstractmethod
    def get_thermal_profile(self) -> Dict[str, float]: pass


class BloomInterface(ABC):
    """Interface for bloom spawning system"""
    @abstractmethod
    def spawn_bloom(self, data: Dict, pulse: Any = None): pass
    @abstractmethod
    def write_bloom(self, **kwargs): pass


class SchemaInterface(ABC):
    """Interface for schema/cognitive systems"""
    @abstractmethod
    def compute_scup(self, **kwargs) -> float: pass
    @abstractmethod
    def update_schema_health(self, scup: float): pass
    @abstractmethod
    def get_total_drift_entropy(self) -> float: pass


# ============================================================================
# DEFAULT IMPLEMENTATIONS
# ============================================================================

class SimplePulse(PulseInterface):
    """Simple pulse implementation for standalone mode"""
    def __init__(self):
        self.heat = 0.5
        self.tick_count = 0
        self.thermal_momentum = 0.1
        self.current_pressure = 0.0
        
    def get_heat(self) -> float:
        return self.heat
        
    def add_heat(self, amount: float, source: str):
        self.heat = min(1.0, self.heat + amount)
        logger.debug(f"Heat added: {amount} from {source}")
        
    def remove_heat(self, amount: float, source: str):
        self.heat = max(0.0, self.heat - amount)
        logger.debug(f"Heat removed: {amount} from {source}")
        
    def update(self, pressure: float):
        self.current_pressure = pressure
        self.heat += (pressure - 0.5) * 0.1
        self.heat = max(0.0, min(1.0, self.heat))
        self.thermal_momentum = self.thermal_momentum * 0.9 + (pressure - 0.5) * 0.1
        
    def classify(self) -> str:
        if self.heat > 0.7:
            return "🔴 surge"
        elif self.heat > 0.3:
            return "🟡 active"
        else:
            return "🟢 calm"
            
    def get_thermal_profile(self) -> Dict[str, float]:
        return {
            'current_heat': self.heat,
            'stability_index': 0.8 - abs(self.heat - 0.5),
            'thermal_momentum': self.thermal_momentum
        }


class SimpleBloomSystem(BloomInterface):
    """Simple bloom system for standalone mode"""
    def __init__(self, output_dir: str = "blooms"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def spawn_bloom(self, data: Dict, pulse: Any = None):
        logger.info(f"🌸 Spawning bloom: {data.get('seed_id', 'unknown')}")
        # Save bloom data to file
        bloom_file = os.path.join(self.output_dir, f"{data['seed_id']}.json")
        with open(bloom_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
    def write_bloom(self, **kwargs):
        bloom_data = BloomData(**kwargs)
        self.spawn_bloom(asdict(bloom_data))


class SimpleSchema(SchemaInterface):
    """Simple schema implementation for standalone mode"""
    def compute_scup(self, **kwargs) -> float:
        # Simple SCUP calculation
        pressure = kwargs.get('pressure_score', 0.5)
        urgency = kwargs.get('urgency_level', 0.5)
        entropy = kwargs.get('sigil_entropy', 0.5)
        return (1 - pressure) * 0.4 + (1 - urgency) * 0.3 + (1 - entropy) * 0.3
        
    def update_schema_health(self, scup: float):
        logger.debug(f"Schema health updated with SCUP: {scup:.3f}")
        
    def get_total_drift_entropy(self) -> float:
        return 0.4  # Default drift


# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

class TickEngineConfig:
    """Configuration management for tick engine"""
    
    DEFAULT_CONFIG = {
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
    
    def __init__(self, config_path: str = "tick_engine_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from file with defaults"""
        try:
            with open(self.config_path, "r") as f:
                loaded_config = json.load(f)
            return self._deep_merge(self.DEFAULT_CONFIG.copy(), loaded_config)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {self.config_path}, using defaults")
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
        except json.JSONDecodeError as e:
            logger.error(f"Config parse error: {e}, using defaults")
            return self.DEFAULT_CONFIG.copy()
            
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
        
    def _save_config(self, config: Dict):
        """Save configuration to file"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            
    def get(self, section: str, key: str = None, default: Any = None) -> Any:
        """Get configuration value"""
        if key is None:
            return self.config.get(section, default)
        return self.config.get(section, {}).get(key, default)
        
    def update(self, section: str, key: str, value: Any):
        """Update configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self._save_config(self.config)


# ============================================================================
# MAIN TICK ENGINE
# ============================================================================

class ConsolidatedTickEngine:
    """
    Consolidated DAWN Tick Engine with all features integrated.
    
    Features:
    - Adaptive tick intervals based on system state
    - Heat engine with stasis detection
    - Drift mechanics affecting system alignment
    - Dynamic rebloom logic based on emotional state
    - SCUP momentum and feedback loops
    - Zone-based reflexes and maintenance
    - Multiple blooms per tick
    - Autonomous bloom generation
    - Comprehensive state persistence
    - Narrative generation
    - Event emission system
    """
    
    # File paths
    TICK_STATE_FILE = "tick_state.json"
    ZONE_OVERLAY_FILE = "juliet_flowers/cluster_report/zone_overlay_log.csv"
    
    def __init__(self, 
                 base_interval: float = 1.0,
                 config_path: str = "tick_engine_config.json",
                 pulse: Optional[PulseInterface] = None,
                 bloom_system: Optional[BloomInterface] = None,
                 schema: Optional[SchemaInterface] = None,
                 activity_sensor: Optional[Callable] = None,
                 pressure_sensor: Optional[Callable] = None,
                 mood_sensor: Optional[Callable] = None,
                 enable_narrative: Optional[bool] = None):
        
        # Load configuration
        self.config_manager = TickEngineConfig(config_path)
        self.config = self.config_manager.config
        
        # Core timing
        self.base_interval = base_interval
        self.last_interval = base_interval
        
        # External systems (use defaults if not provided)
        self.pulse = pulse or SimplePulse()
        self.bloom_system = bloom_system or SimpleBloomSystem()
        self.schema = schema or SimpleSchema()
        
        # Sensors
        self.activity_sensor = activity_sensor or self._default_activity_sensor
        self.pressure_sensor = pressure_sensor or self._default_pressure_sensor
        self.mood_sensor = mood_sensor or self._default_mood_sensor
        
        # Narrative setting
        self.enable_narrative = enable_narrative if enable_narrative is not None else self.config["narrative"]["enabled"]
        
        # State tracking
        self.state = CognitiveState()
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
        
        # Event listeners
        self.event_listeners = []
        
        # Running state
        self._running = False
        
        # Initialize persistence
        self._init_persistence()
        
        logger.info(f"✨ ConsolidatedTickEngine initialized | Base interval: {base_interval}s | Narrative: {self.enable_narrative}")
        
    async def _default_activity_sensor(self) -> float:
        """Default activity sensor based on system state"""
        import random
        base = 0.5
        noise = random.uniform(-0.1, 0.1)
        heat_factor = self.pulse.get_heat() * 0.3
        return max(0.1, min(1.0, base + noise + heat_factor))
        
    async def _default_pressure_sensor(self) -> float:
        """Default pressure sensor based on entropy and SCUP"""
        entropy = self.state.entropy
        scup = self.state.scup
        return (entropy * 0.6) + ((1 - scup) * 0.4)
        
    async def _default_mood_sensor(self) -> float:
        """Default mood sensor based on valence"""
        return (self.state.valence + 0.5)  # Convert from [-0.5, 0.5] to [0, 1]
        
    def _init_persistence(self):
        """Initialize persistence files and load state"""
        os.makedirs("cognitive_states", exist_ok=True)
        os.makedirs(os.path.dirname(self.ZONE_OVERLAY_FILE), exist_ok=True)
        
        # Load tick state
        self._load_tick_state()
        
        # Load cognitive state
        self._load_cognitive_state()
        
    def _load_tick_state(self):
        """Load tick state from JSON file"""
        try:
            if os.path.exists(self.TICK_STATE_FILE):
                with open(self.TICK_STATE_FILE, "r") as f:
                    data = json.load(f)
                    self.state.tick = data.get("tick", 0)
                    if hasattr(self.pulse, 'tick_count'):
                        self.pulse.tick_count = self.state.tick
                    logger.info(f"Loaded tick state: {self.state.tick}")
        except Exception as e:
            logger.warning(f"Failed to load tick state: {e}")
            
    def _load_cognitive_state(self):
        """Load cognitive state from file"""
        try:
            with open("cognitive_states/cognitive_state.json", "r") as f:
                saved_state = json.load(f)
                self.state.rebloom_count = saved_state.get("rebloom_count", 0)
                self.state.autonomous_bloom_count = saved_state.get("autonomous_bloom_count", 0)
                logger.info("Loaded cognitive state")
        except:
            pass
            
    def _save_state(self):
        """Save current state to files"""
        # Save tick state
        tick_state = {
            "tick": self.state.tick,
            "timestamp": datetime.utcnow().isoformat(),
            "zone": self.state.current_zone,
            "pulse": self.state.pulse_heat,
            "drift": self.state.drift_magnitude
        }
        
        try:
            with open(self.TICK_STATE_FILE, "w") as f:
                json.dump(tick_state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save tick state: {e}")
            
        # Save cognitive state
        state_dict = asdict(self.state)
        state_dict["timestamp"] = datetime.now().isoformat()
        
        try:
            with open("cognitive_states/cognitive_state.json", "w") as f:
                json.dump(state_dict, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save cognitive state: {e}")
            
    def _emit_tick(self, zone: str = None, pulse_heat: float = None) -> int:
        """Emit next tick with persistence and zone overlay logging"""
        # Increment tick
        self.state.tick += 1
        tick_id = self.state.tick
        
        if hasattr(self.pulse, 'tick_count'):
            self.pulse.tick_count = tick_id
            
        # Get drift entropy
        drift_entropy = 0.0
        try:
            drift_entropy = round(self.schema.get_total_drift_entropy(), 4)
        except:
            pass
            
        # Log to zone overlay CSV
        try:
            with open(self.ZONE_OVERLAY_FILE, "a") as log:
                log.write(f"{tick_id},{zone},{pulse_heat},{drift_entropy}\n")
        except Exception as e:
            logger.warning(f"Failed to log zone overlay: {e}")
            
        logger.info(f"⏱️ Tick {tick_id} | Zone: {zone} | Heat: {pulse_heat:.3f} | Drift: {drift_entropy}")
        
        # Emit event to listeners
        event = TickEvent(
            tick_id=tick_id,
            zone=zone,
            interval=self.last_interval,
            metrics={
                'pulse_heat': pulse_heat,
                'drift': drift_entropy,
                'scup': self.state.scup,
                'entropy': self.state.entropy
            }
        )
        self._emit_event(event)
        
        return tick_id
        
    def _emit_event(self, event: TickEvent):
        """Emit event to all listeners"""
        for listener in self.event_listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    asyncio.create_task(listener(event))
                else:
                    listener(event)
            except Exception as e:
                logger.error(f"Event listener error: {e}")
                
    def add_event_listener(self, callback: Callable):
        """Add an event listener"""
        self.event_listeners.append(callback)
        
    def remove_event_listener(self, callback: Callable):
        """Remove an event listener"""
        if callback in self.event_listeners:
            self.event_listeners.remove(callback)
            
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
        """Update heat generation and dissipation dynamics"""
        config = self.config["heat"]
        
        # Detect stasis
        activity = self.pulse.get_thermal_profile().get('thermal_momentum', 0.1)
        if self.state.scup > 0.8 and activity < config["stasis_threshold"]:
            self.state.heat_generation_rate = config["generation_base"] * (1 + self.state.scup)
            self.state.stasis_heat += self.state.heat_generation_rate
            
            if self.enable_narrative:
                self.narrative_history.append(f"🔥 Stasis detected. Heat building ({self.state.stasis_heat:.3f})")
                
        # Heat dissipation
        self.state.heat_dissipation_rate = config["dissipation_base"] * self.state.alignment
        self.state.stasis_heat = max(0, self.state.stasis_heat - self.state.heat_dissipation_rate)
        
        # Apply heat to pulse
        if self.state.stasis_heat > 0:
            self.pulse.add_heat(self.state.stasis_heat * 0.1, f"stasis_heat_{self.state.tick}")
            
        # Check cascade risk
        if self.state.stasis_heat > config["critical_threshold"]:
            self.state.cascade_risk += 0.1
            if self.enable_narrative:
                self.narrative_history.append("⚠️ Critical heat levels. System approaching thermal cascade.")
                
    def _update_drift_mechanics(self):
        """Update system drift based on mood and arousal"""
        config = self.config["drift"]
        
        # Calculate drift
        if self.state.arousal > config["critical_drift_threshold"] or abs(self.state.valence) > config["critical_drift_threshold"]:
            drift_x = self.state.valence * config["arousal_factor"] * config["valence_weight"]
            drift_y = self.state.arousal * config["arousal_factor"]
            drift_z = (self.state.entropy - 0.5) * config["arousal_factor"] * config["entropy_weight"]
            
            self.state.drift_vector[0] += drift_x
            self.state.drift_vector[1] += drift_y
            self.state.drift_vector[2] += drift_z
            
            self.state.drift_magnitude = math.sqrt(sum(d**2 for d in self.state.drift_vector))
            
            if self.state.drift_magnitude > 0.05 and self.enable_narrative:
                self.narrative_history.append(f"🌊 Drift detected: magnitude {self.state.drift_magnitude:.3f}")
                
        # Apply decay
        for i in range(3):
            self.state.drift_vector[i] *= (1 - config["decay_rate"])
            
        # Update alignment
        if self.state.drift_magnitude > 0:
            alignment_penalty = self.state.drift_magnitude * config["alignment_impact"]
            self.state.alignment = max(0.1, self.state.alignment - alignment_penalty)
            
    def _check_rebloom_conditions(self):
        """Check and execute rebloom logic"""
        config = self.config["rebloom"]
        
        if (self.state.entropy > config["entropy_threshold"] and 
            self.state.valence < config["valence_threshold"] and
            self.state.tick - self.state.last_rebloom_tick > config["cooldown_ticks"]):
            
            self.state.rebloom_count += 1
            self.state.last_rebloom_tick = self.state.tick
            
            # Create rebloom
            bloom_data = {
                "seed_id": f"rebloom-{self.state.tick}-{self.state.rebloom_count}",
                "mood": "anxious",
                "tick": self.state.tick,
                "arousal_modifier": self.state.arousal * config["arousal_amplification"],
                "stability_penalty": config["stability_penalty_per_generation"] * self.state.rebloom_count,
                "generation": self.state.rebloom_count,
                "triggered_by": "rebloom_conditions"
            }
            
            self.bloom_system.spawn_bloom(bloom_data, pulse=self.pulse)
            
            if self.enable_narrative:
                self.narrative_history.append(f"💭 Rebloom triggered: generation {self.state.rebloom_count}")
                
            # Update state
            self.state.arousal = min(1.0, self.state.arousal * 1.1)
            self.state.entropy *= 0.9
            
    def _update_scup_momentum(self):
        """Track SCUP momentum and adjust system dynamics"""
        self.state.scup_momentum = self.state.scup - self.state.last_scup
        self.state.last_scup = self.state.scup
        
        config = self.config["scup"]
        
        if self.state.scup_momentum > config["rising_threshold"]:
            self.state.tracer_urgency *= (1 - config["urgency_impact"] * self.state.scup_momentum)
            if self.enable_narrative:
                self.narrative_history.append(f"📈 SCUP rising (Δ={self.state.scup_momentum:.3f})")
        elif self.state.scup_momentum < config["falling_threshold"]:
            self.state.tracer_urgency = min(1.0, self.state.tracer_urgency * 1.2)
            if self.enable_narrative:
                self.narrative_history.append(f"📉 SCUP falling")
                
    def _calculate_cascade_risk(self):
        """Calculate overall cascade risk from multiple factors"""
        config = self.config["cascade"]
        
        heat_risk = self.state.stasis_heat * config["heat_weight"]
        entropy_risk = self.state.entropy * config["entropy_weight"]
        drift_risk = self.state.drift_magnitude * config["drift_weight"]
        
        self.state.cascade_risk = heat_risk + entropy_risk + drift_risk
        
        if self.state.cascade_risk > config["critical_threshold"] and self.state.tick - self.reflex_cooldowns["heat_cascade"] > 50:
            if self.enable_narrative:
                self.narrative_history.append("🚨 CASCADE RISK CRITICAL")
            
            self.pulse.remove_heat(self.pulse.get_heat() * config["emergency_cooling_factor"], "cascade_prevention")
            self.state.stasis_heat *= (1 - config["emergency_cooling_factor"])
            self.reflex_cooldowns["heat_cascade"] = self.state.tick
            
    def _generate_tick_blooms(self, tick_id: int):
        """Generate multiple blooms per tick"""
        config = self.config.get("blooms", {})
        blooms_per_tick = config.get("per_tick", 5)
        
        for i in range(blooms_per_tick):
            pressure = config.get("pressure_base", 0.2) + i * config.get("pressure_increment", 0.1)
            activity = config.get("activity_base", 0.5) + i * config.get("activity_increment", 0.05)
            
            mood = self._calculate_bloom_mood(pressure)
            
            self.bloom_system.write_bloom(
                seed_id=f"tick-{tick_id}-bloom-{i}",
                mood=mood,
                tick=tick_id,
                semantic_pressure=pressure,
                seed_coord=[i, tick_id % 100],
                mood_prev=self.state.last_bloom_mood
            )
            
            self.state.last_bloom_mood = mood
            
    def _calculate_bloom_mood(self, current_pressure: float) -> str:
        """Calculate mood based on pressure"""
        config = self.config.get("mood", {})
        
        self.state.pressure_history.append(current_pressure)
        avg_pressure = sum(self.state.pressure_history) / len(self.state.pressure_history)
        
        if avg_pressure > config.get("stressed_threshold", 0.4):
            return "stressed"
        elif avg_pressure < config.get("calm_threshold", 0.2):
            return "calm"
        else:
            return "neutral"
            
    async def _trigger_autonomous_bloom(self, tick_id: int):
        """Trigger autonomous bloom generation"""
        config = self.config.get("autonomous_blooms", {})
        
        if not config.get("enabled", True):
            return
            
        frequency = config.get("frequency", 10)
        
        if tick_id % frequency != 0:
            return
            
        try:
            lineage_depth = (tick_id // frequency) % 5
            bloom_factor = 1.0 + ((tick_id % 30) / 10)
            entropy_score = config.get("base_entropy", 0.25) + ((tick_id % 7) * config.get("entropy_variance", 0.05))
            
            mood_config = config.get("moods", {})
            if tick_id % mood_config.get("reflective_frequency", 20) == 0:
                mood = "reflective"
            else:
                mood = mood_config.get("default_mood", "anxious")
                
            bloom_data = {
                "seed_id": f"auto-{tick_id}-{self.state.autonomous_bloom_count}",
                "lineage_depth": lineage_depth,
                "bloom_factor": bloom_factor,
                "entropy_score": entropy_score,
                "mood": mood,
                "triggered_by": "autonomous",
                "tick": tick_id,
                "system_state": {
                    "zone": self.state.current_zone,
                    "heat": self.pulse.get_heat(),
                    "scup": self.state.scup,
                    "drift": self.state.drift_magnitude
                }
            }
            
            logger.info(f"🌱 Autonomous bloom at tick {tick_id}")
            self.bloom_system.spawn_bloom(bloom_data, pulse=self.pulse)
            
            self.state.autonomous_bloom_count += 1
            self.state.last_autonomous_bloom_tick = tick_id
            
            if self.enable_narrative:
                self.narrative_history.append(f"🤖 Autonomous bloom '{bloom_data['seed_id']}' (mood: {mood})")
                
        except Exception as e:
            logger.error(f"Autonomous bloom error: {e}")
            
    async def _compute_adaptive_interval(self) -> Tuple[float, Dict[str, float]]:
        """Compute adaptive tick interval"""
        # Gather sensor inputs
        activity = await self.activity_sensor()
        pressure = await self.pressure_sensor()
        mood_pressure = await self.mood_sensor()
        
        # Get thermal state
        thermal_profile = self.pulse.get_thermal_profile()
        current_heat = thermal_profile['current_heat']
        stability = thermal_profile['stability_index']
        momentum = thermal_profile['thermal_momentum']
        
        # Update state
        self.state.pulse_heat = current_heat
        self.state.entropy = self._calculate_entropy_score()
        self.state.scup = self._calculate_scup()
        self.state.arousal = activity
        self.state.valence = mood_pressure - 0.5
        
        # Calculate tension
        heat_tension = self.state.stasis_heat * 0.2
        drift_tension = self.state.drift_magnitude * 0.3
        cascade_tension = self.state.cascade_risk * 0.5
        total_tension = heat_tension + drift_tension + cascade_tension
        
        # Base interval
        denominator = (1.0 + 
                      0.2 * activity + 
                      0.4 * pressure + 
                      0.3 * mood_pressure +
                      0.1 * total_tension)
        
        base_interval = self.base_interval / denominator
        
        # Apply momentum and stability
        momentum_factor = 1.0 + (momentum * 0.1)
        thermal_interval = base_interval / momentum_factor
        
        stability_factor = 0.8 + (stability * 0.4)
        final_interval = thermal_interval * stability_factor
        
        # Zone adjustments
        final_interval = self._apply_zone_adjustments(final_interval, current_heat, self.state.scup)
        
        # Clamp
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
        zone = self.pulse.classify()
        zone_config = self.config["zones"]
        
        if zone == "🔴 surge":
            surge_config = zone_config["surge"]
            urgency_multiplier = surge_config["interval_multiplier"] if scup >= self.config["scup"]["critical_scup"] else surge_config["interval_multiplier"] * 0.6
            return interval * urgency_multiplier
        elif zone == "🟢 calm":
            calm_config = zone_config["calm"]
            calm_multiplier = calm_config["interval_multiplier"] if scup > self.config["scup"]["stable_scup"] else calm_config["interval_multiplier"] * 0.8
            return interval * calm_multiplier
        else:
            active_config = zone_config["active"]
            return interval * active_config["interval_multiplier"]
            
    def _calculate_entropy_score(self) -> float:
        """Calculate current system entropy"""
        try:
            # Get entropy from schema
            base_entropy = 0.5
            try:
                # Try to get from schema if available
                drift_entropy = self.schema.get_total_drift_entropy()
                base_entropy = (base_entropy + drift_entropy) / 2
            except:
                pass
                
            # Add bloom entropy
            bloom_count = len(os.listdir("blooms")) if os.path.exists("blooms") else 0
            bloom_entropy = min(bloom_count / 20.0, 1.0) * 0.3
            total_entropy = base_entropy + bloom_entropy
            
            self.entropy_trend.append(total_entropy)
            return total_entropy
            
        except Exception as e:
            logger.warning(f"Entropy calculation error: {e}")
            return 0.5
            
    def _calculate_scup(self) -> float:
        """Calculate current SCUP"""
        try:
            scup = self.schema.compute_scup(
                tp_rar=0.8,  # Default alignment
                pressure_score=self.pulse.get_heat(),
                urgency_level=self.state.tracer_urgency,
                sigil_entropy=self.state.entropy,
                pulse=self.pulse,
                entropy_log=list(self.entropy_trend)
            )
            
            self.scup_trend.append(scup)
            return scup
            
        except Exception as e:
            logger.warning(f"SCUP calculation error: {e}")
            return 0.5
            
    def _update_zone_tracking(self, zone: str):
        """Update zone timing and transitions"""
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
            logger.info(f"🔄 Zone transition: {zone}")
        else:
            self.state.zone_timer[zone] += 1
            
    async def _execute_zone_reflexes(self, zone: str, scup: float, entropy_score: float):
        """Execute zone-specific reflexes"""
        current_tick = self.state.tick
        zone_config = self.config["zones"]
        scup_config = self.config["scup"]
        
        if zone == "🟢 calm":
            calm_config = zone_config["calm"]
            if (self.state.zone_timer[zone] >= calm_config["synthesis_threshold"] and 
                current_tick - self.reflex_cooldowns["synthesis"] > 50):
                logger.info("🧠 Sustained calm — triggering synthesis")
                self.reflex_cooldowns["synthesis"] = current_tick
                
        elif zone == "🟡 active":
            active_config = zone_config["active"]
            if (self.state.zone_timer[zone] % active_config["entropy_scan_interval"] == 0 and 
                current_tick - self.reflex_cooldowns["entropy_scan"] > 25):
                logger.info("🔍 Active mode — entropy scan")
                self.reflex_cooldowns["entropy_scan"] = current_tick
                
        elif zone == "🔴 surge":
            surge_config = zone_config["surge"]
            if (self.state.zone_timer[zone] >= surge_config["emergency_threshold"] and 
                current_tick - self.reflex_cooldowns["emergency_suppression"] > 40):
                logger.info("🚨 Surge pressure — emergency response")
                self.reflex_cooldowns["emergency_suppression"] = current_tick
                
        # Cross-zone reflexes
        if scup < scup_config["critical_scup"]:
            logger.warning(f"⚠️ SCUP critical: {scup:.3f}")
            
    async def start(self):
        """Start the tick engine"""
        logger.info("🚀 Starting ConsolidatedTickEngine")
        self._running = True
        
        while self._running:
            try:
                # Update experimental dynamics
                self._update_heat_engine()
                self._update_drift_mechanics()
                self._check_rebloom_conditions()
                self._update_scup_momentum()
                self._calculate_cascade_risk()
                
                # Compute adaptive interval
                interval, debug_metrics = await self._compute_adaptive_interval()
                
                # Update thermal system
                pressure_val = await self.pressure_sensor()
                self.pulse.update(pressure_val)
                
                # Get zone and update
                zone = self.pulse.classify()
                self._update_zone_tracking(zone)
                
                # Execute reflexes
                await self._execute_zone_reflexes(zone, self.state.scup, self.state.entropy)
                
                # Update schema
                self.schema.update_schema_health(self.state.scup)
                
                # Emit tick
                tick_id = self._emit_tick(zone=zone, pulse_heat=round(self.pulse.get_heat(), 3))
                
                # Generate blooms
                self._generate_tick_blooms(tick_id)
                
                # Trigger autonomous blooms
                await self._trigger_autonomous_bloom(tick_id)
                
                # Log metrics
                self._log_tick_metrics(tick_id, zone, interval, debug_metrics)
                
                # Perform maintenance
                self._perform_maintenance_cycles(tick_id)
                
                # Save state
                self._save_state()
                
                # Update interval tracking
                self.last_interval = interval
                
                # Wait
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                await asyncio.sleep(max(1.0, self.base_interval))
                
    def stop(self):
        """Stop the tick engine"""
        logger.info("🛑 Stopping ConsolidatedTickEngine")
        self._running = False
        self._save_state()
        
    def _log_tick_metrics(self, tick_id: int, zone: str, interval: float, debug_metrics: Dict[str, float]):
        """Log comprehensive tick metrics"""
        try:
            self.interval_history.append(interval)
            
            # Log to CSV
            os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
            with open("juliet_flowers/cluster_report/interval_log.csv", "a") as f:
                f.write(f"{interval:.3f}\n")
                
            # Periodic detailed logging
            if tick_id % 10 == 0:
                logger.info(f"\n📊 Tick {tick_id} Metrics:")
                logger.info(f"  Zone: {zone} | Heat: {debug_metrics['current_heat']:.3f} | SCUP: {debug_metrics['scup']:.3f}")
                logger.info(f"  Interval: {interval:.3f}s | Stability: {debug_metrics['stability']:.3f}")
                logger.info(f"  Entropy: {debug_metrics['entropy_score']:.3f} | Cascade Risk: {self.state.cascade_risk:.3f}")
                
        except Exception as e:
            logger.error(f"Logging error: {e}")
            
    def _perform_maintenance_cycles(self, tick_id: int):
        """Perform periodic maintenance"""
        maintenance = self.config["maintenance"]
        
        try:
            if tick_id % maintenance["shi_check_interval"] == 0:
                logger.info("🧬 Schema health check")
                
            if self.state.zone_timer.get("🟢 calm", 0) % maintenance["memory_decay_interval"] == 0:
                logger.debug("Memory decay cycle")
                
            if tick_id % maintenance["bloom_sweep_interval"] == 0:
                logger.info("🧺 Bloom sweep")
                
        except Exception as e:
            logger.error(f"Maintenance error: {e}")
            
    def get_current_tick(self) -> int:
        """Get current tick value"""
        return self.state.tick
        
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
            'thermal_profile': self.pulse.get_thermal_profile(),
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
                'last_tick': self.state.last_autonomous_bloom_tick
            }
        }


# ============================================================================
# INTEGRATION BRIDGE FOR DAWN
# ============================================================================

class DAWNIntegrationBridge:
    """Bridge for integrating with DAWN consciousness system"""
    
    def __init__(self, dawn_consciousness=None):
        self.dawn = dawn_consciousness
        self.tick_engine: Optional[ConsolidatedTickEngine] = None
        self.engine_thread = None
        self.engine_loop = None
        
    async def activity_sensor(self) -> float:
        """Convert DAWN activity to tick engine metric"""
        if self.dawn:
            try:
                scup = self.dawn.schema_state.get('scup', 0.5)
                arousal = self.dawn.mood_state.get('arousal', 0.5)
                return (scup + arousal) / 2.0
            except:
                pass
        return 0.5
        
    async def pressure_sensor(self) -> float:
        """Convert DAWN pressure to tick engine metric"""
        if self.dawn:
            try:
                import builtins
                pulse = getattr(builtins, 'pulse', None)
                if pulse:
                    current_heat = pulse.get_heat()
                    heat_capacity = getattr(pulse, 'heat_capacity', 10.0)
                    return min(1.0, current_heat / heat_capacity)
            except:
                pass
        return 0.0
        
    async def mood_sensor(self) -> float:
        """Convert DAWN mood to tick engine metric"""
        if self.dawn:
            try:
                valence = self.dawn.mood_state.get('valence', 0.5)
                return valence
            except:
                pass
        return 0.5
        
    async def tick_event_handler(self, event: TickEvent):
        """Handle tick events from the engine"""
        if self.dawn:
            try:
                self.dawn.tick_count += 1
                
                if self.tick_engine and hasattr(self.tick_engine, 'state'):
                    engine_state = self.tick_engine.state
                    self.dawn.schema_state['entropy_index'] = engine_state.entropy
                    self.dawn.schema_state['tension'] = engine_state.cascade_risk
                    self.dawn.mood_state['valence'] = engine_state.valence
                    self.dawn.mood_state['arousal'] = engine_state.arousal
                    
            except Exception as e:
                logger.error(f"Integration event handler error: {e}")
                
    def start_integrated_engine(self, **kwargs):
        """Start tick engine integrated with DAWN"""
        logger.info("Starting integrated tick engine...")
        
        self.tick_engine = ConsolidatedTickEngine(
            activity_sensor=self.activity_sensor,
            pressure_sensor=self.pressure_sensor,
            mood_sensor=self.mood_sensor,
            **kwargs
        )
        
        self.tick_engine.add_event_listener(self.tick_event_handler)
        
        def run_engine():
            self.engine_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.engine_loop)
            
            try:
                self.engine_loop.run_until_complete(self.tick_engine.start())
            except Exception as e:
                logger.error(f"Engine thread error: {e}")
            finally:
                self.engine_loop.close()
                
        self.engine_thread = threading.Thread(
            target=run_engine,
            name="TickEngineThread",
            daemon=True
        )
        self.engine_thread.start()
        
        logger.info("✅ Integrated tick engine started")
        
    def stop_integrated_engine(self):
        """Stop integrated engine"""
        if self.tick_engine:
            logger.info("Stopping integrated engine...")
            self.tick_engine.stop()
            
            if self.engine_loop:
                self.engine_loop.call_soon_threadsafe(self.engine_loop.stop)
                
            if self.engine_thread:
                self.engine_thread.join(timeout=5.0)
                
            logger.info("✅ Integrated engine stopped")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def run_standalone(args):
    """Run tick engine in standalone mode"""
    print("\n" + "="*60)
    print("🚀 DAWN CONSOLIDATED TICK ENGINE v3.0")
    print("="*60 + "\n")
    
    # Create engine
    engine = ConsolidatedTickEngine(
        base_interval=args.interval,
        config_path=args.config,
        enable_narrative=args.narrative
    )
    
    # Display configuration
    print("📋 Configuration:")
    print(f"  - Base interval: {args.interval}s")
    print(f"  - Config file: {args.config}")
    print(f"  - Narrative: {'Enabled' if engine.enable_narrative else 'Disabled'}")
    print(f"  - Starting tick: {engine.get_current_tick()}")
    print()
    
    # Add example event listener
    async def log_tick_event(event: TickEvent):
        if event.tick_id % 20 == 0:
            print(f"\n📌 Event: Tick {event.tick_id} | Zone: {event.zone} | Interval: {event.interval:.3f}s")
            
    engine.add_event_listener(log_tick_event)
    
    print("Press Ctrl+C to stop...\n")
    
    try:
        await engine.start()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutdown requested...")
        engine.stop()
        
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
        

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DAWN Consolidated Tick Engine")
    parser.add_argument("--interval", type=float, default=1.0, help="Base tick interval in seconds")
    parser.add_argument("--config", type=str, default="tick_engine_config.json", help="Configuration file path")
    parser.add_argument("--narrative", action="store_true", help="Enable narrative logging")
    parser.add_argument("--no-narrative", dest="narrative", action="store_false", help="Disable narrative logging")
    parser.set_defaults(narrative=None)
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_standalone(args))
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()