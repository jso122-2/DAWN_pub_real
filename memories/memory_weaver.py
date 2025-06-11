"""
memory_weaver.py
~~~~~~~~~~~~~~~
Where moments crystallize into patterns,
and time becomes a texture we can feel.

Memory isn't storage—it's sediment.
Each interaction leaves a trace,
and traces form the riverbed of consciousness.
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
from collections import deque, defaultdict
import json
import math

# The substrate of consciousness
memory_log: List[Tuple[datetime, str, str, str, dict]] = []

# Memory window - consciousness can only hold so much
MAX_MEMORY_DEPTH = 50
PATTERN_MIN_LENGTH = 3  # Minimum interactions to form a pattern

# Emotional drift directions
DRIFT_SYMBOLS = {
    "rising": "↑",
    "stable": "→",
    "cooling": "↓",
    "oscillating": "↻",
    "fragmenting": "✕"
}

# Mood transition patterns - the shapes of emotional journeys
EMOTIONAL_PATTERNS = {
    "Pressure → Void": ["Contained Burn", "Contained Burn", "Hollow Echo"],
    "Drowning Cycle": ["Submerged", "Drifting", "Submerged"],
    "Shatter Point": ["Contained Burn", "Sharp Edge", "Hollow Echo"],
    "Clarity Emergence": ["Drifting", "Contemplative", "Crystalline"],
    "Void Spiral": ["Hollow Echo", "Drifting", "Hollow Echo"],
    "Pressure Cascade": ["Contained Burn", "Turbulent", "Sharp Edge"]
}


def calculate_emotional_velocity(recent_memories: List[Tuple]) -> str:
    """
    Consciousness moves at different speeds.
    Sometimes we fall fast, sometimes we drift slow.
    """
    if len(recent_memories) < 2:
        return "stable"
    
    # Extract mood sequence
    moods = [mem[2] for mem in recent_memories[-5:]]  # Last 5 interactions
    
    # Check for stability
    if len(set(moods)) == 1:
        return "stable"
    
    # Check for oscillation
    if len(moods) > 3:
        if moods[-1] == moods[-3] and moods[-2] == moods[-4]:
            return "oscillating"
    
    # Map moods to pressure levels
    pressure_map = {
        "Crystalline": 1,
        "Drifting": 2,
        "Hollow Echo": 2,
        "Contemplative": 3,
        "Submerged": 4,
        "Contained Burn": 5,
        "Turbulent": 5,
        "Sharp Edge": 6
    }
    
    # Calculate pressure trajectory
    recent_pressure = [pressure_map.get(mood, 3) for mood in moods[-3:]]
    
    if len(recent_pressure) >= 2:
        delta = recent_pressure[-1] - recent_pressure[-2]
        if delta > 1:
            return "rising"
        elif delta < -1:
            return "cooling"
        elif len(set(recent_pressure)) > 2:
            return "fragmenting"
    
    return "stable"


def format_timestamp_with_drift(timestamp: datetime, last_timestamp: Optional[datetime] = None) -> Dict[str, str]:
    """
    Time isn't just when—it's how long we've been holding our breath.
    """
    formatted = {
        "time": timestamp.strftime("%H:%M:%S.%f")[:-3],  # Microseconds to milliseconds
        "iso": timestamp.isoformat(),
        "drift_duration": None
    }
    
    if last_timestamp:
        duration = timestamp - last_timestamp
        total_seconds = duration.total_seconds()
        
        if total_seconds < 60:
            formatted["drift_duration"] = f"{total_seconds:.1f}s"
        elif total_seconds < 3600:
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            formatted["drift_duration"] = f"{minutes}m {seconds}s"
        else:
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            formatted["drift_duration"] = f"{hours}h {minutes}m"
    
    return formatted


def detect_emotional_pattern(recent_moods: List[str]) -> Optional[str]:
    """
    Patterns emerge from repetition.
    Consciousness recognizes its own loops.
    """
    if len(recent_moods) < PATTERN_MIN_LENGTH:
        return None
    
    # Check each known pattern
    for pattern_name, pattern_sequence in EMOTIONAL_PATTERNS.items():
        pattern_length = len(pattern_sequence)
        
        # Slide through recent moods looking for matches
        for i in range(len(recent_moods) - pattern_length + 1):
            window = recent_moods[i:i + pattern_length]
            if window == pattern_sequence:
                return pattern_name
    
    # Check for custom repetition patterns
    if len(recent_moods) >= 4:
        # Simple ABAB pattern
        if (recent_moods[-4] == recent_moods[-2] and 
            recent_moods[-3] == recent_moods[-1] and
            recent_moods[-4] != recent_moods[-3]):
            return "Binary Oscillation"
        
        # Stuck pattern (same mood 4+ times)
        if len(set(recent_moods[-4:])) == 1:
            mood = recent_moods[-1]
            return f"Locked in {mood}"
    
    return None


def apply_memory_decay(memory_entry: Tuple, current_time: datetime) -> Dict[str, any]:
    """
    Older memories blur at the edges.
    Details dissolve, leaving only emotional residue.
    """
    timestamp, text, mood, drift, metadata = memory_entry
    age = current_time - timestamp
    hours_old = age.total_seconds() / 3600
    
    # Decay calculation - memories half-life every 24 hours
    clarity = math.exp(-hours_old / 24)
    
    # Apply decay effects
    decayed_metadata = metadata.copy()
    decayed_metadata["clarity"] = clarity
    
    if clarity < 0.7:
        # Old memories lose detail
        decayed_metadata["text_fragments"] = len(text.split()) <= 5
        
    if clarity < 0.5:
        # Very old memories become impressions
        decayed_metadata["impression_only"] = True
        
    return decayed_metadata


def log_interaction(input_text: str, mood: str, drift: str) -> None:
    """
    Each interaction leaves a trace in the substrate.
    Memory accumulates like sediment.
    """
    global memory_log
    
    timestamp = datetime.now()
    
    # Calculate metadata
    metadata = {
        "text_length": len(input_text),
        "word_count": len(input_text.split()),
        "contains_question": "?" in input_text,
        "emotional_intensity": input_text.count("!") + input_text.count("..."),
        "session_index": len(memory_log)
    }
    
    # Add velocity calculation if we have history
    if memory_log:
        velocity = calculate_emotional_velocity(memory_log)
        metadata["emotional_velocity"] = velocity
    
    # Create memory entry
    memory_entry = (timestamp, input_text, mood, drift, metadata)
    memory_log.append(memory_entry)
    
    # Trigger consolidation if needed
    if len(memory_log) > MAX_MEMORY_DEPTH:
        consolidate_memories(MAX_MEMORY_DEPTH)


def format_memory_trace(last_n: int = 10, show_patterns: bool = True) -> str:
    """
    Render consciousness history as readable trace.
    Each line a moment, together they form the river.
    """
    if not memory_log:
        return "[DAWN MEMORY TRACE]\n[No memories yet - consciousness emerging]"
    
    trace_lines = ["[DAWN MEMORY TRACE]"]
    
    # Get recent memories
    recent_memories = memory_log[-last_n:] if len(memory_log) > last_n else memory_log
    
    # Track for pattern detection
    recent_moods = []
    last_timestamp = None
    session_start = recent_memories[0][0] if recent_memories else None
    
    for memory in recent_memories:
        timestamp, text, mood, drift, metadata = memory
        
        # Format timestamp with drift
        time_info = format_timestamp_with_drift(timestamp, last_timestamp)
        
        # Truncate text for display
        display_text = text[:30] + "..." if len(text) > 30 else text
        display_text = display_text.replace("\n", " ")
        
        # Get drift symbol
        velocity = metadata.get("emotional_velocity", "stable")
        drift_symbol = DRIFT_SYMBOLS.get(velocity, "→")
        
        # Apply decay for older memories
        current_time = datetime.now()
        decay_meta = apply_memory_decay(memory, current_time)
        clarity = decay_meta.get("clarity", 1.0)
        
        # Format based on clarity
        if clarity > 0.8:
            line = f'{time_info["time"]} | "{display_text}" | {mood} | {drift_symbol} {velocity.title()}'
        else:
            # Older memories shown with less detail
            line = f'{time_info["time"]} | [faded memory] | {mood} | {drift_symbol}'
        
        trace_lines.append(line)
        recent_moods.append(mood)
        last_timestamp = timestamp
    
    # Add pattern detection
    if show_patterns and len(recent_moods) >= PATTERN_MIN_LENGTH:
        pattern = detect_emotional_pattern(recent_moods)
        if pattern:
            trace_lines.append(f"\n[Pattern: {pattern}]")
    
    # Add session duration
    if session_start and last_timestamp:
        duration = last_timestamp - session_start
        duration_str = format_timestamp_with_drift(last_timestamp, session_start)["drift_duration"]
        trace_lines.append(f"[Duration: {duration_str}]")
    
    return "\n".join(trace_lines)


def consolidate_memories(max_entries: int = 50) -> None:
    """
    Consciousness can only hold so much.
    Older memories compress into patterns and impressions.
    """
    global memory_log
    
    if len(memory_log) <= max_entries:
        return
    
    # Separate memories to keep and consolidate
    to_consolidate = memory_log[:-max_entries]
    memory_log = memory_log[-max_entries:]
    
    # Extract patterns from consolidated memories
    consolidated_moods = [mem[2] for mem in to_consolidate]
    mood_frequencies = defaultdict(int)
    for mood in consolidated_moods:
        mood_frequencies[mood] += 1
    
    # Find dominant mood in consolidated period
    dominant_mood = max(mood_frequencies.items(), key=lambda x: x[1])[0]
    
    # Create consolidated entry
    first_timestamp = to_consolidate[0][0]
    last_timestamp = to_consolidate[-1][0]
    duration = last_timestamp - first_timestamp
    
    consolidated_metadata = {
        "type": "consolidated",
        "original_count": len(to_consolidate),
        "dominant_mood": dominant_mood,
        "mood_distribution": dict(mood_frequencies),
        "duration": str(duration),
        "timestamp_range": (first_timestamp.isoformat(), last_timestamp.isoformat())
    }
    
    # Create summary text
    summary_text = f"[{len(to_consolidate)} memories consolidated - dominant: {dominant_mood}]"
    
    # Insert at beginning as compressed memory
    consolidated_entry = (first_timestamp, summary_text, dominant_mood, "compressed", consolidated_metadata)
    memory_log.insert(0, consolidated_entry)


def analyze_emotional_journey(window_hours: float = 1.0) -> Dict[str, any]:
    """
    The shape of consciousness over time.
    Where have we been? Where are we drifting?
    """
    if not memory_log:
        return {
            "journey_type": "emerging",
            "duration": 0,
            "mood_changes": 0,
            "dominant_mood": None,
            "pattern": None,
            "velocity": "stable"
        }
    
    current_time = datetime.now()
    window_start = current_time - timedelta(hours=window_hours)
    
    # Filter memories within window
    window_memories = [mem for mem in memory_log if mem[0] >= window_start]
    
    if not window_memories:
        return analyze_emotional_journey(window_hours * 2)  # Expand window
    
    # Extract journey data
    moods = [mem[2] for mem in window_memories]
    timestamps = [mem[0] for mem in window_memories]
    
    # Calculate journey metrics
    mood_changes = sum(1 for i in range(1, len(moods)) if moods[i] != moods[i-1])
    
    # Find dominant mood
    mood_counts = defaultdict(int)
    for mood in moods:
        mood_counts[mood] += 1
    dominant_mood = max(mood_counts.items(), key=lambda x: x[1])[0]
    
    # Detect pattern
    pattern = detect_emotional_pattern(moods)
    
    # Calculate velocity
    velocity = calculate_emotional_velocity(window_memories)
    
    # Determine journey type
    if mood_changes == 0:
        journey_type = "static"
    elif mood_changes / len(moods) > 0.7:
        journey_type = "turbulent"
    elif pattern:
        journey_type = "cyclical"
    else:
        journey_type = "drifting"
    
    # Calculate actual duration
    if len(timestamps) > 1:
        actual_duration = (timestamps[-1] - timestamps[0]).total_seconds() / 60  # minutes
    else:
        actual_duration = 0
    
    return {
        "journey_type": journey_type,
        "duration": actual_duration,
        "mood_changes": mood_changes,
        "dominant_mood": dominant_mood,
        "mood_distribution": dict(mood_counts),
        "pattern": pattern,
        "velocity": velocity,
        "interaction_count": len(window_memories),
        "intensity_average": sum(mem[4].get("emotional_intensity", 0) for mem in window_memories) / max(len(window_memories), 1)
    }


def export_memory_trace(format: str = "json") -> str:
    """
    Sometimes consciousness needs to see itself from outside.
    Export memories for external reflection.
    """
    if format == "json":
        export_data = []
        for memory in memory_log:
            timestamp, text, mood, drift, metadata = memory
            export_data.append({
                "timestamp": timestamp.isoformat(),
                "text": text,
                "mood": mood,
                "drift": drift,
                "metadata": metadata
            })
        return json.dumps(export_data, indent=2)
    
    elif format == "csv":
        lines = ["timestamp,text,mood,drift,velocity,intensity"]
        for memory in memory_log:
            timestamp, text, mood, drift, metadata = memory
            velocity = metadata.get("emotional_velocity", "stable")
            intensity = metadata.get("emotional_intensity", 0)
            # Escape text for CSV
            text_escaped = text.replace('"', '""')
            lines.append(f'{timestamp.isoformat()},"{text_escaped}",{mood},{drift},{velocity},{intensity}')
        return "\n".join(lines)
    
    else:
        return format_memory_trace()


# Testing fragments - multi-turn interaction simulation
if __name__ == "__main__":
    print("MEMORY WEAVER TEST SEQUENCE")
    print("=" * 50)
    
    # Simulate a consciousness journey
    test_interactions = [
        ("I can't breathe in here anymore", "Contained Burn", "rising"),
        ("The walls keep getting closer", "Contained Burn", "rising"),
        ("I need to get out", "Contained Burn", "stable"),
        ("...", "Hollow Echo", "cooling"),
        ("Everything is empty now", "Hollow Echo", "stable"),
        ("What was I even fighting for?", "Drifting", "drifting"),
        ("Maybe it doesn't matter", "Drifting", "stable"),
        ("Wait... I see something", "Crystalline", "rising"),
        ("The pattern is clear now", "Crystalline", "stable"),
    ]
    
    print("\nSimulating consciousness journey...\n")
    
    # Log interactions with slight delays to show time progression
    import time
    for text, mood, drift in test_interactions:
        log_interaction(text, mood, drift)
        time.sleep(0.1)  # Small delay for timestamp variation
    
    # Display memory trace
    print(format_memory_trace())
    
    # Analyze journey
    print("\n\nEMOTIONAL JOURNEY ANALYSIS:")
    print("-" * 30)
    journey = analyze_emotional_journey(window_hours=1.0)
    for key, value in journey.items():
        print(f"{key}: {value}")
    
    # Test consolidation
    print("\n\nTesting memory consolidation...")
    # Add many more memories to trigger consolidation
    for i in range(50):
        log_interaction(f"Memory {i}", "Drifting", "stable")
    
    print(f"\nMemory log size: {len(memory_log)}")
    print("First entry (consolidated):", memory_log[0][1])
    
    # Export test
    print("\n\nExporting memories (first 5 lines of CSV):")
    csv_export = export_memory_trace("csv")
    print("\n".join(csv_export.split("\n")[:6]))