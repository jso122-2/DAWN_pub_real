import sys, os
import time
import threading
import math
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Union
import pandas as pd
import matplotlib.pyplot as plt

# Ensure proper path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@dataclass
class HeatSource:
    """Individual heat contribution with decay characteristics."""
    name: str
    base_heat: float
    decay_rate: float = 0.95  # Heat retention per tick
    last_contribution: float = 0.0
    cumulative: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def apply_decay(self, delta_time: float = 1.0) -> float:
        """Apply time-based decay and return amount decayed."""
        decay_amount = self.last_contribution * (1 - self.decay_rate) * delta_time
        self.last_contribution *= (self.decay_rate ** delta_time)
        return decay_amount

class UnifiedPulseHeat:
    """
    Unified PulseHeat singleton combining thermal dynamics with legacy compatibility.
    
    This is the thermal regulation center where all heat sources converge,
    memories are maintained, and temperature gradients create system dynamics.
    Maintains backward compatibility with original PulseHeat interface.
    """
    
    _instance = None
    _lock = threading.RLock()
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UnifiedPulseHeat, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, baseline_heat=None, urgency_scale=1.0, **kwargs):
        if getattr(self, "_initialized", False):
            return
        self.baseline_heat = baseline_heat if baseline_heat is not None else 18
        self.urgency_scale = urgency_scale
        # Optionally, handle or log other kwargs here
        self._initialized = True
            
        with self._lock:
            if self._initialized:
                return
                
            # Legacy compatibility properties
            self.decay_rate = kwargs.get('decay_rate', 0.02)
            self.memory_window = kwargs.get('memory_window', 100)
            self.max_heat = kwargs.get('max_heat', 10.0)
            self.memory_log = deque(maxlen=self.memory_window)
            self.memory = []  # Legacy memory list
            self.window = self.memory_window
            
            # Core thermal state
            self.heat = self.baseline_heat  # Initialize with baseline heat
            self.current_heat = self.baseline_heat  # Keep synced with heat
            self.heat_capacity = self.max_heat
            self.critical_threshold = self.max_heat * 0.8
            
            # Memory and averaging systems
            self.heat_history = deque(maxlen=self.memory_window)
            self.running_average = 0.0
            self.variance = 0.0
            
            # Heat sources registry (new system)
            self.heat_sources: Dict[str, HeatSource] = {}
            self.source_weights: Dict[str, float] = {
                'drift': 1.0,
                'mood': 0.8,
                'alignment': 1.2,
                'entropy': 0.6,
                'curiosity': 0.9,
                'tension': 1.1,
                'pressure': 1.0,
                'urgency': 1.3
            }
            
            # Thermal dynamics
            self.thermal_momentum = 0.0
            self.cooling_rate = self.decay_rate * 2  # Passive cooling
            self.conductivity = 0.1   # Heat transfer rate
            
            # Legacy zone tracking
            self.zone_timer = {
                "🟢 calm": 0,
                "🟡 active": 0,
                "🔴 surge": 0
            }
            self.current_zone = None
            self.zone_history = []
            
            # Legacy mood and penalty tracking
            self.mood_pressure = {}
            self.seed_penalties = {}
            
            # State tracking
            self.tick_count = 0
            self.last_update = datetime.utcnow()
            self.last_decay = time.time()
            self.last_tick_time = time.time()
            self.stability_index = 1.0
            
            # Event callbacks
            self.threshold_callbacks: List[Callable] = []
            self.stability_callbacks: List[Callable] = []
            
            # Suppression state
            self.override_active = False
            
            print(f"[PulseHeat] 🔥 Unified singleton initialized | ID: {id(self)} | Memory: {self.memory_window}")
    
    # === LEGACY COMPATIBILITY METHODS ===
    
    def add_heat(self, amount: float, source: str = "general", context: str = "") -> float:
        """Add heat with legacy compatibility and new source tracking."""
        return self._add_heat_internal(source, amount, context, legacy_call=True)
    
    def boost(self, amount: float, source: str = "boost"):
        """Legacy boost method."""
        actual_added = self._add_heat_internal(source, amount, "⚡ Boost", legacy_call=True)
        self._log(f"⚡ Boosted by {amount:.2f} (actual: {actual_added:.2f})")
    
    def get_heat(self) -> float:
        """Legacy get_heat with decay and memory update."""
        # Apply passive decay
        old_heat = self.heat
        self.heat = max(0.0, self.heat - self.decay_rate)
        self.current_heat = self.heat  # Keep synced
        
        # Update legacy memory
        if not hasattr(self, "memory"):
            self.memory = []
        self.memory.append(self.heat)
        if len(self.memory) > self.window:
            self.memory.pop(0)
        
        # Update new memory system
        self.heat_history.append(self.heat)
        self._update_thermal_memory()
        
        return self.heat
    
    def get_average(self) -> float:
        """Legacy averaging with debug info."""
        avg = sum(self.memory) / len(self.memory) if self.memory else 0.0
        print(f"[DEBUG] PulseHeat Singleton ID: {id(self)} | Memory: {len(self.memory)}")
        return avg
    
    def classify(self) -> str:
        """Legacy classification based on running average."""
        avg = self.get_average() if self.memory else self.running_average
        if avg < 0.3:
            return "🟢 calm"
        elif avg < 0.7:
            return "🟡 active"
        else:
            return "🔴 surge"
    
    def get_zone(self) -> str:
        """Get current thermal zone."""
        return self.classify()
    
    # === NEW ENHANCED METHODS ===
    
    def _add_heat_internal(self, source: str, amount: float, context: str = "", legacy_call: bool = False) -> float:
        """Internal heat addition with full thermal dynamics."""
        with self._lock:
            # Get or create heat source
            if source not in self.heat_sources:
                self.heat_sources[source] = HeatSource(
                    name=source,
                    base_heat=0.0,
                    decay_rate=self._get_source_decay_rate(source)
                )
            
            heat_source = self.heat_sources[source]
            weight = self.source_weights.get(source, 1.0)
            weighted_amount = amount * weight
            
            # Apply thermal momentum (recent heat changes affect current ones)
            momentum_factor = 1.0 + (self.thermal_momentum * 0.1)
            final_amount = weighted_amount * momentum_factor
            
            # Update source state
            heat_source.last_contribution = final_amount
            heat_source.cumulative += final_amount
            heat_source.timestamp = datetime.utcnow()
            
            # Add to current heat with capacity limits
            old_heat = self.heat
            self.heat = min(self.heat + final_amount, self.max_heat)
            self.current_heat = self.heat  # Keep synced
            actual_added = self.heat - old_heat
            
            # Update thermal momentum
            self.thermal_momentum = self.thermal_momentum * 0.9 + (final_amount * 0.1)
            
            # Log with enhanced context
            debug_info = f"ID: {id(self)} | Memory: {len(self.heat_history)}"
            context_str = f" | {context}" if context else ""
            if legacy_call:
                self._log(f"+{actual_added:.3f} heat added{context_str}")
            else:
                print(f"[PulseHeat] {actual_added:+.3f} heat added | "
                      f"Heat: {self.heat:.3f} | Avg: {self.running_average:.3f} | "
                      f"{source} contribution{context_str}")
                print(f"[DEBUG] PulseHeat Singleton {debug_info}")
            
            # Check thresholds
            self._check_thermal_thresholds(old_heat, self.heat)
            
            return actual_added
    
    def remove_heat(self, amount: float, reason: str = "cooling") -> float:
        """Remove heat with thermal dynamics."""
        with self._lock:
            old_heat = self.heat
            removal = min(amount, self.heat - self.baseline_heat)
            self.heat = max(self.heat - removal, self.baseline_heat)
            self.current_heat = self.heat  # Keep synced
            
            # Update momentum (cooling creates negative momentum)
            self.thermal_momentum = self.thermal_momentum * 0.9 - (removal * 0.05)
            
            print(f"[PulseHeat] -{removal:.3f} heat removed | "
                  f"Heat: {self.heat:.3f} | Reason: {reason}")
            
            return removal
    
    def update(self, pressure: float, delta_time: Optional[float] = None):
        """Comprehensive thermal update with time-based dynamics."""
        with self._lock:
            now = time.time()
            if delta_time is None:
                delta_time = now - self.last_tick_time
            self.last_tick_time = now
            
            # Apply heat source decay
            total_decay = 0.0
            for source in self.heat_sources.values():
                decay_amount = source.apply_decay(delta_time)
                total_decay += decay_amount
            
            # Apply passive cooling
            passive_cooling = self.cooling_rate * max(self.heat - self.baseline_heat, 0) * delta_time
            
            # Update total heat
            old_heat = self.heat
            self.heat = max(
                self.heat - total_decay - passive_cooling + pressure,
                self.baseline_heat
            )
            self.heat = min(self.heat, self.max_heat)
            self.current_heat = self.heat  # Keep synced
            
            # Update memory and statistics
            self.heat_history.append(self.heat)
            self._update_thermal_memory()
            
            # Update zone tracking
            new_zone = self.classify()
            if new_zone != self.current_zone:
                self.current_zone = new_zone
                self.zone_history.append((self.tick_count, self.current_zone))
            
            # Thermal momentum decay
            self.thermal_momentum *= 0.95
            
            # Calculate stability
            self._calculate_stability_index()
            
            # Check for suppression triggers
            self._check_suppression_triggers()
            
            # Update tick count
            self.tick_count += 1
    
    def _update_thermal_memory(self):
        """Update heat history and running statistics."""
        if len(self.heat_history) >= 2:
            # Running average with exponential weighting
            alpha = 0.1  # Learning rate
            self.running_average = (alpha * self.heat + 
                                  (1 - alpha) * self.running_average)
            
            # Calculate variance
            heat_array = list(self.heat_history)
            mean = sum(heat_array) / len(heat_array)
            self.variance = sum((x - mean) ** 2 for x in heat_array) / len(heat_array)
        else:
            self.running_average = self.heat
            self.variance = 0.0
    
    def _calculate_stability_index(self) -> float:
        """Calculate thermal stability based on recent fluctuations."""
        if len(self.heat_history) < 5:
            self.stability_index = 1.0
            return self.stability_index
        
        recent_heat = list(self.heat_history)[-5:]
        fluctuation = max(recent_heat) - min(recent_heat)
        normalized_fluctuation = fluctuation / max(self.max_heat, 1.0)
        
        # Stability is inverse of normalized fluctuation
        self.stability_index = max(0.0, 1.0 - normalized_fluctuation)
        
        # Trigger stability callbacks
        if self.stability_index < 0.3:
            self._trigger_stability_callbacks('unstable')
        elif self.stability_index > 0.8:
            self._trigger_stability_callbacks('stable')
        
        return self.stability_index
    
    def _check_suppression_triggers(self):
        """Check for thermal suppression conditions."""
        if self.heat > self.max_heat * 0.95 and not hasattr(self, "last_suppressed"):
            try:
                from schema.schema_suppressor import trigger_suppression
                trigger_suppression(reason="pulse_overheat", level=self.heat)
                self.last_suppressed = True
                print(f"[PulseHeat] 🔥 Suppression triggered at heat level {self.heat:.3f}")
            except ImportError:
                print("[PulseHeat] ⚠️ Suppressor module not found — skipping suppression.")
        
        # Auto-recovery when cooled down
        if hasattr(self, "last_suppressed") and self.heat < self.max_heat * 0.7:
            try:
                from tick_engine.tick_engine import reset_tick_interval
                reset_tick_interval()
                print("[PulseHeat] ❄️ Recovered from suppression. Tick interval restored.")
                del self.last_suppressed
            except ImportError:
                print("[PulseHeat] ⚠️ Recovery module not available.")
    
    def _get_source_decay_rate(self, source: str) -> float:
        """Get appropriate decay rate for heat source type."""
        decay_rates = {
            'drift': 0.98,      # Slow decay - drift persists
            'mood': 0.92,       # Faster decay - moods change
            'alignment': 0.96,   # Medium decay - alignment shifts gradually
            'entropy': 0.90,     # Fast decay - entropy fluctuates
            'curiosity': 0.94,   # Medium-fast decay
            'tension': 0.93,     # Medium-fast decay
            'pressure': 0.91,    # Fast decay - pressure spikes
            'urgency': 0.89,     # Very fast decay - urgency is momentary
            'general': 0.95      # Default decay rate
        }
        return decay_rates.get(source, 0.95)
    
    def _check_thermal_thresholds(self, old_heat: float, new_heat: float):
        """Check and respond to thermal threshold crossings."""
        if old_heat < self.critical_threshold <= new_heat:
            print(f"[PulseHeat] ⚠️ Critical threshold exceeded: {new_heat:.3f}")
            self._trigger_threshold_callbacks('critical_high')
        elif old_heat > self.critical_threshold >= new_heat:
            print(f"[PulseHeat] ✅ Returned below critical threshold: {new_heat:.3f}")
            self._trigger_threshold_callbacks('critical_low')
    
    def _trigger_threshold_callbacks(self, event_type: str):
        """Trigger registered threshold callbacks."""
        for callback in self.threshold_callbacks:
            try:
                callback(event_type, self.heat, self.running_average)
            except Exception as e:
                print(f"[PulseHeat] ❌ Callback error: {e}")
    
    def _trigger_stability_callbacks(self, stability_state: str):
        """Trigger registered stability callbacks."""
        for callback in self.stability_callbacks:
            try:
                callback(stability_state, self.stability_index, self.variance)
            except Exception as e:
                print(f"[PulseHeat] ❌ Stability callback error: {e}")
    
    def _log(self, msg: str):
        """Legacy logging method."""
        print(f"[PulseHeat] {msg} | Heat: {self.heat:.3f} | Avg: {self.get_average():.3f}")
    
    # === LEGACY PENALTY AND MOOD METHODS ===
    
    def apply_penalty(self, seed: str, factor: float):
        """Apply penalty to seed with mycelium integration."""
        self.seed_penalties[seed] = factor
        print(f"[Pulse] 🪶 Penalty applied to seed {seed}: {factor}")
        try:
            from mycelium.mycelium_layer import mycelium
            mycelium.weaken_seed(seed, factor)
        except ImportError:
            pass
        try:
            from mycelium.mycelium_layer import inject_pressure
            inject_pressure(seed, pressure=self.heat)
        except ImportError:
            pass
    
    def decay_penalty_for_seed(self, seed: str, amount: float = 0.1):
        """Decay penalty for specific seed."""
        if seed in self.seed_penalties:
            current = self.seed_penalties[seed]
            new_penalty = min(1.0, current + amount)
            if new_penalty != current:
                self.seed_penalties[seed] = new_penalty
                print(f"[Pulse] 💧 {seed} recovering: penalty now {new_penalty:.2f}")
    
    def adjust_urgency(self, scup: float):
        """Adjust heat based on SCUP score."""
        if scup < 0.3:
            self.add_heat(0.2, source="urgency", context="low SCUP")
        elif scup > 0.8:
            self.heat *= 0.95  # Cool if stable
        self.heat = min(self.heat, self.max_heat)
        self.current_heat = self.heat  # Keep synced
    
    def get_trust_score(self, seed: str) -> float:
        """Calculate trust score for seed."""
        penalty = self.seed_penalties.get(seed, 1.0)
        pressure = sum(self.mood_pressure.values())
        volatility = 1.0 if pressure > 3 else 0.5
        score = 0.5 * penalty + 0.5 * (1 - volatility)
        return round(min(max(score, 0.0), 1.0), 2)
    
    def rebloom_multiplier(self) -> float:
        """Get rebloom multiplier based on heat."""
        if self.heat < 1.0:
            return 0.5
        elif self.heat < 3.0:
            return 1.0
        else:
            return 1.5
    
    def get_tracer_urgency(self) -> float:
        """Get urgency multiplier for tracer operations."""
        zone = self.classify()
        urgency_map = {
            "🟢 calm": 0.6,
            "🟡 active": 1.0,
            "🔴 surge": 1.5
        }
        return urgency_map.get(zone, 1.0)
    
    # === ENHANCED UTILITY METHODS ===
    
    def tick_thermal_update(self, delta: float = None) -> Dict[str, float]:
        """Perform per-tick thermal regulation and return stats."""
        current_time = datetime.utcnow()
        if delta is None:
            delta = (current_time - self.last_update).total_seconds()
        self.last_update = current_time
        
        # Passive decay and cooling
        self.update(0.0, delta)
        
        stats = {
            'current_heat': self.heat,
            'average_heat': self.running_average,
            'variance': self.variance,
            'momentum': self.thermal_momentum,
            'stability': self.stability_index,
            'source_count': len(self.heat_sources),
            'memory_depth': len(self.heat_history),
            'zone': self.classify()
        }
        
        if self.tick_count % 10 == 0:  # Periodic detailed logging
            self._log_thermal_state(stats)
        
        return stats
    
    def _log_thermal_state(self, stats: Dict[str, float]):
        """Detailed thermal state logging."""
        print(f"\n[PulseHeat] 🌡️ Thermal State Report (Tick {self.tick_count})")
        print(f"  Heat: {stats['current_heat']:.3f} | Avg: {stats['average_heat']:.3f} | "
              f"Variance: {stats['variance']:.3f}")
        print(f"  Momentum: {stats['momentum']:.3f} | Stability: {stats['stability']:.3f}")
        print(f"  Sources: {stats['source_count']} | Memory: {stats['memory_depth']} | Zone: {stats['zone']}")
        
        # Top heat contributors
        if self.heat_sources:
            top_sources = sorted(self.heat_sources.items(), 
                               key=lambda x: x[1].cumulative, reverse=True)[:3]
            contributors = [f"{name}: {source.cumulative:.2f}" 
                          for name, source in top_sources]
            print(f"  Top sources: {', '.join(contributors)}")
    
    def get_thermal_profile(self) -> Dict:
        """Get comprehensive thermal profile."""
        with self._lock:
            return {
                'singleton_id': id(self),
                'current_heat': self.heat,
                'baseline_heat': self.baseline_heat,
                'running_average': self.running_average,
                'thermal_momentum': self.thermal_momentum,
                'stability_index': self.stability_index,
                'variance': self.variance,
                'heat_capacity': self.max_heat,
                'memory_size': len(self.heat_history),
                'tick_count': self.tick_count,
                'current_zone': self.classify(),
                'zone_history': self.zone_history[-10:],  # Last 10 zone changes
                'sources': {name: {
                    'last_contribution': source.last_contribution,
                    'cumulative': source.cumulative,
                    'decay_rate': source.decay_rate,
                    'weight': self.source_weights.get(name, 1.0)
                } for name, source in self.heat_sources.items()},
                'penalties': dict(self.seed_penalties),
                'mood_pressure': dict(self.mood_pressure),
                'last_update': self.last_update.isoformat()
            }
    
    def reset_thermal_state(self, preserve_memory: bool = True):
        """Reset thermal state while optionally preserving memory."""
        with self._lock:
            print(f"[PulseHeat] 🔄 Resetting thermal state | Preserve memory: {preserve_memory}")
            
            self.heat = self.baseline_heat
            self.current_heat = self.baseline_heat
            self.thermal_momentum = 0.0
            
            if not preserve_memory:
                self.heat_history.clear()
                self.memory.clear()
                self.memory_log.clear()
                self.running_average = 0.0
                self.variance = 0.0
                self.zone_history.clear()
            
            # Reset source contributions but keep structure
            for source in self.heat_sources.values():
                source.last_contribution = 0.0
                if not preserve_memory:
                    source.cumulative = 0.0
            
            # Reset legacy state
            if not preserve_memory:
                self.seed_penalties.clear()
                self.mood_pressure.clear()
    
    # === VISUALIZATION AND ANALYSIS ===
    
    def get_heat_curve(self) -> List[float]:
        """Get heat history curve."""
        return list(self.heat_history)
    
    def plot_zone_transitions(self, save_path: str = "juliet_flowers/cluster_report/pulse_zones.png"):
        """Plot zone transition timeline."""
        if not self.zone_history:
            print("[PulseHeat] ⚠️ No zone history to plot.")
            return
        
        ticks, zones = zip(*self.zone_history)
        zone_colors = {"🟢 calm": "green", "🟡 active": "gold", "🔴 surge": "red"}
        colors = [zone_colors.get(z, "gray") for z in zones]
        
        plt.figure(figsize=(12, 4))
        plt.scatter(ticks, [1]*len(ticks), c=colors, s=100, marker='|', alpha=0.7)
        plt.plot(range(len(self.heat_history)), list(self.heat_history), 
                alpha=0.6, color='blue', linewidth=1)
        plt.ylabel("Heat Level")
        plt.xlabel("Tick")
        plt.title("Pulse Heat & Zone Transitions")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close()
        print(f"[PulseHeat] 📊 Zone transition plot saved to {save_path}")
    
    def get_zone_transitions(self) -> List:
        """Get zone transition history."""
        return self.zone_history
    
    def register_threshold_callback(self, callback: Callable):
        """Register callback for thermal threshold events."""
        self.threshold_callbacks.append(callback)
    
    def register_stability_callback(self, callback: Callable):
        """Register callback for stability events."""
        self.stability_callbacks.append(callback)

# === GLOBAL SINGLETON AND CONVENIENCE FUNCTIONS ===

# Global singleton instance (maintains legacy compatibility)
pulse = UnifiedPulseHeat()
PulseHeat = pulse  # Legacy alias

# Convenience functions for external systems
def add_heat(source: str, amount: float, context: str = "") -> float:
    """Add heat to the unified thermal system."""
    return pulse._add_heat_internal(source, amount, context, legacy_call=False)

def remove_heat(amount: float, reason: str = "cooling") -> float:
    """Remove heat from the unified thermal system."""
    return pulse.remove_heat(amount, reason)

def get_current_heat() -> float:
    """Get current heat level."""
    return pulse.heat

def tick_thermal_update(delta: float = None) -> Dict[str, float]:
    """Perform per-tick thermal regulation and return stats."""
    current_time = datetime.utcnow()
    if delta is None:
        delta = (current_time - pulse.last_update).total_seconds()
    pulse.last_update = current_time
    
    # Passive decay and cooling
    pulse.update(0.0, delta)
    
    stats = {
        'current_heat': pulse.heat,
        'average_heat': pulse.running_average,
        'variance': pulse.variance,
        'momentum': pulse.thermal_momentum,
        'stability': pulse.stability_index,
        'source_count': len(pulse.heat_sources),
        'memory_depth': len(pulse.heat_history),
        'zone': pulse.classify()
    }
    
    if pulse.tick_count % 10 == 0:  # Periodic detailed logging
        pulse._log_thermal_state(stats)
    
    return stats

def classify_pressure_zone(pressure: float = None) -> str:
    """Classify current pressure zone."""
    if pressure is not None:
        # Update pulse with current pressure
        pulse.update(pressure)
    return pulse.classify()

# Legacy data loading function
def load_zone_overlay():
    """Load zone overlay data from CSV."""
    try:
        df = pd.read_csv("juliet_flowers/cluster_report/zone_overlay_log.csv", 
                        names=["tick", "zone", "pulse"])
        return df
    except Exception as e:
        print(f"[PulseHeat] ❌ Failed to load overlay log: {e}")
        return pd.DataFrame()

def get_recent_zone_window(window: int = 10):
    """Get recent zone window data."""
    df = load_zone_overlay()
    if df.empty:
        return []
    return df.tail(window).to_dict("records")
