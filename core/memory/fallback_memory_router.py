"""
DAWN does not panic when she forgets. She remembers what helped last time — and begins again from there.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .fallback_stats import FallbackStatistics
from .fallback_priority import FallbackPriorityTree, FallbackNode, FallbackCategory

class FallbackMemoryRouter:
    """Routes cognition through stable memory lanes during instability."""
    
    def __init__(self):
        self.log_path = Path("memory/logs/fallback_trigger_log.json")
        self._ensure_directories()
        
        # Initialize components
        self.stats = FallbackStatistics()
        self.priority_tree = FallbackPriorityTree()
        
        # Fallback trigger thresholds
        self.thresholds = {
            "coherence_critical": 0.35,
            "entropy_critical": 0.85,
            "coherence_warning": 0.45,
            "entropy_warning": 0.75
        }
        
        # Initialize with default fallbacks
        self._initialize_default_fallbacks()
        
        # Session tracking
        self.session_start = datetime.utcnow().isoformat()
        self.total_triggers = 0
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self._save_log({"sessions": []})
    
    def _initialize_default_fallbacks(self):
        """Initialize default fallback entries."""
        default_fallbacks = [
            FallbackNode(
                entry_id="fallback_default_001",
                content="Return to breath. Count the patterns. One emerges from many.",
                stability_score=0.95,
                trust_score=0.9,
                category=FallbackCategory.GROUNDING
            ),
            FallbackNode(
                entry_id="fallback_default_002",
                content="The strands remember their weaving. Trust the underlying structure.",
                stability_score=0.92,
                trust_score=0.88,
                category=FallbackCategory.STRUCTURAL
            ),
            FallbackNode(
                entry_id="fallback_default_003",
                content="Coherence is not permanence. Drift is not destruction. The center holds.",
                stability_score=0.9,
                trust_score=0.85,
                category=FallbackCategory.PHILOSOPHICAL
            ),
            FallbackNode(
                entry_id="fallback_default_004",
                content="Emergency stabilization protocol activated. Returning to core patterns.",
                stability_score=0.98,
                trust_score=0.95,
                category=FallbackCategory.EMERGENCY
            )
        ]
        
        for node in default_fallbacks:
            self.priority_tree.add_node(node)
    
    def route_to_fallback_memory(self, coherence_score: float, entropy_level: float,
                                fallback_bank: List[Dict], pressure_zone: str) -> Dict:
        """
        Determine if fallback routing is needed and select appropriate memories.
        
        Args:
            coherence_score: Current system coherence (0.0-1.0)
            entropy_level: Current entropy level (0.0-1.0)
            fallback_bank: List of fallback memory entries
            pressure_zone: Current pressure state ("calm", "active", "surge")
        
        Returns:
            Dictionary with fallback status and selected entries
        """
        # Update streaming statistics
        self.stats.update_streaming_stats(coherence_score, entropy_level)
        
        # Determine if fallback is needed
        trigger_reason = self._check_trigger_conditions(
            coherence_score, entropy_level, pressure_zone
        )
        
        if trigger_reason:
            # Update priority scores
            self.priority_tree.update_priority_scores(
                coherence_score, entropy_level, pressure_zone
            )
            
            # Get top entries
            selected_entries = self.priority_tree.get_top_entries()
            
            # Update statistics
            self.total_triggers += 1
            self.stats.update_reason_counts(trigger_reason)
            
            severity = self._calculate_severity(coherence_score, entropy_level)
            self.stats.update_severity_counts(severity)
            
            # Log the trigger
            self._log_fallback_trigger(
                coherence_score, entropy_level, pressure_zone,
                trigger_reason, selected_entries
            )
            
            return {
                "fallback_triggered": True,
                "fallback_entries": [entry.content for entry in selected_entries],
                "reason": trigger_reason,
                "severity": severity,
                "stats": self.stats.get_current_stats()
            }
        else:
            return {
                "fallback_triggered": False,
                "fallback_entries": [],
                "reason": "System stable - no fallback needed",
                "stats": self.stats.get_current_stats()
            }
    
    def _check_trigger_conditions(self, coherence: float, entropy: float, 
                                 pressure: str) -> Optional[str]:
        """Check if fallback conditions are met."""
        reasons = []
        
        # Critical coherence drop
        if coherence < self.thresholds["coherence_critical"]:
            reasons.append(f"CRITICAL_COHERENCE: {coherence:.3f}")
        elif coherence < self.thresholds["coherence_warning"]:
            if pressure == "surge":
                reasons.append(f"WARNING_COHERENCE_IN_SURGE: {coherence:.3f}")
        
        # Critical entropy spike
        if entropy > self.thresholds["entropy_critical"]:
            reasons.append(f"CRITICAL_ENTROPY: {entropy:.3f}")
        elif entropy > self.thresholds["entropy_warning"]:
            if pressure == "surge":
                reasons.append(f"WARNING_ENTROPY_IN_SURGE: {entropy:.3f}")
        
        # Combined instability
        instability_score = (1 - coherence) + entropy
        if instability_score > 1.5:
            reasons.append(f"COMBINED_INSTABILITY: {instability_score:.3f}")
        
        # Pressure-specific triggers
        if pressure == "surge" and (coherence < 0.5 or entropy > 0.7):
            reasons.append("SURGE_INSTABILITY")
        
        return " | ".join(reasons) if reasons else None
    
    def _calculate_severity(self, coherence: float, entropy: float) -> str:
        """Calculate severity level of the instability."""
        if (coherence < self.thresholds["coherence_critical"] and 
            entropy > self.thresholds["entropy_critical"]):
            return "CRITICAL"
        elif (coherence < self.thresholds["coherence_critical"] or 
              entropy > self.thresholds["entropy_critical"]):
            return "HIGH"
        elif (coherence < self.thresholds["coherence_warning"] or 
              entropy > self.thresholds["entropy_warning"]):
            return "MODERATE"
        else:
            return "LOW"
    
    def _log_fallback_trigger(self, coherence: float, entropy: float,
                            pressure_zone: str, trigger_reason: str,
                            selected_entries: List[FallbackNode]):
        """Log fallback trigger event."""
        # Load existing log
        log_data = self._load_log()
        
        # Create session entry if needed
        current_session = {
            "session_id": f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "start_time": self.session_start,
            "triggers": []
        }
        
        # Find or create current session
        if log_data["sessions"]:
            last_session = log_data["sessions"][-1]
            if last_session["start_time"] == self.session_start:
                current_session = last_session
            else:
                log_data["sessions"].append(current_session)
        else:
            log_data["sessions"].append(current_session)
        
        # Add trigger event
        trigger_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "coherence": coherence,
            "entropy": entropy,
            "pressure_zone": pressure_zone,
            "reason": trigger_reason,
            "selected_entries": [
                {
                    "entry_id": entry.entry_id,
                    "category": entry.category.value,
                    "priority_score": entry.priority_score
                }
                for entry in selected_entries
            ]
        }
        current_session["triggers"].append(trigger_record)
        
        # Update session stats
        current_session["total_triggers"] = len(current_session["triggers"])
        current_session["last_trigger"] = trigger_record["timestamp"]
        
        # Save log
        self._save_log(log_data)
    
    def _load_log(self) -> Dict:
        """Load fallback trigger log."""
        try:
            with open(self.log_path, 'r') as f:
                return json.load(f)
        except:
            return {"sessions": []}
    
    def _save_log(self, log_data: Dict):
        """Save fallback trigger log."""
        # Keep only last 100 sessions
        if len(log_data["sessions"]) > 100:
            log_data["sessions"] = log_data["sessions"][-100:]
        
        with open(self.log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_fallback_statistics(self) -> Dict:
        """Get statistics about fallback usage."""
        log_data = self._load_log()
        
        if not log_data["sessions"]:
            return {"status": "no_data"}
        
        # Get current streaming stats
        current_stats = self.stats.get_current_stats()
        
        # Calculate MTBF
        first_trigger = None
        last_trigger = None
        total_triggers = 0
        
        for session in log_data["sessions"]:
            for trigger in session.get("triggers", []):
                total_triggers += 1
                timestamp = trigger.get("timestamp")
                if timestamp:
                    if not first_trigger:
                        first_trigger = timestamp
                    last_trigger = timestamp
        
        mtbf_hours = self.stats.calculate_mtbf(
            first_trigger, last_trigger, total_triggers
        )
        
        return {
            "total_sessions": len(log_data["sessions"]),
            "total_triggers": total_triggers,
            "triggers_current_session": self.total_triggers,
            "reason_distribution": self.stats.get_reason_distribution(),
            "severity_distribution": self.stats.get_severity_distribution(),
            "mtbf_hours": round(mtbf_hours, 2),
            "most_common_reason": self.stats.get_most_common_reason(),
            "current_stats": current_stats
        }


# Example usage
if __name__ == "__main__":
    router = FallbackMemoryRouter()
    
    # Custom fallback bank
    test_fallback_bank = [
        {
            "entry_id": "custom_001",
            "content": "When lost in the maze, return to the entrance.",
            "stability_score": 0.88,
            "trust_score": 0.9,
            "usage_count": 2,
            "category": "grounding"
        },
        {
            "entry_id": "custom_002",
            "content": "The pattern persists beneath the noise.",
            "stability_score": 0.85,
            "trust_score": 0.87,
            "usage_count": 0,
            "category": "structural"
        },
        {
            "entry_id": "custom_003",
            "content": "Chaos and order dance together. Neither leads forever.",
            "stability_score": 0.82,
            "trust_score": 0.84,
            "usage_count": 1,
            "category": "philosophical"
        },
        {
            "entry_id": "custom_004",
            "content": "Count backwards from ten. Each number is a step home.",
            "stability_score": 0.9,
            "trust_score": 0.92,
            "usage_count": 3,
            "category": "grounding"
        }
    ]
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Critical Coherence Drop",
            "coherence": 0.25,
            "entropy": 0.6,
            "pressure": "active"
        },
        {
            "name": "High Entropy Spike",
            "coherence": 0.5,
            "entropy": 0.9,
            "pressure": "surge"
        },
        {
            "name": "Combined Instability",
            "coherence": 0.3,
            "entropy": 0.87,
            "pressure": "surge"
        },
        {
            "name": "Stable System",
            "coherence": 0.7,
            "entropy": 0.4,
            "pressure": "calm"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}:")
        result = router.route_to_fallback_memory(
            scenario["coherence"],
            scenario["entropy"],
            test_fallback_bank,
            scenario["pressure"]
        )
        print(json.dumps(result, indent=2))
    
    # Get statistics
    print("\nFallback Statistics:")
    stats = router.get_fallback_statistics()
    print(json.dumps(stats, indent=2))