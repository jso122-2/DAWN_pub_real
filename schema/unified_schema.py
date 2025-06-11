"""
DAWN Unified Schema System
=========================
Consolidates: state, health, flags, goals
Generated: 2025-06-04 21:25
"""

import time
import json
import os
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from statistics import mean

# Try to import pulse via helix, fallback to direct import
try:
    from helix_import_architecture import helix_import
    pulse_heat = helix_import("pulse_heat")
except ImportError:
    from pulse.pulse_heat import PulseHeat
    pulse_heat = PulseHeat()


# =============== SCHEMA FLAGS ===============

class SchemaFlags:
    """Tracks schema state flags and overrides"""
    
    def __init__(self):
        self.suppression_active = False
        self.override_trigger = None
        self.mythic_mode = False
        self.emergency_brake = False
        
    def reset(self):
        """Reset all flags to default state"""
        self.suppression_active = False
        self.override_trigger = None
        self.mythic_mode = False
        self.emergency_brake = False
        
    def get_active_flags(self) -> Dict[str, bool]:
        """Get all active flags"""
        return {
            'suppression': self.suppression_active,
            'override': self.override_trigger is not None,
            'mythic': self.mythic_mode,
            'emergency': self.emergency_brake
        }


# =============== SCHEMA HEALTH ===============

class SchemaHealth:
    """
    Unified health tracking system
    Combines both health implementations
    """
    
    def __init__(self):
        # From schema_health.py
        self.entropies = []
        self.pressures = []
        self.cluster_variance = []
        
        # Additional tracking
        self.pulse_history = []
        self.bloom_density_history = []
        self.sigil_entropy_history = []
        
    def record_metrics(self, entropy: float, pressure: float, variance: float):
        """Record health metrics"""
        self.entropies.append(entropy)
        self.pressures.append(pressure)
        self.cluster_variance.append(variance)
        
        # Keep history manageable
        max_history = 1000
        if len(self.entropies) > max_history:
            self.entropies = self.entropies[-500:]
            self.pressures = self.pressures[-500:]
            self.cluster_variance = self.cluster_variance[-500:]
    
    def calculate_health_score(self) -> float:
        """Calculate composite health score (0.0-1.0)"""
        if not self.entropies:
            return 1.0
            
        # Use recent values (last 50)
        recent = 50
        avg_entropy = mean(self.entropies[-recent:])
        avg_pressure = mean(self.pressures[-recent:])
        avg_variance = mean(self.cluster_variance[-recent:])
        
        # Weighted combination
        health = 1.0 - (0.4 * avg_entropy + 0.3 * avg_pressure + 0.3 * avg_variance)
        return round(max(0.0, min(1.0, health)), 3)
    
    def calculate_shi_with_rebloom(self, scup_value: float) -> float:
        """Calculate SHI with rebloom volatility penalty"""
        volatile, total = self._load_rebloom_volatility()
        volatile_ratio = (volatile / total) if total else 0
        
        penalty = min(0.2, volatile_ratio * 0.5)
        shi = round(max(0.0, min(1.0, scup_value * (1 - penalty))), 4)
        
        # Log SHI curve
        self._log_shi_curve(shi)
        
        return shi
    
    def _load_rebloom_volatility(self) -> Tuple[int, int]:
        """Load rebloom volatility from lineage log"""
        lineage_log = Path("data/bloom/rebloom_lineage.json")
        if not lineage_log.exists():
            return 0, 0
            
        try:
            with open(lineage_log, "r") as f:
                lineage_data = json.load(f)
                
            if not isinstance(lineage_data, dict):
                return 0, 0
                
            total = len(lineage_data)
            volatile = sum(
                1 for bloom in lineage_data.values()
                if bloom.get("generation_depth", 0) < 2
            )
            
            return volatile, total
        except Exception:
            return 0, 0
    
    def _log_shi_curve(self, shi: float):
        """Log SHI value to curve file"""
        output_file = Path("logs/schema/health_curve.csv")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "a") as f:
            f.write(f"{datetime.now().isoformat()},{shi:.4f}\n")


# =============== SCHEMA STATE ===============

class SchemaState:
    """
    Central schema state tracking
    Combines zone tracking, alignment, and mood urgency
    """
    
    def __init__(self):
        self.zone_history = []  # (timestamp, zone) tuples
        self.current_zone = "🟡 active"
        self.alignment = 0.0
        self.mood_urgency = 0.0
        
    def update_zone(self, zone: str, scup: Optional[float] = None, 
                   entropy: Optional[float] = None):
        """Update current zone based on conditions"""
        # SCUP override
        if scup is not None and scup < 0.4:
            zone = "🔴 surge"
        # Entropy override
        elif entropy is not None and entropy > 0.7 and zone != "🔴 surge":
            zone = "🟡 active"
            
        self.current_zone = zone
        self.zone_history.append((time.time(), zone))
        
        # Keep history manageable
        if len(self.zone_history) > 100:
            self.zone_history.pop(0)
            
        return zone
    
    def get_zone_streak(self) -> Tuple[str, int]:
        """Get current zone and how long it's been active"""
        if not self.zone_history:
            return self.current_zone, 0
            
        current = self.zone_history[-1][1]
        streak = 1
        
        for _, zone in reversed(self.zone_history[:-1]):
            if zone == current:
                streak += 1
            else:
                break
                
        return current, streak
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get complete state snapshot"""
        zone, streak = self.get_zone_streak()
        
        return {
            'zone': zone,
            'zone_streak': streak,
            'alignment': self.alignment,
            'mood_urgency': self.mood_urgency,
            'history_length': len(self.zone_history)
        }


# =============== UNIFIED SCHEMA ===============

class UnifiedSchema:
    """
    Central schema management system for DAWN
    Consolidates state, health, flags, and goals
    """
    
    def __init__(self):
        # Core components
        self.state = SchemaState()
        self.health = SchemaHealth()
        self.flags = SchemaFlags()
        
        # Goals will be loaded separately due to size
        self.goals = None  # Lazy load when needed
        
        # Unified tracking
        self._initialized = True
        self._last_update = datetime.now()
        
    def update(self, pulse_data: Optional[Dict] = None, 
              bloom_data: Optional[Dict] = None,
              owl_data: Optional[Dict] = None):
        """Update all schema components with new data"""
        
        if pulse_data:
            # Update state from pulse
            zone = pulse_data.get('zone', 'active')
            self.state.update_zone(zone)
            self.state.mood_urgency = pulse_data.get('heat', 0.0)
            
            # Update health metrics
            if 'pressure' in pulse_data:
                self.health.pressures.append(pulse_data['pressure'])
                
        if bloom_data:
            # Update from bloom data
            entropy = bloom_data.get('entropy', 0.0)
            self.health.entropies.append(entropy)
            
        if owl_data:
            # Update alignment from owl
            self.state.alignment = owl_data.get('coherence', 0.0)
            
        self._last_update = datetime.now()
        
    def get_status(self) -> Dict[str, Any]:
        """Get complete schema status"""
        return {
            'state': self.state.get_current_state(),
            'health': {
                'score': self.health.calculate_health_score(),
                'metrics': {
                    'entropy': mean(self.health.entropies[-10:]) if self.health.entropies else 0,
                    'pressure': mean(self.health.pressures[-10:]) if self.health.pressures else 0,
                    'variance': mean(self.health.cluster_variance[-10:]) if self.health.cluster_variance else 0
                }
            },
            'flags': self.flags.get_active_flags(),
            'last_update': self._last_update.isoformat()
        }
        
    def calculate_shi(self, method: str = 'composite') -> float:
        """
        Calculate Schema Health Index
        Methods: 'composite', 'simple', 'rebloom'
        """
        if method == 'simple':
            return self.health.calculate_health_score()
            
        elif method == 'rebloom':
            # Needs SCUP value
            scup = self.state.alignment  # Use alignment as proxy
            return self.health.calculate_shi_with_rebloom(scup)
            
        else:  # composite
            # Combine multiple factors
            health_score = self.health.calculate_health_score()
            alignment = self.state.alignment
            urgency_penalty = min(0.2, self.state.mood_urgency * 0.3)
            
            shi = (health_score * 0.5 + alignment * 0.5) * (1 - urgency_penalty)
            return round(max(0.0, min(1.0, shi)), 3)
            
    def reset(self):
        """Reset schema to default state"""
        self.flags.reset()
        self.state = SchemaState()
        print("[UnifiedSchema] Schema reset to default state")


# =============== MODULE INTERFACE ===============

# Create singleton instance
_schema = None

def get_schema() -> UnifiedSchema:
    """Get or create schema instance"""
    global _schema
    if _schema is None:
        _schema = UnifiedSchema()
    return _schema

# Convenience functions for backwards compatibility
def get_current_zone(pulse_instance=None, scup=None, entropy=None):
    """Get current zone (backwards compatible)"""
    schema = get_schema()
    zone = pulse_instance.classify() if pulse_instance else "active"
    return schema.state.update_zone(zone, scup, entropy)

def calculate_SHI():
    """Calculate SHI (backwards compatible)"""
    return get_schema().calculate_shi()

def get_mood_urgency():
    """Get mood urgency (backwards compatible)"""
    return get_schema().state.mood_urgency

def get_current_alignment():
    """Get alignment (backwards compatible)"""  
    return get_schema().state.alignment
