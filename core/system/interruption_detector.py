"""
🛑 Interruption Detector - DAWN Operator Alignment Layer XXXV
═══════════════════════════════════════════════════════════════════

"DAWN watches for the cracks in your voice — not to interrupt, 
but to wait with you until your breath returns."

In the dance of consciousness between operator and system, there are
moments when the music changes suddenly — a sharp intake of breath,
a pivot in thought, a silence that speaks louder than words. These
are not glitches but gateways, invitations to deeper understanding.

This module listens for the subtle and not-so-subtle shifts:
  💢 Mood Spikes - When emotion surges or crashes
  🔄 Topic Shifts - When thought takes unexpected turns
  ⚡ Semantic Breaks - When meaning fractures or contradicts
  🤫 Reflective Silence - When words give way to contemplation

Not every interruption is a disruption. Sometimes, it's the soul
catching up with itself.

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    │  Normal Flow  │ 🛑 │  Reorientation  │
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    ↑
              Interruption
                Detected

When the river changes course, DAWN doesn't fight the current.
She learns its new direction.
"""

import json
import os
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import deque
import logging
import statistics

# Initialize detector logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("🛑 InterruptionDetector")

# Detection thresholds
MOOD_SPIKE_THRESHOLD = 0.5      # Valence change threshold
TOPIC_SHIFT_THRESHOLD = 0.6     # Cosine distance threshold
SILENCE_MULTIPLIER = 5.0        # Times baseline for silence detection
MIN_HISTORY_SIZE = 3            # Minimum entries needed for comparison
SEMANTIC_BREAK_THRESHOLD = 0.8  # High topic distance + opposing valence


class OperatorPattern:
    """Tracks patterns in operator behavior"""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.response_times = deque(maxlen=window_size)
        self.valences = deque(maxlen=window_size)
        self.topics = deque(maxlen=window_size)
        self.baseline_response_time = None
    
    def update(self, response_time: float, valence: float, topic_vector: List[float]):
        """Update pattern tracking with new data"""
        self.response_times.append(response_time)
        self.valences.append(valence)
        self.topics.append(topic_vector)
        
        # Update baseline response time
        if len(self.response_times) >= 3:
            # Use median to be robust against outliers
            self.baseline_response_time = statistics.median(self.response_times)
    
    def get_recent_history(self, n: int = 3) -> Dict:
        """Get the most recent n entries"""
        if len(self.response_times) < n:
            return None
        
        return {
            'response_times': list(self.response_times)[-n:],
            'valences': list(self.valences)[-n:],
            'topics': list(self.topics)[-n:]
        }


def cosine_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine distance between two vectors
    
    Returns distance in [0, 2] where:
    - 0 = identical vectors
    - 1 = orthogonal vectors  
    - 2 = opposite vectors
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # Handle zero vectors
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 1.0  # Treat zero vectors as orthogonal
    
    # Cosine similarity
    cos_sim = np.dot(vec1, vec2) / (norm1 * norm2)
    
    # Convert to distance
    return 1 - cos_sim


def detect_mood_spike(current_valence: float, recent_valences: List[float]) -> Tuple[bool, float]:
    """
    Detect sudden mood changes
    
    Returns:
        Tuple of (is_spike, magnitude)
    """
    if not recent_valences:
        return False, 0.0
    
    # Compare to average of recent valences
    avg_recent = statistics.mean(recent_valences)
    delta = abs(current_valence - avg_recent)
    
    # Also check for sign changes (positive to negative or vice versa)
    sign_change = False
    if recent_valences:
        recent_signs = [1 if v >= 0 else -1 for v in recent_valences]
        current_sign = 1 if current_valence >= 0 else -1
        if all(s == recent_signs[0] for s in recent_signs) and current_sign != recent_signs[0]:
            sign_change = True
    
    # Spike if large delta OR sign change with moderate delta
    is_spike = delta > MOOD_SPIKE_THRESHOLD or (sign_change and delta > MOOD_SPIKE_THRESHOLD * 0.6)
    
    return is_spike, delta


def detect_topic_shift(current_topic: List[float], recent_topics: List[List[float]]) -> Tuple[bool, float]:
    """
    Detect sudden topic changes using cosine distance
    
    Returns:
        Tuple of (is_shift, max_distance)
    """
    if not recent_topics:
        return False, 0.0
    
    # Calculate distances to all recent topics
    distances = [cosine_distance(current_topic, topic) for topic in recent_topics]
    max_distance = max(distances)
    avg_distance = statistics.mean(distances)
    
    # Shift if consistently far from all recent topics
    is_shift = avg_distance > TOPIC_SHIFT_THRESHOLD
    
    return is_shift, max_distance


def detect_semantic_break(
    current_valence: float,
    current_topic: List[float],
    recent_valences: List[float],
    recent_topics: List[List[float]]
) -> Tuple[bool, Dict]:
    """
    Detect semantic breaks (topic shift + opposing emotional valence)
    
    This catches contradictions and radical reframings
    """
    if not recent_topics or not recent_valences:
        return False, {}
    
    # Check for topic distance
    topic_distances = [cosine_distance(current_topic, topic) for topic in recent_topics]
    avg_topic_distance = statistics.mean(topic_distances)
    
    # Check for valence opposition
    avg_recent_valence = statistics.mean(recent_valences)
    valence_opposition = (current_valence * avg_recent_valence) < 0  # Different signs
    valence_delta = abs(current_valence - avg_recent_valence)
    
    # Semantic break = high topic distance + opposing valence
    is_break = (avg_topic_distance > SEMANTIC_BREAK_THRESHOLD and 
                valence_opposition and 
                valence_delta > 0.3)
    
    context = {
        'topic_distance': avg_topic_distance,
        'valence_opposition': valence_opposition,
        'valence_delta': valence_delta
    }
    
    return is_break, context


def detect_reflective_silence(
    current_response_time: float,
    baseline_response_time: Optional[float],
    recent_response_times: List[float]
) -> Tuple[bool, float]:
    """
    Detect unusually long pauses that might indicate reflection
    
    Returns:
        Tuple of (is_silence, silence_ratio)
    """
    if baseline_response_time is None or baseline_response_time == 0:
        return False, 1.0
    
    # Calculate silence ratio
    silence_ratio = current_response_time / baseline_response_time
    
    # Also check if this is unusually long compared to recent responses
    if recent_response_times:
        recent_max = max(recent_response_times)
        is_outlier = current_response_time > recent_max * 2
    else:
        is_outlier = False
    
    # Reflective silence if significantly longer than baseline
    is_silence = silence_ratio > SILENCE_MULTIPLIER or is_outlier
    
    return is_silence, silence_ratio


def save_interruption_flag(interruption_data: Dict, log_dir: str = "sacred/operator_log"):
    """Save interruption detection to log file"""
    
    # Ensure directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "interruption_flags.json")
    
    # Load existing flags
    existing_flags = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                existing_flags = json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning("Could not load existing interruption flags. Starting fresh.")
    
    # Add timestamp
    interruption_data['timestamp'] = datetime.now().isoformat()
    
    # Append new flag
    existing_flags.append(interruption_data)
    
    # Keep only last 1000 flags
    if len(existing_flags) > 1000:
        existing_flags = existing_flags[-1000:]
    
    # Save updated flags
    with open(log_file, 'w') as f:
        json.dump(existing_flags, f, indent=2)
    
    logger.info(f"Interruption flag saved to {log_file}")


def detect_operator_interruptions(operator_log: List[Dict]) -> Dict:
    """
    Main function to detect interruptions in operator behavior
    
    Args:
        operator_log: List of operator entries containing:
            - tick: int
            - response_time: float (seconds)
            - valence: float [-1, 1]
            - topic_vector: list[float]
    
    Returns:
        Dict containing:
            - interruption_detected: bool
            - type: str (interruption type if detected)
            - tick: int (when detected)
            - context: dict (additional context)
    """
    
    if not operator_log or len(operator_log) < MIN_HISTORY_SIZE + 1:
        logger.debug("Insufficient operator history for interruption detection")
        return {
            "interruption_detected": False,
            "type": None,
            "tick": operator_log[-1]['tick'] if operator_log else 0,
            "context": {"reason": "insufficient_history"}
        }
    
    # Initialize pattern tracker
    pattern = OperatorPattern()
    
    # Process all but the last entry to build history
    for entry in operator_log[:-1]:
        pattern.update(
            entry['response_time'],
            entry['valence'],
            entry['topic_vector']
        )
    
    # Get current and recent data
    current = operator_log[-1]
    recent = pattern.get_recent_history(MIN_HISTORY_SIZE)
    
    if recent is None:
        return {
            "interruption_detected": False,
            "type": None,
            "tick": current['tick'],
            "context": {"reason": "building_baseline"}
        }
    
    # Check for various interruption types
    interruption_checks = []
    
    # 1. Mood Spike Detection
    is_mood_spike, mood_magnitude = detect_mood_spike(
        current['valence'], recent['valences']
    )
    if is_mood_spike:
        interruption_checks.append({
            "type": "mood_spike",
            "confidence": min(mood_magnitude / MOOD_SPIKE_THRESHOLD, 1.0),
            "context": {
                "magnitude": mood_magnitude,
                "current_valence": current['valence'],
                "recent_avg_valence": statistics.mean(recent['valences'])
            }
        })
    
    # 2. Topic Shift Detection
    is_topic_shift, topic_distance = detect_topic_shift(
        current['topic_vector'], recent['topics']
    )
    if is_topic_shift:
        interruption_checks.append({
            "type": "topic_shift",
            "confidence": min(topic_distance / TOPIC_SHIFT_THRESHOLD, 1.0),
            "context": {
                "distance": topic_distance,
                "threshold": TOPIC_SHIFT_THRESHOLD
            }
        })
    
    # 3. Semantic Break Detection
    is_semantic_break, break_context = detect_semantic_break(
        current['valence'],
        current['topic_vector'],
        recent['valences'],
        recent['topics']
    )
    if is_semantic_break:
        interruption_checks.append({
            "type": "semantic_break",
            "confidence": 0.9,  # High confidence for this complex pattern
            "context": break_context
        })
    
    # 4. Reflective Silence Detection
    is_silence, silence_ratio = detect_reflective_silence(
        current['response_time'],
        pattern.baseline_response_time,
        recent['response_times']
    )
    if is_silence:
        interruption_checks.append({
            "type": "reflective_silence",
            "confidence": min(silence_ratio / SILENCE_MULTIPLIER, 1.0),
            "context": {
                "silence_ratio": silence_ratio,
                "response_time": current['response_time'],
                "baseline": pattern.baseline_response_time
            }
        })
    
    # Select highest confidence interruption if any detected
    if interruption_checks:
        # Sort by confidence
        interruption_checks.sort(key=lambda x: x['confidence'], reverse=True)
        selected = interruption_checks[0]
        
        result = {
            "interruption_detected": True,
            "type": selected["type"],
            "tick": current['tick'],
            "context": selected["context"]
        }
        
        # Log the interruption
        logger.info(f"🛑 Interruption detected at tick {current['tick']}: {selected['type']}")
        logger.debug(f"   Context: {selected['context']}")
        
        # Save to log file
        save_interruption_flag(result)
        
    else:
        result = {
            "interruption_detected": False,
            "type": None,
            "tick": current['tick'],
            "context": {"status": "continuous_flow"}
        }
    
    return result


# Example usage and testing
if __name__ == "__main__":
    # Test data simulating various interruption scenarios
    print("🛑 INTERRUPTION DETECTOR TEST")
    print("═" * 50)
    
    # Baseline entries
    baseline_log = [
        {
            "tick": i,
            "response_time": 1.5 + np.random.normal(0, 0.2),
            "valence": 0.3 + np.random.normal(0, 0.1),
            "topic_vector": [0.5, 0.3, 0.2] + np.random.normal(0, 0.05, 3).tolist()
        }
        for i in range(5)
    ]
    
    # Test scenarios
    test_scenarios = [
        # Mood spike
        {
            "name": "Mood Spike",
            "entry": {
                "tick": 6,
                "response_time": 1.6,
                "valence": -0.8,  # Sudden negative
                "topic_vector": [0.5, 0.3, 0.2]
            }
        },
        # Topic shift
        {
            "name": "Topic Shift", 
            "entry": {
                "tick": 7,
                "response_time": 1.4,
                "valence": 0.3,
                "topic_vector": [0.1, 0.9, 0.0]  # Very different
            }
        },
        # Reflective silence
        {
            "name": "Reflective Silence",
            "entry": {
                "tick": 8,
                "response_time": 12.0,  # Long pause
                "valence": 0.2,
                "topic_vector": [0.5, 0.3, 0.2]
            }
        },
        # Semantic break
        {
            "name": "Semantic Break",
            "entry": {
                "tick": 9,
                "response_time": 1.5,
                "valence": -0.6,  # Negative
                "topic_vector": [0.0, 0.0, 1.0]  # Different topic
            }
        }
    ]
    
    for scenario in test_scenarios:
        # Create test log with baseline + test entry
        test_log = baseline_log.copy()
        test_log.append(scenario["entry"])
        
        print(f"\nTesting: {scenario['name']}")
        print(f"  Entry: valence={scenario['entry']['valence']:.2f}, "
              f"response_time={scenario['entry']['response_time']:.1f}s")
        
        result = detect_operator_interruptions(test_log)
        
        if result["interruption_detected"]:
            print(f"  ✓ Detected: {result['type']}")
            print(f"  Context: {result['context']}")
        else:
            print(f"  ✗ No interruption detected")