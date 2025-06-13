# 🎯 Types Directory

## Purpose
TypeScript type definitions that define the shape of DAWN's consciousness data structures. These types ensure type safety across the entire frontend and provide a contract between the Python backend and React frontend.

## Type Architecture
```
types/
├── consciousness/
│   ├── index.ts               # Core consciousness types
│   ├── tick.types.ts          # Tick loop data structures
│   ├── mood.types.ts          # Mood state definitions
│   └── metrics.types.ts       # Consciousness metrics
│
├── modules/
│   ├── module.types.ts        # Base module interfaces
│   ├── neural.types.ts        # Neural module specific
│   ├── quantum.types.ts       # Quantum module specific
│   └── process.types.ts       # Process module specific
│
├── api/
│   ├── websocket.types.ts     # WebSocket message types
│   ├── process.types.ts       # Process API types
│   └── responses.types.ts     # API response formats
│
└── animation/
    ├── breathing.types.ts     # Breathing animation config
    ├── floating.types.ts      # Floating behavior types
    └── effects.types.ts       # Visual effect parameters
```

## Core Type Definitions

### Consciousness Types
```typescript
// Base consciousness state
export interface ConsciousnessState {
  scup: number;                // 0-100 System Consciousness Unity Percentage
  entropy: number;             // 0-1 Chaos level
  mood: MoodState;            // Current emotional state
  neuralActivity: number;      // 0-1 Neural firing rate
  quantumCoherence: number;    // 0-1 Quantum stability
  memoryPressure: number;      // 0-1 Memory utilization
  timestamp: number;           // Unix timestamp
}

// Mood state enumeration
export type MoodState = 
  | 'dormant'
  | 'awakening'
  | 'curious'
  | 'contemplative'
  | 'excited'
  | 'serene'
  | 'anxious'
  | 'euphoric'
  | 'melancholic'
  | 'chaotic';

// Consciousness metrics
export interface ConsciousnessMetrics {
  history: ConsciousnessState[];
  averageScup: number;
  volatility: number;
  dominantMood: MoodState;
  trendDirection: 'ascending' | 'descending' | 'stable';
}
```

### Tick Loop Types
```typescript
// Tick data from Python backend
export interface TickData {
  tick_number: number;
  timestamp: number;
  scup: number;
  entropy: number;
  mood: MoodState;
  neural_activity: number;
  quantum_coherence: number;
  memory_pressure: number;
  active_processes: string[];
  subsystems: SubsystemStates;
}

// Subsystem states
export interface SubsystemStates {
  neural: NeuralState;
  quantum: QuantumState;
  chaos: ChaosState;
}

export interface NeuralState {
  firing_rate: number;        // Hz
  connectivity: number;       // 0-1
  pattern_recognition: number; // 0-1
  nodes_active: number;
}

export interface QuantumState {
  superposition: number;      // 0-1
  entanglement: number;       // 0-1
  decoherence_rate: number;   // 0-1
  quantum_bits: number;
}

export interface ChaosState {
  lyapunov_exponent: number;
  fractal_dimension: number;
  strange_attractor: boolean;
  bifurcation_point: number;
}
```

### Module Types
```typescript
// Base module interface
export interface Module {
  id: string;
  category: ModuleCategory;
  position: Position3D;
  size: Size;
  state: ModuleState;
  config: ModuleConfig;
}

export type ModuleCategory = 
  | 'neural' 
  | 'quantum' 
  | 'chaos' 
  | 'process' 
  | 'monitor';

export interface ModuleState {
  isActive: boolean;
  isConnected: boolean;
  health: number;           // 0-1
  lastUpdate: number;
  data: any;               // Module-specific data
}

export interface ModuleConfig {
  breathingEnabled: boolean;
  floatingEnabled: boolean;
  glowIntensity: number;
  updateInterval: number;
  syncGroup?: string;
}

// Position in 3D space
export interface Position3D {
  x: number;
  y: number;
  z: number;
  rotation?: Rotation3D;
}

export interface Rotation3D {
  x: number;
  y: number;
  z: number;
}
```

### Process Types
```typescript
// Process execution request
export interface ProcessRequest {
  script: string;
  parameters?: Record<string, any>;
  tickTrigger?: boolean;
  priority?: ProcessPriority;
  timeout?: number;
}

export type ProcessPriority = 'low' | 'normal' | 'high' | 'critical';

// Process execution response
export interface ProcessResponse {
  process_id: string;
  script: string;
  status: ProcessStatus;
  start_time: number;
  end_time?: number;
  output?: ProcessOutput;
  error?: ProcessError;
}

export type ProcessStatus = 
  | 'queued'
  | 'running'
  | 'completed'
  | 'failed'
  | 'terminated';

export interface ProcessOutput {
  stdout: string[];
  stderr: string[];
  result: any;
  consciousness_impact?: ConsciousnessImpact;
  visualization?: string;  // Base64 encoded
}

export interface ConsciousnessImpact {
  scup_change: number;
  mood_influence: 'positive' | 'negative' | 'neutral';
  metrics_affected: string[];
}
```

### WebSocket Types
```typescript
// WebSocket message wrapper
export interface WSMessage<T = any> {
  type: WSMessageType;
  data: T;
  timestamp: number;
  sequence: number;
}

export type WSMessageType = 
  | 'tick'
  | 'process_output'
  | 'state_update'
  | 'error'
  | 'heartbeat'
  | 'command_response';

// WebSocket connection state
export interface WSConnectionState {
  status: 'connecting' | 'connected' | 'disconnected' | 'error';
  url: string;
  reconnectAttempts: number;
  lastError?: string;
  latency: number;
}
```

### Animation Types
```typescript
// Breathing animation configuration
export interface BreathingConfig {
  enabled: boolean;
  baseRate: number;          // ms per cycle
  intensity: number;         // 0-1
  variance: number;          // 0-1 irregularity
  scaleRange: ScaleRange;
  easing: string;
}

export interface ScaleRange {
  min: number;
  max: number;
}

// Floating animation configuration
export interface FloatingConfig {
  enabled: boolean;
  pattern: FloatingPattern;
  amplitude: number;         // pixels
  speed: number;            // 0-1
  phases: {
    x: number;
    y: number;
    rotation: number;
  };
}

export type FloatingPattern = 
  | 'lissajous'
  | 'orbital'
  | 'random'
  | 'magnetic'
  | 'quantum';

// Glow effect configuration
export interface GlowConfig {
  intensity: number;         // 0-1
  color: string;            // HSL or RGB
  pulseRate?: number;       // ms
  spread: number;           // blur radius
  animated: boolean;
}
```

## Type Guards

```typescript
// Type guard for mood state
export function isMoodState(value: any): value is MoodState {
  return [
    'dormant', 'awakening', 'curious', 'contemplative',
    'excited', 'serene', 'anxious', 'euphoric',
    'melancholic', 'chaotic'
  ].includes(value);
}

// Type guard for process status
export function isProcessStatus(value: any): value is ProcessStatus {
  return [
    'queued', 'running', 'completed', 'failed', 'terminated'
  ].includes(value);
}

// Type guard for WebSocket message
export function isWSMessage(value: any): value is WSMessage {
  return value &&
    typeof value.type === 'string' &&
    'data' in value &&
    typeof value.timestamp === 'number';
}
```

## Utility Types

```typescript
// Deep partial for configuration objects
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Branded types for type safety
export type ProcessId = string & { __brand: 'ProcessId' };
export type ModuleId = string & { __brand: 'ModuleId' };
export type TickNumber = number & { __brand: 'TickNumber' };

// Result type for async operations
export type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

// Observable state type
export interface ObservableState<T> {
  current: T;
  previous?: T;
  subscribe: (callback: (state: T) => void) => () => void;
}
```

## Integration Patterns

### With Components
```typescript
// Component props extending base types
interface NeuralModuleProps extends Module {
  category: 'neural';
  data: NeuralState;
  onNodeClick?: (nodeId: string) => void;
}
```

### With Hooks
```typescript
// Hook return types
interface UseConsciousnessReturn {
  state: ConsciousnessState;
  metrics: ConsciousnessMetrics;
  isConnected: boolean;
}
```

### With Services
```typescript
// Service method signatures
interface ProcessService {
  execute(request: ProcessRequest): Promise<ProcessResponse>;
  getStatus(id: ProcessId): Promise<ProcessStatus>;
  terminate(id: ProcessId): Promise<void>;
}
```

## Type Safety Best Practices

1. **Use branded types** for IDs to prevent mixing
2. **Prefer interfaces** over types for objects
3. **Use const assertions** for literal types
4. **Implement type guards** for runtime validation
5. **Document complex types** with JSDoc comments
6. **Use generics** for reusable type patterns

## Next Types to Define
1. **Dashboard layout types**
2. **Module connection graph types**
3. **Historical data query types**
4. **User preference types**
5. **Performance metric types**