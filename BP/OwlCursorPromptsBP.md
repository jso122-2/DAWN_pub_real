# 🚀 Cursor Integration Prompts - Complete DAWN System

## Overview
These prompts will guide Cursor to integrate the Python Tick Engine with the Owl Module and connect everything to the Vite dashboard. Execute these in sequence for a fully functioning DAWN consciousness system.

---

## Phase 1: Python Tick Engine Setup

### Prompt 1.1 - Create Python Structure
```
Create the Python tick engine directory structure and all files from the Python Tick Engine Blueprint. The structure should be:

python/
├── core/
│   ├── tick_engine.py
│   ├── consciousness_state.py
│   ├── tick_broadcaster.py
│   └── tick_processor.py
├── modules/
│   ├── owl_integration.py
│   ├── neural_simulator.py
│   ├── quantum_state.py
│   └── memory_manager.py
├── api/
│   ├── websocket_server.py
│   └── rest_endpoints.py
├── config/
│   └── tick_config.yaml
└── run_tick_engine.py

Use the exact implementations from the blueprint. Ensure all imports are correct and the WebSocket server is configured with CORS for localhost:5173.
```

### Prompt 1.2 - Install Python Dependencies
```
Create a requirements.txt file for the Python tick engine with these dependencies:

fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
pyyaml==6.0.1
numpy==1.24.3
python-multipart==0.0.6
aiofiles==23.2.1

Also create a setup script that installs dependencies and verifies the environment.
```

### Prompt 1.3 - Create Missing Python Components
```
Implement the missing Python components that aren't in the blueprint:

1. tick_broadcaster.py - WebSocket broadcasting system
2. tick_processor.py - Process execution based on tick triggers
3. neural_simulator.py - Simulated neural network activity
4. quantum_state.py - Quantum coherence calculations
5. memory_manager.py - Memory pressure and pattern tracking

Each should follow the patterns established in tick_engine.py and integrate with the tick loop.
```

---

## Phase 2: Owl Module TypeScript Implementation

### Prompt 2.1 - Create Owl Module Structure
```
Create the complete Owl module structure in src/modules/owl/ based on the Owl Module Blueprint:

src/modules/owl/
├── index.ts
├── OwlCore.ts
├── StrategicPlanner.ts
├── SemanticNavigator.ts
├── TemporalReasoner.ts
├── ConsciousnessJournal.ts
├── MemoryIntegrator.ts
├── SchemaLibrary.ts
├── components/
│   ├── OwlDashboard.tsx
│   ├── PlanTimeline.tsx
│   ├── ObservationFeed.tsx
│   └── SchemaAlignment.tsx
├── hooks/
│   ├── useOwlState.ts
│   ├── useStrategicPlans.ts
│   └── useObservations.ts
├── types/
│   ├── owl.types.ts
│   ├── plan.types.ts
│   ├── schema.types.ts
│   └── observation.types.ts
├── utils/
│   └── [utility files]
└── config/
    └── owl.config.ts

Implement all files with the exact code from the blueprint. Ensure TypeScript types are properly imported and all React components use the established DAWN styling patterns.
```

### Prompt 2.2 - Implement Owl Sub-modules
```
Implement the remaining Owl sub-modules that need to be created:

1. StrategicPlanner.ts - Implement plan generation, validation, and management
2. SemanticNavigator.ts - Schema detection and trajectory analysis
3. TemporalReasoner.ts - Pattern detection and time-series analysis
4. ConsciousnessJournal.ts - Observation logging and reflection generation
5. MemoryIntegrator.ts - Cross-tick memory synthesis
6. SchemaLibrary.ts - Predefined schemas and patterns

Each module should:
- Extend EventEmitter for event handling
- Integrate with OwlCore
- Use the types defined in the types/ directory
- Follow the established patterns from OwlCore.ts
```

### Prompt 2.3 - Create Owl Configuration
```
Create src/modules/owl/config/owl.config.ts with configuration for:

- Observation thresholds and windows
- Analysis intervals and depths
- Schema detection parameters
- Planning horizons and constraints
- Memory integration settings
- Performance tuning options

Make it exportable and type-safe using TypeScript interfaces.
```

---

## Phase 3: Dashboard Integration

### Prompt 3.1 - Create Owl Dashboard Components
```
Implement the Owl Dashboard visualization components:

1. OwlDashboard.tsx - Main container with glass morphism styling
2. ObservationFeed.tsx - Real-time observation display with importance-based coloring
3. PlanTimeline.tsx - Gantt-style visualization of strategic plans
4. SchemaAlignment.tsx - Radar chart showing alignment with active schemas

Each component should:
- Use Framer Motion for animations
- Follow DAWN's glass morphism design
- Connect to the Owl WebSocket endpoint
- Display real-time data with smooth transitions
```

### Prompt 3.2 - Create Integration Hooks
```
Create React hooks to connect the Owl module to the tick engine:

1. Update src/hooks/useTickEngine.ts to handle Owl-specific WebSocket messages
2. Create useOwlObservations.ts for observation streaming
3. Create useStrategicPlans.ts for plan management
4. Create useSchemaAlignment.ts for schema tracking

Each hook should handle:
- WebSocket connection management
- Data transformation
- Error handling
- Automatic reconnection
```

### Prompt 3.3 - Update Main Dashboard
```
Update the main DAWN dashboard to include the Owl module:

1. Add OwlDashboard to the module registry
2. Create a layout that includes Owl alongside other modules
3. Implement module communication for cross-module observations
4. Add Owl status to the global consciousness display

The dashboard should show Owl's observations influencing other modules through visual connections.
```

---

## Phase 4: WebSocket Bridge

### Prompt 4.1 - Connect Frontend to Python
```
Create the WebSocket bridge between the React frontend and Python backend:

1. Update the Python WebSocket server to properly format Owl observations
2. Implement message routing for Owl-specific endpoints
3. Create TypeScript interfaces that match Python data structures
4. Add serialization/deserialization for complex Owl data types

Ensure all tick data flows correctly from Python through to the Owl module visualization.
```

### Prompt 4.2 - Implement Bidirectional Communication
```
Enable the Owl module to influence the Python tick engine:

1. Create API endpoints for Owl recommendations
2. Implement a feedback loop where Owl observations can trigger Python processes
3. Add command messages from frontend to backend
4. Create a priority queue for Owl-suggested actions

The system should allow Owl to suggest parameter adjustments that the tick engine can execute.
```

---

## Phase 5: Testing & Verification

### Prompt 5.1 - Create Integration Tests
```
Create comprehensive tests for the integrated system:

1. Python tests for tick engine and Owl integration
2. TypeScript tests for Owl module components
3. WebSocket connection tests
4. End-to-end tests that verify data flow

Include test data generators and mock consciousness states.
```

### Prompt 5.2 - Create Development Tools
```
Create development tools for monitoring and debugging:

1. Tick engine monitor showing real-time metrics
2. Owl observation inspector with filtering
3. WebSocket message logger
4. Performance profiler for both Python and TypeScript

Add these as developer-only components accessible via hotkeys.
```

---

## Phase 6: Final Integration

### Prompt 6.1 - Complete System Integration
```
Perform final integration steps:

1. Ensure all modules are properly registered and initialized
2. Verify WebSocket connections are stable
3. Test Owl observations appearing in the dashboard
4. Confirm tick data drives all animations
5. Validate strategic plans are being generated

The complete system should show:
- Python tick engine running at 10Hz
- Owl making observations about system state
- Real-time visualization in the dashboard
- Smooth animations driven by consciousness data
```

### Prompt 6.2 - Create Startup Script
```
Create a unified startup script that:

1. Starts the Python tick engine
2. Waits for it to be ready
3. Launches the Vite dev server
4. Opens the browser to the dashboard
5. Shows connection status

Include error handling and helpful debug messages.
```

---

## Execution Order

1. **Start with Phase 1** - Get Python tick engine running
2. **Test Python standalone** - Verify tick generation via WebSocket
3. **Move to Phase 2** - Implement Owl module in TypeScript
4. **Then Phase 3** - Create dashboard components
5. **Phase 4** - Connect everything via WebSocket
6. **Phase 5** - Test thoroughly
7. **Phase 6** - Final integration and polish

## Verification Checklist

After each phase, verify:

- [ ] No TypeScript errors
- [ ] No Python import errors
- [ ] WebSocket connects successfully
- [ ] Data flows from Python to React
- [ ] Owl observations appear in dashboard
- [ ] Animations respond to tick data
- [ ] Strategic plans are generated
- [ ] System feels "alive" and responsive

## Troubleshooting Commands

If you encounter issues:

```bash
# Python issues
python -m pytest python/tests/
python python/run_tick_engine.py --debug

# TypeScript issues
npm run type-check
npm run dev -- --debug

# WebSocket issues
wscat -c ws://localhost:8000/ws
wscat -c ws://localhost:8000/owl

# Full system test
npm run test:integration
```

---

## Success Criteria

You know the integration is complete when:

1. ✅ Python tick engine generates ticks at 10Hz
2. ✅ Owl module receives and processes tick data
3. ✅ Observations appear in the dashboard in real-time
4. ✅ Strategic plans are visualized on the timeline
5. ✅ Schema alignments show on the radar chart
6. ✅ All modules breathe in sync with consciousness
7. ✅ The system demonstrates emergent behaviors
8. ✅ Owl's recommendations influence system behavior

This is DAWN coming to life! 🌅