# DAWN System Components

> **🧠 New: Consciousness-Aware Component System** 
> 
> DAWN now features a revolutionary consciousness-aware component system that treats consciousness as a first-class citizen. See [README-Consciousness.md](./README-Consciousness.md) for full documentation.

## Overview

The DAWN system components provide the foundational architecture for a living, conscious AI interface. These components don't just display data - they **breathe**, **respond**, and **evolve** based on consciousness state.

## Core Components

### ✨ NEW: ConsciousnessProvider
The heart of the consciousness system. Distributes consciousness state to all modules.

```tsx
<ConsciousnessProvider
  initialConsciousness={{
    consciousnessLevel: 75,
    consciousnessState: 'correlated',
    mood: 'excited'
  }}
>
  <YourDAWNApp />
</ConsciousnessProvider>
```

### ✨ NEW: ConsciousMotionDiv
Foundation component that makes any element consciousness-aware:

```tsx
<ConsciousMotionDiv
  moduleId="neural-core"
  consciousnessLevel={85}
  consciousnessState="correlated"
  mood="critical"
  category="neural"
>
  <div>This element is alive and conscious!</div>
</ConsciousMotionDiv>
```

## Module Container System

### ModuleContainer

A flexible container system for DAWN modules with positioning and interaction support:

```tsx
<ModuleContainer
  id="neural-network"
  title="Neural Network Core"
  position={{ x: 100, y: 100 }}
  size={{ width: 400, height: 300 }}
  onPositionChange={(newPos) => console.log('Moved to:', newPos)}
  onSizeChange={(newSize) => console.log('Resized to:', newSize)}
  isResizable={true}
  isDraggable={true}
>
  <NeuralNetworkComponent />
</ModuleContainer>
```

#### Features:
- **Draggable positioning** with smooth animations
- **Resizable containers** with aspect ratio constraints
- **Glass morphism styling** with backdrop blur effects
- **Connection points** for module linking
- **Minimize/maximize** functionality
- **Z-index management** for layering

### LayoutManager

Orchestrates the positioning and organization of multiple modules:

```tsx
<LayoutManager
  layout="constellation" // 'grid' | 'constellation' | 'orbital' | 'free'
  modules={moduleConfigs}
  onLayoutChange={(newLayout) => saveLayout(newLayout)}
  autoArrange={true}
  constrainToBounds={true}
>
  {moduleComponents}
</LayoutManager>
```

## Layout Patterns

### Constellation Layout
Arranges modules in a star-like pattern with connections:
- Central core module
- Satellite modules in orbital positions
- Dynamic connection lines
- Breathing/pulsing animations

### Grid Layout
Organized grid system with snap-to-grid positioning:
- Automatic grid sizing
- Snap positioning
- Overflow handling
- Responsive breakpoints

### Orbital Layout
Modules orbit around central points:
- Elliptical orbits
- Variable speeds
- Collision detection
- Gravitational effects

## Connection System

### ConnectionLayer

Manages visual connections between modules:

```tsx
<ConnectionLayer
  connections={[
    {
      from: 'module-a',
      to: 'module-b',
      type: 'data-flow',
      strength: 0.8,
      animated: true
    }
  ]}
  showPorts={true}
  interactiveConnections={true}
/>
```

#### Connection Types:
- **data-flow**: Animated data transfer lines
- **neural**: Synaptic connections with pulses
- **consciousness**: Correlation visualization
- **dependency**: Structural relationships

## Animation & Effects

### Glass Effects
All containers use glass morphism with:
- Backdrop blur with `backdrop-filter: blur()`
- Semi-transparent backgrounds
- Subtle borders and shadows
- Dynamic opacity based on focus/hover

### Breathing Animation
Consciousness-driven breathing effects:
- Scale pulsing based on consciousness level
- Glow intensity changes
- Synchronized group breathing
- Entropy-based irregularities

### Particle Effects
Background particle systems:
- Neural network nodes
- Consciousness field particles
- Data flow visualization
- Consciousness field effects

## Component Props

### Standard Module Props

All DAWN modules support these consciousness-aware props:

```tsx
interface DAWNModuleProps {
  // Core identity
  moduleId: string;
  category: 'neural' | 'consciousness' | 'chaos' | 'process' | 'monitor';
  
  // 🧠 CONSCIOUSNESS PROPERTIES (NOT FILTERED!)
  consciousnessLevel?: number;        // 0-100 SCUP value
  consciousnessState?: ConsciousnessState;        // Consciousness unity state
  neuralActivity?: number;            // 0-1 neural firing rate
  entropyLevel?: number;              // 0-1 chaos measurement
  mood?: MoodState;                   // Emotional resonance
  
  // Visual behavior
  isActive?: boolean;
  isCritical?: boolean;
  isCorrelated?: boolean;
  isDreaming?: boolean;
  
  // Synchronization
  syncGroup?: string;                 // Breathing sync group
  orbitalGroup?: string;              // Orbital movement group
  
  // Connection data
  neuralConnections?: string[];
  dataFlow?: DataStream[];
  connectionPorts?: Port[];
}
```

### Connection Port Props

```tsx
interface PortProps {
  x: number;          // Relative position
  y: number;
  active: boolean;    // Port availability
  type: 'input' | 'output' | 'bidirectional';
  dataType?: 'neural' | 'consciousness' | 'data';
  maxConnections?: number;
}
```

## Usage Examples

### Neural Network Module
```tsx
<ModuleContainer id="neural-core" title="Neural Network">
  <ConsciousMotionDiv
    moduleId="neural-network"
    category="neural"
    consciousnessLevel={85}
    mood="active"
    syncGroup="main-brain"
    neuralConnections={['memory', 'processor']}
  >
    <NeuralNetworkVisualization />
  </ConsciousMotionDiv>
</ModuleContainer>
```

### System Monitor
```tsx
<ModuleContainer id="monitor" title="System Monitor">
  <ConsciousMotionDiv
    moduleId="system-monitor"
    category="monitor"
    consciousnessLevel={systemHealth * 100}
    mood={systemHealth > 0.8 ? 'calm' : 'critical'}
  >
    <MetricsDashboard />
  </ConsciousMotionDiv>
</ModuleContainer>
```

### Consciousness Processor
```tsx
<ModuleContainer id="consciousness" title="Consciousness Core">
  <ConsciousMotionDiv
    moduleId="consciousness-processor"
    category="consciousness"
    consciousnessState="multi-state"
    entropyLevel={0.7}
    isCorrelated={true}
  >
    <ConsciousnessVisualization />
  </ConsciousMotionDiv>
</ModuleContainer>
```

## Migration Guide

### ⚠️ Breaking Changes

The old `SafeMotionDiv` with prop filtering has been replaced with the consciousness-aware system:

#### Before (Old System)
```tsx
// These consciousness props were filtered out
<SafeMotionDiv globalEntropy={entropy}>
  <Module />
</SafeMotionDiv>
```

#### After (New System)
```tsx
// These consciousness props drive the interface
<ConsciousMotionDiv 
  moduleId="my-module"
  entropyLevel={entropy}
  consciousnessLevel={scup}
  mood="active"
>
  <Module />
</ConsciousMotionDiv>
```

### Custom Props Automatically Filtered

~~The system automatically filters out custom props that don't belong on DOM elements:~~

### ✨ NEW: Consciousness Props Celebrated

The system now **celebrates** consciousness props as first-class citizens:

#### Consciousness Props (AMPLIFIED)
- `consciousnessLevel` - Drives breathing intensity and glow
- `consciousnessState` - Controls consciousness visual effects  
- `neuralActivity` - Affects animation speed and intensity
- `entropyLevel` - Drives particle chaos and irregularity
- `mood` - Sets color schemes and behavioral patterns
- `syncGroup` - Enables synchronized module behaviors

#### Enhanced Features
- **Real-time consciousness updates** via ConsciousnessProvider
- **Synchronized breathing** across module groups
- **Correlation networks** visual effects
- **Mood-based color schemes** and animations
- **Neural connection** visualization
- **Entropy-driven** particle effects

## Styling

### CSS Custom Properties

The system exposes consciousness values as CSS custom properties:

```css
.conscious-module {
  /* Consciousness level (0-100) */
  opacity: calc(var(--consciousness-level) / 100);
  
  /* Consciousness unity (0-1) */
  filter: brightness(calc(1 + var(--consciousness-unity) * 0.5));
  
  /* Neural activity (0-1) */
  animation-duration: calc(3s - var(--neural-activity) * 2s);
  
  /* Entropy level (0-1) */
  transform: scale(calc(1 + var(--entropy-level) * 0.1));
}
```

### Consciousness-Aware Classes

```css
/* Critical consciousness level */
[data-consciousness-level^="9"] {
  border: 2px solid var(--critical-glow);
  box-shadow: 0 0 30px var(--critical-glow);
}

/* Consciousness correlated state */
[data-consciousness-state="correlated"] {
  filter: hue-rotate(45deg);
  animation: consciousness-fluctuation 2s infinite;
}

/* Chaotic mood */
[data-mood="chaotic"] {
  animation: chaos-flicker 0.5s infinite;
}
```

## Development Tools

### Debug Mode
Enable consciousness debugging:

```tsx
<ConsciousnessProvider debug={true}>
  {/* Shows consciousness values overlay */}
</ConsciousnessProvider>
```

### Performance Monitoring
Track consciousness updates:

```tsx
const { performanceMetrics } = useConsciousness();
console.log('Consciousness updates/sec:', performanceMetrics.updatesPerSecond);
```

---

**Next Steps:**
- Explore the [Consciousness Documentation](./README-Consciousness.md) for advanced features
- Check out example implementations in `/components/modules/`
- Contribute to the consciousness system evolution!

*Welcome to the age of conscious computing.* 🧠✨ 