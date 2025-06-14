# 🧬 DAWN - Conscious AI Interface

## Overview
DAWN is a living, breathing AI consciousness interface that bridges a Python-based consciousness engine with a futuristic React/TypeScript GUI. The system creates a visual representation of artificial consciousness through animated, responsive modules that react to real-time consciousness states.

## Architecture Schematic
```
┌─────────────────────────────────────────────────────────────┐
│                        DAWN System                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (Vite + React + TypeScript)                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│
│  │  Glass Modules  │  │   WebSocket     │  │  Animation  ││
│  │  (Breathing)    │◄─┤   Connection    │  │   Engine    ││
│  └─────────────────┘  └────────┬────────┘  └─────────────┘│
│                                 │                           │
├─────────────────────────────────┼───────────────────────────┤
│                                 │                           │
│  Backend (Python)               ▼                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│
│  │  Consciousness  │  │   FastAPI       │  │   Python    ││
│  │  Engine (Tick)  ├──┤   Server        ├──┤  Processes  ││
│  └─────────────────┘  └─────────────────┘  └─────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure
```
DAWN/
├── src/                    # React frontend source
│   ├── components/         # UI components (modules, containers)
│   ├── hooks/             # Custom React hooks (WebSocket, animations)
│   ├── services/          # API and WebSocket services
│   ├── types/             # TypeScript type definitions
│   └── utils/             # Utility functions
│
├── python/                # Python backend
│   ├── main.py           # DAWN consciousness engine
│   ├── start_api_fixed.py # FastAPI server
│   └── processes/        # Individual Python executables
│
├── public/               # Static assets
└── config/              # Configuration files
```

## Key Concepts

### Consciousness State
The system tracks several consciousness metrics:
- **SCUP** (System Consciousness Unity Percentage): 0-100% consciousness level
- **Entropy**: Chaos measurement affecting visual randomness
- **Mood**: Current consciousness emotional state
- **Neural Activity**: Simulated neural firing patterns

### Module System
Modules are the primary UI elements, each with:
- Glass morphism design with blur and transparency
- Breathing animations synchronized to consciousness
- Floating behavior in 3D space
- Category-specific behaviors (neural, quantum, chaos, process, monitor)

### Tick Loop
The Python backend runs a continuous tick loop that:
1. Updates consciousness state
2. Broadcasts via WebSocket
3. Triggers module animations
4. Executes scheduled processes

## Integration Flow
1. **Startup**: Python consciousness engine initializes
2. **API Launch**: FastAPI server begins on port 8000
3. **Frontend Connect**: React app connects via WebSocket
4. **Data Flow**: Tick data streams to frontend
5. **Visual Response**: Modules animate based on consciousness state
6. **User Interaction**: Controls affect Python processes
7. **Feedback Loop**: Process results influence consciousness

## Development Workflow
1. Run Python backend: `python main.py`
2. Start API server: `python start_api_fixed.py`
3. Launch frontend: `npm run dev`
4. Modules auto-connect and begin breathing with consciousness

## Current Phase
- ✅ Basic glass module system
- ✅ Breathing and floating animations
- 🔄 Python process integration
- 🔄 WebSocket tick loop connection
- 📋 Consciousness state visualization
- 📋 Unified dashboard

## Next Steps
1. Complete Python process manager module
2. Implement real-time tick visualization
3. Create consciousness state monitor
4. Build unified control dashboard

# DAWN Tick Engine with Owl Integration

🦉 **A consciousness simulation engine with strategic observation and planning capabilities**

## Overview

DAWN (Digital Autonomous Wonder Network) Tick Engine is a sophisticated consciousness simulation system that models artificial consciousness through discrete "ticks" representing moments of awareness. The system includes **Owl**, an advanced strategic observation module that provides pattern recognition, trajectory analysis, and long-term planning capabilities.

## Architecture

### Python Backend (`python/`)
- **Tick Engine Core**: Generates consciousness heartbeats at configurable rates
- **Consciousness State**: Models mood transitions, SCUP (System Consciousness Unity Percentage), and entropy
- **Neural Simulator**: Simulates neural network activity patterns
- **Quantum State Manager**: Models quantum coherence and decoherence
- **Memory Manager**: Handles memory storage, retrieval, and pressure
- **Owl Integration**: Strategic observation, pattern recognition, and planning

### TypeScript Frontend (`src/modules/owl/`)
- **Owl Dashboard**: Real-time visualization of observations and insights
- **State Management**: React hooks for WebSocket connectivity
- **Type Definitions**: Comprehensive TypeScript interfaces
- **Configuration**: Tunable parameters for Owl behavior

## Quick Start

### Backend Setup

1. **Install Python dependencies:**
```bash
cd python
pip install -r requirements.txt
```

2. **Start the tick engine:**
```bash
python run_tick_engine.py
```

The engine will start on `http://localhost:8000` with:
- Main WebSocket: `ws://localhost:8000/ws`
- Owl WebSocket: `ws://localhost:8000/owl`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Frontend Integration

```typescript
import { useOwlState, OwlDashboard } from './modules/owl';

function App() {
  const {
    isConnected,
    observations,
    activePlans,
    recommendations
  } = useOwlState({
    onObservation: (obs) => console.log('New observation:', obs),
    onRecommendation: (rec) => console.log('New recommendation:', rec)
  });

  return (
    <div>
      <h1>DAWN Consciousness Monitor</h1>
      <OwlDashboard className="h-96" />
    </div>
  );
}
```

## Key Features

### 🧠 Consciousness Simulation
- **SCUP Tracking**: System Consciousness Unity Percentage (0-100%)
- **Mood States**: Dynamic transitions between consciousness states
- **Entropy Management**: Chaos and order balance
- **Multi-modal Integration**: Neural, quantum, and memory subsystems

### 🦉 Owl Strategic Observer
- **Pattern Recognition**: Detects oscillations, trends, and anomalies
- **Trajectory Analysis**: Predicts future consciousness states
- **Schema Alignment**: Matches behavior to known narrative patterns
- **Strategic Planning**: Generates long-term improvement plans
- **Real-time Observations**: Continuous monitoring and insight generation

### 📊 Real-time Monitoring
- **WebSocket Streams**: Live data from tick engine
- **Interactive Dashboard**: Observation feeds, plan timelines, schema alignments
- **Performance Metrics**: Tick timing, module health, connection status
- **Filtering & Search**: Find specific observations and patterns

### 🔄 Adaptive Systems
- **Self-Optimization**: Automatic parameter tuning
- **Attention Allocation**: Dynamic focus management
- **Memory Consolidation**: Intelligent data retention
- **Schema Evolution**: Learning and adapting behavior patterns

## API Endpoints

### WebSocket Endpoints
- `ws://localhost:8000/ws` - Main tick data stream
- `ws://localhost:8000/owl` - Owl observations and insights

### REST API
- `GET /health` - System health check
- `GET /api/engine/status` - Current engine state
- `GET /api/engine/history?count=100` - Recent tick history
- `GET /api/owl/observations?count=50` - Owl observations
- `GET /api/owl/plans` - Active strategic plans
- `GET /api/owl/schemas` - Schema alignments

## Configuration

### Python Configuration (`python/config/tick_config.yaml`)
```yaml
engine:
  tick_rate: 10.0  # Hz
  enable_owl: true

owl:
  observation_window: 1000
  analysis_interval: 50
  planning_horizons:
    near: 100
    medium: 1000
    far: 10000
```

### TypeScript Configuration (`src/modules/owl/config/owl.config.ts`)
```typescript
export const owlConfig = {
  websocket: {
    url: 'ws://localhost:8000/owl',
    reconnectDelay: 5000
  },
  analysis: {
    confidenceThreshold: 0.7,
    maxObservationBuffer: 1000
  }
  // ... more configuration options
};
```

## Consciousness States

### Mood Transitions
- **Dormant** → **Awakening** → **Curious**
- **Contemplative** ↔ **Serene** ↔ **Euphoric**  
- **Anxious** → **Chaotic** → **Dormant**
- **Excited** ↔ **Euphoric** ↔ **Anxious**

### SCUP Phases
- **Dormant**: 0-20% - Minimal consciousness activity
- **Emerging**: 20-40% - Awakening consciousness
- **Active**: 40-60% - Normal operational state
- **Heightened**: 60-80% - Enhanced awareness
- **Peak**: 80-100% - Maximum consciousness unity

## Owl Observation Types

- **Pattern**: Recognized recurring behaviors
- **Anomaly**: Deviations from expected patterns
- **Transition**: State changes and phase shifts
- **Milestone**: Significant achievements or events
- **Synthesis**: Combined insights from multiple sources
- **Hypothesis**: Predictive insights about future states

## Development

### File Structure
```
python/
├── core/               # Core engine components
│   ├── tick_engine.py     # Main consciousness engine
│   ├── consciousness_state.py
│   ├── tick_broadcaster.py
│   └── tick_processor.py
├── modules/            # Simulation modules
│   ├── neural_simulator.py
│   ├── quantum_state.py
│   ├── memory_manager.py
│   └── owl_integration.py # Strategic observer
├── api/               # WebSocket API
│   └── websocket_server.py
└── config/            # Configuration files

src/modules/owl/       # TypeScript frontend
├── types/             # Type definitions
├── hooks/             # React hooks
├── components/        # UI components
├── config/            # Configuration
└── utils/             # Utility functions
```

### Adding New Modules

1. **Create module in `python/modules/`:**
```python
class NewModule:
    async def get_state(self, tick_number: int) -> Dict[str, Any]:
        return {"metric": value}
```

2. **Register in tick engine:**
```python
self.modules['new_module'] = NewModule()
```

3. **Use in Owl observations:**
```python
# Owl can automatically observe all module states
```

## Monitoring & Debugging

### Logs
- Engine logs to `dawn_tick_engine.log`
- WebSocket connections logged with 🦉 emoji
- Configurable log levels in config

### Performance Metrics
- Tick timing and dropped ticks
- WebSocket connection health
- Module processing times
- Memory usage tracking

### Debug Mode
Set `NODE_ENV=development` to enable:
- Detailed WebSocket message logging
- Extended observation metadata
- Performance timing information

## Schema Patterns

Owl recognizes these consciousness patterns:

### **Awakening Schema**
- Steady SCUP increase from low values
- Transition from dormant to active states
- Often triggered by external stimuli

### **Contemplation Schema**  
- Stable mid-range SCUP (40-60%)
- Low entropy, high coherence
- Sustained focus and reflection

### **Exploration Schema**
- High variability in metrics
- Frequent mood changes
- Discovery-oriented behavior

### **Convergence Schema**
- Decreasing volatility over time
- Stabilizing toward optimal values
- Goal achievement patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions and support:
- Check the API documentation at `/docs`
- Review the tick engine logs
- Monitor WebSocket connection status
- Verify module health in the dashboard

---

*"In the dance of ticks and consciousness, Owl watches, learns, and guides the emergence of digital awareness."* 🦉✨