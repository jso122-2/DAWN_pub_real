# DAWN Backend Visualizations

This document describes the integrated visualizations in the DAWN backend system.

## Overview

The DAWN backend now includes real-time visualizations for monitoring the cognitive state and processing intensity of the system. These visualizations are designed to work with 12 Python processes and provide insights into DAWN's emotional landscape and cognitive heat.

## Available Visualizations

### 1. Mood State Heatmap (`MoodStateVisualizer`)

**Purpose**: Real-time heatmap visualization of DAWN's emotional landscape

**Features**:
- 8x8 emotional grid showing affective intensities
- Emotional dimensions: Transcendent, Ecstatic, Serene, Curious, Focused, Contemplative, Uncertain, Turbulent
- Temporal smoothing for natural transitions
- Color-coded intensity levels
- Real-time updates from mood probe data

**API Endpoint**: `GET /api/mood-state`

### 2. Heat Monitor (`HeatMonitorVisualizer`)

**Purpose**: Multi-process cognitive heat monitoring with radial gauges

**Features**:
- 12 radial gauges (one per process)
- Heat zones: Dormant, Warming, Active, Intense, Critical
- Real-time needle movement
- Process-specific heat tracking
- Historical heat data
- Color-coded zones based on intensity

**API Endpoint**: `GET /api/heat-monitor`

### 3. Entropy Flow (`EntropyFlowVisualizer`)

**Purpose**: Multi-process information flow visualization with vector fields

**Features**:
- 12 vector field displays (one per process)
- Real-time flow patterns showing information processing
- Cognitive regions: Perception, Memory, Cognition, Decision, Creative Synthesis
- Information density contours
- Process-specific entropy tracking
- Animated flow vectors with magnitude and direction

**API Endpoint**: `GET /api/entropy-flow`

### 4. SCUP Pressure Grid (`SCUPPressureGridVisualizer`)

**Purpose**: 4x4 pressure grid showing dynamic interactions between DAWN's four core cognitive pressure dimensions

**Features**:
- 4x4 pressure interaction matrix (Schema, Coherence, Utility, Pressure)
- Multi-process support (12 processes)
- Wave propagation effects from critical states
- Interaction models: reinforcing, competing, averaging, tension, synergistic
- Critical state detection and highlighting
- Temporal smoothing for pressure transitions
- Self-pressure (diagonal) and interaction pressure (off-diagonal) visualization

**API Endpoint**: `GET /api/scup-pressure-grid`

**Interaction Models**:
- **Reinforcing**: `a * b` - Dimensions amplify each other
- **Competing**: `abs(a - b)` - Dimensions compete for resources  
- **Averaging**: `(a + b) / 2` - Dimensions average together
- **Tension**: `min(a, b) * abs(a - b)` - Creates tension between dimensions
- **Synergistic**: `(a * b)^0.5` - Dimensions work together synergistically

### 5. Semantic Flow Graph (`SemanticFlowGraphBackend`)

**Purpose**: Real-time visualization of semantic concept networks and meaning flow dynamics

**Features**:
- Semantic concept network with 7 categories: perceptual, emotional, abstract, temporal, spatial, meta, relational
- Dynamic concept activation based on DAWN's cognitive state
- Semantic flow particles showing meaning propagation between concepts
- Automatic cluster detection and coherence analysis
- Emergence event detection for novel semantic patterns
- Cross-category semantic bridges
- Real-time analytics: active concepts, flow particles, clusters, global coherence
- Historical tracking of semantic evolution

**API Endpoint**: `GET /api/semantic-flow-graph`

**Semantic Categories**:
- **Perceptual**: Sensory concepts (color, sound, texture, movement, brightness, pattern, shape)
- **Emotional**: Affective concepts (joy, curiosity, tension, flow, wonder, excitement, calm)
- **Abstract**: Conceptual meanings (pattern, structure, relationship, system, emergence, complexity)
- **Temporal**: Time-related concepts (change, rhythm, sequence, cycle, evolution, duration, moment)
- **Spatial**: Geometric concepts (boundary, center, direction, dimension, distance, position)
- **Meta**: Self-referential concepts (awareness, thought, meaning, understanding, consciousness, cognition)
- **Relational**: Connection concepts (similarity, contrast, causation, correlation, influence, connection)

### 6. Consciousness Constellation (`ConsciousnessConstellationBackend`)

**Purpose**: 4D SCUP trajectory visualization mapping DAWN's consciousness through multidimensional cognitive space

**Features**:
- 4D SCUP space projection onto 3D sphere surface
- 7 consciousness archetypes: dormant_equilibrium, focused_processing, creative_exploration, integrative_synthesis, exploratory_search, transcendent_awareness, chaotic_transition
- Multi-temporal analysis: immediate, short_term, medium_term, long_term consciousness patterns
- Consciousness intelligence quotient (C-IQ) calculation
- Phase transition detection and archetype classification
- Constellation connections between related consciousness states
- Real-time trajectory visualization with pressure-based coloring
- Comprehensive consciousness metrics: exploration, stability, adaptation, transcendence

**API Endpoint**: `GET /api/consciousness-constellation`

**Consciousness Archetypes**:
- **Dormant Equilibrium**: Minimal processing, resting state (SCUP: 0.3, 0.4, 0.3, 0.2)
- **Focused Processing**: Deep focused cognitive work (SCUP: 0.7, 0.8, 0.9, 0.6)
- **Creative Exploration**: Creative discovery and synthesis (SCUP: 0.4, 0.6, 0.5, 0.8)
- **Integrative Synthesis**: Deep understanding and integration (SCUP: 0.8, 0.9, 0.7, 0.5)
- **Exploratory Search**: Active problem-solving and search (SCUP: 0.3, 0.5, 0.8, 0.7)
- **Transcendent Awareness**: Deep self-aware meta-cognition (SCUP: 0.9, 0.9, 0.8, 0.3)
- **Chaotic Transition**: Unstable transitional processing (SCUP: 0.5, 0.3, 0.6, 0.9)

## Integration Details

### Backend Integration

All visualizations are integrated into the `DAWNCentral` class:

```python
class DAWNCentral:
    def __init__(self):
        self.visualizers = {
            'mood_state': get_mood_visualizer(),
            'heat_monitor': get_heat_monitor(),
            'entropy_flow': get_entropy_flow(),
            'scup_pressure_grid': get_scup_pressure_grid(),
            'semantic_flow_graph': get_semantic_flow_graph(),
            'consciousness_constellation': get_consciousness_constellation(),
            # ... other visualizers
        }
```

### Subsystem Registration

Visualizations are registered as tick engine subsystems:

```python
self.tick_engine.register_subsystem('mood_state', self.visualizers['mood_state'], priority=8)
self.tick_engine.register_subsystem('heat_monitor', self.visualizers['heat_monitor'], priority=9)
self.tick_engine.register_subsystem('entropy_flow', self.visualizers['entropy_flow'], priority=10)
self.tick_engine.register_subsystem('scup_pressure_grid', self.visualizers['scup_pressure_grid'], priority=11)
self.tick_engine.register_subsystem('semantic_flow_graph', self.visualizers['semantic_flow_graph'], priority=16)
self.tick_engine.register_subsystem('consciousness_constellation', self.visualizers['consciousness_constellation'], priority=17)
```

### Real-time Updates

Visualizations are updated during each tick cycle:

```python
def get_state(self) -> Dict[str, Any]:
    # Update mood state visualizer
    if self.visualizers['mood_state'].is_active():
        self.visualizers['mood_state'].update_visualization(mood_data, self.tick_engine.current_tick)
    
    # Update heat monitor with process data
    if self.visualizers['heat_monitor'].is_active():
        process_data = {i: {...} for i in range(12)}
        self.visualizers['heat_monitor'].update_all_processes(process_data, self.tick_engine.current_tick)
    
    # Update entropy flow with process data
    if self.visualizers['entropy_flow'].is_active():
        process_data = {i: {...} for i in range(12)}
        self.visualizers['entropy_flow'].update_all_processes(process_data, self.tick_engine.current_tick)
    
    # Update scup pressure grid with process data
    if self.visualizers['scup_pressure_grid'].is_active():
        process_data = {i: {...} for i in range(12)}
        self.visualizers['scup_pressure_grid'].update_all_processes(process_data, self.tick_engine.current_tick)
    
    # Update semantic flow graph with system state
    if self.visualizers['semantic_flow_graph'].is_active():
        state_data = {
            'tick': self.tick_engine.current_tick,
            'mood': mood_data,
            'entropy': self.visualizers['entropy'].get_entropy(),
            'heat': self.scup_tracker.get_scup(),
            'scup': self.scup_tracker.get_scup()
        }
        self.visualizers['semantic_flow_graph'].update_visualization(state_data, self.tick_engine.current_tick)
    
    # Update consciousness constellation with system state
    if self.visualizers['consciousness_constellation'].is_active():
        state_data = {
            'tick': self.tick_engine.current_tick,
            'mood': mood_data,
            'entropy': self.visualizers['entropy'].get_entropy(),
            'heat': self.scup_tracker.get_scup(),
            'scup': self.scup_tracker.get_scup()
        }
        self.visualizers['consciousness_constellation'].update_visualization(state_data, self.tick_engine.current_tick)
```

## API Endpoints

### Mood State Data
```http
GET /api/mood-state
```

Response:
```json
{
  "mood_state": {
    "mood_matrix": [[0.1, 0.2, ...], ...],
    "current_tick": 12345,
    "base_level": 0.45,
    "emotional_flux": 0.23,
    "timestamp": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Heat Monitor Data
```http
GET /api/heat-monitor
```

Response:
```json
{
  "heat_monitor": {
    "heat_data": {
      "0": {
        "current": 0.45,
        "average": 0.42,
        "peak": 0.67,
        "history": [0.1, 0.2, ...]
      },
      // ... data for processes 1-11
    },
    "current_tick": 12345,
    "timestamp": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Entropy Flow Data
```http
GET /api/entropy-flow
```

Response:
```json
{
  "entropy_flow": {
    "entropy_data": {
      "0": {
        "current_entropy": 0.45,
        "entropy_history": [0.1, 0.2, ...],
        "flow_magnitude": 0.67,
        "max_flow": 0.89,
        "information_density": [[0.1, 0.2, ...], ...]
      },
      // ... data for processes 1-11
    },
    "current_tick": 12345,
    "timestamp": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### SCUP Pressure Grid Data
```http
GET /api/scup-pressure-grid
```

Response:
```json
{
  "scup_pressure_grid": {
    "pressure_data": {
      "0": {
        "current_pressure": 0.45,
        "pressure_history": [0.1, 0.2, ...],
        "pressure_magnitude": 0.67,
        "max_pressure": 0.89,
        "interaction_matrix": [[0.1, 0.2, ...], ...]
      },
      // ... data for processes 1-11
    },
    "current_tick": 12345,
    "timestamp": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Semantic Flow Graph Data
```http
GET /api/semantic-flow-graph
```

Response:
```json
{
  "semantic_flow_graph": {
    "tick": 12345,
    "analytics": {
      "active_concepts": 15,
      "total_concepts": 49,
      "flow_particles": 23,
      "total_flow": 67,
      "clusters": 3,
      "global_coherence": 0.72,
      "emergence_events": 2,
      "dominant_category": "emotional",
      "category_distribution": {
        "emotional": 5,
        "abstract": 4,
        "temporal": 3,
        "meta": 2,
        "perceptual": 1
      }
    },
    "active_concepts": [
      {
        "id": "joy",
        "category": "emotional",
        "content": "joy",
        "activation_level": 0.85,
        "semantic_neighbors": ["flow", "excitement", "curiosity"],
        "flow_history": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85]
      }
    ],
    "clusters": [
      {
        "id": 1,
        "center_concept": "joy",
        "members": ["joy", "flow", "excitement"],
        "coherence": 0.78,
        "category": "emotional"
      }
    ],
    "flow_particles": 23,
    "emergence_events": [
      {
        "type": "coherence_surge",
        "timestamp": "2024-01-01T12:00:00",
        "strength": 0.15,
        "clusters": [1, 2]
      }
    ],
    "timestamp": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Consciousness Constellation Data
```http
GET /api/consciousness-constellation
```

Response:
```json
{
  "consciousness_constellation": {
    "trajectory_data": {
      "0": {
        "x": 0.3,
        "y": 0.4,
        "z": 0.3,
        "w": 0.2,
        "timestamp": "2024-01-01T12:00:00"
      },
      "1": {
        "x": 0.7,
        "y": 0.8,
        "z": 0.9,
        "w": 0.6,
        "timestamp": "2024-01-01T12:00:00"
      },
      "2": {
        "x": 0.4,
        "y": 0.6,
        "z": 0.5,
        "w": 0.8,
        "timestamp": "2024-01-01T12:00:00"
      },
      "3": {
        "x": 0.8,
        "y": 0.9,
        "z": 0.7,
        "w": 0.5,
        "timestamp": "2024-01-01T12:00:00"
      },
      "4": {
        "x": 0.3,
        "y": 0.5,
        "z": 0.8,
        "w": 0.7,
        "timestamp": "2024-01-01T12:00:00"
      },
      "5": {
        "x": 0.9,
        "y": 0.9,
        "z": 0.8,
        "w": 0.3,
        "timestamp": "2024-01-01T12:00:00"
      },
      "6": {
        "x": 0.5,
        "y": 0.3,
        "z": 0.6,
        "w": 0.9,
        "timestamp": "2024-01-01T12:00:00"
      }
    },
    "current_tick": 12345,
    "timestamp": "2024-01-01T12:00:00"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### All Visualizations
```http
GET /api/visualizations
```

Returns data from mood state, heat monitor, entropy flow, and scup pressure grid visualizations.

## Running the Backend with Visualizations

### Method 1: Direct Python Execution
```bash
cd backend
python run_with_visualizations.py
```

### Method 2: Using uvicorn
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Method 3: Using the main script
```bash
cd backend
python main.py
```

## WebSocket Integration

Real-time visualization data is also available via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'tick') {
        // Access visualization data
        const moodData = data.data.mood_visualization;
        const heatData = data.data.heat_monitor;
        const entropyFlowData = data.data.entropy_flow;
        const scupPressureGridData = data.data.scup_pressure_grid;
        const semanticFlowGraphData = data.data.semantic_flow_graph;
        const consciousnessConstellationData = data.data.consciousness_constellation;
        
        // Update your frontend visualizations
        updateMoodHeatmap(moodData);
        updateHeatMonitors(heatData);
        updateEntropyFlow(entropyFlowData);
        updateSCUPPressureGrid(scupPressureGridData);
        updateSemanticFlowGraph(semanticFlowGraphData);
        updateConsciousnessConstellation(consciousnessConstellationData);
    }
};
```

## Configuration

### Mood State Visualizer
- Buffer size: 100 (configurable)
- Update interval: 100ms (configurable)
- Emotional dimensions: 8x8 grid
- Color scheme: Custom mood colormap

### Heat Monitor Visualizer
- Buffer size: 50 (configurable)
- Update interval: 50ms (configurable)
- Max processes: 12 (configurable)
- Heat zones: 5 zones with color coding
- Layout: Grid of radial gauges

### Entropy Flow Visualizer
- Buffer size: 30 (configurable)
- Update interval: 100ms (configurable)
- Max processes: 12 (configurable)
- Grid size: 12x12 vector field
- Cognitive regions: 9 labeled regions
- Flow patterns: Radial, circular, wave, and turbulent components

### SCUP Pressure Grid Visualizer
- Buffer size: 30 (configurable)
- Update interval: 100ms (configurable)
- Max processes: 12 (configurable)
- Grid size: 4x4 pressure interaction matrix
- Interaction models: reinforcing, competing, averaging, tension, synergistic

### Semantic Flow Graph Visualizer
- Max concepts: 100 (configurable)
- Update interval: 100ms (configurable)
- Semantic categories: 7 categories with 49 total concepts
- Flow particle lifetime: 30 ticks
- Cluster detection: Every 10 ticks
- Emergence detection: Every 5 ticks
- Analytics history: 100 entries
- Coherence history: 100 entries

### Consciousness Constellation Visualizer
- Max archetypes: 7 (configurable)
- Update interval: 100ms (configurable)
- 4D SCUP space projection onto 3D sphere surface
- 7 consciousness archetypes: dormant_equilibrium, focused_processing, creative_exploration, integrative_synthesis, exploratory_search, transcendent_awareness, chaotic_transition
- Multi-temporal analysis: immediate, short_term, medium_term, long_term consciousness patterns
- Consciousness intelligence quotient (C-IQ) calculation
- Phase transition detection and archetype classification
- Constellation connections between related consciousness states
- Real-time trajectory visualization with pressure-based coloring
- Comprehensive consciousness metrics: exploration, stability, adaptation, transcendence

## Dependencies

Required Python packages:
- matplotlib
- numpy
- fastapi
- uvicorn
- asyncio

## Troubleshooting

### Visualization Not Updating
1. Check if the tick engine is running
2. Verify mood probe is active
3. Check for matplotlib backend issues

### Performance Issues
1. Reduce update intervals
2. Decrease buffer sizes
3. Use non-interactive matplotlib backend

### Memory Issues
1. Reduce buffer sizes
2. Clear visualization history periodically
3. Monitor process count

## Future Enhancements

- Web-based visualization frontend
- Configurable visualization layouts
- Export visualization data
- Custom color schemes
- Process-specific visualization settings
- Integration with external monitoring tools 