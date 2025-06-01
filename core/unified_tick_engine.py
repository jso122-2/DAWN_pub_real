"""
Unified DAWN Tick Engine
Merges production architecture with experimental dynamics
"""

from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
import sys, os
import asyncio
import time
import math
import json
from typing import Dict, List, Optional, Callable, Tuple
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime

# Ensure proper path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Core system imports
from core.event_bus import TickEvent
from core.tick_hook_autonomous import AutonomousFieldTrigger
from core.tick_emitter import emit_tick

# Unified Pulse Heat System
from pulse.pulse_field_logger import log_field_snapshot

# Schema and semantic systems
from semantic.sigil_ring import decay_all_sigils, age_all_sigils
from persephone.lifecycle import fade_sigils, soft_seal_bloom, prune_dead_branches
from persephone.sigil_decay import expire_ephemeral_sigils

# Analysis and monitoring
from core.scup import compute_scup, classify_scup_zone, log_scup
from schema.schema_health_index import calculate_SHI, update_schema_health
from schema.schema_decay_handler import decay_schema_memory
from schema.mood_urgency_probe import mood_urgency_probe
from schema.alignment_probe import current_alignment_probe
from owl.entropy_tracker import get_entropy_score
from semantic.vector_drift_analyzer import compute_drift_score

# Reflex and response systems
from owl.trigger_logic import owl_visual_reflex
from core.visual_reflex_launcher import launch_reflex
from owl.owl_drift_sentinel import owl_drift_check
from schema.dawn_claude_logs import log_claude_voice
from schema.mythic_mode import propose_code_patch
from schema.pressure_reflex import pressure_reflex

# Bloom and rebloom systems
from schema.rebloom_queue import pop_rebloom_candidate
from bloom.spawn_bloom import spawn_bloom
from bloom.juliet_flower import trigger_synthesis, load_all_blooms

# Visualization and analysis
from field_entropy_map import render_entropy_field
from owl.owl_tracer_log import owl_log
from owl.lineage_log import log_rebloom_lineage
from owl.owl_auditor import run_entropy_scan

# Memory and storage systems
from codex.sigil_memory_ring import sigil_memory_ring, get_active_sigil_entropy_list
from core.cognitive_trace import attach_cognitive_trace, CognitiveTraceGenerator


@dataclass
class UnifiedCognitiveState:
    """Unified cognitive state combining both approaches"""
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
    
    def __post_init__(self):
        if self.drift_vector is None:
            self.drift_vector = [0.0, 0.0, 0.0]
        if self.tracer_zones is None:
            self.tracer_zones = ["stable"]
        if self.zone_timer is None:
            self.zone_timer = {"🟢 calm": 0, "🟡 active": 0, "🔴 surge": 0}


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
    """
    
    def __init__(self, base_interval: float = 1.0, 
                 activity_sensor: Optional[Callable] = None,
                 pressure_sensor: Optional[Callable] = None,
                 mood_sensor: Optional[Callable] = None,
                 gas_pedal: Optional[Callable] = None,
                 emit_tick_event: Optional[Callable] = None,
                 enable_narrative: bool = True):
        
        # Core timing configuration
        self.base_interval = base_interval
        self.last_interval = base_interval
        
        # Sensor configuration
        self.activity_sensor = activity_sensor
        self.pressure_sensor = pressure_sensor
        self.mood_sensor = mood_sensor
        self.gas_pedal = gas_pedal
        self.emit_tick_event = emit_tick_event
        self.cognitive_trace = CognitiveTraceGenerator()
        self.enable_cognitive_trace = True
        self.enable_narrative = enable_narrative
        
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
        self.narrative_history = deque(maxlen=100)
        
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
        
        # Configuration
        self.config = self._load_config()
        
        # Autonomous systems
        self.tick_hook = None
        self._running = False
        
        # Initialize state files
        self._init_state_files()
        
        print(f"[UnifiedTickEngine] 🎯 Initialized | Base interval: {base_interval}s | Narrative: {enable_narrative}")
    
    def _load_config(self) -> Dict:
        """Load configuration from file or use defaults"""
        try:
            with open("tick_engine_config.json", "r") as f:
                return json.load(f)
        except:
            # Default configuration
            return {
                "heat": {
                    "stasis_threshold": 0.1,
                    "generation_base": 0.02,
                    "dissipation_base": 0.1,
                    "critical_threshold": 0.85
                },
                "rebloom": {
                    "entropy_threshold": 0.45,
                    "valence_threshold": 0.2,
                    "cooldown_ticks": 30
                },
                "drift": {
                    "arousal_factor": 0.1,
                    "decay_rate": 0.05,
                    "alignment_impact": 0.8
                },
                "scup": {
                    "momentum_weight": 0.3,
                    "urgency_impact": 0.5
                },
                "cascade": {
                    "heat_weight": 0.4,
                    "entropy_weight": 0.3,
                    "drift_weight": 0.3
                }
            }
    
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
    
    def _save_state(self):
        """Save current state to file"""
        state_dict = asdict(self.state)
        state_dict["timestamp"] = datetime.now().isoformat()
        
        with open("cognitive_states/cognitive_state.json", "w") as f:
            json.dump(state_dict, f, indent=2)
    
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
        if self.state.arousal > 0.5 or abs(self.state.valence) > 0.5:
            # Add directional drift
            drift_x = self.state.valence * config["arousal_factor"]
            drift_y = self.state.arousal * config["arousal_factor"]
            drift_z = (self.state.entropy - 0.5) * config["arousal_factor"]
            
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
                new_data["arousal_modifier"] = self.state.arousal * 1.2
                new_data["stability_penalty"] = 0.1 * self.state.rebloom_count
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
        if self.state.scup_momentum > 0.02:
            # SCUP rising - reduce urgency
            self.state.tracer_urgency *= (1 - config["urgency_impact"] * self.state.scup_momentum)
            if self.enable_narrative:
                self.narrative_history.append(f"📈 SCUP rising (Δ={self.state.scup_momentum:.3f}). System stabilizing.")
        elif self.state.scup_momentum < -0.02:
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
        
        if self.state.cascade_risk > 0.8 and self.state.tick - self.reflex_cooldowns["heat_cascade"] > 50:
            # Trigger cascade prevention
            if self.enable_narrative:
                self.narrative_history.append("🚨 CASCADE RISK CRITICAL - Emergency measures activated")
            
            # Emergency cooling
            pulse.remove_heat(pulse.heat * 0.3, "cascade_prevention")
            self.state.stasis_heat *= 0.5
            self.reflex_cooldowns["heat_cascade"] = self.state.tick
    
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
        
        if zone == "🔴 surge":
            urgency_multiplier = 0.3 if scup < 0.4 else 0.5
            return interval * urgency_multiplier
        elif zone == "🟢 calm":
            calm_multiplier = 1.5 if scup > 0.7 else 1.2
            return interval * calm_multiplier
        else:
            if heat > pulse.heat_capacity * 0.6:
                return interval * 0.8
            else:
                return interval * 1.1
    
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
        if not self.enable_narrative:
            return
            
        try:
            with open("cognitive_states/narrative_log.txt", "a", encoding="utf-8") as f:
                for narrative in list(self.narrative_history)[-10:]:  # Last 10 entries
                    f.write(f"{narrative}\n")
                self.narrative_history.clear()
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Narrative log error: {e}")
    
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
                
                # Execute zone reflexes (from original implementation)
                await self._execute_zone_reflexes(zone, self.state.scup, self.state.entropy)
                
                # Update schema health
                update_schema_health(self.state.scup)
                pulse.adjust_urgency(self.state.scup)
                
                # Emit tick event
                tick_id = emit_tick(zone=zone, pulse=round(pulse.heat, 3))
                
                # Run drift sentinel
                drift_result = owl_drift_check(tick_id=tick_id)
                if drift_result == "override_suppression":
                    print(f"[UnifiedTickEngine] 🚫 Drift sentinel override at tick {tick_id}")
                    pulse.override_active = True
                    launch_reflex("suppression_override")
                
                # Execute tick hook if available
                if self.tick_hook:
                    await self.tick_hook(tick_id=tick_id)
                
                # Emit tick event to other systems
                if self.emit_tick_event:
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
                await asyncio.sleep(1.0)
    
    def stop(self):
        """Stop the unified tick engine"""
        print("[UnifiedTickEngine] 🛑 Stopping unified engine")
        self._running = False
        self._write_narrative_log()
        self._save_state()
    
    # Include all the helper methods from the original implementation
    async def _execute_zone_reflexes(self, zone: str, scup: float, entropy_score: float):
        """Execute zone-specific reflexes and responses"""
        current_tick = self.state.tick
        
        if zone == "🟢 calm":
            if (self.state.zone_timer[zone] >= 20 and 
                current_tick - self.reflex_cooldowns["synthesis"] > 50):
                
                print("[UnifiedTickEngine] 🧠 Sustained calm — triggering Juliet synthesis")
                await self._trigger_synthesis()
                self.reflex_cooldowns["synthesis"] = current_tick
            
            if (self.state.zone_timer[zone] >= 15 and 
                current_tick - self.reflex_cooldowns["rebloom_queue"] > 30):
                
                print("[UnifiedTickEngine] 🪴 Calm zone — processing rebloom queue")
                await self._process_rebloom_queue()
                self.reflex_cooldowns["rebloom_queue"] = current_tick
        
        elif zone == "🟡 active":
            if (self.state.zone_timer[zone] % 30 == 0 and 
                current_tick - self.reflex_cooldowns["entropy_scan"] > 25):
                
                print("[UnifiedTickEngine] 🔍 Active mode — entropy scan")
                await self._trigger_entropy_scan()
                self.reflex_cooldowns["entropy_scan"] = current_tick
        
        elif zone == "🔴 surge":
            if (self.state.zone_timer[zone] >= 10 and 
                current_tick - self.reflex_cooldowns["emergency_suppression"] > 40):
                
                print("[UnifiedTickEngine] 🚨 Surge pressure — emergency response")
                await self._trigger_emergency_response(scup)
                self.reflex_cooldowns["emergency_suppression"] = current_tick
        
        if scup < 0.3:
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
            
            with open("juliet_flowers/cluster_report/zone_overlay_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{tick_id},{zone},{debug_metrics['current_heat']:.3f}\n")
            
            if tick_id % 10 == 0:
                print(f"\n[UnifiedTickEngine] 📊 Tick {tick_id} Metrics:")
                print(f"  Zone: {zone} | Heat: {debug_metrics['current_heat']:.3f} | SCUP: {debug_metrics['scup']:.3f}")
                print(f"  Interval: {interval:.3f}s | Stability: {debug_metrics['stability']:.3f}")
                print(f"  Entropy: {debug_metrics['entropy_score']:.3f} | Cascade Risk: {self.state.cascade_risk:.3f}")
                print(f"  Drift: {self.state.drift_magnitude:.3f} | Stasis Heat: {self.state.stasis_heat:.3f}")
            
            if self.enable_cognitive_trace:
                active_sigils = []
                try:
                    from codex.sigil_memory_ring import sigil_memory_ring
                    active_sigils = [s.name for s in sigil_memory_ring.values() 
                                    if hasattr(s, 'name') and s.entropy < 0.9][:6]
                except:
                    pass
                
                tick_data = {
                    'tick': tick_id,
                    'zone': zone,
                    'pulse_heat': debug_metrics['current_heat'],
                    'entropy': debug_metrics['entropy_score'],
                    'scup': debug_metrics['scup'],
                    'schema_health': debug_metrics.get('schema_health', 1.0),
                    'active_sigils': active_sigils,
                    'bloom_count': self.state.rebloom_count,
                    'drift_magnitude': self.state.drift_magnitude
                }
                
                snapshot = self.cognitive_trace.process_tick(tick_data)
                print(f"\n💭 {snapshot.commentary}")
                
                if tick_id % 10 == 0:
                    self.cognitive_trace.save_trace(snapshot)

        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Logging error: {e}")
    
    def _perform_maintenance_cycles(self, tick_id: int):
        """Perform periodic maintenance and cleanup"""
        try:
            if tick_id % 25 == 0:
                shi = calculate_SHI(
                    pulse.heat,
                    len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                        if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0,
                    len(os.listdir("juliet_flowers/sealed")) if os.path.exists("juliet_flowers/sealed") else 0,
                    [sigil.entropy for sigil in sigil_memory_ring.values() if hasattr(sigil, 'entropy')]
                )
                print(f"[UnifiedTickEngine] 🧬 Schema Health Index: {shi:.3f}")
            
            if self.state.zone_timer.get("🟢 calm", 0) % 10 == 0:
                decay_schema_memory()
            
            if tick_id % 15 == 0:
                decay_all_sigils()
                age_all_sigils()
            
            if tick_id % 20 == 0:
                fade_sigils()
                expire_ephemeral_sigils()
                prune_dead_branches()
            
            if tick_id % 50 == 0:
                print("[UnifiedTickEngine] 🧺 Scheduled bloom sweep")
                for bloom in load_all_blooms():
                    soft_seal_bloom(bloom)
            
            if tick_id % 75 == 0:
                render_entropy_field()
        
        except Exception as e:
            print(f"[UnifiedTickEngine] ⚠️ Maintenance error: {e}")
    
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
            }
        }


# Factory function for easy initialization
def create_unified_tick_engine(base_interval: float = 1.0, 
                              activity_sensor: Optional[Callable] = None,
                              pressure_sensor: Optional[Callable] = None,
                              mood_sensor: Optional[Callable] = None,
                              enable_narrative: bool = True) -> UnifiedTickEngine:
    """Create and configure a unified tick engine"""
    engine = UnifiedTickEngine(
        base_interval=base_interval,
        activity_sensor=activity_sensor,
        pressure_sensor=pressure_sensor,
        mood_sensor=mood_sensor,
        enable_narrative=enable_narrative
    )
    
    trigger = AutonomousFieldTrigger()
    engine.tick_hook = trigger.on_tick
    
    return engine


# Global engine instance
engine = create_unified_tick_engine()
cognitive_hook = attach_cognitive_trace(engine)

print("[UnifiedTickEngine] ✨ Unified TickEngine with experimental dynamics loaded")