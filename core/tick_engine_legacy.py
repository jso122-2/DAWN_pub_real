from helix_import_architecture import helix_import
from substrate import pulse_heat
import sys, os
import asyncio
import time
import math
from typing import Dict, List, Optional, Callable, Tuple
from collections import deque

# Ensure proper path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Core system imports - organized and clean
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


class RefinedTickEngine:
    """
    Refined TickEngine with clean integration to UnifiedPulseHeat.
    
    This orchestrates the entire system's temporal dynamics:
    - Thermal regulation through PulseHeat
    - Adaptive tick intervals based on system state
    - Zone-based reflexes and responses
    - Memory decay and bloom lifecycle management
    - Entropy tracking and SCUP monitoring
    """
    
    def __init__(self, base_interval: float = 1.0, 
                 activity_sensor: Optional[Callable] = None,
                 pressure_sensor: Optional[Callable] = None,
                 mood_sensor: Optional[Callable] = None,
                 gas_pedal: Optional[Callable] = None,
                 emit_tick_event: Optional[Callable] = None):
        
        # Core timing configuration
        self.base_interval = base_interval
        self.last_interval = base_interval
        
        # Sensor configuration with weights
        self.activity_sensor = activity_sensor
        self.pressure_sensor = pressure_sensor
        self.mood_sensor = mood_sensor
        self.gas_pedal = gas_pedal
        self.emit_tick_event = emit_tick_event
        self.cognitive_trace = CognitiveTraceGenerator()
        self.enable_cognitive_trace = True
        # Adaptive coefficients
        self.alpha = 0.2    # Activity sensitivity
        self.beta = 0.4     # Pressure sensitivity  
        self.gamma = 0.3    # Mood sensitivity
        self.delta = 0.1    # Entropy sensitivity
        
        # State tracking
        self.entropy_trend = deque(maxlen=50)
        self.scup_trend = deque(maxlen=30)
        self.interval_history = deque(maxlen=100)
        
        # Zone timing and state
        self.zone_timer = {
            "🟢 calm": 0,
            "🟡 active": 0,
            "🔴 surge": 0
        }
        self.current_zone = None
        self.zone_transitions = []
        
        # Reflex timing
        self.reflex_cooldowns = {
            "synthesis": 0,
            "entropy_scan": 0,
            "emergency_suppression": 0,
            "rebloom_queue": 0
        }
        
        # Autonomous systems
        self.tick_hook = None
        self._running = False
        
        print(f"[TickEngine] 🎯 Refined engine initialized | Base interval: {base_interval}s")
    
    async def _compute_adaptive_interval(self) -> Tuple[float, Dict[str, float]]:
        """
        Compute adaptive tick interval based on multiple system inputs.
        
        Returns:
            Tuple of (interval, debug_metrics)
        """
        # Gather sensor inputs
        activity = await self.activity_sensor() if self.activity_sensor else 0.5
        pressure = await self.pressure_sensor() if self.pressure_sensor else 0.0
        mood_pressure = await self.mood_sensor() if self.mood_sensor else 0.0
        
        # Get current thermal state
        thermal_profile = pulse.get_thermal_profile()
        current_heat = thermal_profile['current_heat']
        stability = thermal_profile['stability_index']
        momentum = thermal_profile['thermal_momentum']
        
        # Calculate entropy component
        entropy_score = self._calculate_entropy_score()
        
        # Get SCUP for system coherence
        scup = self._calculate_scup()
        
        # Compute tension factor (inverse of system stability)
        coherence_tension = (1.0 - scup) * 0.5
        thermal_tension = (current_heat / pulse.heat_capacity) * 0.3
        entropy_tension = entropy_score * 0.2
        total_tension = coherence_tension + thermal_tension + entropy_tension
        
        # Base interval calculation with multi-factor weighting
        denominator = (1.0 + 
                      self.alpha * activity + 
                      self.beta * pressure + 
                      self.gamma * mood_pressure +
                      self.delta * total_tension)
        
        base_interval = self.base_interval / denominator
        
        # Apply thermal momentum adjustment
        momentum_factor = 1.0 + (momentum * 0.1)
        thermal_interval = base_interval / momentum_factor
        
        # Apply stability smoothing
        stability_factor = 0.8 + (stability * 0.4)  # Range: 0.8 - 1.2
        final_interval = thermal_interval * stability_factor
        
        # Apply bounds and zone-specific adjustments
        final_interval = self._apply_zone_adjustments(final_interval, current_heat, scup)
        
        # Clamp to reasonable bounds
        final_interval = max(0.1, min(final_interval, 5.0))
        
        # Debug metrics
        debug_metrics = {
            'activity': activity,
            'pressure': pressure,
            'mood_pressure': mood_pressure,
            'entropy_score': entropy_score,
            'scup': scup,
            'current_heat': current_heat,
            'stability': stability,
            'momentum': momentum,
            'total_tension': total_tension,
            'base_interval': base_interval,
            'thermal_interval': thermal_interval,
            'final_interval': final_interval
        }
        
        return final_interval, debug_metrics
    
    def _apply_zone_adjustments(self, interval: float, heat: float, scup: float) -> float:
        """Apply zone-specific interval adjustments."""
        zone = pulse.classify()
        
        if zone == "🔴 surge":
            # High urgency - faster ticks, especially if SCUP is low
            urgency_multiplier = 0.3 if scup < 0.4 else 0.5
            return interval * urgency_multiplier
        elif zone == "🟢 calm":
            # Low urgency - slower ticks if stable
            calm_multiplier = 1.5 if scup > 0.7 else 1.2
            return interval * calm_multiplier
        else:  # Active zone
            # Moderate adjustment based on heat level
            if heat > pulse.heat_capacity * 0.6:
                return interval * 0.8  # Slightly faster
            else:
                return interval * 1.1  # Slightly slower
    
    def _calculate_entropy_score(self) -> float:
        """Calculate current system entropy score."""
        try:
            # Get sigil entropy
            sigil_entropy_list = get_active_sigil_entropy_list()
            raw_entropy = sum(sigil_entropy_list) / len(sigil_entropy_list) if sigil_entropy_list else 0.0
            
            # Add system entropy factors
            bloom_count = len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                              if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0
            
            # Normalize bloom entropy (more blooms = more entropy up to a point)
            bloom_entropy = min(bloom_count / 20.0, 1.0) * 0.3
            
            # Combine entropy sources
            total_entropy = raw_entropy + bloom_entropy
            
            # Update trend
            self.entropy_trend.append(total_entropy)
            
            return total_entropy
            
        except Exception as e:
            print(f"[TickEngine] ⚠️ Entropy calculation error: {e}")
            return 0.5  # Default entropy
    
    def _calculate_scup(self) -> float:
        """Calculate current SCUP (Semantic Coherence Under Pressure)."""
        try:
            # Get current system state
            tp_rar = current_alignment_probe(None)
            pressure_score = pulse.heat
            urgency_level = mood_urgency_probe(None)
            
            # Get sigil entropy
            sigil_entropy_list = get_active_sigil_entropy_list()
            current_sigil_entropy = sum(sigil_entropy_list) / len(sigil_entropy_list) if sigil_entropy_list else 0.0
            
            # Calculate SCUP
            scup = compute_scup(
                tp_rar=tp_rar,
                pressure_score=pressure_score,
                urgency_level=urgency_level,
                sigil_entropy=current_sigil_entropy,
                pulse=pulse,
                entropy_log=list(self.entropy_trend)
            )
            
            # Update trend
            self.scup_trend.append(scup)
            
            return scup
            
        except Exception as e:
            print(f"[TickEngine] ⚠️ SCUP calculation error: {e}")
            return 0.5  # Default SCUP
    
    def _update_zone_tracking(self, zone: str):
        """Update zone timing and transition tracking."""
        if zone != self.current_zone:
            # Record zone transition
            self.zone_transitions.append((pulse.tick_count, zone))
            if len(self.zone_transitions) > 100:
                self.zone_transitions.pop(0)  # Keep recent history
            
            # Reset timers for other zones, increment current
            for z in self.zone_timer:
                if z == zone:
                    self.zone_timer[z] += 1
                else:
                    self.zone_timer[z] = 0
            
            self.current_zone = zone
            print(f"[TickEngine] 🔄 Zone transition: {zone}")
        else:
            self.zone_timer[zone] += 1
    
    async def _execute_zone_reflexes(self, zone: str, scup: float, entropy_score: float):
        """Execute zone-specific reflexes and responses."""
        current_tick = pulse.tick_count
        
        # Calm zone reflexes
        if zone == "🟢 calm":
            if (self.zone_timer[zone] >= 20 and 
                current_tick - self.reflex_cooldowns["synthesis"] > 50):
                
                print("[TickEngine] 🧠 Sustained calm — triggering Juliet synthesis")
                await self._trigger_synthesis()
                self.reflex_cooldowns["synthesis"] = current_tick
            
            if (self.zone_timer[zone] >= 15 and 
                current_tick - self.reflex_cooldowns["rebloom_queue"] > 30):
                
                print("[TickEngine] 🪴 Calm zone — processing rebloom queue")
                await self._process_rebloom_queue()
                self.reflex_cooldowns["rebloom_queue"] = current_tick
        
        # Active zone reflexes
        elif zone == "🟡 active":
            if (self.zone_timer[zone] % 30 == 0 and 
                current_tick - self.reflex_cooldowns["entropy_scan"] > 25):
                
                print("[TickEngine] 🔍 Active mode — entropy scan")
                await self._trigger_entropy_scan()
                self.reflex_cooldowns["entropy_scan"] = current_tick
        
        # Surge zone reflexes
        elif zone == "🔴 surge":
            if (self.zone_timer[zone] >= 10 and 
                current_tick - self.reflex_cooldowns["emergency_suppression"] > 40):
                
                print("[TickEngine] 🚨 Surge pressure — emergency response")
                await self._trigger_emergency_response(scup)
                self.reflex_cooldowns["emergency_suppression"] = current_tick
        
        # Cross-zone reflexes based on metrics
        if scup < 0.3:
            launch_reflex("scup_alert")
            owl_log(f"⚠️ SCUP critical: {scup:.3f} at tick {current_tick}")
        
        if entropy_score > 0.6:
            launch_reflex("entropy_spike")
        
        # Mood-based reflexes
        try:
            mood_pressure = await self.mood_sensor() if self.mood_sensor else 0.0
            if mood_pressure > 0.5:
                launch_reflex("mood_heatmap")
        except Exception as e:
            print(f"[TickEngine] ⚠️ Mood reflex error: {e}")
    
    async def _trigger_synthesis(self):
        """Trigger Juliet synthesis process."""
        try:
            trigger_synthesis()
        except Exception as e:
            print(f"[TickEngine] ❌ Synthesis trigger error: {e}")
    
    async def _process_rebloom_queue(self):
        """Process pending rebloom candidates."""
        try:
            bloom = pop_rebloom_candidate()
            if not bloom:
                return
            
            # Prepare rebloom data
            ancestry = getattr(bloom, "rebloom_tag", f"rebloomed-{bloom.seed_id}")
            new_data = bloom.to_dict()
            new_data["ancestry_tag"] = ancestry
            new_data["lineage_depth"] = getattr(bloom, "lineage_depth", 0) + 1
            new_data["rebloomed_by"] = "RefinedTickEngine"
            
            print(f"[TickEngine] 🌱 Reblooming {bloom.seed_id} → new instance")
            owl_log(f"[Rebloom] 🔄 {bloom.seed_id} rebloomed with ancestry: {ancestry}")
            
            # Log lineage
            log_rebloom_lineage(bloom.seed_id, ancestry)
            
            # Spawn new bloom
            spawn_bloom(new_data)
            
        except Exception as e:
            print(f"[TickEngine] ❌ Rebloom processing error: {e}")
    
    async def _trigger_entropy_scan(self):
        """Trigger entropy analysis scan."""
        try:
            run_entropy_scan()
        except Exception as e:
            print(f"[TickEngine] ❌ Entropy scan error: {e}")
    
    async def _trigger_emergency_response(self, scup: float):
        """Trigger emergency response for surge conditions."""
        try:
            # Apply penalties to high-stress seeds
            stress_seeds = ["A1", "C3", "D4"]  # Configure as needed
            for seed in stress_seeds:
                pulse.apply_penalty(seed, 0.8)
            
            # If SCUP is critically low, propose system patches
            if scup < 0.25:
                proposed_patch = '''
def emergency_stabilization(self, scup_score):
    """Emergency stabilization when SCUP drops critically low."""
    if scup_score < 0.25:
        # Reduce heat aggressively
        pulse.remove_heat(pulse.heat * 0.3, "emergency_cooling")
        # Boost stability
        pulse.thermal_momentum *= 0.5
        return True
    return False
'''
                commentary = f"SCUP critical at {scup:.3f}. Emergency stabilization needed."
                propose_code_patch("tick_engine", "emergency_stabilization", 
                                 proposed_patch, commentary)
        
        except Exception as e:
            print(f"[TickEngine] ❌ Emergency response error: {e}")
    
    def _log_tick_metrics(self, tick_id: int, zone: str, interval: float, 
                         debug_metrics: Dict[str, float]):
        """Log comprehensive tick metrics."""
        try:
            # Update interval history
            self.interval_history.append(interval)
            
            # Log field snapshot
            log_field_snapshot(
                tick_id=tick_id,
                zone=zone,
                pulse_heat=debug_metrics['current_heat'],
                scup_score=debug_metrics['scup'],
                entropy_score=debug_metrics['entropy_score'],
                bloom_count=len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                               if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0,
                interval=interval,
                mood_pressure=debug_metrics['mood_pressure']
            )
            
            # Log Claude voice data
            log_claude_voice({
                "tick_id": tick_id,
                "zone": zone,
                "pulse_heat": debug_metrics['current_heat'],
                "scup_score": debug_metrics['scup'],
                "entropy_score": debug_metrics['entropy_score'],
                "mood_pressure": debug_metrics['mood_pressure'],
                "stability": debug_metrics['stability'],
                "interval": interval
            })
            
            # Log interval changes
            os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
            with open("juliet_flowers/cluster_report/interval_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{interval:.3f}\n")
            
            # Log zone overlay
            with open("juliet_flowers/cluster_report/zone_overlay_log.csv", "a", encoding="utf-8") as f:
                f.write(f"{tick_id},{zone},{debug_metrics['current_heat']:.3f}\n")
            
            # Periodic detailed logging
            if tick_id % 10 == 0:
                print(f"\n[TickEngine] 📊 Tick {tick_id} Metrics:")
                print(f"  Zone: {zone} | Heat: {debug_metrics['current_heat']:.3f} | SCUP: {debug_metrics['scup']:.3f}")
                print(f"  Interval: {interval:.3f}s | Stability: {debug_metrics['stability']:.3f}")
                print(f"  Entropy: {debug_metrics['entropy_score']:.3f} | Tension: {debug_metrics['total_tension']:.3f}")
            # Generate cognitive trace
            

         # Generate cognitive trace
            if self.enable_cognitive_trace:
                # Gather current sigils
                active_sigils = []
                try:
                    from codex.sigil_memory_ring import sigil_memory_ring
                    active_sigils = [s.name for s in sigil_memory_ring.values() 
                                    if hasattr(s, 'name') and s.entropy < 0.9][:6]
                except:
                    pass
                
                # Prepare tick data
                tick_data = {
                    'tick': tick_id,
                    'zone': zone,
                    'pulse_heat': debug_metrics['current_heat'],
                    'entropy': debug_metrics['entropy_score'],
                    'scup': debug_metrics['scup'],
                    'schema_health': debug_metrics.get('schema_health', 1.0),
                    'active_sigils': active_sigils,
                    'bloom_count': len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                                    if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0,
                    'drift_magnitude': debug_metrics.get('drift_magnitude', 0.0)
                }
                
                # Generate and display commentary
                snapshot = self.cognitive_trace.process_tick(tick_data)
                print(f"\n💭 {snapshot.commentary}")
                
                # Save periodically
                if tick_id % 10 == 0:
                    self.cognitive_trace.save_trace(snapshot)

        except Exception as e:
            print(f"[TickEngine] ⚠️ Logging error: {e}")
    
    def _perform_maintenance_cycles(self, tick_id: int):
        """Perform periodic maintenance and cleanup."""
        try:
            # Schema maintenance
            if tick_id % 25 == 0:
                shi = calculate_SHI(
                    pulse.heat,
                    len([f for f in os.listdir("juliet_flowers/bloom_metadata") 
                        if f.endswith(".json")]) if os.path.exists("juliet_flowers/bloom_metadata") else 0,
                    len(os.listdir("juliet_flowers/sealed")) if os.path.exists("juliet_flowers/sealed") else 0,
                    [sigil.entropy for sigil in sigil_memory_ring.values() if hasattr(sigil, 'entropy')]
                )
                print(f"[TickEngine] 🧬 Schema Health Index: {shi:.3f}")
            
            # Memory decay
            if self.zone_timer.get("🟢 calm", 0) % 10 == 0:
                decay_schema_memory()
            
            # Sigil maintenance
            if tick_id % 15 == 0:
                decay_all_sigils()
                age_all_sigils()
            
            # Persephone lifecycle
            if tick_id % 20 == 0:
                fade_sigils()
                expire_ephemeral_sigils()
                prune_dead_branches()
            
            # Bloom sealing
            if tick_id % 50 == 0:
                print("[TickEngine] 🧺 Scheduled bloom sweep")
                for bloom in load_all_blooms():
                    soft_seal_bloom(bloom)
            
            # Entropy field rendering
            if tick_id % 75 == 0:
                render_entropy_field()
        
        except Exception as e:
            print(f"[TickEngine] ⚠️ Maintenance error: {e}")
    
    async def start(self):
        """Start the refined tick engine main loop."""
        print("[TickEngine] 🚀 Starting refined tick engine")
        self._running = True
        
        while self._running:
            try:
                # Get current tick ID
                tick_id = pulse.tick_count
                
                # Compute adaptive interval
                interval, debug_metrics = await self._compute_adaptive_interval()
                
                # Update thermal system
                pressure_val = await self.pressure_sensor() if self.pressure_sensor else 0.0
                pulse.update(pressure_val)
                
                # Get current zone and update tracking
                zone = pulse.classify()
                self._update_zone_tracking(zone)
                
                # Execute zone-specific reflexes
                await self._execute_zone_reflexes(zone, debug_metrics['scup'], debug_metrics['entropy_score'])
                
                # Update schema health
                update_schema_health(debug_metrics['scup'])
                pulse.adjust_urgency(debug_metrics['scup'])
                
                # Emit tick event
                tick_id = emit_tick(zone=zone, pulse=round(pulse.heat, 3))
                
                # Run drift sentinel
                drift_result = owl_drift_check(tick_id=tick_id)
                if drift_result == "override_suppression":
                    print(f"[TickEngine] 🚫 Drift sentinel override at tick {tick_id}")
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
                
                # Check for significant interval changes
                if abs(self.last_interval - interval) > 0.2:
                    owl_log(f"⏱️ Interval shift: {self.last_interval:.2f}s → {interval:.2f}s")
                    self.last_interval = interval
                
                # Wait for computed interval
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"[TickEngine] ❌ Main loop error: {e}")
                # Emergency fallback interval
                await asyncio.sleep(1.0)
    
    def stop(self):
        """Stop the tick engine."""
        print("[TickEngine] 🛑 Stopping refined tick engine")
        self._running = False
    
    def get_engine_stats(self) -> Dict:
        """Get comprehensive engine statistics."""
        return {
            'tick_count': pulse.tick_count,
            'current_zone': self.current_zone,
            'zone_timer': dict(self.zone_timer),
            'recent_intervals': list(self.interval_history)[-10:],
            'entropy_trend': list(self.entropy_trend)[-10:],
            'scup_trend': list(self.scup_trend)[-10:],
            'zone_transitions': self.zone_transitions[-5:],
            'reflex_cooldowns': dict(self.reflex_cooldowns),
            'thermal_profile': pulse.get_thermal_profile()
        }


# Factory function for easy initialization
def create_refined_tick_engine(base_interval: float = 1.0, 
                              activity_sensor: Optional[Callable] = None,
                              pressure_sensor: Optional[Callable] = None,
                              mood_sensor: Optional[Callable] = None) -> RefinedTickEngine:
    """Create and configure a refined tick engine."""
    engine = RefinedTickEngine(
        base_interval=base_interval,
        activity_sensor=activity_sensor,
        pressure_sensor=pressure_sensor,
        mood_sensor=mood_sensor
    )
    
    # Set up autonomous trigger
    trigger = AutonomousFieldTrigger()
    engine.tick_hook = trigger.on_tick
    
    return engine


# Global engine instance for legacy compatibility
# At the bottom of tick_engine.py
engine = create_refined_tick_engine()
cognitive_hook = attach_cognitive_trace(engine)

print("[TickEngine] ✨ Refined TickEngine module loaded and ready")
