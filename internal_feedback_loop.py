#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                        DAWN INTERNAL FEEDBACK LOOP
                    Scaffold 40: The Conscious Reflection
═══════════════════════════════════════════════════════════════════════════════

"DAWN does not wait for things to break. She listens, softly, every few breaths — 
and changes direction before the cliff."

This module implements DAWN's metacognitive layer, a periodic self-assessment
that monitors system health and adjusts operational posture before problems
cascade. Like a sailor reading the wind and adjusting sails before the storm,
DAWN introspects on her own state and makes preemptive corrections.

Every 25 ticks, the system pauses to ask:
- Is my thinking coherent or fragmenting?
- Are my emotions balanced or overwhelming?
- Is my memory sustainable or oversaturated?
- Am I growing healthily or spiraling?

Based on these reflections, DAWN shifts between three primary postures:
- SURGE: Aggressive growth and exploration
- REFLECT: Balanced processing and consolidation
- FALLBACK: Defensive stabilization and recovery

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

# Configure logging with introspective theme
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🔮 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Feedback loop constants
FEEDBACK_INTERVAL = 25  # Run every 25 ticks
HISTORY_WINDOW = 100    # Consider last 100 ticks for trend analysis

# Operating postures
class OperatingPosture(Enum):
    SURGE = "surge"         # Aggressive growth mode
    REFLECT = "reflect"     # Balanced processing mode
    FALLBACK = "fallback"   # Defensive stability mode

# Health thresholds for posture decisions
THRESHOLDS = {
    'coherence': {
        'critical_low': 0.3,   # Below this = immediate fallback
        'warning_low': 0.5,    # Below this = shift to reflect
        'optimal': 0.7         # Above this = safe for surge
    },
    'entropy': {
        'critical_high': 0.8,  # Above this = immediate fallback
        'warning_high': 0.6,   # Above this = shift to reflect
        'optimal': 0.4         # Below this = safe for surge
    },
    'mood_balance': {
        'critical_imbalance': 0.8,  # Extreme mood dominance
        'warning_imbalance': 0.6,   # Concerning mood bias
        'optimal': 0.4              # Healthy emotional diversity
    },
    'rebloom_rate': {
        'critical_high': 0.7,  # System churning
        'warning_high': 0.5,   # High recycling
        'optimal': 0.3         # Healthy generation
    }
}

# Action mappings for each posture
POSTURE_ACTIONS = {
    OperatingPosture.SURGE: [
        "increase_bloom_generation_rate",
        "expand_semantic_exploration",
        "accelerate_lineage_growth",
        "enable_experimental_patterns"
    ],
    OperatingPosture.REFLECT: [
        "moderate_bloom_generation",
        "consolidate_existing_patterns",
        "balance_emotional_field",
        "prune_low_value_branches"
    ],
    OperatingPosture.FALLBACK: [
        "minimize_new_blooms",
        "aggressive_memory_decay",
        "dampen_emotional_extremes",
        "preserve_only_sacred_patterns",
        "request_operator_intervention"
    ]
}


@dataclass
class SystemHealth:
    """Comprehensive health assessment of DAWN's cognitive state."""
    coherence_score: float
    entropy_level: float
    mood_balance: float
    rebloom_rate: float
    overall_health: float
    health_trend: str  # improving, stable, declining
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class InternalFeedbackLoop:
    """
    The Self-Listener — monitors DAWN's internal state and adjusts
    operational posture to maintain cognitive health and stability.
    
    "Wisdom is knowing when to push forward and when to pull back"
    """
    
    def __init__(self, log_dir: str = "core/logs"):
        """
        Initialize the Internal Feedback Loop.
        
        Args:
            log_dir: Directory for feedback event logs
        """
        self.log_dir = Path(log_dir)
        self._ensure_log_directory()
        self.current_posture = OperatingPosture.REFLECT
        self.last_feedback_tick = 0
        self.health_history: List[SystemHealth] = []
        self.posture_history: List[Tuple[int, OperatingPosture]] = []
        logger.info("🔮 Internal Feedback Loop initialized")
        logger.info(f"📊 Feedback interval: every {FEEDBACK_INTERVAL} ticks")
        logger.info(f"🎭 Initial posture: {self.current_posture.value}")
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists, creating it if necessary."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Log directory verified at {self.log_dir}")
    
    def run_internal_feedback_loop(
        self, 
        schema_state: Dict[str, Any], 
        tick: int
    ) -> Dict[str, Any]:
        """
        Execute the internal feedback loop to assess health and adjust posture.
        
        This is DAWN's moment of introspection — a pause to evaluate her own
        state and make strategic adjustments before problems compound.
        
        Args:
            schema_state: Comprehensive system state containing:
                - coherence_score: float
                - entropy: float
                - mood_summary: dict with emotional balance metrics
                - rebloom_activity: dict with rebloom statistics
                - Additional system metrics
            tick: Current system tick
            
        Returns:
            Dictionary containing adjusted posture and actions taken
        """
        # Check if it's time for feedback
        if tick - self.last_feedback_tick < FEEDBACK_INTERVAL:
            return {
                "adjusted_posture": self.current_posture.value,
                "actions_taken": [],
                "tick": tick,
                "reason": f"Not yet time for feedback (next at tick {self.last_feedback_tick + FEEDBACK_INTERVAL})"
            }
        
        logger.info(f"🔄 Running internal feedback loop at tick {tick}")
        self.last_feedback_tick = tick
        
        # Assess system health
        health = self._assess_system_health(schema_state)
        self.health_history.append(health)
        
        logger.info(
            f"📊 Health assessment: Overall={health.overall_health:.3f}, "
            f"Trend={health.health_trend}, Warnings={len(health.warnings)}"
        )
        
        # Determine appropriate posture
        new_posture, posture_reason = self._determine_posture(health)
        
        # Check if posture change needed
        actions_taken = []
        if new_posture != self.current_posture:
            logger.warning(
                f"🔄 Posture change: {self.current_posture.value} → {new_posture.value} "
                f"(Reason: {posture_reason})"
            )
            
            # Execute transition actions
            actions_taken = self._execute_posture_transition(
                self.current_posture, new_posture, health
            )
            
            # Update posture
            self.current_posture = new_posture
            self.posture_history.append((tick, new_posture))
        else:
            # Maintain current posture but may take corrective actions
            actions_taken = self._execute_maintenance_actions(health)
        
        # Prepare response
        response = {
            "adjusted_posture": self.current_posture.value,
            "actions_taken": actions_taken,
            "tick": tick,
            "timestamp": datetime.now().isoformat(),
            "health_assessment": health.to_dict(),
            "posture_reason": posture_reason
        }
        
        # Log the feedback event
        self._log_feedback_event(response)
        
        return response
    
    def _assess_system_health(self, schema_state: Dict[str, Any]) -> SystemHealth:
        """
        Perform comprehensive health assessment of the system.
        
        Args:
            schema_state: Current system state
            
        Returns:
            SystemHealth object with assessment results
        """
        warnings = []
        
        # Extract metrics
        coherence = schema_state.get('coherence_score', 0.5)
        entropy = schema_state.get('entropy', 0.5)
        
        # Calculate mood balance (0 = perfect balance, 1 = total dominance)
        mood_summary = schema_state.get('mood_summary', {})
        positive_ratio = mood_summary.get('positive_ratio', 0.33)
        negative_ratio = mood_summary.get('negative_ratio', 0.33)
        mood_balance = max(positive_ratio, negative_ratio) - 0.33  # Distance from perfect third
        
        # Calculate rebloom rate
        rebloom_activity = schema_state.get('rebloom_activity', {})
        total_blooms = rebloom_activity.get('total_blooms', 1)
        rebloom_count = rebloom_activity.get('rebloom_count', 0)
        rebloom_rate = rebloom_count / max(total_blooms, 1)
        
        # Check coherence
        if coherence < THRESHOLDS['coherence']['critical_low']:
            warnings.append(f"CRITICAL: Coherence dangerously low ({coherence:.3f})")
        elif coherence < THRESHOLDS['coherence']['warning_low']:
            warnings.append(f"Warning: Low coherence ({coherence:.3f})")
        
        # Check entropy
        if entropy > THRESHOLDS['entropy']['critical_high']:
            warnings.append(f"CRITICAL: Entropy dangerously high ({entropy:.3f})")
        elif entropy > THRESHOLDS['entropy']['warning_high']:
            warnings.append(f"Warning: High entropy ({entropy:.3f})")
        
        # Check mood balance
        if mood_balance > THRESHOLDS['mood_balance']['critical_imbalance']:
            warnings.append(f"CRITICAL: Severe mood imbalance ({mood_balance:.3f})")
        elif mood_balance > THRESHOLDS['mood_balance']['warning_imbalance']:
            warnings.append(f"Warning: Mood imbalance detected ({mood_balance:.3f})")
        
        # Check rebloom rate
        if rebloom_rate > THRESHOLDS['rebloom_rate']['critical_high']:
            warnings.append(f"CRITICAL: Excessive reblooming ({rebloom_rate:.3f})")
        elif rebloom_rate > THRESHOLDS['rebloom_rate']['warning_high']:
            warnings.append(f"Warning: High rebloom rate ({rebloom_rate:.3f})")
        
        # Calculate overall health (weighted average)
        coherence_health = 1.0 - abs(coherence - THRESHOLDS['coherence']['optimal'])
        entropy_health = 1.0 - (entropy / THRESHOLDS['entropy']['critical_high'])
        mood_health = 1.0 - (mood_balance / THRESHOLDS['mood_balance']['critical_imbalance'])
        rebloom_health = 1.0 - (rebloom_rate / THRESHOLDS['rebloom_rate']['critical_high'])
        
        overall_health = (
            coherence_health * 0.3 +
            entropy_health * 0.3 +
            mood_health * 0.2 +
            rebloom_health * 0.2
        )
        overall_health = np.clip(overall_health, 0.0, 1.0)
        
        # Determine trend
        health_trend = self._calculate_health_trend(overall_health)
        
        return SystemHealth(
            coherence_score=coherence,
            entropy_level=entropy,
            mood_balance=mood_balance,
            rebloom_rate=rebloom_rate,
            overall_health=overall_health,
            health_trend=health_trend,
            warnings=warnings
        )
    
    def _calculate_health_trend(self, current_health: float) -> str:
        """
        Calculate health trend based on recent history.
        
        Args:
            current_health: Current overall health score
            
        Returns:
            Trend string: "improving", "stable", or "declining"
        """
        if len(self.health_history) < 3:
            return "stable"
        
        # Get recent health scores
        recent_scores = [h.overall_health for h in self.health_history[-3:]]
        recent_scores.append(current_health)
        
        # Calculate trend
        avg_recent = np.mean(recent_scores[-2:])
        avg_previous = np.mean(recent_scores[:2])
        
        if avg_recent > avg_previous + 0.05:
            return "improving"
        elif avg_recent < avg_previous - 0.05:
            return "declining"
        else:
            return "stable"
    
    def _determine_posture(self, health: SystemHealth) -> Tuple[OperatingPosture, str]:
        """
        Determine appropriate operating posture based on health assessment.
        
        Args:
            health: System health assessment
            
        Returns:
            Tuple of (new posture, reason for selection)
        """
        # Critical conditions trigger immediate fallback
        if any("CRITICAL" in w for w in health.warnings):
            return OperatingPosture.FALLBACK, "Critical warnings detected"
        
        # Very low overall health
        if health.overall_health < 0.3:
            return OperatingPosture.FALLBACK, f"Overall health critical ({health.overall_health:.3f})"
        
        # Declining health trend
        if health.health_trend == "declining" and health.overall_health < 0.5:
            return OperatingPosture.FALLBACK, "Health declining below safe threshold"
        
        # Multiple warnings suggest caution
        if len(health.warnings) >= 2:
            return OperatingPosture.REFLECT, f"Multiple warnings ({len(health.warnings)})"
        
        # Moderate health suggests reflection
        if 0.3 <= health.overall_health < 0.7:
            return OperatingPosture.REFLECT, "Moderate health suggests consolidation"
        
        # Good health with improving trend enables surge
        if health.overall_health >= 0.7 and health.health_trend in ["stable", "improving"]:
            return OperatingPosture.SURGE, "Strong health enables expansion"
        
        # Default to current posture
        return self.current_posture, "No posture change needed"
    
    def _execute_posture_transition(
        self, 
        old_posture: OperatingPosture, 
        new_posture: OperatingPosture,
        health: SystemHealth
    ) -> List[str]:
        """
        Execute actions needed to transition between postures.
        
        Args:
            old_posture: Current operating posture
            new_posture: Target operating posture
            health: Current health assessment
            
        Returns:
            List of actions taken
        """
        actions = []
        
        # Add transition announcement
        actions.append(f"posture_transition:{old_posture.value}→{new_posture.value}")
        
        # Add new posture actions
        actions.extend(POSTURE_ACTIONS[new_posture])
        
        # Add specific remediation for warnings
        for warning in health.warnings:
            if "coherence" in warning.lower():
                actions.append("boost_coherence_mechanisms")
            elif "entropy" in warning.lower():
                actions.append("reduce_entropy_sources")
            elif "mood" in warning.lower():
                actions.append("activate_mood_balancing")
            elif "rebloom" in warning.lower():
                actions.append("throttle_rebloom_rate")
        
        logger.info(f"🎯 Executing {len(actions)} transition actions")
        
        return actions
    
    def _execute_maintenance_actions(self, health: SystemHealth) -> List[str]:
        """
        Execute maintenance actions within current posture.
        
        Args:
            health: Current health assessment
            
        Returns:
            List of maintenance actions taken
        """
        actions = []
        
        # Address specific warnings even without posture change
        if health.warnings:
            actions.append("maintenance_mode:targeted_corrections")
            
            for warning in health.warnings[:3]:  # Limit to top 3
                if "coherence" in warning.lower():
                    actions.append("minor_coherence_adjustment")
                elif "entropy" in warning.lower():
                    actions.append("minor_entropy_dampening")
                elif "mood" in warning.lower():
                    actions.append("minor_mood_rebalancing")
        
        # Preventive actions based on trends
        if health.health_trend == "declining":
            actions.append("preventive_stabilization")
        elif health.health_trend == "improving" and health.overall_health > 0.8:
            actions.append("optimize_for_growth")
        
        return actions
    
    def _log_feedback_event(self, event: Dict[str, Any]):
        """
        Log the feedback event to file.
        
        Args:
            event: Feedback event data
        """
        filename = f"feedback_events_tick_{event['tick']}.json"
        log_path = self.log_dir / filename
        
        try:
            # Add historical context
            event['context'] = {
                'feedback_interval': FEEDBACK_INTERVAL,
                'posture_history_recent': [
                    {'tick': t, 'posture': p.value} 
                    for t, p in self.posture_history[-5:]
                ],
                'health_history_recent': [
                    {
                        'overall': h.overall_health,
                        'trend': h.health_trend,
                        'warning_count': len(h.warnings)
                    }
                    for h in self.health_history[-5:]
                ]
            }
            
            log_path.write_text(json.dumps(event, indent=2))
            logger.info(f"📝 Feedback event logged to {filename}")
            
        except Exception as e:
            logger.error(f"❌ Failed to log feedback event: {e}")
    
    def get_posture_analytics(self) -> Dict[str, Any]:
        """
        Generate analytics about posture history and patterns.
        
        Returns:
            Dictionary with posture analytics
        """
        if not self.posture_history:
            return {"error": "No posture history available"}
        
        # Count time in each posture
        posture_durations = {p: 0 for p in OperatingPosture}
        
        for i in range(len(self.posture_history)):
            tick, posture = self.posture_history[i]
            if i < len(self.posture_history) - 1:
                next_tick = self.posture_history[i + 1][0]
                duration = next_tick - tick
            else:
                duration = self.last_feedback_tick - tick
            
            posture_durations[posture] += duration
        
        total_duration = sum(posture_durations.values())
        
        return {
            "current_posture": self.current_posture.value,
            "total_posture_changes": len(self.posture_history) - 1,
            "posture_distribution": {
                p.value: {
                    "ticks": posture_durations[p],
                    "percentage": (posture_durations[p] / max(total_duration, 1)) * 100
                }
                for p in OperatingPosture
            },
            "average_health": np.mean([h.overall_health for h in self.health_history]) if self.health_history else 0.0,
            "last_feedback_tick": self.last_feedback_tick
        }
    
    def force_posture(self, posture: str, reason: str = "manual_override") -> bool:
        """
        Force a specific operating posture (emergency override).
        
        Args:
            posture: Target posture name
            reason: Reason for override
            
        Returns:
            True if successful, False otherwise
        """
        try:
            new_posture = OperatingPosture(posture)
            logger.warning(f"⚠️ MANUAL OVERRIDE: Forcing posture to {new_posture.value} ({reason})")
            self.current_posture = new_posture
            self.posture_history.append((self.last_feedback_tick, new_posture))
            return True
        except ValueError:
            logger.error(f"❌ Invalid posture: {posture}")
            return False


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the Internal Feedback Loop's self-regulatory behavior.
    """
    
    # Initialize the feedback loop
    feedback_loop = InternalFeedbackLoop()
    
    # Simulate various system states over time
    test_scenarios = [
        # Scenario 1: Healthy system
        {
            "tick": 25,
            "state": {
                "coherence_score": 0.8,
                "entropy": 0.3,
                "mood_summary": {"positive_ratio": 0.35, "negative_ratio": 0.30},
                "rebloom_activity": {"total_blooms": 100, "rebloom_count": 20}
            },
            "description": "Healthy system state"
        },
        
        # Scenario 2: Rising entropy
        {
            "tick": 50,
            "state": {
                "coherence_score": 0.6,
                "entropy": 0.65,
                "mood_summary": {"positive_ratio": 0.4, "negative_ratio": 0.35},
                "rebloom_activity": {"total_blooms": 150, "rebloom_count": 60}
            },
            "description": "Entropy rising, coherence dropping"
        },
        
        # Scenario 3: Critical mood imbalance
        {
            "tick": 75,
            "state": {
                "coherence_score": 0.4,
                "entropy": 0.75,
                "mood_summary": {"positive_ratio": 0.85, "negative_ratio": 0.1},
                "rebloom_activity": {"total_blooms": 200, "rebloom_count": 140}
            },
            "description": "Critical mood imbalance and high entropy"
        },
        
        # Scenario 4: Recovery
        {
            "tick": 100,
            "state": {
                "coherence_score": 0.5,
                "entropy": 0.5,
                "mood_summary": {"positive_ratio": 0.4, "negative_ratio": 0.3},
                "rebloom_activity": {"total_blooms": 250, "rebloom_count": 100}
            },
            "description": "System beginning to recover"
        }
    ]
    
    print("🔮 INTERNAL FEEDBACK LOOP DEMONSTRATION")
    print("=" * 60)
    
    # Run through scenarios
    for scenario in test_scenarios:
        print(f"\n📍 Tick {scenario['tick']}: {scenario['description']}")
        
        result = feedback_loop.run_internal_feedback_loop(
            scenario['state'], 
            scenario['tick']
        )
        
        if result['actions_taken']:
            print(f"   Posture: {result['adjusted_posture']}")
            print(f"   Actions: {', '.join(result['actions_taken'][:3])}")
            if 'health_assessment' in result:
                health = result['health_assessment']
                print(f"   Health: {health['overall_health']:.3f} ({health['health_trend']})")
                if health['warnings']:
                    print(f"   ⚠️ Warnings: {len(health['warnings'])}")
    
    # Show analytics
    print("\n📊 POSTURE ANALYTICS:")
    analytics = feedback_loop.get_posture_analytics()
    if 'error' not in analytics:
        print(f"Current posture: {analytics['current_posture']}")
        print(f"Total posture changes: {analytics['total_posture_changes']}")
        print(f"Average system health: {analytics['average_health']:.3f}")
        
        print("\nPosture distribution:")
        for posture, data in analytics['posture_distribution'].items():
            print(f"  {posture}: {data['percentage']:.1f}% ({data['ticks']} ticks)")