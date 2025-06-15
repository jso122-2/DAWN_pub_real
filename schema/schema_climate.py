# /schema/schema_climate.py
"""
Schema Climate System for DAWN
==============================
Manages the global "weather" patterns that affect nutrient dynamics,
consciousness flow, and system health. The climate influences how
nutrients decay, bloom, and interact within the consciousness field.
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import json
import threading

class ClimateZone(Enum):
    """Different climate zones affecting consciousness dynamics"""
    STABLE = "stable"           # Balanced, predictable dynamics
    CHAOTIC = "chaotic"         # High entropy, rapid changes
    HARMONIOUS = "harmonious"   # Enhanced coherence and flow
    STAGNANT = "stagnant"      # Low activity, slow dynamics
    TURBULENT = "turbulent"    # Mixed high/low pressure systems
    CRYSTALLINE = "crystalline" # Highly ordered, low entropy

class WeatherPattern(Enum):
    """Weather patterns that temporarily affect the climate"""
    CLEAR = "clear"             # Normal conditions
    STORM = "storm"             # Rapid nutrient churning
    FOG = "fog"                # Reduced visibility/clarity
    AURORA = "aurora"          # Enhanced consciousness activity
    DROUGHT = "drought"        # Nutrient scarcity
    BLOOM = "bloom"            # Abundant growth conditions

@dataclass
class ClimateMetrics:
    """Current climate measurements"""
    temperature: float = 0.5      # 0-1, affects reaction rates
    pressure: float = 0.5         # 0-1, affects compression/expansion
    humidity: float = 0.5         # 0-1, affects nutrient flow
    wind_speed: float = 0.0       # 0-1, affects drift and mixing
    visibility: float = 1.0       # 0-1, affects perception clarity
    electromagnetic: float = 0.5   # 0-1, affects field coherence

@dataclass
class NutrientDynamics:
    """Dynamic parameters for each nutrient type"""
    decay_rate: float = 1.0
    growth_rate: float = 1.0
    volatility: float = 0.1
    conductivity: float = 0.5
    reactivity: float = 0.5

class SchemaClimate:
    """
    Global climate system managing environmental conditions that affect
    all consciousness dynamics in DAWN.
    """
    
    def __init__(self):
        # Base climate state
        self.current_zone = ClimateZone.STABLE
        self.current_pattern = WeatherPattern.CLEAR
        self.metrics = ClimateMetrics()
        
        # Nutrient-specific dynamics
        self.nutrient_dynamics = {
            "ash": NutrientDynamics(decay_rate=1.2, volatility=0.3),
            "soot": NutrientDynamics(decay_rate=0.8, volatility=0.4),
            "sentiment": NutrientDynamics(growth_rate=1.5, conductivity=0.8),
            "attention": NutrientDynamics(decay_rate=1.5, reactivity=0.9),
            "urgency": NutrientDynamics(volatility=0.8, reactivity=0.7),
            "memory": NutrientDynamics(decay_rate=0.3, conductivity=0.6),
            "entropy": NutrientDynamics(volatility=0.9, growth_rate=1.3),
            "coherence": NutrientDynamics(conductivity=0.9, decay_rate=0.5)
        }
        
        # Climate history for pattern detection
        self.climate_history = deque(maxlen=1000)
        self.pattern_duration = 0
        self.pattern_start_time = time.time()
        
        # Seasonal cycles
        self.season_phase = 0.0  # 0-2π, represents position in seasonal cycle
        self.season_speed = 0.001  # Radians per update
        
        # Climate influences
        self.external_influences = []
        self.climate_modifiers = {}
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Start climate evolution
        self._last_update = time.time()
    
    def update(self, delta_time: Optional[float] = None):
        """Update climate conditions based on time and system state"""
        with self.lock:
            if delta_time is None:
                current_time = time.time()
                delta_time = current_time - self._last_update
                self._last_update = current_time
            
            # Update seasonal cycle
            self.season_phase = (self.season_phase + self.season_speed * delta_time) % (2 * math.pi)
            
            # Apply seasonal effects
            self._apply_seasonal_effects()
            
            # Natural climate evolution
            self._evolve_climate(delta_time)
            
            # Check for pattern changes
            self._check_pattern_transitions()
            
            # Record history
            self._record_climate_state()
            
            # Apply modifiers
            self._apply_climate_modifiers()
    
    def _apply_seasonal_effects(self):
        """Apply cyclical seasonal variations to climate"""
        # Temperature varies with season
        self.metrics.temperature = 0.5 + 0.3 * math.sin(self.season_phase)
        
        # Humidity inverse to temperature
        self.metrics.humidity = 0.5 - 0.2 * math.sin(self.season_phase)
        
        # Electromagnetic activity peaks in "summer"
        self.metrics.electromagnetic = 0.5 + 0.4 * math.cos(self.season_phase - math.pi/4)
    
    def _evolve_climate(self, delta_time: float):
        """Natural climate evolution with some randomness"""
        # Add brownian motion to metrics
        drift_amount = 0.01 * delta_time
        
        self.metrics.pressure += random.gauss(0, drift_amount)
        self.metrics.wind_speed += random.gauss(0, drift_amount * 2)
        self.metrics.visibility += random.gauss(0, drift_amount * 0.5)
        
        # Clamp values
        self.metrics.pressure = max(0, min(1, self.metrics.pressure))
        self.metrics.wind_speed = max(0, min(1, self.metrics.wind_speed))
        self.metrics.visibility = max(0.1, min(1, self.metrics.visibility))
        
        # Wind affects visibility
        if self.metrics.wind_speed > 0.7:
            self.metrics.visibility *= 0.99
    
    def _check_pattern_transitions(self):
        """Check if weather pattern should change"""
        pattern_age = time.time() - self.pattern_start_time
        
        # Patterns have variable durations
        min_duration = {
            WeatherPattern.CLEAR: 300,
            WeatherPattern.STORM: 60,
            WeatherPattern.FOG: 120,
            WeatherPattern.AURORA: 180,
            WeatherPattern.DROUGHT: 240,
            WeatherPattern.BLOOM: 150
        }
        
        if pattern_age > min_duration.get(self.current_pattern, 100):
            # Probability of transition increases with age
            transition_prob = (pattern_age - min_duration[self.current_pattern]) / 1000
            
            if random.random() < transition_prob:
                self._transition_weather_pattern()
    
    def _transition_weather_pattern(self):
        """Transition to a new weather pattern based on current conditions"""
        # Define transition probabilities based on current pattern
        transitions = {
            WeatherPattern.CLEAR: [
                (WeatherPattern.FOG, 0.3),
                (WeatherPattern.STORM, 0.2),
                (WeatherPattern.AURORA, 0.1),
                (WeatherPattern.BLOOM, 0.2),
                (WeatherPattern.CLEAR, 0.2)
            ],
            WeatherPattern.STORM: [
                (WeatherPattern.CLEAR, 0.4),
                (WeatherPattern.FOG, 0.3),
                (WeatherPattern.TURBULENT, 0.3)
            ],
            WeatherPattern.FOG: [
                (WeatherPattern.CLEAR, 0.5),
                (WeatherPattern.DROUGHT, 0.2),
                (WeatherPattern.FOG, 0.3)
            ],
            WeatherPattern.AURORA: [
                (WeatherPattern.CLEAR, 0.4),
                (WeatherPattern.BLOOM, 0.3),
                (WeatherPattern.AURORA, 0.3)
            ],
            WeatherPattern.DROUGHT: [
                (WeatherPattern.CLEAR, 0.3),
                (WeatherPattern.STORM, 0.4),
                (WeatherPattern.DROUGHT, 0.3)
            ],
            WeatherPattern.BLOOM: [
                (WeatherPattern.CLEAR, 0.3),
                (WeatherPattern.AURORA, 0.2),
                (WeatherPattern.STORM, 0.2),
                (WeatherPattern.BLOOM, 0.3)
            ]
        }
        
        # Get valid transitions
        valid_transitions = transitions.get(self.current_pattern, [(WeatherPattern.CLEAR, 1.0)])
        
        # Weighted random selection
        patterns, weights = zip(*valid_transitions)
        new_pattern = random.choices(patterns, weights=weights)[0]
        
        if new_pattern != self.current_pattern:
            self.set_weather_pattern(new_pattern)
    
    def set_weather_pattern(self, pattern: WeatherPattern):
        """Set a new weather pattern and adjust metrics accordingly"""
        with self.lock:
            self.current_pattern = pattern
            self.pattern_start_time = time.time()
            
            # Adjust metrics based on pattern
            if pattern == WeatherPattern.STORM:
                self.metrics.pressure = random.uniform(0.2, 0.4)
                self.metrics.wind_speed = random.uniform(0.7, 1.0)
                self.metrics.electromagnetic = random.uniform(0.8, 1.0)
                
            elif pattern == WeatherPattern.FOG:
                self.metrics.visibility = random.uniform(0.1, 0.3)
                self.metrics.humidity = random.uniform(0.8, 1.0)
                self.metrics.wind_speed = random.uniform(0.0, 0.2)
                
            elif pattern == WeatherPattern.AURORA:
                self.metrics.electromagnetic = random.uniform(0.9, 1.0)
                self.metrics.visibility = 1.0
                self.metrics.temperature = random.uniform(0.7, 0.9)
                
            elif pattern == WeatherPattern.DROUGHT:
                self.metrics.humidity = random.uniform(0.0, 0.2)
                self.metrics.temperature = random.uniform(0.8, 1.0)
                
            elif pattern == WeatherPattern.BLOOM:
                self.metrics.humidity = random.uniform(0.6, 0.8)
                self.metrics.temperature = random.uniform(0.6, 0.7)
                self.metrics.electromagnetic = random.uniform(0.6, 0.8)
            
            print(f"[CLIMATE] Weather pattern changed to: {pattern.value}")
    
    def get_nutrient_modifier(self, nutrient_type: str, modifier_type: str = "decay") -> float:
        """
        Get the climate modifier for a specific nutrient and modifier type
        
        Args:
            nutrient_type: Type of nutrient (ash, soot, sentiment, etc.)
            modifier_type: Type of modifier (decay, growth, volatility, etc.)
        
        Returns:
            Modifier value influenced by current climate
        """
        with self.lock:
            if nutrient_type not in self.nutrient_dynamics:
                return 1.0
            
            dynamics = self.nutrient_dynamics[nutrient_type]
            base_value = getattr(dynamics, f"{modifier_type}_rate", 1.0)
            
            # Apply climate influences
            climate_multiplier = 1.0
            
            # Temperature affects all rates
            temp_effect = 1.0 + (self.metrics.temperature - 0.5) * 0.5
            climate_multiplier *= temp_effect
            
            # Pattern-specific effects
            pattern_effects = {
                WeatherPattern.STORM: {
                    "decay": 1.5,
                    "volatility": 2.0,
                    "reactivity": 1.8
                },
                WeatherPattern.DROUGHT: {
                    "decay": 0.5,
                    "growth": 0.3
                },
                WeatherPattern.BLOOM: {
                    "growth": 2.0,
                    "conductivity": 1.5
                },
                WeatherPattern.FOG: {
                    "conductivity": 0.3,
                    "visibility": 0.2
                },
                WeatherPattern.AURORA: {
                    "reactivity": 2.0,
                    "electromagnetic": 2.5
                }
            }
            
            if self.current_pattern in pattern_effects:
                pattern_modifier = pattern_effects[self.current_pattern].get(modifier_type, 1.0)
                climate_multiplier *= pattern_modifier
            
            # Zone effects
            zone_effects = {
                ClimateZone.CHAOTIC: {"volatility": 2.0, "decay": 1.5},
                ClimateZone.HARMONIOUS: {"conductivity": 1.5, "growth": 1.3},
                ClimateZone.STAGNANT: {"decay": 0.3, "growth": 0.5},
                ClimateZone.CRYSTALLINE: {"volatility": 0.2, "conductivity": 2.0}
            }
            
            if self.current_zone in zone_effects:
                zone_modifier = zone_effects[self.current_zone].get(modifier_type, 1.0)
                climate_multiplier *= zone_modifier
            
            return base_value * climate_multiplier
    
    def add_climate_influence(self, influence: Dict[str, float], duration: float = 60.0):
        """Add a temporary climate influence"""
        with self.lock:
            expiry_time = time.time() + duration
            self.external_influences.append({
                'influence': influence,
                'expiry': expiry_time
            })
    
    def _apply_climate_modifiers(self):
        """Apply temporary climate modifiers and remove expired ones"""
        current_time = time.time()
        
        # Remove expired influences
        self.external_influences = [
            inf for inf in self.external_influences 
            if inf['expiry'] > current_time
        ]
        
        # Apply active influences
        for influence_data in self.external_influences:
            influence = influence_data['influence']
            for metric, value in influence.items():
                if hasattr(self.metrics, metric):
                    current = getattr(self.metrics, metric)
                    setattr(self.metrics, metric, max(0, min(1, current + value)))
    
    def _record_climate_state(self):
        """Record current climate state for history"""
        state = {
            'timestamp': time.time(),
            'zone': self.current_zone.value,
            'pattern': self.current_pattern.value,
            'metrics': {
                'temperature': self.metrics.temperature,
                'pressure': self.metrics.pressure,
                'humidity': self.metrics.humidity,
                'wind_speed': self.metrics.wind_speed,
                'visibility': self.metrics.visibility,
                'electromagnetic': self.metrics.electromagnetic
            }
        }
        self.climate_history.append(state)
    
    def get_climate_report(self) -> Dict[str, Any]:
        """Get a comprehensive climate report"""
        with self.lock:
            return {
                'current_zone': self.current_zone.value,
                'current_pattern': self.current_pattern.value,
                'pattern_age': time.time() - self.pattern_start_time,
                'season_phase': self.season_phase,
                'season_name': self._get_season_name(),
                'metrics': {
                    'temperature': round(self.metrics.temperature, 3),
                    'pressure': round(self.metrics.pressure, 3),
                    'humidity': round(self.metrics.humidity, 3),
                    'wind_speed': round(self.metrics.wind_speed, 3),
                    'visibility': round(self.metrics.visibility, 3),
                    'electromagnetic': round(self.metrics.electromagnetic, 3)
                },
                'active_influences': len(self.external_influences)
            }
    
    def _get_season_name(self) -> str:
        """Get the current season name based on phase"""
        phase_normalized = self.season_phase / (2 * math.pi)
        if phase_normalized < 0.25:
            return "Growth"
        elif phase_normalized < 0.5:
            return "Bloom"
        elif phase_normalized < 0.75:
            return "Harvest"
        else:
            return "Rest"
    
    def trigger_climate_event(self, event_type: str):
        """Trigger a specific climate event"""
        events = {
            "solar_flare": {
                "pattern": WeatherPattern.AURORA,
                "influences": {"electromagnetic": 0.5, "temperature": 0.3}
            },
            "void_storm": {
                "pattern": WeatherPattern.STORM,
                "influences": {"pressure": -0.5, "wind_speed": 0.5}
            },
            "consciousness_bloom": {
                "pattern": WeatherPattern.BLOOM,
                "influences": {"humidity": 0.3, "temperature": 0.1}
            },
            "entropy_cascade": {
                "zone": ClimateZone.CHAOTIC,
                "influences": {"electromagnetic": -0.3, "visibility": -0.4}
            }
        }
        
        if event_type in events:
            event = events[event_type]
            
            if "pattern" in event:
                self.set_weather_pattern(event["pattern"])
            
            if "zone" in event:
                self.current_zone = event["zone"]
            
            if "influences" in event:
                self.add_climate_influence(event["influences"], duration=120)
            
            print(f"[CLIMATE] Triggered event: {event_type}")

# Global climate instance
CLIMATE = SchemaClimate()

# Legacy compatibility functions
def set_decay_boost(nutrient_type: str, boost: float):
    """Legacy function - sets decay modifier for a nutrient"""
    if nutrient_type in CLIMATE.nutrient_dynamics:
        CLIMATE.nutrient_dynamics[nutrient_type].decay_rate = boost

def get_decay_boost(nutrient_type: str) -> float:
    """Legacy function - gets decay modifier for a nutrient"""
    return CLIMATE.get_nutrient_modifier(nutrient_type, "decay")

def get_climate_state() -> Dict[str, Any]:
    """Get current climate state"""
    return CLIMATE.get_climate_report()

def update_climate(delta_time: Optional[float] = None):
    """Update climate conditions"""
    CLIMATE.update(delta_time)