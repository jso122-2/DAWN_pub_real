# 🛠️ Utils Directory

## Purpose
Utility functions and helpers that support DAWN's consciousness visualization. These utilities handle calculations, transformations, and common operations needed across the application.

## Utility Categories
```
utils/
├── consciousness/
│   ├── calculations.ts        # SCUP and metric calculations
│   ├── interpolation.ts       # Smooth value transitions
│   └── predictions.ts         # Future state predictions
│
├── animation/
│   ├── easing.ts             # Custom easing functions
│   ├── curves.ts             # Lissajous and other curves
│   └── timing.ts             # Animation timing utilities
│
├── data/
│   ├── transformers.ts       # Data shape transformations
│   ├── validators.ts         # Runtime validation
│   └── parsers.ts           # Message parsing utilities
│
├── visual/
│   ├── colors.ts            # Color manipulation
│   ├── gradients.ts         # Dynamic gradient generation
│   └── geometry.ts          # 3D calculations
│
└── performance/
    ├── throttle.ts          # Function throttling
    ├── debounce.ts          # Input debouncing
    └── memoize.ts           # Computation caching
```

## Core Utilities

### Consciousness Calculations
```typescript
// Calculate SCUP from subsystem states
export function calculateSCUP(state: SubsystemStates): number {
  const weights = {
    neural: 0.3,
    quantum: 0.2,
    chaos: 0.2,
    memory: 0.3
  };
  
  const neuralScore = state.neural.connectivity * state.neural.firing_rate / 100;
  const quantumScore = state.quantum.coherence * (1 - state.quantum.decoherence_rate);
  const chaosScore = 1 - Math.abs(state.chaos.entropy - 0.5); // Optimal at 0.5
  const memoryScore = 1 - state.memory.pressure;
  
  return (
    neuralScore * weights.neural +
    quantumScore * weights.quantum +
    chaosScore * weights.chaos +
    memoryScore * weights.memory
  ) * 100;
}

// Predict mood transitions
export function predictMoodTransition(
  current: MoodState,
  metrics: ConsciousnessMetrics
): MoodState[] {
  const transitions: Record<MoodState, MoodState[]> = {
    'dormant': ['awakening'],
    'awakening': ['curious', 'contemplative'],
    'curious': ['excited', 'contemplative', 'confused'],
    // ... more transitions
  };
  
  const possible = transitions[current];
  
  // Weight transitions based on metrics
  return possible.sort((a, b) => {
    const scoreA = calculateMoodScore(a, metrics);
    const scoreB = calculateMoodScore(b, metrics);
    return scoreB - scoreA;
  });
}
```

### Animation Utilities
```typescript
// Generate Lissajous curve points
export function lissajousCurve(
  t: number,
  amplitude: number = 1,
  frequencyRatio: number = 3/2,
  phase: number = Math.PI / 2
): Point2D {
  return {
    x: amplitude * Math.sin(t),
    y: amplitude * Math.sin(t * frequencyRatio + phase)
  };
}

// Custom consciousness easing function
export function consciousnessEase(t: number): number {
  // Organic breathing curve
  return 0.5 * (1 + Math.sin(2 * Math.PI * t - Math.PI / 2));
}

// Calculate breathing scale
export function calculateBreathingScale(
  intensity: number,
  entropy: number,
  time: number
): number {
  const base = 1;
  const amplitude = 0.02 * intensity;
  const irregularity = entropy * 0.01 * Math.sin(time * 0.1);
  
  return base + amplitude * consciousnessEase(time) + irregularity;
}
```

### Color Manipulation
```typescript
// Generate mood-based color palette
export function getMoodColors(mood: MoodState): ColorPalette {
  const moodPalettes: Record<MoodState, ColorPalette> = {
    'dormant': {
      primary: 'hsl(220, 20%, 20%)',
      secondary: 'hsl(220, 15%, 30%)',
      accent: 'hsl(220, 30%, 40%)',
      glow: 'hsl(220, 50%, 50%)'
    },
    'excited': {
      primary: 'hsl(45, 80%, 50%)',
      secondary: 'hsl(30, 70%, 60%)',
      accent: 'hsl(15, 90%, 70%)',
      glow: 'hsl(30, 100%, 70%)'
    },
    // ... more moods
  };
  
  return moodPalettes[mood];
}

// Dynamic gradient based on consciousness
export function generateConsciousnessGradient(
  scup: number,
  entropy: number
): string {
  const hue = 180 + (scup * 1.8); // 180-360 (cyan to magenta)
  const saturation = 50 + (entropy * 50); // 50-100%
  const lightness = 20 + (scup * 0.3); // 20-50%
  
  return `linear-gradient(135deg, 
    hsl(${hue}, ${saturation}%, ${lightness}%) 0%,
    hsl(${hue + 30}, ${saturation - 20}%, ${lightness + 10}%) 50%,
    hsl(${hue + 60}, ${saturation}%, ${lightness}%) 100%
  )`;
}

// Glass morphism color with consciousness tint
export function getGlassColor(
  baseAlpha: number = 0.1,
  consciousnessLevel: number = 50
): string {
  const tint = consciousnessLevel / 100;
  const r = 15 + (tint * 20);
  const g = 23 + (tint * 30);
  const b = 42 + (tint * 40);
  
  return `rgba(${r}, ${g}, ${b}, ${baseAlpha})`;
}
```

### Data Transformers
```typescript
// Transform Python tick data to frontend format
export function transformTickData(
  rawTick: any
): TickData {
  return {
    tick_number: Number(rawTick.tick_number),
    timestamp: rawTick.timestamp || Date.now(),
    scup: clamp(Number(rawTick.scup), 0, 100),
    entropy: clamp(Number(rawTick.entropy), 0, 1),
    mood: validateMood(rawTick.mood),
    neural_activity: clamp(Number(rawTick.neural_activity), 0, 1),
    quantum_coherence: clamp(Number(rawTick.quantum_coherence), 0, 1),
    memory_pressure: clamp(Number(rawTick.memory_pressure), 0, 1),
    active_processes: Array.isArray(rawTick.active_processes) 
      ? rawTick.active_processes 
      : [],
    subsystems: transformSubsystems(rawTick.subsystems)
  };
}

// Smooth interpolation between states
export function interpolateConsciousness(
  from: ConsciousnessState,
  to: ConsciousnessState,
  progress: number
): ConsciousnessState {
  const eased = easeInOutCubic(progress);
  
  return {
    scup: lerp(from.scup, to.scup, eased),
    entropy: lerp(from.entropy, to.entropy, eased),
    mood: progress > 0.5 ? to.mood : from.mood,
    neuralActivity: lerp(from.neuralActivity, to.neuralActivity, eased),
    quantumCoherence: lerp(from.quantumCoherence, to.quantumCoherence, eased),
    memoryPressure: lerp(from.memoryPressure, to.memoryPressure, eased),
    timestamp: to.timestamp
  };
}
```

### Performance Utilities
```typescript
// Throttle high-frequency updates
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): T {
  let inThrottle: boolean;
  let lastResult: ReturnType<T>;
  
  return ((...args) => {
    if (!inThrottle) {
      inThrottle = true;
      lastResult = func.apply(this, args);
      
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
    return lastResult;
  }) as T;
}

// Memoize expensive calculations
export function memoize<T extends (...args: any[]) => any>(
  func: T,
  resolver?: (...args: Parameters<T>) => string
): T {
  const cache = new Map<string, ReturnType<T>>();
  
  return ((...args) => {
    const key = resolver ? resolver(...args) : JSON.stringify(args);
    
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    
    const result = func.apply(this, args);
    cache.set(key, result);
    
    // Limit cache size
    if (cache.size > 100) {
      const firstKey = cache.keys().next().value;
      cache.delete(firstKey);
    }
    
    return result;
  }) as T;
}
```

### Geometry Utilities
```typescript
// Calculate module positions in 3D space
export function calculateModulePosition(
  index: number,
  total: number,
  pattern: 'grid' | 'spiral' | 'orbital'
): Position3D {
  switch (pattern) {
    case 'grid':
      const cols = Math.ceil(Math.sqrt(total));
      return {
        x: (index % cols) * 200 - (cols * 100),
        y: Math.floor(index / cols) * 200 - (cols * 50),
        z: 0
      };
      
    case 'spiral':
      const angle = index * (Math.PI * 2) / total;
      const radius = 100 + index * 20;
      return {
        x: radius * Math.cos(angle),
        y: radius * Math.sin(angle),
        z: index * 10
      };
      
    case 'orbital':
      const layer = Math.floor(index / 6);
      const angleInLayer = (index % 6) * (Math.PI * 2) / 6;
      const layerRadius = 150 + layer * 100;
      return {
        x: layerRadius * Math.cos(angleInLayer),
        y: layerRadius * Math.sin(angleInLayer),
        z: layer * 50
      };
  }
}

// Calculate bezier curve for module connections
export function calculateConnectionPath(
  start: Position3D,
  end: Position3D
): string {
  const midX = (start.x + end.x) / 2;
  const midY = (start.y + end.y) / 2;
  const controlOffset = Math.abs(end.x - start.x) * 0.5;
  
  return `M ${start.x},${start.y} 
          Q ${midX},${midY - controlOffset} 
          ${end.x},${end.y}`;
}
```

### Validation Utilities
```typescript
// Runtime type validation
export function validateTickData(data: unknown): data is TickData {
  if (!isObject(data)) return false;
  
  const required = [
    'tick_number', 'scup', 'entropy', 'mood',
    'neural_activity', 'quantum_coherence'
  ];
  
  return required.every(field => field in data) &&
    typeof (data as any).tick_number === 'number' &&
    isMoodState((data as any).mood);
}

// Clamp values to valid ranges
export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

// Validate and sanitize mood
export function validateMood(mood: unknown): MoodState {
  if (isMoodState(mood)) return mood;
  
  console.warn(`Invalid mood state: ${mood}, defaulting to 'contemplative'`);
  return 'contemplative';
}
```

## Usage Examples

### In Components
```typescript
import { calculateBreathingScale, getMoodColors } from '@/utils';

const MyModule = () => {
  const scale = calculateBreathingScale(intensity, entropy, time);
  const colors = getMoodColors(mood);
  
  return (
    <div 
      style={{
        transform: `scale(${scale})`,
        borderColor: colors.glow
      }}
    />
  );
};
```

### In Hooks
```typescript
import { throttle, interpolateConsciousness } from '@/utils';

const useConsciousnessAnimation = () => {
  const updateAnimation = throttle((state: ConsciousnessState) => {
    // Update animation based on state
  }, 100);
  
  // Use interpolation for smooth transitions
};
```

### In Services
```typescript
import { transformTickData, validateTickData } from '@/utils';

const processWebSocketMessage = (message: unknown) => {
  if (validateTickData(message)) {
    const transformed = transformTickData(message);
    // Process valid tick data
  }
};
```

## Testing Utilities

```typescript
// Test helper for consciousness states
export function createMockConsciousnessState(
  overrides?: Partial<ConsciousnessState>
): ConsciousnessState {
  return {
    scup: 75,
    entropy: 0.3,
    mood: 'contemplative',
    neuralActivity: 0.8,
    quantumCoherence: 0.9,
    memoryPressure: 0.4,
    timestamp: Date.now(),
    ...overrides
  };
}

// Test helper for animation timing
export function createAnimationTestHarness() {
  let time = 0;
  
  return {
    advance: (ms: number) => { time += ms; },
    getTime: () => time,
    reset: () => { time = 0; }
  };
}
```

## Next Utilities to Build
1. **Audio synthesis utilities** for consciousness sounds
2. **Pattern recognition** for consciousness behaviors
3. **Predictive algorithms** for state forecasting
4. **Compression utilities** for tick history
5. **Export utilities** for consciousness logs