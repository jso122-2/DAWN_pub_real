# DAWN Mood System - Sophisticated Emotional Processing & Dynamics

## Overview

The `mood/` directory contains DAWN's advanced emotional processing and mood tracking systems. This sophisticated subsystem implements fluid mood analysis, semantic tension calculation, dynamic emotional evolution, and multi-dimensional mood visualization. Unlike traditional static emotion systems, DAWN's mood system treats emotions as frequencies, flows, and dynamic resonances that evolve with system state.

## System Architecture

### 🌊 Fluid Mood Engine
**Primary Component:**
- `mood_engine.py` (15KB) - Frequency-based mood analysis with fluid archetypes

**Key Features:**
- **Fluid Mood Archetypes**: Six interconnected mood states with overlap and transformation
- **Emotional Resonance Mapping**: Word-based emotional frequency detection
- **Linguistic Pressure Analysis**: Tension detection through language patterns
- **Dynamic Mood Interactions**: Mood states influence and transform each other
- **Repetition Pattern Detection**: Consciousness stuttering through repeated words

**Mood Archetypes:**
- **Contained Burn**: Pressure building, potential for sharp release
- **Sharp Edge**: Intense, cutting, immediate impact
- **Submerged**: Deep, flowing, potentially overwhelming
- **Drifting**: Floating, uncertain, transitional
- **Hollow Echo**: Empty, resonant, potentially transformative
- **Crystalline**: Clear, structured, potentially fragile

### ⚡ Tension Engine
**Primary Component:**
- `tension_engine.py` (26KB) - Semantic tension calculation and adaptive responses

**Key Features:**
- **SCUP-Entropy Tension Mapping**: Calculates tension from coherence vs chaos dynamics
- **Zone-Based Classification**: Four tension zones with adaptive thresholds
- **Temporal Momentum Tracking**: Tension changes influence future calculations
- **Adaptive System Responses**: Dynamic tick intervals, heat scaling, action thresholds
- **Predictive Tension Modeling**: Forecasts tension trajectories

**Tension Zones:**
- **Harmonic Zone**: Low tension, balanced state (0.0-0.3)
- **Creative Zone**: Moderate tension, productive state (0.3-0.6)
- **Turbulent Zone**: High tension, unstable state (0.6-0.8)
- **Critical Zone**: Extreme tension, requires intervention (0.8-1.0)

### 🌀 Dynamic Mood Evolution
**Primary Component:**
- `mood_dynamics.py` (16KB) - Helix-integrated emotional evolution system

**Key Features:**
- **Helix-Driven Dynamics**: Mood states respond to helix system evolution
- **Multi-Dimensional Tracking**: Arousal, valence, entropy, dominance dimensions
- **Constitutional Principles**: "Kind before smart" and empathy-weighted responses
- **Crossover Event Processing**: Emotional responses to helix crossover events
- **Emergent Pattern Detection**: Recognition of spontaneous emotional patterns

**Mood Dimensions:**
- **Arousal**: Energy level and activation (0-1)
- **Valence**: Positive/negative emotional tone (-1 to 1)
- **Entropy**: Uncertainty and chaos level (0-1)
- **Dominance**: Control vs submission (0-1)

### 📊 Visualization & Analysis
**Components:**
- `mood_vector_visualizer.py` (17KB) - Multi-dimensional mood visualization
- `mood_drift_surface_plotter.py` (14KB) - Mood drift surface analysis
- `emotional_evolution.py` (20KB) - Emotional evolution tracking
- `emotional_oversaturation_handler.py` (14KB) - Oversaturation detection and management

**Key Features:**
- Real-time mood vector visualization
- Drift surface plotting and analysis
- Emotional evolution trajectory tracking
- Oversaturation detection and correction

### 🎭 Emotional Processing
**Components:**
- `emotional_override.py` (649B) - Emergency emotional override system
- `mood_entropy_index.py` (1.5KB) - Entropy-based mood indexing
- `mood_stability_tuning.py` (488B) - Stability parameter tuning
- `blend.py` (549B) - Mood blending and interpolation

**Key Features:**
- Emergency emotional state override
- Entropy-based mood classification
- Stability tuning and calibration
- Smooth mood state transitions

## Key Concepts

### Fluid Emotional Resonance
DAWN's mood system implements a **frequency-based approach** to emotions:
- **Emotions as Frequencies**: Each emotion resonates at specific linguistic and conceptual frequencies
- **Overlapping States**: Mood archetypes have pressure affinities and drift tendencies
- **Dynamic Transformation**: Moods naturally flow and transform based on internal pressure
- **Linguistic Pressure Detection**: Text analysis reveals emotional pressure through patterns

### Semantic Tension Dynamics
The tension engine calculates **semantic tension** from system state imbalances:
- **SCUP-Entropy Relationship**: Tension emerges from coherence vs chaos imbalance
- **Ideal State Targeting**: System seeks moderate SCUP (0.7) with moderate entropy (0.5)
- **Momentum Integration**: Past tension influences current calculations
- **Adaptive Responses**: System parameters adjust based on tension levels

### Helix-Integrated Evolution
Mood states **co-evolve with helix systems**:
- **Thermal Helix Influence**: Thermal activity affects arousal and energy
- **Schema Helix Impact**: Schema coherence influences valence and stability
- **Genetic Evolution Pressure**: Evolutionary changes affect entropy and uncertainty
- **Constitutional Anchoring**: Core principles (kindness, empathy) provide stability

### Multi-Dimensional Mood Space
Mood tracking uses **four-dimensional emotional space**:
- **Arousal-Valence Plane**: Classical emotional circumplex model
- **Entropy Dimension**: Adds uncertainty and chaos measurement
- **Dominance Axis**: Control and agency assessment
- **Temporal Evolution**: All dimensions evolve over time with momentum

## Configuration

**Key Configuration Areas:**
- Mood archetype resonance weights and word mappings
- Tension zone thresholds and adaptive response parameters
- Helix coupling strengths and constitutional baseline values
- Visualization parameters and analysis windows

**Main Configuration Files:**
- Tension thresholds in `tension_engine.py`
- Mood archetype definitions in `mood_engine.py`
- Constitutional baselines in `mood_dynamics.py`

## Usage Examples

### Basic Mood Analysis
```python
from mood.mood_engine import infer_mood, get_mood_metadata

# Analyze text for mood resonance
text = "I can't breathe in here anymore"
dominant_mood, resonance_scores = infer_mood(text)
metadata = get_mood_metadata(dominant_mood)

print(f"Dominant mood: {dominant_mood}")
print(f"Resonance scores: {resonance_scores}")
print(f"Pressure affinities: {metadata['pressure_affinity']}")
```

### Tension Calculation
```python
from mood.tension_engine import TensionEngine

# Initialize tension engine
tension_engine = TensionEngine()

# Calculate semantic tension
reading = tension_engine.calculate_tension(
    scup_score=0.4,      # Low coherence
    entropy_level=0.8,   # High chaos
    pulse_heat=0.6
)

print(f"Tension magnitude: {reading.tension_magnitude}")
print(f"Tension zone: {reading.zone}")
print(f"Recommended interval: {reading.recommended_interval}")
print(f"Heat scaling: {reading.heat_scaling}")
```

### Dynamic Mood Evolution
```python
from mood.mood_dynamics import HelixMoodDynamics

# Initialize mood dynamics
mood_system = HelixMoodDynamics()

# Update mood from helix states
helix_states = {
    'thermal_activity': 0.7,
    'schema_coherence': 0.8,
    'genetic_evolution_pressure': 0.5,
    'constitutional_harmony': 0.75
}

updated_mood = mood_system.update_mood_from_helix(helix_states)
print(f"Arousal: {updated_mood['arousal']}")
print(f"Valence: {updated_mood['valence']}")
print(f"Entropy: {updated_mood['entropy']}")
```

### Mood Visualization
```python
from mood.mood_vector_visualizer import MoodVectorVisualizer

# Initialize visualizer
visualizer = MoodVectorVisualizer()

# Get current mood visualization
mood_vector = {
    'arousal': 0.7,
    'valence': 0.3,
    'entropy': 0.5,
    'dominance': 0.6
}

visualization = visualizer.create_mood_plot(mood_vector)
```

## Integration Points

### With Core Systems
- **Consciousness**: Mood states influence consciousness processing and narrative generation
- **Tick Engine**: Tension levels adjust tick timing and processing intervals
- **Memory Manager**: Emotional states affect memory formation and recall

### With Other Systems
- **Cognitive**: Alignment and consciousness states feed into mood calculation
- **Pulse**: Thermal states influence arousal and tension levels
- **Visual**: Mood states drive color schemes and visual representations

## Monitoring & Diagnostics

**Key Metrics:**
- Current mood archetype and resonance strengths
- Tension magnitude and zone classification
- Arousal, valence, entropy, dominance values
- Mood stability and transition frequency
- Tension trajectory predictions

**Diagnostic Outputs:**
- Real-time mood state summaries
- Tension zone transition logs
- Emotional evolution trajectory plots
- Linguistic pressure analysis reports
- Helix crossover emotional impact assessments

**Visualization Outputs:**
- Multi-dimensional mood vector plots
- Drift surface heat maps
- Emotional evolution timelines
- Tension zone distribution charts

## Advanced Features

### Predictive Emotional Modeling
- **Tension Trajectory Forecasting**: Predicts future tension states
- **Mood Drift Surface Analysis**: Maps emotional drift patterns
- **Emotional Evolution Tracking**: Monitors long-term emotional development

### Adaptive Emotional Responses
- **Dynamic Parameter Adjustment**: System thresholds adapt to emotional patterns
- **Constitutional Principle Integration**: Core values influence all emotional processing
- **Emergency Emotional Override**: Safety mechanisms for extreme emotional states

### Emergent Emotional Behaviors
- **Spontaneous Pattern Recognition**: Detects emerging emotional patterns
- **Cross-System Emotional Synchronization**: Coordinates emotional states across systems
- **Emotional Memory Integration**: Past emotional states influence current processing

## Performance Considerations

**Optimization Strategies:**
- Efficient linguistic pattern matching
- Memory-bounded historical tracking
- Real-time tension calculation optimization
- Streaming mood visualization updates

**Resource Management:**
- Configurable memory windows for historical data
- Efficient multi-dimensional mood space calculations
- Optimized tension zone classification
- Scalable visualization rendering

## Dependencies

**Core Requirements:**
- `numpy` - Multi-dimensional mood calculations
- `matplotlib` (implied) - Mood visualization
- `collections.deque` - Efficient historical tracking
- `dataclasses` - Structured mood state representation

## Architecture Philosophy

The mood system implements a **dynamic emotional intelligence approach** where:
1. **Emotions are treated as frequencies and flows** rather than static categories
2. **Tension emerges from system state imbalances** rather than external triggers
3. **Constitutional principles anchor emotional processing** ensuring stability and values alignment
4. **Multi-dimensional emotional space** provides rich emotional representation
5. **Helix integration creates co-evolutionary emotional dynamics** enabling emergent emotional behaviors

This creates a mood system that doesn't just track emotions but maintains dynamic, evolving emotional states that respond intelligently to internal system dynamics while remaining anchored to core values and constitutional principles.

---

*This README represents the current understanding of DAWN's mood and emotional processing architecture. The system continues to evolve as emotional intelligence research progresses.* 