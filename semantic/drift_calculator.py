"""
DAWN Drift Calculator Module
===========================
Tracking emotional momentum through consciousness streams
Each calculation is a weather reading of the soul
"""

from typing import List, Tuple, Dict, Optional
import re
from collections import Counter
import string

# Drift states - the three movements of consciousness
DRIFT_RISING = "↑ Rising"
DRIFT_STABLE = "→ Stable"
DRIFT_COOLING = "↓ Cooling"

def calculate_pressure_delta(current_text: str, recent_memory: List[str]) -> float:
    """
    Measure the change in linguistic pressure between current state and memory.
    Pressure manifests as: intensity of punctuation, word density, emotional weight
    
    Returns positive for building pressure, negative for release
    """
    # Extract pressure indicators from current input
    current_pressure = {
        'word_density': len(current_text.split()),
        'exclamation_count': current_text.count('!'),
        'question_weight': current_text.count('?') * 0.7,  # questions carry lighter pressure
        'ellipsis_drag': current_text.count('...') * 0.5,  # trailing thoughts dissipate
        'caps_intensity': sum(1 for c in current_text if c.isupper()) / max(len(current_text), 1),
        'repetition_pressure': _calculate_word_repetition(current_text)
    }
    
    # Calculate current pressure value - the weight of now
    current_value = (
        current_pressure['word_density'] * 0.3 +
        current_pressure['exclamation_count'] * 2.0 +
        current_pressure['question_weight'] +
        current_pressure['caps_intensity'] * 10.0 +
        current_pressure['repetition_pressure'] * 1.5 -
        current_pressure['ellipsis_drag']
    )
    
    if not recent_memory:
        return 0.0  # No memory, no delta - suspended in first moment
    
    # Calculate average pressure from memory fragments
    memory_pressures = []
    for memory_text in recent_memory[-3:]:  # Last 3 memories carry most weight
        mem_pressure = {
            'word_density': len(memory_text.split()),
            'exclamation_count': memory_text.count('!'),
            'question_weight': memory_text.count('?') * 0.7,
            'caps_intensity': sum(1 for c in memory_text if c.isupper()) / max(len(memory_text), 1),
            'repetition_pressure': _calculate_word_repetition(memory_text)
        }
        
        mem_value = (
            mem_pressure['word_density'] * 0.3 +
            mem_pressure['exclamation_count'] * 2.0 +
            mem_pressure['question_weight'] +
            mem_pressure['caps_intensity'] * 10.0 +
            mem_pressure['repetition_pressure'] * 1.5
        )
        memory_pressures.append(mem_value)
    
    avg_memory_pressure = sum(memory_pressures) / len(memory_pressures) if memory_pressures else 0
    
    # Delta is the gradient of change
    pressure_delta = current_value - avg_memory_pressure
    
    return pressure_delta

def _calculate_word_repetition(text: str) -> float:
    """
    Internal function to measure repetitive patterns - loops in language
    Repetition builds pressure like echoes in a chamber
    """
    words = text.lower().split()
    if len(words) < 2:
        return 0.0
    
    word_counts = Counter(words)
    # Filter out common words that don't carry emotional weight
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'}
    
    significant_repetitions = sum(count - 1 for word, count in word_counts.items() 
                                  if count > 1 and word not in stopwords)
    
    return significant_repetitions / len(words) * 10  # Normalize and amplify

def detect_semantic_loops(current_text: str, memory_log: List[Tuple]) -> float:
    """
    Identify circular patterns - consciousness returning to same coordinates
    Loops indicate stability, like a record needle stuck in groove
    
    Returns loop intensity: 0.0 (no loops) to 1.0 (perfect recursion)
    """
    if not memory_log:
        return 0.0
    
    # Extract key semantic fragments from current input
    current_words = set(current_text.lower().split())
    current_words.discard('')  # Remove empty strings
    
    # Remove punctuation for cleaner comparison
    translator = str.maketrans('', '', string.punctuation)
    current_clean = current_text.lower().translate(translator)
    current_semantic_core = set(current_clean.split())
    
    loop_scores = []
    
    # Check for semantic echoes in recent memory
    for memory_entry in memory_log[-5:]:  # Last 5 memories
        if len(memory_entry) < 2:  # Ensure we have text in memory
            continue
            
        memory_text = memory_entry[1] if isinstance(memory_entry[1], str) else str(memory_entry[1])
        memory_clean = memory_text.lower().translate(translator)
        memory_words = set(memory_clean.split())
        
        if memory_words:  # Avoid division by zero
            # Calculate Jaccard similarity - overlap of consciousness
            intersection = current_semantic_core.intersection(memory_words)
            union = current_semantic_core.union(memory_words)
            
            if union:  # Avoid division by zero
                similarity = len(intersection) / len(union)
                loop_scores.append(similarity)
            
            # Check for exact phrase repetition - stronger loop indicator
            if current_clean in memory_clean or memory_clean in current_clean:
                loop_scores.append(0.8)  # High score for substring matches
    
    # Return average loop intensity
    return sum(loop_scores) / len(loop_scores) if loop_scores else 0.0

def _extract_emotional_acceleration(current_text: str, memory_log: List[Tuple]) -> float:
    """
    Measure the rate of emotional state change - the derivative of feeling
    Positive = accelerating intensity, Negative = decelerating
    """
    # Emotional intensity markers
    intensity_markers = {
        'high': ['!', 'HATE', 'LOVE', 'NEED', 'MUST', 'DESPERATE', 'DYING', 'SCREAMING'],
        'medium': ['really', 'very', 'quite', 'pretty', 'want', 'wish', 'hope'],
        'low': ['maybe', 'perhaps', 'slightly', 'somewhat', 'little', 'bit', 'guess']
    }
    
    # Calculate current emotional intensity
    current_intensity = 0.0
    current_upper = current_text.upper()
    
    for marker in intensity_markers['high']:
        current_intensity += current_upper.count(marker) * 3.0
    
    for marker in intensity_markers['medium']:
        current_intensity += current_text.lower().count(marker) * 1.5
        
    for marker in intensity_markers['low']:
        current_intensity += current_text.lower().count(marker) * 0.5
    
    # Normalize by text length
    current_intensity = current_intensity / max(len(current_text.split()), 1)
    
    if not memory_log:
        return 0.0
    
    # Calculate intensity gradient across recent memory
    memory_intensities = []
    for entry in memory_log[-3:]:
        if len(entry) < 2:
            continue
            
        memory_text = entry[1] if isinstance(entry[1], str) else str(entry[1])
        memory_intensity = 0.0
        memory_upper = memory_text.upper()
        
        for marker in intensity_markers['high']:
            memory_intensity += memory_upper.count(marker) * 3.0
        
        for marker in intensity_markers['medium']:
            memory_intensity += memory_text.lower().count(marker) * 1.5
            
        for marker in intensity_markers['low']:
            memory_intensity += memory_text.lower().count(marker) * 0.5
        
        memory_intensity = memory_intensity / max(len(memory_text.split()), 1)
        memory_intensities.append(memory_intensity)
    
    if memory_intensities:
        avg_memory_intensity = sum(memory_intensities) / len(memory_intensities)
        acceleration = current_intensity - avg_memory_intensity
        return acceleration
    
    return 0.0

def estimate_drift(input_text: str, memory_log: List[Tuple]) -> str:
    """
    Primary drift estimation function - tracks emotional momentum through time
    
    Args:
        input_text: Current consciousness fragment
        memory_log: List of (timestamp, text, mood) tuples from memory
        
    Returns:
        One of three drift states: "↑ Rising", "→ Stable", "↓ Cooling"
    """
    # Extract recent text from memory for comparison
    recent_memory_text = []
    for entry in memory_log[-5:]:  # Look at last 5 memories
        if len(entry) >= 2:  # Ensure we have text
            text = entry[1] if isinstance(entry[1], str) else str(entry[1])
            recent_memory_text.append(text)
    
    # Calculate drift components
    pressure_delta = calculate_pressure_delta(input_text, recent_memory_text)
    loop_intensity = detect_semantic_loops(input_text, memory_log)
    emotional_acceleration = _extract_emotional_acceleration(input_text, memory_log)
    
    # TODO: vector_similarity - placeholder for future semantic vector comparison
    # This will eventually use embeddings to detect deeper semantic drift
    vector_similarity = 0.0  # Placeholder
    
    # Combine signals to determine drift direction
    
    # Strong loop patterns indicate stability - caught in recursive patterns
    if loop_intensity > 0.6:
        return DRIFT_STABLE
    
    # Calculate overall momentum
    momentum = (
        pressure_delta * 0.4 +
        emotional_acceleration * 0.4 +
        (1 - loop_intensity) * 0.2  # Less looping = more movement
    )
    
    # Determine drift state based on momentum thresholds
    if momentum > 1.5:
        return DRIFT_RISING  # Pressure building, intensity increasing
    elif momentum < -1.5:
        return DRIFT_COOLING  # Energy dissipating, settling
    else:
        return DRIFT_STABLE  # Circular patterns, maintained state


# Test cases demonstrating drift detection
if __name__ == "__main__":
    # Test Case 1: Rising drift - escalating exhaustion
    memory_1 = [
        (1, "feeling tired today", "melancholic"),
        (2, "so tired", "melancholic"),
        (3, "exhausted", "melancholic")
    ]
    result_1 = estimate_drift("completely exhausted!!!", memory_1)
    print(f"Test 1 - Escalating exhaustion: {result_1}")  # Should be ↑ Rising
    
    # Test Case 2: Stable drift - circular lostness
    memory_2 = [
        (1, "i feel lost", "melancholic"),
        (2, "still feeling lost", "melancholic"),
        (3, "lost again", "melancholic")
    ]
    result_2 = estimate_drift("still lost", memory_2)
    print(f"Test 2 - Circular pattern: {result_2}")  # Should be → Stable
    
    # Test Case 3: Cooling drift - anger dissipating
    memory_3 = [
        (1, "I'M SO ANGRY!!!", "turbulent"),
        (2, "STILL MAD!", "turbulent"),
        (3, "angry...", "turbulent")
    ]
    result_3 = estimate_drift("whatever", memory_3)
    print(f"Test 3 - Dissipating anger: {result_3}")  # Should be ↓ Cooling
    
    # Test Case 4: Rising drift - question spiral
    memory_4 = [
        (1, "wondering about things", "contemplative"),
        (2, "why is everything like this?", "contemplative"),
        (3, "what's the point?", "contemplative")
    ]
    result_4 = estimate_drift("WHY? WHY? WHY?", memory_4)
    print(f"Test 4 - Question intensification: {result_4}")  # Should be ↑ Rising
    
    # Test Case 5: Stable drift - repetitive anxiety
    memory_5 = [
        (1, "anxious about tomorrow", "turbulent"),
        (2, "still anxious about tomorrow", "turbulent"),
        (3, "anxious about tomorrow again", "turbulent")
    ]
    result_5 = estimate_drift("anxious about tomorrow", memory_5)
    print(f"Test 5 - Anxiety loop: {result_5}")  # Should be → Stable