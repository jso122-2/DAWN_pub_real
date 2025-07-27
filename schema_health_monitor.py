#!/usr/bin/env python3
"""
DAWN Schema Health Monitor - SHI Implementation  
==============================================

Implements the Schema Health Index (SHI) calculation:
SHI = Σ(component_i × weight_i) for components: V, M, O, A, S

Where:
- V: Vitality (system energy and responsiveness)
- M: Memory Health (memory coherence and stability)  
- O: Orbit Load (processing load, inverted)
- A: Ash Availability (cognitive resources)
- S: Soft Edge Response (adaptability and flexibility)

The monitor provides real-time schema health assessment, intervention
recommendations, and system modulation based on cognitive wellness.
"""

import time
import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable
from datetime import datetime, timezone
from collections import deque
from enum import Enum
from pathlib import Path
import json

logger = logging.getLogger("schema_health_monitor")

class HealthLevel(Enum):
    """Schema health level classifications"""
    CRITICAL = "critical"   # < 0.2: Emergency intervention needed
    POOR = "poor"          # 0.2-0.4: Significant health issues
    FAIR = "fair"          # 0.4-0.6: Below optimal, needs attention
    GOOD = "good"          # 0.6-0.8: Healthy operation
    EXCELLENT = "excellent" # > 0.8: Optimal health state

class HealthComponent(Enum):
    """Schema health components"""
    VITALITY = "vitality"                   # V: System energy and responsiveness
    MEMORY_HEALTH = "memory_health"         # M: Memory coherence and stability
    ORBIT_LOAD = "orbit_load"              # O: Processing load (inverted)
    ASH_AVAILABILITY = "ash_availability"   # A: Cognitive resource availability
    SOFT_EDGE_RESPONSE = "soft_edge_response" # S: Adaptability and flexibility

@dataclass
class HealthReading:
    """Single schema health measurement"""
    timestamp: float
    
    # Component values (0.0 to 1.0)
    vitality: float
    memory_health: float
    orbit_load: float           # Note: Higher load = lower health
    ash_availability: float
    soft_edge_response: float
    
    # Calculated values
    shi_value: float            # Overall SHI score
    health_level: HealthLevel
    health_trend: float         # Rate of change
    
    # Analysis
    component_breakdown: Dict[str, float] = field(default_factory=dict)
    health_alerts: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    intervention_priority: float = 0.0  # 0.0 = low, 1.0 = critical

@dataclass
class HealthMonitorState:
    """Current state of the health monitor"""
    readings_history: deque = field(default_factory=lambda: deque(maxlen=50))
    last_reading: Optional[HealthReading] = None
    assessments_count: int = 0
    interventions_triggered: int = 0
    health_incidents: int = 0
    average_shi: float = 0.5
    lowest_shi: float = 1.0
    health_stability: float = 1.0

class SchemaHealthMonitor:
    """
    Schema Health Monitor
    
    Implements the Schema Health Index (SHI) calculation and provides
    real-time health monitoring, early warning systems, and intervention
    recommendations for DAWN's cognitive schema wellness.
    """
    
    def __init__(self):
        """Initialize the Schema Health Monitor"""
        
        # SHI component weights (must sum to 1.0)
        self.SHI_WEIGHTS = {
            HealthComponent.VITALITY: 0.25,          # 25% - Core system energy
            HealthComponent.MEMORY_HEALTH: 0.25,     # 25% - Memory system wellness  
            HealthComponent.ORBIT_LOAD: 0.20,        # 20% - Processing efficiency
            HealthComponent.ASH_AVAILABILITY: 0.15,  # 15% - Resource availability
            HealthComponent.SOFT_EDGE_RESPONSE: 0.15 # 15% - Adaptability
        }
        
        # Health level thresholds
        self.HEALTH_THRESHOLDS = {
            HealthLevel.CRITICAL: 0.0,
            HealthLevel.POOR: 0.2,
            HealthLevel.FAIR: 0.4,
            HealthLevel.GOOD: 0.6,
            HealthLevel.EXCELLENT: 0.8
        }
        
        # Component analysis thresholds
        self.COMPONENT_ALERT_THRESHOLDS = {
            HealthComponent.VITALITY: 0.3,
            HealthComponent.MEMORY_HEALTH: 0.4,
            HealthComponent.ORBIT_LOAD: 0.7,  # High load threshold
            HealthComponent.ASH_AVAILABILITY: 0.3,
            HealthComponent.SOFT_EDGE_RESPONSE: 0.4
        }
        
        # Monitor configuration
        self.health_sensitivity = 1.0
        self.stability_window = 10     # Readings for stability calculation
        self.intervention_cooldown = 15.0  # Seconds between interventions
        self.trend_smoothing = 0.8     # Smoothing factor for trends
        
        # State tracking
        self.state = HealthMonitorState()
        self.last_intervention_time = 0.0
        self.active_interventions: set = set()
        
        # Callback system
        self.health_callbacks: List[Callable] = []
        self.emergency_callback: Optional[Callable] = None
        
        logger.info("❤️ [HEALTH] Schema Health Monitor initialized")
        logger.info(f"❤️ [HEALTH] Component weights: {[(comp.value, weight) for comp, weight in self.SHI_WEIGHTS.items()]}")
        logger.info(f"❤️ [HEALTH] Health thresholds: {[(level.value, thresh) for level, thresh in self.HEALTH_THRESHOLDS.items()]}")
    
    def calculate_shi(self, state: Dict[str, Any]) -> HealthReading:
        """
        Calculate Schema Health Index (SHI) from system state
        
        Args:
            state: DAWN cognitive state containing health metrics
            
        Returns:
            HealthReading with comprehensive health analysis
        """
        assessment_start = time.time()
        
        try:
            current_time = time.time()
            
            # Extract health components (normalize to 0.0-1.0 range)
            vitality = self._extract_vitality(state)
            memory_health = self._extract_memory_health(state)
            orbit_load = self._extract_orbit_load(state)
            ash_availability = self._extract_ash_availability(state)
            soft_edge_response = self._extract_soft_edge_response(state)
            
            # Calculate weighted SHI
            shi_value = (
                vitality * self.SHI_WEIGHTS[HealthComponent.VITALITY] +
                memory_health * self.SHI_WEIGHTS[HealthComponent.MEMORY_HEALTH] +
                orbit_load * self.SHI_WEIGHTS[HealthComponent.ORBIT_LOAD] +
                ash_availability * self.SHI_WEIGHTS[HealthComponent.ASH_AVAILABILITY] +
                soft_edge_response * self.SHI_WEIGHTS[HealthComponent.SOFT_EDGE_RESPONSE]
            )
            
            # Apply sensitivity adjustment
            shi_value = max(0.0, min(1.0, shi_value * self.health_sensitivity))
            
            # Classify health level
            health_level = self._classify_health_level(shi_value)
            
            # Calculate health trend
            health_trend = self._calculate_health_trend(shi_value)
            
            # Analyze components for alerts and recommendations
            component_breakdown = {
                "vitality": vitality,
                "memory_health": memory_health,
                "orbit_load": orbit_load,
                "ash_availability": ash_availability,
                "soft_edge_response": soft_edge_response,
                "weighted_contributions": {
                    f"{comp.value}_contribution": value * self.SHI_WEIGHTS[comp] 
                    for comp, value in [
                        (HealthComponent.VITALITY, vitality),
                        (HealthComponent.MEMORY_HEALTH, memory_health),
                        (HealthComponent.ORBIT_LOAD, orbit_load),
                        (HealthComponent.ASH_AVAILABILITY, ash_availability),
                        (HealthComponent.SOFT_EDGE_RESPONSE, soft_edge_response)
                    ]
                }
            }
            
            health_alerts = self._generate_health_alerts(
                vitality, memory_health, orbit_load, ash_availability, soft_edge_response, health_level
            )
            
            recommendations = self._generate_health_recommendations(
                vitality, memory_health, orbit_load, ash_availability, soft_edge_response, health_level, state
            )
            
            intervention_priority = self._calculate_intervention_priority(
                shi_value, health_level, health_alerts
            )
            
            # Create comprehensive reading
            reading = HealthReading(
                timestamp=current_time,
                vitality=vitality,
                memory_health=memory_health,
                orbit_load=orbit_load,
                ash_availability=ash_availability,
                soft_edge_response=soft_edge_response,
                shi_value=shi_value,
                health_level=health_level,
                health_trend=health_trend,
                component_breakdown=component_breakdown,
                health_alerts=health_alerts,
                recommendations=recommendations,
                intervention_priority=intervention_priority
            )
            
            # Update state
            self.state.readings_history.append(reading)
            self.state.last_reading = reading
            self.state.assessments_count += 1
            self._update_health_metrics()
            
            # Execute interventions if needed
            self._execute_health_interventions(reading, state)
            
            assessment_time = time.time() - assessment_start
            logger.debug(f"❤️ [HEALTH] SHI={shi_value:.3f} ({health_level.value}) V:{vitality:.2f} M:{memory_health:.2f} O:{orbit_load:.2f} A:{ash_availability:.2f} S:{soft_edge_response:.2f} [{assessment_time*1000:.1f}ms]")
            
            return reading
            
        except Exception as e:
            logger.error(f"❤️ [HEALTH] SHI calculation error: {e}")
            # Return safe fallback reading
            return HealthReading(
                timestamp=time.time(),
                vitality=0.5, memory_health=0.5, orbit_load=0.5,
                ash_availability=0.5, soft_edge_response=0.5,
                shi_value=0.5, health_level=HealthLevel.FAIR, health_trend=0.0,
                health_alerts=["Error in health calculation"],
                recommendations=["Check health monitor integrity"]
            )
    
    def _extract_vitality(self, state: Dict[str, Any]) -> float:
        """Extract and normalize system vitality (V)"""
        
        # Combine multiple vitality indicators
        base_vitality = state.get('system_vitality', 0.5)
        energy_level = state.get('cognitive_energy', 0.5)
        responsiveness = state.get('system_responsiveness', 0.5)
        uptime_ratio = min(1.0, state.get('uptime_hours', 0) / 24.0)  # Normalize to daily cycle
        
        # Calculate composite vitality
        vitality = (base_vitality * 0.4 + energy_level * 0.3 + 
                   responsiveness * 0.2 + uptime_ratio * 0.1)
        
        return max(0.0, min(1.0, vitality))
    
    def _extract_memory_health(self, state: Dict[str, Any]) -> float:
        """Extract and normalize memory health (M)"""
        
        # Memory system health indicators
        memory_coherence = state.get('memory_coherence', 0.5)
        memory_stability = state.get('memory_stability', 0.5)
        memory_fragmentation = 1.0 - state.get('memory_fragmentation', 0.5)  # Inverted
        memory_accessibility = state.get('memory_accessibility', 0.5)
        
        # Calculate composite memory health
        memory_health = (memory_coherence * 0.35 + memory_stability * 0.25 +
                        memory_fragmentation * 0.25 + memory_accessibility * 0.15)
        
        return max(0.0, min(1.0, memory_health))
    
    def _extract_orbit_load(self, state: Dict[str, Any]) -> float:
        """Extract and normalize orbit load (O) - inverted for health"""
        
        # Processing load indicators (higher load = lower health)
        processing_load = state.get('processing_orbit_load', 0.5)
        cpu_utilization = state.get('cpu_utilization', 0.5)
        queue_depth = min(1.0, state.get('processing_queue_depth', 0) / 100.0)
        concurrent_tasks = min(1.0, state.get('concurrent_task_count', 0) / 50.0)
        
        # Calculate composite load (higher values = more load)
        raw_load = (processing_load * 0.4 + cpu_utilization * 0.3 +
                   queue_depth * 0.2 + concurrent_tasks * 0.1)
        
        # Invert for health calculation (lower load = better health)
        orbit_health = 1.0 - raw_load
        
        return max(0.0, min(1.0, orbit_health))
    
    def _extract_ash_availability(self, state: Dict[str, Any]) -> float:
        """Extract and normalize cognitive ash availability (A)"""
        
        # Cognitive resource indicators
        ash_level = state.get('cognitive_ash_level', 0.5)
        resource_availability = state.get('cognitive_resources_available', 0.5)
        processing_capacity = state.get('available_processing_capacity', 0.5)
        memory_headroom = state.get('memory_headroom', 0.5)
        
        # Calculate composite resource availability
        ash_availability = (ash_level * 0.4 + resource_availability * 0.3 +
                          processing_capacity * 0.2 + memory_headroom * 0.1)
        
        return max(0.0, min(1.0, ash_availability))
    
    def _extract_soft_edge_response(self, state: Dict[str, Any]) -> float:
        """Extract and normalize soft edge responsiveness (S)"""
        
        # Adaptability and flexibility indicators
        adaptability = state.get('soft_edge_responsiveness', 0.5)
        flexibility = state.get('cognitive_flexibility', 0.5)
        learning_rate = state.get('learning_adaptation_rate', 0.5)
        context_switching = state.get('context_switching_efficiency', 0.5)
        
        # Calculate composite soft edge response
        soft_edge_response = (adaptability * 0.4 + flexibility * 0.25 +
                            learning_rate * 0.2 + context_switching * 0.15)
        
        return max(0.0, min(1.0, soft_edge_response))
    
    def _classify_health_level(self, shi_value: float) -> HealthLevel:
        """Classify health level based on SHI value"""
        
        if shi_value >= self.HEALTH_THRESHOLDS[HealthLevel.EXCELLENT]:
            return HealthLevel.EXCELLENT
        elif shi_value >= self.HEALTH_THRESHOLDS[HealthLevel.GOOD]:
            return HealthLevel.GOOD
        elif shi_value >= self.HEALTH_THRESHOLDS[HealthLevel.FAIR]:
            return HealthLevel.FAIR
        elif shi_value >= self.HEALTH_THRESHOLDS[HealthLevel.POOR]:
            return HealthLevel.POOR
        else:
            return HealthLevel.CRITICAL
    
    def _calculate_health_trend(self, current_shi: float) -> float:
        """Calculate rate of health change"""
        
        if len(self.state.readings_history) < 2:
            return 0.0
        
        recent_readings = list(self.state.readings_history)[-self.stability_window:]
        shi_values = [r.shi_value for r in recent_readings] + [current_shi]
        
        # Calculate trend using linear regression
        if len(shi_values) >= 3:
            x = list(range(len(shi_values)))
            y = shi_values
            n = len(x)
            
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            
            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator > 0:
                trend = numerator / denominator
                
                # Apply smoothing if we have previous trend
                if self.state.last_reading:
                    prev_trend = self.state.last_reading.health_trend
                    return trend * (1 - self.trend_smoothing) + prev_trend * self.trend_smoothing
                
                return trend
        
        return 0.0
    
    def _generate_health_alerts(self, vitality: float, memory_health: float, 
                              orbit_load: float, ash_availability: float, 
                              soft_edge_response: float, health_level: HealthLevel) -> List[str]:
        """Generate component-specific health alerts"""
        
        alerts = []
        
        # Critical system alerts
        if health_level == HealthLevel.CRITICAL:
            alerts.append("🚨 CRITICAL: Schema health emergency - immediate intervention required")
        elif health_level == HealthLevel.POOR:
            alerts.append("⚠️ WARNING: Poor schema health - urgent attention needed")
        
        # Component-specific alerts
        if vitality < self.COMPONENT_ALERT_THRESHOLDS[HealthComponent.VITALITY]:
            alerts.append(f"🔋 LOW VITALITY: {vitality:.2f} - system energy critically low")
        
        if memory_health < self.COMPONENT_ALERT_THRESHOLDS[HealthComponent.MEMORY_HEALTH]:
            alerts.append(f"🧠 MEMORY ISSUES: {memory_health:.2f} - memory system degraded")
        
        if orbit_load < self.COMPONENT_ALERT_THRESHOLDS[HealthComponent.ORBIT_LOAD]:
            # Remember: orbit_load is inverted, so low value = high actual load
            actual_load = 1.0 - orbit_load
            alerts.append(f"⚡ HIGH LOAD: {actual_load:.2f} - processing orbit overloaded")
        
        if ash_availability < self.COMPONENT_ALERT_THRESHOLDS[HealthComponent.ASH_AVAILABILITY]:
            alerts.append(f"🔥 ASH DEPLETION: {ash_availability:.2f} - cognitive resources low")
        
        if soft_edge_response < self.COMPONENT_ALERT_THRESHOLDS[HealthComponent.SOFT_EDGE_RESPONSE]:
            alerts.append(f"🌊 REDUCED ADAPTABILITY: {soft_edge_response:.2f} - flexibility compromised")
        
        return alerts
    
    def _generate_health_recommendations(self, vitality: float, memory_health: float,
                                       orbit_load: float, ash_availability: float,
                                       soft_edge_response: float, health_level: HealthLevel,
                                       state: Dict[str, Any]) -> List[str]:
        """Generate targeted health improvement recommendations"""
        
        recommendations = []
        
        # Overall health recommendations
        if health_level in [HealthLevel.CRITICAL, HealthLevel.POOR]:
            recommendations.extend([
                "🏥 Activate emergency health protocols",
                "🛑 Halt non-essential processing",
                "🔄 Initiate system recovery procedures"
            ])
        elif health_level == HealthLevel.FAIR:
            recommendations.extend([
                "🔧 Optimize system performance",
                "📊 Monitor health trends closely",
                "⚖️ Balance processing load"
            ])
        
        # Component-specific recommendations
        if vitality < 0.5:
            recommendations.extend([
                "💤 Schedule system rest periods",
                "⚡ Boost cognitive energy reserves",
                "🔋 Reduce energy-intensive operations"
            ])
        
        if memory_health < 0.5:
            recommendations.extend([
                "🧠 Execute memory consolidation",
                "🗂️ Defragment memory structures",
                "🔄 Refresh memory accessibility"
            ])
        
        if orbit_load < 0.5:  # High actual load
            recommendations.extend([
                "⏸️ Reduce concurrent processing",
                "📦 Clear processing queues",
                "🚦 Implement load balancing"
            ])
        
        if ash_availability < 0.5:
            recommendations.extend([
                "🔥 Restore cognitive ash reserves",
                "💾 Free up processing resources",
                "⚡ Optimize resource allocation"
            ])
        
        if soft_edge_response < 0.5:
            recommendations.extend([
                "🌊 Enhance adaptability systems",
                "🧘 Improve cognitive flexibility",
                "🔄 Practice context switching"
            ])
        
        # Proactive recommendations for good health
        if health_level in [HealthLevel.GOOD, HealthLevel.EXCELLENT]:
            recommendations.extend([
                "🚀 Consider performance enhancements",
                "🧠 Enable advanced cognitive features",
                "🌟 Maintain current health protocols"
            ])
        
        return recommendations
    
    def _calculate_intervention_priority(self, shi_value: float, health_level: HealthLevel, 
                                       alerts: List[str]) -> float:
        """Calculate priority level for health interventions"""
        
        base_priority = 1.0 - shi_value  # Lower health = higher priority
        
        # Level-based priority adjustment
        level_multipliers = {
            HealthLevel.CRITICAL: 1.0,
            HealthLevel.POOR: 0.8,
            HealthLevel.FAIR: 0.6,
            HealthLevel.GOOD: 0.3,
            HealthLevel.EXCELLENT: 0.1
        }
        
        level_priority = base_priority * level_multipliers[health_level]
        
        # Alert-based priority boost
        alert_boost = min(0.3, len(alerts) * 0.05)  # Up to 0.3 boost
        
        final_priority = min(1.0, level_priority + alert_boost)
        
        return final_priority
    
    def _update_health_metrics(self):
        """Update aggregate health metrics"""
        
        if not self.state.readings_history:
            return
        
        recent_readings = list(self.state.readings_history)
        shi_values = [r.shi_value for r in recent_readings]
        
        # Update average SHI
        self.state.average_shi = sum(shi_values) / len(shi_values)
        
        # Update lowest SHI
        self.state.lowest_shi = min(self.state.lowest_shi, shi_values[-1])
        
        # Count health incidents
        incident_threshold = self.HEALTH_THRESHOLDS[HealthLevel.POOR]
        recent_incidents = sum(1 for shi in shi_values if shi < incident_threshold)
        if recent_incidents > 0:
            self.state.health_incidents += 1
        
        # Calculate health stability
        if len(shi_values) > 1:
            variance = np.var(shi_values)
            self.state.health_stability = 1.0 / (1.0 + variance * 10)  # Normalized
        else:
            self.state.health_stability = 1.0
    
    def _execute_health_interventions(self, reading: HealthReading, state: Dict[str, Any]):
        """Execute automatic health interventions"""
        
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_intervention_time < self.intervention_cooldown:
            return
        
        interventions_executed = []
        
        # Critical health interventions
        if reading.health_level == HealthLevel.CRITICAL:
            if "emergency_health" not in self.active_interventions:
                self._trigger_emergency_health_protocol(reading, state)
                interventions_executed.append("emergency_health")
            
            if self.emergency_callback:
                try:
                    self.emergency_callback(reading, state)
                except Exception as e:
                    logger.error(f"❤️ [HEALTH] Emergency callback failed: {e}")
        
        # Poor health interventions
        elif reading.health_level == HealthLevel.POOR:
            if "health_recovery" not in self.active_interventions:
                self._trigger_health_recovery(reading, state)
                interventions_executed.append("health_recovery")
        
        # Update intervention tracking
        if interventions_executed:
            self.active_interventions.update(interventions_executed)
            self.state.interventions_triggered += len(interventions_executed)
            self.last_intervention_time = current_time
            
            # Execute callbacks
            for callback in self.health_callbacks:
                try:
                    callback(reading, interventions_executed)
                except Exception as e:
                    logger.warning(f"❤️ [HEALTH] Health callback failed: {e}")
    
    def _trigger_emergency_health_protocol(self, reading: HealthReading, state: Dict[str, Any]):
        """Trigger emergency health protocol"""
        
        logger.critical(f"🏥 [EMERGENCY_HEALTH] Activating emergency protocol - SHI: {reading.shi_value:.3f}")
        
        self._log_health_intervention("emergency_health_protocol", reading, {
            "trigger_shi": reading.shi_value,
            "critical_components": [
                comp for comp, value in [
                    ("vitality", reading.vitality),
                    ("memory_health", reading.memory_health),
                    ("orbit_load", reading.orbit_load),
                    ("ash_availability", reading.ash_availability),
                    ("soft_edge_response", reading.soft_edge_response)
                ] if value < 0.3
            ],
            "recommended_actions": reading.recommendations[:5]  # Top 5 actions
        })
    
    def _trigger_health_recovery(self, reading: HealthReading, state: Dict[str, Any]):
        """Trigger health recovery procedures"""
        
        logger.warning(f"🔄 [HEALTH_RECOVERY] Initiating recovery - SHI: {reading.shi_value:.3f}")
        
        self._log_health_intervention("health_recovery", reading, {
            "recovery_priority": reading.intervention_priority,
            "health_alerts": reading.health_alerts,
            "target_components": [
                comp for comp, value in [
                    ("vitality", reading.vitality),
                    ("memory_health", reading.memory_health),
                    ("orbit_load", reading.orbit_load),
                    ("ash_availability", reading.ash_availability),
                    ("soft_edge_response", reading.soft_edge_response)
                ] if value < 0.5
            ]
        })
    
    def _log_health_intervention(self, intervention_type: str, reading: HealthReading, details: Dict[str, Any]):
        """Log health intervention to file system"""
        
        log_entry = {
            "timestamp": reading.timestamp,
            "intervention_type": intervention_type,
            "health_state": {
                "shi_value": reading.shi_value,
                "health_level": reading.health_level.value,
                "vitality": reading.vitality,
                "memory_health": reading.memory_health,
                "orbit_load": reading.orbit_load,
                "ash_availability": reading.ash_availability,
                "soft_edge_response": reading.soft_edge_response,
                "health_trend": reading.health_trend,
                "intervention_priority": reading.intervention_priority
            },
            "details": details
        }
        
        # Write to health intervention log
        try:
            log_path = Path("runtime/logs/health_interventions.log")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, "a") as f:
                f.write(f"{json.dumps(log_entry)}\n")
                
        except Exception as e:
            logger.error(f"❤️ [HEALTH] Failed to log intervention: {e}")
    
    # Public interface methods
    
    def register_health_callback(self, callback: Callable):
        """Register callback for health notifications"""
        self.health_callbacks.append(callback)
        logger.info(f"❤️ [HEALTH] Registered health callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def register_emergency_callback(self, callback: Callable):
        """Register emergency health callback"""
        self.emergency_callback = callback
        logger.info("🏥 [HEALTH] Registered emergency health callback")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current health monitor state"""
        
        return {
            "current_reading": {
                "shi_value": self.state.last_reading.shi_value if self.state.last_reading else 0.5,
                "health_level": self.state.last_reading.health_level.value if self.state.last_reading else "fair",
                "vitality": self.state.last_reading.vitality if self.state.last_reading else 0.5,
                "memory_health": self.state.last_reading.memory_health if self.state.last_reading else 0.5,
                "orbit_load": self.state.last_reading.orbit_load if self.state.last_reading else 0.5,
                "ash_availability": self.state.last_reading.ash_availability if self.state.last_reading else 0.5,
                "soft_edge_response": self.state.last_reading.soft_edge_response if self.state.last_reading else 0.5,
                "health_trend": self.state.last_reading.health_trend if self.state.last_reading else 0.0,
                "intervention_priority": self.state.last_reading.intervention_priority if self.state.last_reading else 0.0,
                "health_alerts": self.state.last_reading.health_alerts if self.state.last_reading else [],
                "recommendations": self.state.last_reading.recommendations if self.state.last_reading else []
            } if self.state.last_reading else None,
            "metrics": {
                "assessments_count": self.state.assessments_count,
                "interventions_triggered": self.state.interventions_triggered,
                "health_incidents": self.state.health_incidents,
                "average_shi": self.state.average_shi,
                "lowest_shi": self.state.lowest_shi,
                "health_stability": self.state.health_stability
            },
            "active_interventions": list(self.active_interventions),
            "readings_history_length": len(self.state.readings_history)
        }
    
    def get_health_modulation(self) -> Dict[str, float]:
        """Get health-based modulation factors for other systems"""
        
        if not self.state.last_reading:
            return {
                "processing_efficiency": 1.0,
                "memory_optimization": 0.0,
                "resource_conservation": 0.0,
                "adaptability_enhancement": 1.0
            }
        
        reading = self.state.last_reading
        
        # Calculate modulation based on health level
        if reading.health_level == HealthLevel.CRITICAL:
            processing_efficiency = 0.3
            memory_optimization = 1.0
            resource_conservation = 1.0
            adaptability_enhancement = 0.5
        elif reading.health_level == HealthLevel.POOR:
            processing_efficiency = 0.6
            memory_optimization = 0.8
            resource_conservation = 0.8
            adaptability_enhancement = 0.7
        elif reading.health_level == HealthLevel.FAIR:
            processing_efficiency = 0.8
            memory_optimization = 0.5
            resource_conservation = 0.5
            adaptability_enhancement = 0.8
        elif reading.health_level == HealthLevel.GOOD:
            processing_efficiency = 1.0
            memory_optimization = 0.2
            resource_conservation = 0.2
            adaptability_enhancement = 1.0
        else:  # EXCELLENT
            processing_efficiency = 1.2  # Boost for excellent health
            memory_optimization = 0.0
            resource_conservation = 0.0
            adaptability_enhancement = 1.2
        
        return {
            "processing_efficiency": processing_efficiency,
            "memory_optimization": memory_optimization,
            "resource_conservation": resource_conservation,
            "adaptability_enhancement": adaptability_enhancement,
            "health_priority": reading.intervention_priority,
            "system_wellness": reading.shi_value
        }

# Global health monitor instance
_global_health_monitor: Optional[SchemaHealthMonitor] = None

def get_schema_health_monitor() -> SchemaHealthMonitor:
    """Get global schema health monitor instance"""
    global _global_health_monitor
    if _global_health_monitor is None:
        _global_health_monitor = SchemaHealthMonitor()
    return _global_health_monitor

def calculate_schema_health(state: Dict[str, Any]) -> HealthReading:
    """Convenience function to calculate schema health"""
    monitor = get_schema_health_monitor()
    return monitor.calculate_shi(state)

def get_health_modulation() -> Dict[str, float]:
    """Convenience function to get health-based modulation"""
    monitor = get_schema_health_monitor()
    return monitor.get_health_modulation()

# Export key classes and functions
__all__ = [
    'SchemaHealthMonitor',
    'HealthReading',
    'HealthLevel',
    'HealthComponent',
    'get_schema_health_monitor',
    'calculate_schema_health',
    'get_health_modulation'
] 