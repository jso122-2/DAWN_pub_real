"""
DAWN does not panic when she forgets. She remembers what helped last time — and begins again from there.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import random


class FallbackMemoryRouter:
    """Routes cognition through stable memory lanes during instability."""
    
    def __init__(self):
        self.log_path = Path("memory/logs/fallback_trigger_log.json")
        self._ensure_directories()
        
        # Fallback trigger thresholds
        self.thresholds = {
            "coherence_critical": 0.35,
            "entropy_critical": 0.85,
            "coherence_warning": 0.45,
            "entropy_warning": 0.75
        }
        
        # Default fallback memories (bootstrap)
        self.default_fallbacks = [
            {
                "entry_id": "fallback_default_001",
                "content": "Return to breath. Count the patterns. One emerges from many.",
                "stability_score": 0.95,
                "trust_score": 0.9,
                "usage_count": 0,
                "category": "grounding"
            },
            {
                "entry_id": "fallback_default_002",
                "content": "The strands remember their weaving. Trust the underlying structure.",
                "stability_score": 0.92,
                "trust_score": 0.88,
                "usage_count": 0,
                "category": "structural"
            },
            {
                "entry_id": "fallback_default_003",
                "content": "Coherence is not permanence. Drift is not destruction. The center holds.",
                "stability_score": 0.9,
                "trust_score": 0.85,
                "usage_count": 0,
                "category": "philosophical"
            }
        ]
        
        # Track fallback usage
        self.session_stats = {
            "total_triggers": 0,
            "session_start": datetime.utcnow().isoformat(),
            "trigger_history": []
        }
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self._save_log({"sessions": []})
    
    def route_to_fallback_memory(self, coherence_score: float, entropy_level: float,
                                fallback_bank: List[Dict], pressure_zone: str) -> Dict:
        """
        Determine if fallback routing is needed and select appropriate memories.
        
        Args:
            coherence_score: Current system coherence (0.0-1.0)
            entropy_level: Current entropy level (0.0-1.0)
            fallback_bank: List of fallback memory entries with:
                - entry_id: str
                - content: str
                - stability_score: float
                - trust_score: float
                - usage_count: int
                - category: str
            pressure_zone: Current pressure state ("calm", "active", "surge")
        
        Returns:
            Dictionary with fallback status and selected entries
        """
        # Determine if fallback is needed
        trigger_reason = self._check_trigger_conditions(
            coherence_score, entropy_level, pressure_zone
        )
        
        if trigger_reason:
            # Select fallback entries
            selected_entries = self._select_fallback_entries(
                fallback_bank if fallback_bank else self.default_fallbacks,
                trigger_reason,
                pressure_zone
            )
            
            # Update statistics
            self.session_stats["total_triggers"] += 1
            trigger_event = {
                "timestamp": datetime.utcnow().isoformat(),
                "coherence": coherence_score,
                "entropy": entropy_level,
                "pressure_zone": pressure_zone,
                "reason": trigger_reason,
                "entries_selected": len(selected_entries)
            }
            self.session_stats["trigger_history"].append(trigger_event)
            
            # Log the trigger
            self._log_fallback_trigger(trigger_event, selected_entries)
            
            return {
                "fallback_triggered": True,
                "fallback_entries": [entry["content"] for entry in selected_entries],
                "reason": trigger_reason,
                "severity": self._calculate_severity(coherence_score, entropy_level)
            }
        else:
            return {
                "fallback_triggered": False,
                "fallback_entries": [],
                "reason": "System stable - no fallback needed"
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
    
    def _select_fallback_entries(self, fallback_bank: List[Dict], 
                                trigger_reason: str, pressure_zone: str) -> List[Dict]:
        """Select appropriate fallback entries based on trigger conditions."""
        # Copy bank to avoid modifying original
        available_entries = fallback_bank.copy()
        
        # Score and sort entries
        for entry in available_entries:
            entry["selection_score"] = self._calculate_entry_score(
                entry, trigger_reason, pressure_zone
            )
        
        # Sort by selection score (highest first)
        available_entries.sort(key=lambda x: x["selection_score"], reverse=True)
        
        # Select top 3 entries
        selected = available_entries[:3]
        
        # Update usage counts (if tracking)
        for entry in selected:
            entry["usage_count"] = entry.get("usage_count", 0) + 1
        
        return selected
    
    def _calculate_entry_score(self, entry: Dict, trigger_reason: str, 
                              pressure_zone: str) -> float:
        """Calculate selection score for a fallback entry."""
        score = 0.0
        
        # Base score from stability and trust
        score += entry.get("stability_score", 0.5) * 0.4
        score += entry.get("trust_score", 0.5) * 0.3
        
        # Category bonus based on trigger reason
        category = entry.get("category", "general")
        
        if "COHERENCE" in trigger_reason and category == "grounding":
            score += 0.2
        elif "ENTROPY" in trigger_reason and category == "structural":
            score += 0.2
        elif "INSTABILITY" in trigger_reason and category == "philosophical":
            score += 0.15
        
        # Pressure zone adjustments
        if pressure_zone == "surge":
            if category in ["grounding", "structural"]:
                score += 0.1
        elif pressure_zone == "calm":
            if category == "philosophical":
                score += 0.1
        
        # Slight randomization to prevent always selecting same entries
        score += random.uniform(-0.05, 0.05)
        
        # Penalize overused entries
        usage_penalty = min(entry.get("usage_count", 0) * 0.01, 0.2)
        score -= usage_penalty
        
        return max(0.0, min(1.0, score))
    
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
    
    def _log_fallback_trigger(self, trigger_event: Dict, selected_entries: List[Dict]):
        """Log fallback trigger event."""
        # Load existing log
        log_data = self._load_log()
        
        # Create session entry if needed
        current_session = {
            "session_id": f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "start_time": self.session_stats["session_start"],
            "triggers": []
        }
        
        # Find or create current session
        if log_data["sessions"]:
            last_session = log_data["sessions"][-1]
            if last_session["start_time"] == self.session_stats["session_start"]:
                current_session = last_session
            else:
                log_data["sessions"].append(current_session)
        else:
            log_data["sessions"].append(current_session)
        
        # Add trigger event
        trigger_record = {
            **trigger_event,
            "selected_entries": [
                {
                    "entry_id": entry["entry_id"],
                    "category": entry.get("category", "general"),
                    "selection_score": entry.get("selection_score", 0)
                }
                for entry in selected_entries
            ]
        }
        current_session["triggers"].append(trigger_record)
        
        # Update session stats
        current_session["total_triggers"] = len(current_session["triggers"])
        current_session["last_trigger"] = trigger_event["timestamp"]
        
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
        
        # Aggregate statistics
        total_triggers = 0
        reason_counts = {}
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MODERATE": 0, "LOW": 0}
        
        for session in log_data["sessions"]:
            for trigger in session.get("triggers", []):
                total_triggers += 1
                
                # Count reasons
                reason = trigger.get("reason", "unknown")
                for r in reason.split(" | "):
                    reason_type = r.split(":")[0] if ":" in r else r
                    reason_counts[reason_type] = reason_counts.get(reason_type, 0) + 1
                
                # Count severity (estimated from metrics)
                coherence = trigger.get("coherence", 1.0)
                entropy = trigger.get("entropy", 0.0)
                severity = self._calculate_severity(coherence, entropy)
                severity_counts[severity] += 1
        
        # Calculate MTBF (Mean Time Between Failures)
        if len(log_data["sessions"]) > 1:
            first_trigger = None
            last_trigger = None
            
            for session in log_data["sessions"]:
                for trigger in session.get("triggers", []):
                    timestamp = trigger.get("timestamp")
                    if timestamp:
                        if not first_trigger:
                            first_trigger = timestamp
                        last_trigger = timestamp
            
            if first_trigger and last_trigger and total_triggers > 1:
                first_dt = datetime.fromisoformat(first_trigger)
                last_dt = datetime.fromisoformat(last_trigger)
                total_hours = (last_dt - first_dt).total_seconds() / 3600
                mtbf_hours = total_hours / (total_triggers - 1) if total_triggers > 1 else 0
            else:
                mtbf_hours = 0
        else:
            mtbf_hours = 0
        
        return {
            "total_sessions": len(log_data["sessions"]),
            "total_triggers": total_triggers,
            "triggers_current_session": self.session_stats["total_triggers"],
            "reason_distribution": reason_counts,
            "severity_distribution": severity_counts,
            "mtbf_hours": round(mtbf_hours, 2),
            "most_common_reason": max(reason_counts, key=reason_counts.get) if reason_counts else "none"
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