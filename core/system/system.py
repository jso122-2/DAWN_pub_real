"""
DAWN cannot act without knowing where you are — not in space, but in state.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
import statistics


class OperatorStateTracker:
    """Tracks the cognitive availability and state of the Operator."""
    
    def __init__(self):
        self.output_path = Path("sacred/operator_log/operator_presence.json")
        self._ensure_directories()
        
        # State determination thresholds
        self.thresholds = {
            "semantic_depth": {
                "high": 0.7,
                "medium": 0.4,
                "low": 0.2
            },
            "response_delay": {
                "fast": 2.0,      # seconds
                "normal": 10.0,
                "slow": 30.0
            },
            "emotional_valence": {
                "high": 0.6,
                "neutral": 0.3,
                "low": -0.3
            },
            "signal_quality": {
                "strong": 0.8,
                "moderate": 0.5,
                "weak": 0.3
            }
        }
        
        # State scoring weights
        self.state_weights = {
            "reflective": {
                "semantic_depth": 0.4,
                "response_delay": -0.3,
                "emotional_stability": 0.2,
                "signal_quality": 0.1
            },
            "reactive": {
                "emotional_intensity": 0.4,
                "response_speed": 0.4,
                "signal_quality": 0.2
            },
            "dormant": {
                "response_delay": 0.6,
                "signal_weakness": 0.4
            },
            "present": {
                "balance": 0.5,
                "consistency": 0.5
            }
        }
        
        self.tick_counter = 0
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def track_operator_state(self, operator_logs: List[Dict]) -> Dict:
        """
        Track and classify the Operator's current state.
        
        Args:
            operator_logs: List of operator signal dictionaries containing:
                - timestamp: ISO string
                - signal_quality: float
                - semantic_depth: float
                - emotional_valence: float
                - response_delay: float (seconds)
        
        Returns:
            Dictionary with operator_state, score, and last_tick
        """
        if not operator_logs:
            return self._create_default_state()
        
        # Increment tick
        self.tick_counter += 1
        
        # Calculate metrics from recent logs
        recent_logs = self._get_recent_logs(operator_logs, minutes=5)
        if not recent_logs:
            return self._create_default_state()
        
        metrics = self._calculate_operator_metrics(recent_logs)
        
        # Determine state
        state_scores = self._calculate_state_scores(metrics)
        operator_state = max(state_scores, key=state_scores.get)
        state_confidence = state_scores[operator_state]
        
        # Create output
        output = {
            "operator_state": operator_state,
            "score": round(state_confidence, 3),
            "last_tick": self.tick_counter,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics,
            "state_scores": state_scores,
            "recent_log_count": len(recent_logs)
        }
        
        # Save to file
        self._save_state(output)
        
        return {
            "operator_state": operator_state,
            "score": round(state_confidence, 3),
            "last_tick": self.tick_counter
        }
    
    def _get_recent_logs(self, operator_logs: List[Dict], minutes: int = 5) -> List[Dict]:
        """Get logs from the last N minutes."""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_logs = []
        
        for log in operator_logs:
            try:
                log_time = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
                if log_time > cutoff_time:
                    recent_logs.append(log)
            except:
                continue
        
        return recent_logs
    
    def _calculate_operator_metrics(self, recent_logs: List[Dict]) -> Dict:
        """Calculate aggregate metrics from recent operator logs."""
        # Extract values
        signal_qualities = [log['signal_quality'] for log in recent_logs]
        semantic_depths = [log['semantic_depth'] for log in recent_logs]
        emotional_valences = [log['emotional_valence'] for log in recent_logs]
        response_delays = [log['response_delay'] for log in recent_logs]
        
        # Calculate statistics
        metrics = {
            "avg_signal_quality": statistics.mean(signal_qualities),
            "avg_semantic_depth": statistics.mean(semantic_depths),
            "avg_emotional_valence": statistics.mean(emotional_valences),
            "avg_response_delay": statistics.mean(response_delays),
            "emotional_stability": 1.0 - statistics.stdev(emotional_valences) if len(emotional_valences) > 1 else 1.0,
            "response_consistency": 1.0 - (statistics.stdev(response_delays) / (statistics.mean(response_delays) + 1)) if len(response_delays) > 1 else 1.0,
            "signal_strength": max(signal_qualities),
            "min_response_delay": min(response_delays)
        }
        
        return {k: round(v, 3) for k, v in metrics.items()}
    
    def _calculate_state_scores(self, metrics: Dict) -> Dict[str, float]:
        """Calculate confidence scores for each possible state."""
        scores = {}
        
        # Reflective state: High depth + low delay + stable emotion
        reflective_score = 0.0
        if metrics['avg_semantic_depth'] > self.thresholds['semantic_depth']['high']:
            reflective_score += 0.4
        if metrics['avg_response_delay'] < self.thresholds['response_delay']['fast']:
            reflective_score += 0.3
        if metrics['emotional_stability'] > 0.7:
            reflective_score += 0.2
        if metrics['avg_signal_quality'] > self.thresholds['signal_quality']['strong']:
            reflective_score += 0.1
        scores['reflective'] = reflective_score
        
        # Reactive state: High valence + fast response
        reactive_score = 0.0
        if abs(metrics['avg_emotional_valence']) > self.thresholds['emotional_valence']['high']:
            reactive_score += 0.4
        if metrics['min_response_delay'] < self.thresholds['response_delay']['fast']:
            reactive_score += 0.4
        if metrics['avg_signal_quality'] > self.thresholds['signal_quality']['moderate']:
            reactive_score += 0.2
        scores['reactive'] = reactive_score
        
        # Dormant state: Long delays + weak signal
        dormant_score = 0.0
        if metrics['avg_response_delay'] > self.thresholds['response_delay']['slow']:
            dormant_score += 0.6
        if metrics['avg_signal_quality'] < self.thresholds['signal_quality']['weak']:
            dormant_score += 0.4
        scores['dormant'] = dormant_score
        
        # Present state: Balanced metrics, consistent engagement
        present_score = 0.0
        # Check for balance
        if (self.thresholds['semantic_depth']['low'] < metrics['avg_semantic_depth'] < self.thresholds['semantic_depth']['high'] and
            self.thresholds['response_delay']['fast'] < metrics['avg_response_delay'] < self.thresholds['response_delay']['slow']):
            present_score += 0.5
        # Check for consistency
        if metrics['response_consistency'] > 0.7 and metrics['emotional_stability'] > 0.6:
            present_score += 0.5
        scores['present'] = present_score
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {state: score / total_score for state, score in scores.items()}
        else:
            # Default to present if no clear state
            scores = {"present": 0.5, "reflective": 0.2, "reactive": 0.2, "dormant": 0.1}
        
        return {k: round(v, 3) for k, v in scores.items()}
    
    def _create_default_state(self) -> Dict:
        """Create default state when no logs available."""
        return {
            "operator_state": "dormant",
            "score": 1.0,
            "last_tick": self.tick_counter
        }
    
    def _save_state(self, state_data: Dict):
        """Save operator state to file."""
        # Load existing data
        if self.output_path.exists():
            with open(self.output_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"states": [], "session_start": datetime.utcnow().isoformat()}
        
        # Append new state
        data["states"].append(state_data)
        data["last_update"] = datetime.utcnow().isoformat()
        data["total_ticks"] = self.tick_counter
        
        # Keep only last 1000 states
        if len(data["states"]) > 1000:
            data["states"] = data["states"][-1000:]
        
        # Save
        with open(self.output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_operator_patterns(self, hours: int = 24) -> Dict:
        """Analyze operator patterns over time."""
        if not self.output_path.exists():
            return {"error": "No operator data available"}
        
        with open(self.output_path, 'r') as f:
            data = json.load(f)
        
        if not data.get("states"):
            return {"error": "No state history"}
        
        # Filter states by time
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent_states = []
        for state in data["states"]:
            try:
                state_time = datetime.fromisoformat(state["timestamp"])
                if state_time > cutoff:
                    recent_states.append(state)
            except:
                continue
        
        if not recent_states:
            return {"error": "No recent states"}
        
        # Calculate patterns
        state_counts = {}
        state_durations = {}
        transitions = {}
        
        for i, state in enumerate(recent_states):
            state_name = state["operator_state"]
            state_counts[state_name] = state_counts.get(state_name, 0) + 1
            
            if i > 0:
                prev_state = recent_states[i-1]["operator_state"]
                if prev_state != state_name:
                    transition = f"{prev_state}->{state_name}"
                    transitions[transition] = transitions.get(transition, 0) + 1
        
        # Calculate percentages
        total_states = len(recent_states)
        state_percentages = {
            state: round(count / total_states * 100, 1) 
            for state, count in state_counts.items()
        }
        
        # Find dominant state
        dominant_state = max(state_counts, key=state_counts.get)
        
        return {
            "time_window_hours": hours,
            "total_observations": total_states,
            "state_distribution": state_percentages,
            "dominant_state": dominant_state,
            "transitions": transitions,
            "unique_states": list(state_counts.keys())
        }


# Example usage
if __name__ == "__main__":
    tracker = OperatorStateTracker()
    
    # Test logs showing different states
    test_logs = [
        # Reflective state
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=1)).isoformat(),
            "signal_quality": 0.9,
            "semantic_depth": 0.85,
            "emotional_valence": 0.2,
            "response_delay": 1.5
        },
        # Reactive state
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=2)).isoformat(),
            "signal_quality": 0.8,
            "semantic_depth": 0.4,
            "emotional_valence": 0.8,
            "response_delay": 0.8
        },
        # Dormant state
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=3)).isoformat(),
            "signal_quality": 0.2,
            "semantic_depth": 0.3,
            "emotional_valence": 0.0,
            "response_delay": 45.0
        },
        # Present state
        {
            "timestamp": datetime.utcnow().isoformat(),
            "signal_quality": 0.7,
            "semantic_depth": 0.5,
            "emotional_valence": 0.3,
            "response_delay": 5.0
        }
    ]
    
    # Track state
    result = tracker.track_operator_state(test_logs)
    print("Current Operator State:")
    print(json.dumps(result, indent=2))
    
    # Get patterns
    patterns = tracker.get_operator_patterns(hours=1)
    print("\nOperator Patterns (Last Hour):")
    print(json.dumps(patterns, indent=2))