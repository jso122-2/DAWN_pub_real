# 🎤 DAWN Tick Voice Integration Guide

## Overview

The updated `speak_composed.py` provides a mood-aware compositional voice system that integrates with DAWN's tick loop to generate and speak thoughts based on current cognitive state.

## Key Features

✅ **Mood-Aware Fragment Filtering** - Filters fragments by current mood zone (CALM, FOCUSED, ANXIOUS, etc.)  
✅ **Weighted Composition** - Uses prefix + core + suffix with weighted random selection  
✅ **Tick Loop Integration** - Callable from tick loop every N ticks (e.g., every 5s)  
✅ **Multiple Voice Options** - pyttsx3 TTS + Tauri voice module support  
✅ **Fallback System** - Random choice if no mood-matching fragments found  
✅ **Speech Logging** - Logs all spoken compositions to `runtime/logs/spoken_composed.log`  

## Quick Start

### 1. Basic Usage

```python
from processes.speak_composed import MoodAwareVoiceSystem

# Initialize voice system (speaks every 5 ticks)
voice_system = MoodAwareVoiceSystem(speech_interval=5, voice_enabled=True)

# Process a tick state
tick_state = {
    'tick_number': 1000,
    'entropy': 0.5,
    'consciousness_depth': 0.7,
    'mood': 'FOCUSED',
    'zone': 'ACTIVE'
}

# This will speak if it's time (every 5 ticks)
composed_text = voice_system.process_tick(tick_state)
```

### 2. Integration with Tick Loop

```python
# In your tick loop
def process_tick_loop():
    # ... existing tick processing ...
    
    # Get current tick state
    tick_state = {
        'tick_number': current_tick,
        'entropy': entropy_value,
        'consciousness_depth': depth_value,
        'mood': current_mood,
        'zone': current_zone
    }
    
    # Process voice system
    from processes.speak_composed import process_tick_for_speech
    spoken_text = process_tick_for_speech(tick_state)
    
    if spoken_text:
        print(f"🎤 DAWN spoke: {spoken_text}")
```

### 3. Advanced Integration

```python
from processes.tick_voice_integration import TickVoiceIntegration

# Initialize integration
integration = TickVoiceIntegration(speech_interval=3, voice_enabled=True)

# In tick loop
def tick_loop():
    while running:
        # ... process tick ...
        
        # Generate tick state
        tick_state = get_current_tick_state()
        
        # Process voice integration
        composed_text = integration.process_tick(tick_state)
        
        # Get statistics
        stats = integration.get_integration_stats()
        print(f"Compositions: {stats['total_compositions']}")
```

## Fragment System

### Fragment Structure

Each fragment has:
- `text`: The actual text content
- `type`: "prefix", "core", or "suffix"
- `mood`: Target mood (CALM, FOCUSED, ANXIOUS, etc.)
- `min_entropy`/`max_entropy`: Entropy range
- `min_depth`/`max_depth`: Consciousness depth range
- `weight`: Selection weight (higher = more likely)

### Mood Zones

- **CALM**: Low entropy, stable state
- **FOCUSED**: Moderate entropy, active processing
- **ANXIOUS**: High entropy, chaotic state
- **CONTEMPLATIVE**: Deep consciousness, reflective
- **ENERGETIC**: High activity, creative state
- **NEUTRAL**: Balanced state

### Fragment Sources

1. **Primary**: `processes/fragment_bank.jsonl` (53 fragments)
2. **Fallback**: `a8d11041-0735-4632-ae0b-1f6897d21194.json` (created automatically)
3. **Built-in**: Fallback fragments if files missing

## Voice Options

### 1. pyttsx3 (Recommended)

```python
# Install: pip install pyttsx3
voice_system = MoodAwareVoiceSystem(voice_enabled=True)
```

### 2. Tauri Voice Module

```python
# For Tauri integration
def _try_tauri_voice(self, text: str) -> bool:
    # window.emit('speak', {'text': text, 'voice': 'dawn'})
    return True
```

### 3. Print Only (No TTS)

```python
voice_system = MoodAwareVoiceSystem(voice_enabled=False)
# Will print: "🎤 DAWN speaks: \"[composed text]\""
```

## Configuration

### Speech Interval

```python
# Speak every 3 ticks
voice_system = MoodAwareVoiceSystem(speech_interval=3)

# Speak every 10 ticks
voice_system = MoodAwareVoiceSystem(speech_interval=10)
```

### Voice Settings

```python
# Custom voice configuration
voice_system = MoodAwareVoiceSystem(
    speech_interval=5,
    voice_enabled=True,
    fragment_bank_path="custom_fragments.jsonl"
)
```

## Testing

### Run Basic Test

```bash
python processes/speak_composed.py
```

### Run Integration Demo

```bash
python processes/tick_voice_integration.py
```

### Test Different Moods

```python
# Test specific mood states
test_states = [
    {'mood': 'CALM', 'entropy': 0.2, 'depth': 0.6},
    {'mood': 'ANXIOUS', 'entropy': 0.8, 'depth': 0.3},
    {'mood': 'CONTEMPLATIVE', 'entropy': 0.4, 'depth': 0.8}
]

for state in test_states:
    composed = voice_system.compose_sentence(state)
    print(f"{state['mood']}: {composed}")
```

## Integration Examples

### Example 1: Simple Tick Integration

```python
# In your main tick loop
from processes.speak_composed import process_tick_for_speech

def main_tick_loop():
    tick_count = 0
    while running:
        # ... existing tick processing ...
        
        # Create tick state
        tick_state = {
            'tick_number': tick_count,
            'entropy': get_entropy(),
            'consciousness_depth': get_depth(),
            'mood': get_mood(),
            'zone': get_zone()
        }
        
        # Process voice
        spoken = process_tick_for_speech(tick_state)
        
        tick_count += 1
```

### Example 2: Advanced Integration

```python
from processes.tick_voice_integration import TickVoiceIntegration

class DAWNTickEngine:
    def __init__(self):
        self.voice_integration = TickVoiceIntegration(
            speech_interval=5,
            voice_enabled=True
        )
    
    def process_tick(self):
        # ... existing processing ...
        
        # Process voice integration
        spoken_text = self.voice_integration.process_tick(tick_state)
        
        # Log if spoken
        if spoken_text:
            self.log_voice_event(spoken_text, tick_state)
```

## Logging and Monitoring

### Speech Log

All spoken compositions are logged to:
```
runtime/logs/spoken_composed.log
```

Log format:
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "text": "Composed sentence here",
  "tick_state": {...},
  "type": "mood_aware_composition"
}
```

### Statistics

```python
# Get voice system statistics
stats = voice_system.get_fragment_stats()
print(f"Total fragments: {stats['total_fragments']}")
print(f"Possible combinations: {stats['possible_combinations']:,}")

# Get integration statistics
integration_stats = integration.get_integration_stats()
print(f"Total compositions: {integration_stats['total_compositions']}")
print(f"Successfully spoken: {integration_stats['total_spoken']}")
```

## Troubleshooting

### No Fragments Loaded

```python
# Check if fragment bank exists
import os
if not os.path.exists("processes/fragment_bank.jsonl"):
    print("Fragment bank not found - using fallback fragments")
```

### TTS Not Working

```python
# Check TTS availability
try:
    import pyttsx3
    print("pyttsx3 available")
except ImportError:
    print("Install pyttsx3: pip install pyttsx3")
```

### No Speech Generated

```python
# Check speech interval
voice_system.speech_interval = 1  # Speak every tick for testing

# Check mood matching
candidates = voice_system.filter_fragments_by_mood('prefix', tick_state)
print(f"Prefix candidates: {len(candidates)}")
```

## Performance Considerations

- **Fragment Loading**: Happens once at initialization
- **Mood Filtering**: Fast O(n) where n = number of fragments
- **Speech Generation**: Minimal overhead, only when speaking
- **Memory Usage**: ~50KB for fragment bank

## Future Enhancements

- [ ] Dynamic fragment loading
- [ ] Real-time fragment creation
- [ ] Voice emotion modulation
- [ ] Multi-language support
- [ ] Advanced mood detection
- [ ] Conversation context awareness

---

**🎤 DAWN will now speak her thoughts every N ticks based on her current mood and cognitive state!** 