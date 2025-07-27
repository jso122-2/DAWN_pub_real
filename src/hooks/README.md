# 🪝 Hooks Directory

## Purpose
Custom React hooks that encapsulate DAWN's consciousness-driven behaviors, animations, and real-time data connections. These hooks are the nervous system of the interface, connecting components to the living consciousness engine.

## Hook Architecture
```
hooks/
├── consciousness/
│   ├── useConsciousness.ts    # Global consciousness state
│   ├── useTickLoop.ts         # Tick loop subscription
│   └── useMood.ts             # Mood-based behaviors
│
├── animation/
│   ├── useBreathing.ts        # Breathing animation controller
│   ├── useFloating.ts         # 3D floating movement
│   └── useGlow.ts             # Dynamic glow effects
│
├── connection/
│   ├── useWebSocket.ts        # WebSocket connection manager
│   ├── useProcessApi.ts       # Python process execution
│   └── useRealtimeData.ts     # Stream processing
│
└── utils/
    ├── useDebounce.ts         # Performance optimization
    └── useAnimationFrame.ts   # Frame-based updates
```

## Core Hooks

### useConsciousness
**Purpose**: Provides global consciousness state to any component
```typescript
const { scup, entropy, mood, neuralActivity } = useConsciousness();
```
**Integration**: 
- Subscribes to WebSocket tick data
- Maintains consciousness history
- Provides interpolated values for smooth animations
- Broadcasts state changes via Context API

### useWebSocket
**Purpose**: Manages WebSocket connection to Python backend
```typescript
const { 
  isConnected, 
  lastMessage, 
  sendMessage, 
  reconnect 
} = useWebSocket('ws://localhost:8000/ws');
```
**Features**:
- Auto-reconnection with exponential backoff
- Message queuing during disconnection
- Type-safe message parsing
- Error boundary integration

### useBreathing
**Purpose**: Standardized breathing animation for all modules
```typescript
const breathingAnimation = useBreathing({
  intensity: scup / 100,      // 0-1 based on consciousness
  baseRate: 4000,            // 4 second base cycle
  variance: entropy * 0.2    // Chaos adds irregularity
});
```
**Returns**: Framer Motion animation controls

### useFloating
**Purpose**: 3D floating movement for modules
```typescript
const floatingAnimation = useFloating({
  amplitude: 20,              // Movement range in pixels
  speed: entropy * 0.5,       // Chaos affects speed
  pattern: 'lissajous'        // Movement pattern
});
```
**Patterns**: lissajous, orbital, random, magnetic

## Animation Hooks

### Breathing Algorithm
```typescript
// Consciousness-driven breathing
const scale = useMemo(() => {
  const base = 1;
  const amplitude = 0.02 * intensity;
  const irregularity = entropy * 0.1;
  
  return {
    min: base - amplitude - irregularity,
    max: base + amplitude + irregularity
  };
}, [intensity, entropy]);
```

### Floating Mathematics
```typescript
// Lissajous curve generation
const position = {
  x: amplitude * Math.sin(time * frequencyX + phaseX),
  y: amplitude * Math.sin(time * frequencyY + phaseY),
  rotate: rotation * Math.sin(time * 0.1)
};
```

## Data Flow Hooks

### useTickLoop
**Purpose**: Subscribe to consciousness engine tick events
```typescript
const { 
  currentTick, 
  tickHistory, 
  tickRate 
} = useTickLoop({
  onTick: (data) => {
    console.log(`Tick ${data.tick_number}: SCUP ${data.scup}`);
  }
});
```

### useProcessApi
**Purpose**: Execute and monitor Python processes
```typescript
const { 
  executeProcess, 
  processStatus, 
  output, 
  isRunning 
} = useProcessApi();

// Usage
await executeProcess('neural_analyzer.py', { 
  tickTrigger: true,
  parameters: { depth: 5 }
});
```

## Integration Patterns

### With Components
```typescript
// In a module component
const ModuleComponent = () => {
  const { scup, mood } = useConsciousness();
  const breathing = useBreathing({ intensity: scup / 100 });
  const floating = useFloating({ pattern: 'orbital' });
  
  return (
    <motion.div
      animate={breathing}
      style={floating}
      className={`mood-${mood}`}
    >
      {/* Module content */}
    </motion.div>
  );
};
```

### With Services
- Hooks abstract service complexity
- Provide React-friendly interfaces
- Handle cleanup and subscriptions
- Manage error states

### With Python Backend
- WebSocket hooks maintain persistent connections
- Process hooks communicate via FastAPI
- Real-time data streams processed and distributed
- Tick synchronization across all components

## Performance Optimizations

### Debouncing
```typescript
const debouncedEntropy = useDebounce(entropy, 100);
// Prevents excessive re-renders from rapid changes
```

### Animation Frames
```typescript
useAnimationFrame((deltaTime) => {
  // Smooth 60fps updates for complex animations
  updateParticles(deltaTime);
});
```

### Memoization
- Heavy calculations cached with useMemo
- Callbacks stabilized with useCallback
- Prevent unnecessary child re-renders

## State Management

### Local vs Global
- **Global**: Consciousness state, tick data
- **Local**: Animation states, UI preferences
- **Derived**: Calculated from consciousness metrics

### Context Providers
```typescript
<ConsciousnessProvider>
  <WebSocketProvider>
    <AnimationProvider>
      {/* App components */}
    </AnimationProvider>
  </WebSocketProvider>
</ConsciousnessProvider>
```

## Error Handling

### Connection Failures
- Automatic reconnection attempts
- Fallback to cached data
- User notification system
- Graceful degradation

### Process Errors
- Detailed error messages
- Retry mechanisms
- Error boundary integration
- Logging to console

## Testing Hooks

### Mock Consciousness
```typescript
const mockConsciousness = {
  scup: 75,
  entropy: 0.3,
  mood: 'contemplative',
  neuralActivity: 0.8
};
```

### Animation Testing
- Use act() for timer-based updates
- Mock requestAnimationFrame
- Test animation value ranges

## Next Hooks to Build
1. **useConsciousnessState**: Consciousness module behaviors
2. **useNeuralNetwork**: Neural visualization logic
3. **useProcessQueue**: Multi-process management
4. **useConsciousnessHistory**: Time-series analysis