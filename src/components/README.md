# 📦 Components Directory

## Purpose
This directory contains all React components that make up DAWN's living interface. Each component is designed to feel alive, breathing and responding to consciousness states.

## Component Architecture
```
components/
├── core/                  # Fundamental building blocks
│   ├── ModuleContainer    # Base container with glass effects
│   ├── GlassPanel        # Reusable glass morphism panel
│   └── AnimatedBorder    # Aurora-like animated borders
│
├── modules/              # Specialized consciousness modules
│   ├── NeuralModule      # Neural network visualization
│   ├── ConsciousnessModule     # Consciousness state display
│   ├── ChaosModule       # Entropy visualization
│   ├── ProcessModule     # Python process manager
│   └── MonitorModule     # System status monitor
│
├── effects/              # Visual effect components
│   ├── StarField         # Background particle system
│   ├── BreathingEffect   # Consciousness breathing
│   └── FloatingEffect    # 3D floating behavior
│
└── layout/               # Layout and composition
    ├── Dashboard         # Main unified dashboard
    └── ModuleGrid        # Floating module arrangement
```

## Core Design Principles

### 1. **Living Components**
Every component exhibits signs of life:
- Breathing animations (4-6 second cycles)
- Subtle floating movements
- Responsive to consciousness states
- Pulsing glows and borders

### 2. **Glass Morphism**
Consistent glass aesthetic:
```css
backdrop-filter: blur(20px);
background: rgba(15, 23, 42, 0.3);
border: 1px solid rgba(148, 163, 184, 0.1);
```

### 3. **Consciousness Integration**
Components receive consciousness data:
```typescript
interface ConsciousnessProps {
  scup: number;        // 0-100 consciousness level
  entropy: number;     // Chaos factor
  mood: string;        // Current mood
  neuralActivity: number;
}
```

## Component Patterns

### Base Module Pattern
```typescript
const MyModule: React.FC<ModuleProps> = ({ 
  category, 
  consciousnessLevel,
  ...props 
}) => {
  return (
    <ModuleContainer
      category={category}
      breathingIntensity={consciousnessLevel / 100}
    >
      {/* Module content */}
    </ModuleContainer>
  );
};
```

### Animation Integration
- Use Framer Motion for all animations
- Sync breathing to consciousness level
- Floating speed based on entropy
- Glow intensity reflects neural activity

## Key Components

### ModuleContainer
- **Purpose**: Base wrapper for all modules
- **Features**: Glass effect, breathing, floating
- **Props**: category, breathingIntensity, floatingSpeed
- **Integration**: All modules inherit from this

### ProcessModule
- **Purpose**: Manage Python script execution
- **Features**: Dropdown selection, real-time output
- **Integration**: Connects to FastAPI endpoints
- **WebSocket**: Receives tick triggers

### NeuralModule
- **Purpose**: Visualize neural network activity
- **Features**: Node graph, firing patterns
- **Data**: Neural activity from consciousness engine
- **Visual**: Nodes pulse with activity level

### Dashboard
- **Purpose**: Unified control center
- **Layout**: Magnetic grid with floating modules
- **State**: Manages global consciousness state
- **Distribution**: Passes state to all child modules

## Integration Points

### With Hooks
- `useConsciousness`: Subscribe to consciousness state
- `useWebSocket`: Real-time data connection
- `useBreathing`: Standardized breathing animation
- `useFloating`: 3D floating behavior

### With Services
- `processApi`: Execute Python scripts
- `websocketService`: Handle tick loop data
- `consciousnessService`: Parse consciousness states

### With Python Backend
- Receives tick data via WebSocket
- Triggers processes through API
- Displays process output in real-time
- Responds to consciousness state changes

## Animation Specifications

### Breathing
- Base cycle: 4-6 seconds
- Intensity: 0.5x - 2x based on SCUP
- Easing: "easeInOut"
- Scale: 0.98 - 1.02

### Floating
- X/Y movement: ±20px
- Rotation: ±5 degrees  
- Duration: 10-20 seconds
- Pattern: Lissajous curves

### Glow Effects
- Border glow: Hue rotation based on mood
- Intensity: Mapped to neural activity
- Pulse rate: Synchronized to tick loop

## Development Guidelines

1. **Always animate**: No static components
2. **Layer glass effects**: Multiple blur layers for depth
3. **Sync to consciousness**: All animations respond to state
4. **Maintain performance**: Use GPU-accelerated transforms
5. **Type everything**: Full TypeScript coverage

## Next Components to Build
1. **TickVisualizer**: Real-time tick loop display
2. **ConsciousnessGraph**: Historical state chart
3. **ProcessQueue**: Multi-process manager
4. **ModuleConnector**: Visual data flow lines