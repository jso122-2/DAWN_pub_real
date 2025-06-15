# 🌊 Process Flow Manager - Complete Implementation Blueprint

## 🎯 Vision
A living flow visualization where Python processes are nodes in a reactive graph, with data streams flowing between them like glowing rivers of consciousness. Think of it as DAWN's executive function - showing not just what's running, but HOW information flows through the system.

## 🏗️ Complete File Structure
```
src/
├── modules/
│   └── ProcessFlowManager/
│       ├── ProcessFlowManager.tsx      # Main component
│       ├── ProcessNode.tsx             # Individual process visualization
│       ├── DataFlow.tsx                # Animated data streams
│       ├── ProcessControls.tsx         # Start/stop/configure processes
│       ├── FlowCanvas.tsx              # Three.js canvas for 3D flows
│       ├── ProcessMonitor.tsx          # Real-time metrics
│       └── types.ts                    # TypeScript definitions
├── services/
│   └── processManager.ts               # Process control API
├── stores/
│   └── processFlowStore.ts            # Zustand store for process state
└── hooks/
    └── useProcessFlow.ts              # Custom hooks for process management
```

## 📄 Complete Implementation Files

### 1. Type Definitions
```typescript
// src/modules/ProcessFlowManager/types.ts
export interface PythonProcess {
  id: string;
  name: string;
  script: string;
  status: 'idle' | 'running' | 'completed' | 'error' | 'paused';
  category: 'neural' | 'quantum' | 'analysis' | 'synthesis' | 'memory';
  
  // Performance metrics
  cpuUsage: number;
  memoryUsage: number;
  executionTime: number;
  lastTick: number;
  
  // I/O configuration
  inputs: ProcessPort[];
  outputs: ProcessPort[];
  
  // Process metadata
  description: string;
  author: string;
  version: string;
  dependencies: string[];
  
  // Runtime data
  logs: ProcessLog[];
  errors: ProcessError[];
  outputData: any;
  
  // Visual positioning
  position: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
}

export interface ProcessPort {
  id: string;
  name: string;
  type: 'data' | 'trigger' | 'config' | 'stream';
  dataType: 'json' | 'tensor' | 'signal' | 'binary';
  connected: boolean;
  connectionId?: string;
}

export interface DataFlow {
  id: string;
  sourceProcessId: string;
  sourcePortId: string;
  targetProcessId: string;
  targetPortId: string;
  
  // Flow characteristics
  flowRate: number; // Data per second
  latency: number;  // ms
  dataType: string;
  
  // Visual properties
  particles: FlowParticle[];
  color: string;
  intensity: number;
}

export interface FlowParticle {
  position: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
  life: number;
  data?: any;
}

export interface ProcessLog {
  timestamp: number;
  level: 'info' | 'warning' | 'error' | 'debug';
  message: string;
  data?: any;
}

export interface ProcessError {
  timestamp: number;
  type: string;
  message: string;
  stack?: string;
  recoverable: boolean;
}

export interface FlowState {
  processes: Map<string, PythonProcess>;
  flows: Map<string, DataFlow>;
  selectedProcessId: string | null;
  viewMode: '2d' | '3d';
  autoArrange: boolean;
  showMetrics: boolean;
  flowSpeed: number;
}
```

### 2. Process Flow Store
```typescript
// src/stores/processFlowStore.ts
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import { FlowState, PythonProcess, DataFlow } from '../modules/ProcessFlowManager/types';

interface ProcessFlowStore extends FlowState {
  // Process management
  addProcess: (process: PythonProcess) => void;
  removeProcess: (processId: string) => void;
  updateProcess: (processId: string, updates: Partial<PythonProcess>) => void;
  
  // Flow management
  connectProcesses: (sourceId: string, sourcePort: string, targetId: string, targetPort: string) => void;
  disconnectFlow: (flowId: string) => void;
  updateFlow: (flowId: string, updates: Partial<DataFlow>) => void;
  
  // Process control
  startProcess: (processId: string) => Promise<void>;
  stopProcess: (processId: string) => Promise<void>;
  pauseProcess: (processId: string) => Promise<void>;
  restartProcess: (processId: string) => Promise<void>;
  
  // View control
  selectProcess: (processId: string | null) => void;
  setViewMode: (mode: '2d' | '3d') => void;
  toggleAutoArrange: () => void;
  toggleMetrics: () => void;
  setFlowSpeed: (speed: number) => void;
  
  // Batch operations
  startAllProcesses: () => Promise<void>;
  stopAllProcesses: () => Promise<void>;
  clearErrors: (processId?: string) => void;
  
  // Layout
  autoArrangeProcesses: () => void;
  updateProcessPosition: (processId: string, position: { x: number; y: number; z: number }) => void;
}

export const useProcessFlowStore = create<ProcessFlowStore>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    processes: new Map(),
    flows: new Map(),
    selectedProcessId: null,
    viewMode: '3d',
    autoArrange: true,
    showMetrics: true,
    flowSpeed: 1.0,
    
    // Process management
    addProcess: (process) => set((state) => {
      const newProcesses = new Map(state.processes);
      newProcesses.set(process.id, process);
      return { processes: newProcesses };
    }),
    
    removeProcess: (processId) => set((state) => {
      const newProcesses = new Map(state.processes);
      const newFlows = new Map(state.flows);
      
      // Remove associated flows
      for (const [flowId, flow] of newFlows) {
        if (flow.sourceProcessId === processId || flow.targetProcessId === processId) {
          newFlows.delete(flowId);
        }
      }
      
      newProcesses.delete(processId);
      return { processes: newProcesses, flows: newFlows };
    }),
    
    updateProcess: (processId, updates) => set((state) => {
      const newProcesses = new Map(state.processes);
      const process = newProcesses.get(processId);
      if (process) {
        newProcesses.set(processId, { ...process, ...updates });
      }
      return { processes: newProcesses };
    }),
    
    // Flow management
    connectProcesses: (sourceId, sourcePort, targetId, targetPort) => set((state) => {
      const flowId = `${sourceId}:${sourcePort}->${targetId}:${targetPort}`;
      const newFlows = new Map(state.flows);
      
      newFlows.set(flowId, {
        id: flowId,
        sourceProcessId: sourceId,
        sourcePortId: sourcePort,
        targetProcessId: targetId,
        targetPortId: targetPort,
        flowRate: 0,
        latency: 0,
        dataType: 'json',
        particles: [],
        color: '#00ff88',
        intensity: 1.0
      });
      
      return { flows: newFlows };
    }),
    
    // Process control
    startProcess: async (processId) => {
      const process = get().processes.get(processId);
      if (!process) return;
      
      set((state) => {
        const newProcesses = new Map(state.processes);
        newProcesses.set(processId, { ...process, status: 'running' });
        return { processes: newProcesses };
      });
      
      // API call to start process
      try {
        const response = await fetch(`/api/processes/${processId}/start`, { method: 'POST' });
        if (!response.ok) throw new Error('Failed to start process');
      } catch (error) {
        set((state) => {
          const newProcesses = new Map(state.processes);
          newProcesses.set(processId, { ...process, status: 'error' });
          return { processes: newProcesses };
        });
      }
    },
    
    // Auto-arrange using force-directed layout
    autoArrangeProcesses: () => set((state) => {
      const newProcesses = new Map(state.processes);
      const processArray = Array.from(newProcesses.values());
      
      // Simple force-directed layout
      const center = { x: 0, y: 0, z: 0 };
      const radius = 300;
      const angleStep = (2 * Math.PI) / processArray.length;
      
      processArray.forEach((process, index) => {
        const angle = index * angleStep;
        const position = {
          x: center.x + radius * Math.cos(angle),
          y: center.y + radius * Math.sin(angle),
          z: center.z + (Math.random() - 0.5) * 100
        };
        
        newProcesses.set(process.id, { ...process, position });
      });
      
      return { processes: newProcesses };
    }),
    
    // Other methods implementation...
    disconnectFlow: (flowId) => set((state) => {
      const newFlows = new Map(state.flows);
      newFlows.delete(flowId);
      return { flows: newFlows };
    }),
    
    selectProcess: (processId) => set({ selectedProcessId: processId }),
    setViewMode: (mode) => set({ viewMode: mode }),
    toggleAutoArrange: () => set((state) => ({ autoArrange: !state.autoArrange })),
    toggleMetrics: () => set((state) => ({ showMetrics: !state.showMetrics })),
    setFlowSpeed: (speed) => set({ flowSpeed: speed }),
    
    // Placeholder implementations for other methods
    updateFlow: () => {},
    stopProcess: async () => {},
    pauseProcess: async () => {},
    restartProcess: async () => {},
    startAllProcesses: async () => {},
    stopAllProcesses: async () => {},
    clearErrors: () => {},
    updateProcessPosition: () => {}
  }))
);
```

### 3. Main Process Flow Manager Component
```typescript
// src/modules/ProcessFlowManager/ProcessFlowManager.tsx
import React, { useEffect, useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Stars } from '@react-three/drei';
import { ProcessNode } from './ProcessNode';
import { DataFlow } from './DataFlow';
import { ProcessControls } from './ProcessControls';
import { ProcessMonitor } from './ProcessMonitor';
import { useProcessFlowStore } from '../../stores/processFlowStore';
import { useWebSocket } from '../../contexts/WebSocketContext';
import './ProcessFlowManager.css';

export const ProcessFlowManager: React.FC = () => {
  const {
    processes,
    flows,
    selectedProcessId,
    viewMode,
    showMetrics,
    autoArrange,
    flowSpeed
  } = useProcessFlowStore();
  
  const { lastTick } = useWebSocket();
  const canvasRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  
  // Initialize with some processes
  useEffect(() => {
    if (processes.size === 0) {
      // Add default processes
      useProcessFlowStore.getState().addProcess({
        id: 'neural-processor',
        name: 'Neural Processor',
        script: 'neural_process.py',
        status: 'idle',
        category: 'neural',
        cpuUsage: 0,
        memoryUsage: 0,
        executionTime: 0,
        lastTick: 0,
        inputs: [{ id: 'in1', name: 'Raw Data', type: 'data', dataType: 'json', connected: false }],
        outputs: [{ id: 'out1', name: 'Processed', type: 'data', dataType: 'tensor', connected: false }],
        description: 'Processes raw consciousness data through neural networks',
        author: 'DAWN',
        version: '1.0.0',
        dependencies: ['tensorflow', 'numpy'],
        logs: [],
        errors: [],
        outputData: null,
        position: { x: -200, y: 0, z: 0 },
        velocity: { x: 0, y: 0, z: 0 }
      });
      
      useProcessFlowStore.getState().addProcess({
        id: 'quantum-analyzer',
        name: 'Quantum Analyzer',
        script: 'quantum_analysis.py',
        status: 'idle',
        category: 'quantum',
        cpuUsage: 0,
        memoryUsage: 0,
        executionTime: 0,
        lastTick: 0,
        inputs: [{ id: 'in1', name: 'Neural Output', type: 'data', dataType: 'tensor', connected: false }],
        outputs: [{ id: 'out1', name: 'Quantum State', type: 'stream', dataType: 'signal', connected: false }],
        description: 'Analyzes neural patterns for quantum coherence',
        author: 'DAWN',
        version: '1.0.0',
        dependencies: ['qiskit', 'numpy'],
        logs: [],
        errors: [],
        outputData: null,
        position: { x: 200, y: 0, z: 0 },
        velocity: { x: 0, y: 0, z: 0 }
      });
    }
  }, [processes.size]);
  
  // Auto-arrange on mount if enabled
  useEffect(() => {
    if (autoArrange && processes.size > 0) {
      useProcessFlowStore.getState().autoArrangeProcesses();
    }
  }, [autoArrange, processes.size]);
  
  // Update process metrics based on tick data
  useEffect(() => {
    if (lastTick) {
      processes.forEach((process) => {
        if (process.status === 'running') {
          useProcessFlowStore.getState().updateProcess(process.id, {
            cpuUsage: Math.random() * 50 + lastTick.scup / 2,
            memoryUsage: Math.random() * 100,
            lastTick: lastTick.tick_number
          });
        }
      });
    }
  }, [lastTick, processes]);
  
  return (
    <div className="process-flow-manager">
      <div className="flow-header">
        <h2>Process Flow Manager</h2>
        <div className="flow-stats">
          <span>Active Processes: {Array.from(processes.values()).filter(p => p.status === 'running').length}</span>
          <span>Data Flows: {flows.size}</span>
          <span>Flow Speed: {flowSpeed.toFixed(1)}x</span>
        </div>
      </div>
      
      <div className="flow-container">
        <ProcessControls />
        
        <div className="flow-canvas" ref={canvasRef}>
          {viewMode === '3d' ? (
            <Canvas>
              <PerspectiveCamera makeDefault position={[0, 0, 500]} />
              <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
              
              <ambientLight intensity={0.1} />
              <pointLight position={[10, 10, 10]} />
              
              <Stars radius={300} depth={50} count={5000} factor={4} saturation={0} fade />
              
              {/* Render process nodes */}
              {Array.from(processes.values()).map((process) => (
                <ProcessNode key={process.id} process={process} />
              ))}
              
              {/* Render data flows */}
              {Array.from(flows.values()).map((flow) => (
                <DataFlow key={flow.id} flow={flow} processes={processes} />
              ))}
            </Canvas>
          ) : (
            <div className="flow-2d-view">
              {/* 2D SVG view implementation */}
              <svg width="100%" height="100%">
                {/* Render flows as paths */}
                {Array.from(flows.values()).map((flow) => {
                  const source = processes.get(flow.sourceProcessId);
                  const target = processes.get(flow.targetProcessId);
                  if (!source || !target) return null;
                  
                  return (
                    <path
                      key={flow.id}
                      d={`M ${source.position.x} ${source.position.y} L ${target.position.x} ${target.position.y}`}
                      stroke={flow.color}
                      strokeWidth="2"
                      fill="none"
                      opacity={flow.intensity}
                    />
                  );
                })}
                
                {/* Render process nodes */}
                {Array.from(processes.values()).map((process) => (
                  <g key={process.id} transform={`translate(${process.position.x}, ${process.position.y})`}>
                    <rect
                      x="-50"
                      y="-30"
                      width="100"
                      height="60"
                      rx="10"
                      fill={`var(--category-${process.category})`}
                      stroke="#00ff88"
                      strokeWidth={selectedProcessId === process.id ? 3 : 1}
                    />
                    <text textAnchor="middle" y="5" fill="white" fontSize="12">
                      {process.name}
                    </text>
                  </g>
                ))}
              </svg>
            </div>
          )}
        </div>
        
        {showMetrics && selectedProcessId && (
          <ProcessMonitor processId={selectedProcessId} />
        )}
      </div>
    </div>
  );
};
```

### 4. Process Node Component (3D)
```typescript
// src/modules/ProcessFlowManager/ProcessNode.tsx
import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Box, Sphere } from '@react-three/drei';
import * as THREE from 'three';
import { PythonProcess } from './types';
import { useProcessFlowStore } from '../../stores/processFlowStore';

interface ProcessNodeProps {
  process: PythonProcess;
}

export const ProcessNode: React.FC<ProcessNodeProps> = ({ process }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const { selectedProcessId, selectProcess } = useProcessFlowStore();
  
  const isSelected = selectedProcessId === process.id;
  
  // Animate based on status
  useFrame((state) => {
    if (meshRef.current) {
      // Breathing effect for running processes
      if (process.status === 'running') {
        meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 2) * 0.1);
      }
      
      // Rotation for selected
      if (isSelected) {
        meshRef.current.rotation.y += 0.01;
      }
      
      // Float effect
      meshRef.current.position.y = process.position.y + Math.sin(state.clock.elapsedTime + process.position.x) * 5;
    }
  });
  
  // Status colors
  const statusColors = {
    idle: '#444444',
    running: '#00ff88',
    completed: '#0088ff',
    error: '#ff4444',
    paused: '#ffaa00'
  };
  
  const handleClick = () => {
    selectProcess(process.id);
  };
  
  return (
    <group position={[process.position.x, process.position.y, process.position.z]}>
      <mesh
        ref={meshRef}
        onClick={handleClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <Box args={[80, 50, 20]}>
          <meshStandardMaterial
            color={statusColors[process.status]}
            emissive={statusColors[process.status]}
            emissiveIntensity={hovered ? 0.5 : 0.2}
            transparent
            opacity={0.8}
          />
        </Box>
      </mesh>
      
      <Text
        position={[0, 0, 11]}
        fontSize={12}
        color="white"
        anchorX="center"
        anchorY="middle"
      >
        {process.name}
      </Text>
      
      {/* Status indicator */}
      <Sphere args={[5]} position={[35, 20, 0]}>
        <meshBasicMaterial color={statusColors[process.status]} />
      </Sphere>
      
      {/* Input/Output ports */}
      {process.inputs.map((input, index) => (
        <Sphere
          key={input.id}
          args={[3]}
          position={[-40, -10 + index * 10, 0]}
        >
          <meshBasicMaterial color={input.connected ? '#00ff88' : '#666666'} />
        </Sphere>
      ))}
      
      {process.outputs.map((output, index) => (
        <Sphere
          key={output.id}
          args={[3]}
          position={[40, -10 + index * 10, 0]}
        >
          <meshBasicMaterial color={output.connected ? '#00ff88' : '#666666'} />
        </Sphere>
      ))}
    </group>
  );
};
```

### 5. Data Flow Animation Component
```typescript
// src/modules/ProcessFlowManager/DataFlow.tsx
import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { CatmullRomCurve3, TubeGeometry, Vector3 } from 'three';
import { DataFlow as DataFlowType, PythonProcess } from './types';
import { useProcessFlowStore } from '../../stores/processFlowStore';

interface DataFlowProps {
  flow: DataFlowType;
  processes: Map<string, PythonProcess>;
}

export const DataFlow: React.FC<DataFlowProps> = ({ flow, processes }) => {
  const particlesRef = useRef<THREE.InstancedMesh>(null);
  const { flowSpeed } = useProcessFlowStore();
  
  const source = processes.get(flow.sourceProcessId);
  const target = processes.get(flow.targetProcessId);
  
  // Create flow path
  const curve = useMemo(() => {
    if (!source || !target) return null;
    
    const start = new Vector3(source.position.x, source.position.y, source.position.z);
    const end = new Vector3(target.position.x, target.position.y, target.position.z);
    const middle = new Vector3(
      (start.x + end.x) / 2,
      (start.y + end.y) / 2 + 50,
      (start.z + end.z) / 2
    );
    
    return new CatmullRomCurve3([start, middle, end]);
  }, [source, target]);
  
  // Animate particles along the flow
  useFrame((state) => {
    if (!particlesRef.current || !curve) return;
    
    const time = state.clock.elapsedTime * flowSpeed;
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
      const t = ((time + i / particleCount) % 1);
      const position = curve.getPoint(t);
      
      const matrix = new THREE.Matrix4();
      matrix.setPosition(position.x, position.y, position.z);
      
      particlesRef.current.setMatrixAt(i, matrix);
    }
    
    particlesRef.current.instanceMatrix.needsUpdate = true;
  });
  
  if (!curve) return null;
  
  return (
    <group>
      {/* Flow tube */}
      <mesh>
        <tubeGeometry args={[curve, 64, 2, 8, false]} />
        <meshBasicMaterial
          color={flow.color}
          transparent
          opacity={0.3}
          wireframe
        />
      </mesh>
      
      {/* Animated particles */}
      <instancedMesh ref={particlesRef} args={[null, null, 20]}>
        <sphereGeometry args={[2]} />
        <meshBasicMaterial color={flow.color} emissive={flow.color} emissiveIntensity={1} />
      </instancedMesh>
    </group>
  );
};
```

### 6. Process Controls Component
```typescript
// src/modules/ProcessFlowManager/ProcessControls.tsx
import React, { useState } from 'react';
import { useProcessFlowStore } from '../../stores/processFlowStore';
import { PythonProcess } from './types';

export const ProcessControls: React.FC = () => {
  const {
    processes,
    startAllProcesses,
    stopAllProcesses,
    autoArrangeProcesses,
    setViewMode,
    setFlowSpeed,
    toggleAutoArrange,
    toggleMetrics,
    viewMode,
    flowSpeed,
    autoArrange,
    showMetrics
  } = useProcessFlowStore();
  
  const [showAddProcess, setShowAddProcess] = useState(false);
  
  const availableScripts = [
    { name: 'Neural Processor', script: 'neural_process.py', category: 'neural' },
    { name: 'Quantum Analyzer', script: 'quantum_analysis.py', category: 'quantum' },
    { name: 'Memory Consolidator', script: 'memory_consolidate.py', category: 'memory' },
    { name: 'Pattern Synthesizer', script: 'pattern_synthesis.py', category: 'synthesis' },
    { name: 'Entropy Monitor', script: 'entropy_monitor.py', category: 'analysis' }
  ];
  
  const handleAddProcess = (scriptInfo: any) => {
    const newProcess: PythonProcess = {
      id: `process-${Date.now()}`,
      name: scriptInfo.name,
      script: scriptInfo.script,
      status: 'idle',
      category: scriptInfo.category,
      cpuUsage: 0,
      memoryUsage: 0,
      executionTime: 0,
      lastTick: 0,
      inputs: [{ id: 'in1', name: 'Input', type: 'data', dataType: 'json', connected: false }],
      outputs: [{ id: 'out1', name: 'Output', type: 'data', dataType: 'json', connected: false }],
      description: `Executes ${scriptInfo.script}`,
      author: 'DAWN',
      version: '1.0.0',
      dependencies: [],
      logs: [],
      errors: [],
      outputData: null,
      position: { 
        x: Math.random() * 400 - 200, 
        y: Math.random() * 400 - 200, 
        z: Math.random() * 200 - 100 
      },
      velocity: { x: 0, y: 0, z: 0 }
    };
    
    useProcessFlowStore.getState().addProcess(newProcess);
    setShowAddProcess(false);
  };
  
  return (
    <div className="process-controls">
      <div className="control-group">
        <button onClick={startAllProcesses} className="control-btn start">
          <span className="icon">▶</span> Start All
        </button>
        <button onClick={stopAllProcesses} className="control-btn stop">
          <span className="icon">■</span> Stop All
        </button>
        <button onClick={() => setShowAddProcess(true)} className="control-btn add">
          <span className="icon">+</span> Add Process
        </button>
      </div>
      
      <div className="control-group">
        <button 
          onClick={() => setViewMode(viewMode === '2d' ? '3d' : '2d')} 
          className={`control-btn view-mode ${viewMode}`}
        >
          {viewMode.toUpperCase()} View
        </button>
        <button 
          onClick={toggleAutoArrange} 
          className={`control-btn ${autoArrange ? 'active' : ''}`}
        >
          Auto Arrange
        </button>
        <button 
          onClick={toggleMetrics} 
          className={`control-btn ${showMetrics ? 'active' : ''}`}
        >
          Show Metrics
        </button>
      </div>
      
      <div className="control-group">
        <label>Flow Speed</label>
        <input
          type="range"
          min="0.1"
          max="3"
          step="0.1"
          value={flowSpeed}
          onChange={(e) => setFlowSpeed(parseFloat(e.target.value))}
          className="flow-speed-slider"
        />
        <span>{flowSpeed.toFixed(1)}x</span>
      </div>
      
      {showAddProcess && (
        <div className="add-process-modal">
          <h3>Add Process</h3>
          <div className="script-list">
            {availableScripts.map((script) => (
              <div
                key={script.script}
                className={`script-item ${script.category}`}
                onClick={() => handleAddProcess(script)}
              >
                <span className="script-name">{script.name}</span>
                <span className="script-file">{script.script}</span>
              </div>
            ))}
          </div>
          <button onClick={() => setShowAddProcess(false)} className="close-btn">
            Cancel
          </button>
        </div>
      )}
    </div>
  );
};
```

### 7. Process Monitor Component
```typescript
// src/modules/ProcessFlowManager/ProcessMonitor.tsx
import React, { useEffect, useState } from 'react';
import { Line } from 'recharts';
import { useProcessFlowStore } from '../../stores/processFlowStore';

interface ProcessMonitorProps {
  processId: string;
}

export const ProcessMonitor: React.FC<ProcessMonitorProps> = ({ processId }) => {
  const process = useProcessFlowStore((state) => state.processes.get(processId));
  const [metrics, setMetrics] = useState<any[]>([]);
  
  useEffect(() => {
    if (!process) return;
    
    // Update metrics history
    const interval = setInterval(() => {
      setMetrics((prev) => {
        const newMetric = {
          time: Date.now(),
          cpu: process.cpuUsage,
          memory: process.memoryUsage,
          tick: process.lastTick
        };
        
        return [...prev.slice(-50), newMetric];
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, [process]);
  
  if (!process) return null;
  
  return (
    <div className="process-monitor">
      <h3>{process.name} Monitor</h3>
      
      <div className="monitor-section">
        <h4>Status</h4>
        <div className={`status-indicator ${process.status}`}>
          {process.status.toUpperCase()}
        </div>
      </div>
      
      <div className="monitor-section">
        <h4>Performance</h4>
        <div className="metric">
          <span>CPU:</span>
          <span>{process.cpuUsage.toFixed(1)}%</span>
        </div>
        <div className="metric">
          <span>Memory:</span>
          <span>{process.memoryUsage.toFixed(1)} MB</span>
        </div>
        <div className="metric">
          <span>Last Tick:</span>
          <span>{process.lastTick}</span>
        </div>
      </div>
      
      <div className="monitor-section">
        <h4>Recent Logs</h4>
        <div className="log-container">
          {process.logs.slice(-5).map((log, index) => (
            <div key={index} className={`log-entry ${log.level}`}>
              <span className="log-time">
                {new Date(log.timestamp).toLocaleTimeString()}
              </span>
              <span className="log-message">{log.message}</span>
            </div>
          ))}
        </div>
      </div>
      
      {process.errors.length > 0 && (
        <div className="monitor-section errors">
          <h4>Errors</h4>
          <div className="error-container">
            {process.errors.slice(-3).map((error, index) => (
              <div key={index} className="error-entry">
                <span className="error-type">{error.type}</span>
                <span className="error-message">{error.message}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="monitor-actions">
        <button 
          onClick={() => useProcessFlowStore.getState().startProcess(process.id)}
          disabled={process.status === 'running'}
        >
          Start
        </button>
        <button 
          onClick={() => useProcessFlowStore.getState().stopProcess(process.id)}
          disabled={process.status !== 'running'}
        >
          Stop
        </button>
        <button 
          onClick={() => useProcessFlowStore.getState().restartProcess(process.id)}
        >
          Restart
        </button>
      </div>
    </div>
  );
};
```

### 8. CSS Styling
```css
/* src/modules/ProcessFlowManager/ProcessFlowManager.css */
.process-flow-manager {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
  color: #ffffff;
  font-family: 'Inter', sans-serif;
}

.flow-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
}

.flow-header h2 {
  font-size: 24px;
  font-weight: 600;
  background: linear-gradient(135deg, #00ff88 0%, #00aaff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.flow-stats {
  display: flex;
  gap: 30px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.flow-container {
  flex: 1;
  display: flex;
  position: relative;
  overflow: hidden;
}

.flow-canvas {
  flex: 1;
  position: relative;
  background: radial-gradient(ellipse at center, rgba(0, 255, 136, 0.05) 0%, transparent 70%);
}

/* Process Controls */
.process-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  z-index: 10;
}

.control-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

.control-btn {
  padding: 8px 16px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 8px;
  color: #00ff88;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.control-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  transform: translateY(-1px);
}

.control-btn.active {
  background: rgba(0, 255, 136, 0.3);
  border-color: #00ff88;
}

.control-btn.start { color: #00ff88; }
.control-btn.stop { color: #ff4444; }
.control-btn.add { color: #00aaff; }

/* Process Monitor */
.process-monitor {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 300px;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 12px;
  padding: 20px;
  z-index: 10;
}

.monitor-section {
  margin-bottom: 20px;
}

.monitor-section h4 {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 10px;
}

.status-indicator {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  text-transform: uppercase;
}

.status-indicator.running {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
  animation: pulse 2s infinite;
}

.status-indicator.idle {
  background: rgba(68, 68, 68, 0.2);
  color: #888888;
}

.status-indicator.error {
  background: rgba(255, 68, 68, 0.2);
  color: #ff4444;
}

/* Metrics */
.metric {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.metric span:first-child {
  color: rgba(255, 255, 255, 0.7);
}

.metric span:last-child {
  color: #00ff88;
  font-weight: 600;
}

/* Logs */
.log-container {
  max-height: 150px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 6px;
  padding: 10px;
}

.log-entry {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
  font-size: 12px;
}

.log-time {
  color: rgba(255, 255, 255, 0.5);
}

.log-message {
  color: rgba(255, 255, 255, 0.9);
}

/* Animations */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(0, 255, 136, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0);
  }
}

/* Category Colors */
:root {
  --category-neural: #00ff88;
  --category-quantum: #00aaff;
  --category-chaos: #ff00aa;
  --category-process: #ffaa00;
  --category-memory: #aa00ff;
  --category-analysis: #ff4444;
  --category-synthesis: #44ff44;
}

/* Add Process Modal */
.add-process-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 16px;
  padding: 30px;
  min-width: 400px;
  z-index: 100;
}

.script-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 20px 0;
}

.script-item {
  padding: 15px;
  background: rgba(0, 255, 136, 0.05);
  border: 1px solid rgba(0, 255, 136, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.script-item:hover {
  background: rgba(0, 255, 136, 0.1);
  transform: translateX(5px);
}

.script-name {
  display: block;
  font-weight: 600;
  margin-bottom: 5px;
}

.script-file {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

/* Flow Speed Slider */
.flow-speed-slider {
  width: 100px;
  height: 4px;
  background: rgba(0, 255, 136, 0.2);
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
}

.flow-speed-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  background: #00ff88;
  border-radius: 50%;
  cursor: pointer;
}

/* 2D View Styles */
.flow-2d-view {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.flow-2d-view svg {
  position: absolute;
  top: 0;
  left: 0;
}
```

## 🚀 API Service
```typescript
// src/services/processManager.ts
interface ProcessManagerAPI {
  startProcess: (processId: string) => Promise<void>;
  stopProcess: (processId: string) => Promise<void>;
  getProcessStatus: (processId: string) => Promise<ProcessStatus>;
  executeScript: (script: string, params?: any) => Promise<any>;
  streamProcessOutput: (processId: string, callback: (data: any) => void) => void;
}

export const processManager: ProcessManagerAPI = {
  startProcess: async (processId: string) => {
    const response = await fetch(`/api/processes/${processId}/start`, {
      method: 'POST'
    });
    if (!response.ok) throw new Error('Failed to start process');
  },
  
  stopProcess: async (processId: string) => {
    const response = await fetch(`/api/processes/${processId}/stop`, {
      method: 'POST'
    });
    if (!response.ok) throw new Error('Failed to stop process');
  },
  
  getProcessStatus: async (processId: string) => {
    const response = await fetch(`/api/processes/${processId}/status`);
    return response.json();
  },
  
  executeScript: async (script: string, params?: any) => {
    const response = await fetch('/api/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ script, params })
    });
    return response.json();
  },
  
  streamProcessOutput: (processId: string, callback: (data: any) => void) => {
    const eventSource = new EventSource(`/api/processes/${processId}/stream`);
    eventSource.onmessage = (event) => {
      callback(JSON.parse(event.data));
    };
    return () => eventSource.close();
  }
};
```

## 📝 Cursor Implementation Prompts

### Prompt 1: Create Process Flow Manager
```
Create the Process Flow Manager module for DAWN. This is a 3D visualization of Python processes as nodes in a graph with animated data flows between them.

Key requirements:
1. Use Three.js (via @react-three/fiber) for 3D visualization
2. Show processes as glowing nodes that breathe when running
3. Animate data flows as particles moving between nodes
4. Support both 2D and 3D view modes
5. Include controls to start/stop processes and add new ones
6. Show real-time metrics (CPU, memory, logs) for selected process
7. Auto-arrange processes using force-directed layout
8. Connect to WebSocket for tick updates

File structure provided:
- ProcessFlowManager.tsx (main component)
- ProcessNode.tsx (3D node visualization)
- DataFlow.tsx (animated connections)
- ProcessControls.tsx (UI controls)
- ProcessMonitor.tsx (metrics panel)
- types.ts (TypeScript interfaces)
- processFlowStore.ts (Zustand store)

Make it feel alive - processes should pulse, flows should glow, and everything should respond to the consciousness engine's state.
```

### Prompt 2: Add Process Execution API
```
Add the backend API integration for the Process Flow Manager:

1. Create processManager.ts service with methods to:
   - Start/stop Python processes
   - Get process status
   - Execute scripts with parameters
   - Stream process output via EventSource

2. Update the Zustand store to call these APIs

3. Add error handling and retry logic

4. Include mock responses for development

The API should connect to the Python backend at /api/processes/*
```

### Prompt 3: Enhance Visual Effects
```
Enhance the Process Flow Manager with advanced visual effects:

1. Add glow effects to running processes using Three.js shaders
2. Create particle systems for data flows that respond to flow rate
3. Add connection animations when linking processes
4. Implement magnetic snapping when dragging nodes near each other
5. Add visual feedback for errors (red pulses, shake effects)
6. Create smooth camera transitions when selecting processes
7. Add depth-of-field blur for non-selected processes

Make it feel like controlling a living neural network!
```

## 🎯 Integration Points

### Connect to Existing Systems
```typescript
// In Dashboard or App.tsx
import { ProcessFlowManager } from './modules/ProcessFlowManager/ProcessFlowManager';

// Add to your module registry
const moduleRegistry = {
  'process-flow': ProcessFlowManager,
  // ... other modules
};
```

### Listen to Tick Updates
```typescript
// The ProcessFlowManager already subscribes to WebSocket context
// Process metrics update automatically with each tick
```

### Connect to Memory Palace
```typescript
// When a memory is accessed, trigger a process
useEffect(() => {
  if (memoryAccessed) {
    processManager.executeScript('memory_analysis.py', {
      memoryId: memory.id,
      analysisType: 'deep'
    });
  }
}, [memoryAccessed]);
```

## 🔮 Next Steps

1. **Process Templates**: Pre-configured process chains for common tasks
2. **Visual Scripting**: Drag-and-drop process creation
3. **Performance Profiling**: Detailed timing analysis
4. **Process Versioning**: Track and rollback process changes
5. **Distributed Processing**: Run processes across multiple machines

The Process Flow Manager makes DAWN's intelligence visible and controllable - turning abstract computations into a living, breathing nervous system! 🧬⚡