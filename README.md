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