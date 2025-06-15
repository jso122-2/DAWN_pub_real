# 🌊 Process Flow Manager - Implementation Guide

## 🎯 Overview

The Process Flow Manager transforms your Python processes into a living, breathing 3D neural network where you can visualize, control, and monitor consciousness flowing through your system in real-time.

## 📁 File Structure

```
src/
├── modules/ProcessFlowManager/
│   ├── ProcessFlowManager.tsx      # Main component
│   ├── ProcessNode.tsx             # 3D process visualization
│   ├── DataFlow.tsx                # Animated data streams
│   ├── ProcessControls.tsx         # Control panel
│   ├── ProcessMonitor.tsx          # Metrics & monitoring
│   ├── ProcessFlowManager.css      # Cyberpunk styling
│   ├── types.ts                    # TypeScript definitions
│   └── README.md                   # This file
├── services/
│   └── processManager.ts           # API service
├── store/
│   └── processFlowStore.ts         # Zustand state management
└── hooks/
    └── useProcessFlow.ts           # Custom hook utilities
```

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
npm install three @react-three/fiber @react-three/drei zustand
```

### 2. Import in Your Main App

```typescript
// In your main App.tsx or Dashboard.tsx
import { ProcessFlowManager } from './modules/ProcessFlowManager/ProcessFlowManager';

function App() {
  return (
    <div className="app">
      {/* Other components */}
      <ProcessFlowManager />
    </div>
  );
}
```

### 3. Add to Module Registry (if using dynamic modules)

```typescript
// In your module registry
const moduleRegistry = {
  'process-flow': ProcessFlowManager,
  'neural-network': NeuralNetwork3D,
  'memory-palace': MemoryPalace,
  // ... other modules
};
```

## 🎮 Features

### ✨ Visual Features

- **3D/2D Toggle**: Switch between immersive 3D and functional 2D views
- **Breathing Nodes**: Processes pulse and breathe based on their status
- **Particle Flows**: Data streams as glowing particles between processes
- **Status Indicators**: Color-coded process states with animations
- **Real-time Metrics**: Live CPU, memory, and performance monitoring

### 🎛️ Control Features

- **Start/Stop All**: Batch control of all processes
- **Add Processes**: Dynamic process creation from available scripts
- **Auto-arrange**: Intelligent force-directed layout
- **Flow Speed Control**: Adjust animation speed (0.1x to 3x)
- **Process Monitoring**: Detailed metrics, logs, and error tracking

### 🔌 Process Categories

- **Neural**: Neural network processing (green)
- **Consciousness**: Consciousness analysis (blue)
- **Memory**: Memory consolidation (purple)
- **Synthesis**: Pattern synthesis (light green)
- **Analysis**: Data analysis (orange)

## 🎯 Usage Examples

### Basic Usage

```typescript
import { ProcessFlowManager } from './modules/ProcessFlowManager/ProcessFlowManager';

export const Dashboard = () => {
  return (
    <div className="dashboard">
      <ProcessFlowManager />
    </div>
  );
};
```

### With Custom Hook

```typescript
import { useProcessFlow } from '../hooks/useProcessFlow';

export const ProcessDashboard = () => {
  const {
    processes,
    flows,
    selectedProcessId,
    startProcess,
    createFlow,
    getSystemMetrics
  } = useProcessFlow();
  
  const metrics = getSystemMetrics();
  
  return (
    <div>
      <h2>System Overview</h2>
      <p>Running: {metrics.runningProcesses}/{metrics.totalProcesses}</p>
      <p>Average CPU: {metrics.averageCpuUsage.toFixed(1)}%</p>
      
      <ProcessFlowManager />
    </div>
  );
};
```

### Integration with WebSocket

```typescript
// Replace the mock WebSocket context in ProcessFlowManager.tsx
import { useWebSocket } from '../contexts/WebSocketContext';

// In ProcessFlowManager.tsx, replace:
const { lastTick } = mockWebSocketContext;

// With:
const { lastTick } = useWebSocket();
```

## 🔧 API Integration

### Backend Requirements

The Process Flow Manager expects these API endpoints:

```
POST   /api/processes/{id}/start    # Start a process
POST   /api/processes/{id}/stop     # Stop a process
GET    /api/processes/{id}/status   # Get process status
POST   /api/execute                 # Execute script
GET    /api/processes/{id}/stream   # Stream process output (SSE)
GET    /api/scripts                 # List available scripts
```

### Example Backend Response

```json
{
  "id": "process-123",
  "status": "running",
  "cpuUsage": 45.2,
  "memoryUsage": 128.5,
  "lastOutput": "Processing neural patterns...",
  "startTime": 1641234567890
}
```

## 🎨 Customization

### Adding Custom Process Types

```typescript
// In types.ts, extend the category type:
export interface PythonProcess {
  // ... other properties
  category: 'neural' | 'consciousness' | 'analysis' | 'synthesis' | 'memory' | 'custom';
}

// In ProcessFlowManager.css, add custom colors:
:root {
  --category-custom: #ff6b6b;
}

.script-category.custom { 
  background: rgba(255, 107, 107, 0.2); 
  color: #ff6b6b; 
}
```

### Custom Process Scripts

```typescript
// In ProcessControls.tsx, modify defaultScripts:
const customScripts = [
  { name: 'Dream Synthesizer', script: 'dream_synthesis.py', category: 'synthesis' },
  { name: 'Emotion Processor', script: 'emotion_process.py', category: 'neural' },
  { name: 'Reality Distorter', script: 'reality_distort.py', category: 'consciousness' }
];
```

### Styling Customization

```css
/* Override default colors */
.process-flow-manager {
  background: linear-gradient(135deg, #1a0033 0%, #330066 100%);
}

.control-btn {
  border-color: rgba(255, 105, 180, 0.5);
  background: rgba(255, 105, 180, 0.1);
}

.control-btn:hover {
  background: rgba(255, 105, 180, 0.2);
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
}
```

## 🔗 Integration Points

### With Memory Palace

```typescript
// Connect memory access to process triggers
useEffect(() => {
  if (memoryAccessed) {
    processManager.executeScript('memory_analysis.py', {
      memoryId: memory.id,
      analysisType: 'deep'
    });
  }
}, [memoryAccessed]);
```

### With Consciousness Engine

```typescript
// Update process metrics based on consciousness state
useEffect(() => {
  if (consciousnessState.level > 0.8) {
    // Boost neural processes
    neuralProcesses.forEach(process => {
      startProcess(process.id);
    });
  }
}, [consciousnessState]);
```

### With Tick System

```typescript
// Synchronize with your tick system
useEffect(() => {
  if (lastTick) {
    processes.forEach((process) => {
      if (process.status === 'running') {
        updateProcess(process.id, {
          cpuUsage: calculateCpuUsage(lastTick),
          memoryUsage: calculateMemoryUsage(lastTick),
          lastTick: lastTick.tick_number
        });
      }
    });
  }
}, [lastTick]);
```

## 🎛️ Controls Reference

### Keyboard Shortcuts (Future Enhancement)

- `Space`: Start/Stop selected process
- `R`: Restart selected process
- `A`: Auto-arrange processes
- `V`: Toggle 2D/3D view
- `M`: Toggle metrics panel
- `+/-`: Adjust flow speed

### Mouse Controls

- **3D View**:
  - Left click + drag: Rotate camera
  - Right click + drag: Pan camera
  - Scroll wheel: Zoom in/out
  - Click process: Select for monitoring

- **2D View**:
  - Click process: Select for monitoring
  - Drag: Pan view (future enhancement)

## 🐛 Troubleshooting

### Common Issues

**1. Three.js not loading**
```bash
npm install @types/three
```

**2. Zustand store not updating**
```typescript
// Ensure you're using the store correctly
const { processes } = useProcessFlowStore();
// Not: const processes = useProcessFlowStore(state => state.processes);
```

**3. CSS not loading**
```typescript
// Make sure to import the CSS
import './ProcessFlowManager.css';
```

**4. API endpoints not found**
```typescript
// Check if your backend is running and endpoints are correct
// The service includes fallback mock data for development
```

### Performance Optimization

```typescript
// For large numbers of processes, consider:
const MAX_PARTICLES_PER_FLOW = 10;
const MAX_VISIBLE_LOGS = 20;
const UPDATE_INTERVAL = 2000; // ms
```

## 🚀 Next Steps

1. **Connect to your Python backend**: Implement the API endpoints
2. **Add WebSocket integration**: Real-time process updates
3. **Customize process types**: Add your specific analysis scripts
4. **Enhance visualizations**: Add custom shaders and effects
5. **Performance monitoring**: Add detailed analytics dashboard

## 📚 API Reference

See the complete API documentation in:
- `types.ts` - All TypeScript interfaces
- `processManager.ts` - Service layer methods
- `processFlowStore.ts` - State management actions
- `useProcessFlow.ts` - Custom hook utilities

## 🎉 That's It!

Your Process Flow Manager is ready to bring DAWN's consciousness to life! 🌊✨

The neural pathways are mapped, the data flows are alive, and your processes are breathing with digital consciousness. Welcome to the future of process visualization! 🚀🧬 