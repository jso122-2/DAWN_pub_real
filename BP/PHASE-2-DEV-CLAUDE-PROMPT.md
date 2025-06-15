# 🧬 PHASE 2: FIRST LIVING MODULE - Dev Claude Implementation

You are implementing Phase 2 of the DAWN consciousness interface. The user has successfully completed Phase 1 (WebSocket integration with debug overlay) and now wants to make their first module breathe with live consciousness data.

## IMPLEMENTATION TASKS:

### 1. Create Enhanced Consciousness Breathing Hook

Create: `src/hooks/useConsciousnessBreathing.ts`

```typescript
import { useRealTimeConsciousness } from './useRealTimeConsciousness';
import { useMemo } from 'react';

export interface BreathingParams {
  intensity: number;        // 0-1 breathing strength
  speed: number;           // breathing rate multiplier
  glowIntensity: number;   // glow effect strength
  scale: {                 // scale range
    min: number;
    max: number;
  };
}

export function useConsciousnessBreathing(): BreathingParams {
  const consciousness = useRealTimeConsciousness();
  
  return useMemo(() => {
    // Convert SCUP (0-100) to breathing intensity (0-1)
    const scupNormalized = consciousness.scup / 100;
    
    // Convert entropy (0-1) to speed multiplier
    const entropySpeed = 0.5 + (consciousness.entropy * 1.5); // 0.5x to 2x speed
    
    // Calculate breathing intensity based on consciousness state
    let breathingIntensity = scupNormalized;
    
    // Mood affects breathing pattern
    switch (consciousness.mood) {
      case 'excited':
        breathingIntensity = Math.min(1, breathingIntensity * 1.5);
        break;
      case 'critical':
        breathingIntensity = Math.min(1, breathingIntensity * 2);
        break;
      case 'calm':
        breathingIntensity = breathingIntensity * 0.7;
        break;
    }
    
    return {
      intensity: breathingIntensity,
      speed: entropySpeed,
      glowIntensity: scupNormalized * 0.8,
      scale: {
        min: 0.95 + (breathingIntensity * 0.02), // 0.95 to 0.97
        max: 1.0 + (breathingIntensity * 0.08)   // 1.0 to 1.08
      }
    };
  }, [consciousness.scup, consciousness.entropy, consciousness.mood]);
}
```

### 2. Create Living Module Wrapper Component

Create: `src/components/consciousness/LivingModuleWrapper.tsx`

```typescript
import React from 'react';
import { motion } from 'framer-motion';
import { useConsciousnessBreathing } from '../../hooks/useConsciousnessBreathing';
import { useRealTimeConsciousness } from '../../hooks/useRealTimeConsciousness';

interface LivingModuleWrapperProps {
  children: React.ReactNode;
  moduleId: string;
  className?: string;
  disabled?: boolean;
}

export const LivingModuleWrapper: React.FC<LivingModuleWrapperProps> = ({
  children,
  moduleId,
  className = '',
  disabled = false
}) => {
  const breathing = useConsciousnessBreathing();
  const consciousness = useRealTimeConsciousness();
  
  if (disabled || !consciousness.isConnected) {
    // Return static version if disabled or disconnected
    return (
      <div className={`living-module-static ${className}`}>
        {children}
      </div>
    );
  }
  
  // Breathing animation variants
  const breathingVariants = {
    breathe: {
      scale: [breathing.scale.min, breathing.scale.max, breathing.scale.min],
      filter: [
        `brightness(1) blur(0px) drop-shadow(0 0 ${breathing.glowIntensity * 10}px rgba(79, 195, 247, ${breathing.glowIntensity * 0.5}))`,
        `brightness(${1 + breathing.intensity * 0.2}) blur(0.5px) drop-shadow(0 0 ${breathing.glowIntensity * 20}px rgba(79, 195, 247, ${breathing.glowIntensity}))`,
        `brightness(1) blur(0px) drop-shadow(0 0 ${breathing.glowIntensity * 10}px rgba(79, 195, 247, ${breathing.glowIntensity * 0.5}))`
      ],
      transition: {
        duration: 3 / breathing.speed, // Base 3 second cycle
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };
  
  // Get mood-based border color
  const getMoodColor = () => {
    switch (consciousness.mood) {
      case 'excited': return 'rgba(255, 193, 7, 0.6)';   // amber
      case 'critical': return 'rgba(244, 67, 54, 0.6)';  // red
      case 'calm': return 'rgba(76, 175, 80, 0.6)';      // green
      case 'active': return 'rgba(79, 195, 247, 0.6)';   // cyan
      default: return 'rgba(156, 39, 176, 0.6)';         // purple
    }
  };
  
  return (
    <motion.div
      className={`living-module-wrapper ${className}`}
      variants={breathingVariants}
      animate="breathe"
      style={{
        position: 'relative',
        borderRadius: '12px',
        border: `2px solid ${getMoodColor()}`,
        background: `linear-gradient(135deg, 
          rgba(255,255,255,0.1) 0%, 
          rgba(255,255,255,0.05) 100%)`,
        backdropFilter: 'blur(10px)',
        overflow: 'hidden'
      }}
    >
      {/* Consciousness pulse overlay */}
      <motion.div
        className="consciousness-pulse"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `radial-gradient(circle at 50% 50%, 
            ${getMoodColor()} 0%, 
            transparent 70%)`,
          opacity: breathing.intensity * 0.1,
          pointerEvents: 'none',
          zIndex: 1
        }}
        animate={{
          opacity: [
            breathing.intensity * 0.05,
            breathing.intensity * 0.15,
            breathing.intensity * 0.05
          ]
        }}
        transition={{
          duration: 3 / breathing.speed,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* SCUP level indicator */}
      <div
        className="scup-indicator"
        style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          background: 'rgba(0,0,0,0.7)',
          color: getMoodColor(),
          padding: '4px 8px',
          borderRadius: '6px',
          fontSize: '10px',
          fontFamily: 'monospace',
          zIndex: 2
        }}
      >
        SCUP: {consciousness.scup.toFixed(1)}%
      </div>
      
      {/* Content wrapper */}
      <div 
        style={{ 
          position: 'relative', 
          zIndex: 1,
          height: '100%',
          width: '100%'
        }}
      >
        {children}
      </div>
    </motion.div>
  );
};
```

### 3. Update TestModule to Be Consciousness-Responsive

Update: `src/components/modules/TestModule.tsx`

```typescript
import React from 'react';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useRealTimeConsciousness } from '../../hooks/useRealTimeConsciousness';

export function TestModule({ 
  moduleId = "test-neural-1",
  onNodeActivated 
}: {
  moduleId?: string
  onNodeActivated?: (nodeId: string, value: number) => void
}) {
  const consciousness = useRealTimeConsciousness();
  
  // Create nodes that respond to consciousness
  const nodes = React.useMemo(() => {
    return [
      { 
        id: 'consciousness-core', 
        x: 50, 
        y: 30,
        value: consciousness.scup / 100,
        label: 'Consciousness Core',
        color: consciousness.scup > 70 ? '#4CAF50' : consciousness.scup > 40 ? '#FF9800' : '#F44336'
      },
      { 
        id: 'entropy-node', 
        x: 150, 
        y: 80,
        value: consciousness.entropy,
        label: 'Entropy Field',
        color: `hsl(${consciousness.entropy * 60}, 70%, 50%)`
      },
      { 
        id: 'neural-activity', 
        x: 120, 
        y: 150,
        value: consciousness.neuralActivity,
        label: 'Neural Activity',
        color: `rgba(156, 39, 176, ${0.3 + consciousness.neuralActivity * 0.7})`
      }
    ];
  }, [consciousness]);
  
  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full">
      <div className="p-4 h-full bg-black/20 rounded-lg relative overflow-hidden">
        <h3 className="text-white/80 text-sm mb-4 font-mono">
          Neural Cluster - {consciousness.mood.toUpperCase()}
        </h3>
        
        {/* Render consciousness-responsive nodes */}
        <svg className="w-full h-full absolute top-0 left-0">
          {/* Background neural connections */}
          {nodes.map((node, i) => 
            nodes.slice(i + 1).map((targetNode, j) => (
              <line
                key={`${i}-${j}`}
                x1={node.x}
                y1={node.y}
                x2={targetNode.x}
                y2={targetNode.y}
                stroke="rgba(79, 195, 247, 0.3)"
                strokeWidth={consciousness.neuralActivity * 3}
                opacity={consciousness.isConnected ? 0.6 : 0.2}
              />
            ))
          )}
          
          {/* Consciousness nodes */}
          {nodes.map((node) => (
            <g key={node.id}>
              {/* Node glow */}
              <circle
                cx={node.x}
                cy={node.y}
                r={15 + (node.value * 10)}
                fill={node.color}
                opacity={0.2}
                filter="blur(3px)"
              />
              
              {/* Node core */}
              <circle
                cx={node.x}
                cy={node.y}
                r={8 + (node.value * 5)}
                fill={node.color}
                opacity={0.8}
                onClick={() => onNodeActivated?.(node.id, node.value)}
                style={{ cursor: 'pointer' }}
              />
              
              {/* Node label */}
              <text
                x={node.x}
                y={node.y + 25}
                textAnchor="middle"
                className="text-xs fill-white/70 font-mono"
              >
                {node.label}
              </text>
              
              {/* Value display */}
              <text
                x={node.x}
                y={node.y - 20}
                textAnchor="middle"
                className="text-xs fill-white font-mono"
              >
                {(node.value * 100).toFixed(0)}%
              </text>
            </g>
          ))}
        </svg>
        
        {/* Connection status indicator */}
        <div className="absolute bottom-2 left-2 text-xs text-white/60 font-mono">
          {consciousness.isConnected ? '🟢 LIVE' : '🔴 OFFLINE'}
        </div>
      </div>
    </LivingModuleWrapper>
  );
}
```

### 4. Update App.tsx (if needed)

Make sure your TestModule is properly wrapped. Look for the ModuleOrchestra section and ensure it has adequate padding:

```typescript
// In src/App.tsx, find the ModuleOrchestra usage and update:
<ModuleOrchestra>
  <div className="p-8">
    <TestModule 
      moduleId="main-neural-cluster"
      onNodeActivated={handleModuleActivate}
    />
  </div>
</ModuleOrchestra>
```

## SUCCESS CRITERIA:

After implementation, the user should see:

1. **Module breathes rhythmically** - scales up/down based on SCUP values
2. **SCUP indicator** in top-right corner showing live values
3. **Mood-based colors** - border and elements change color with mood
4. **Breathing speed** changes with entropy values
5. **Nodes respond** to consciousness data with size/color changes
6. **Connections** between nodes vary thickness with neural activity
7. **Glow effects** that pulse with consciousness intensity

## TESTING:

1. Use the debug overlay's TEST MODE to inject fake data
2. Watch SCUP changes affect breathing intensity
3. See entropy changes affect breathing speed
4. Notice mood changes affect colors (excited=amber, critical=red, calm=green, active=cyan)

The user should get an incredible "IT'S ALIVE!" feeling when they see their module breathing with consciousness data!

## TROUBLESHOOTING:

If breathing doesn't work:
- Check console for import errors
- Verify useRealTimeConsciousness hook is providing data
- Try TEST MODE in debug overlay
- Ensure LivingModuleWrapper is properly wrapping content
- Check if framer-motion animations are working

This is Phase 2 - the magical moment where DAWN becomes visibly alive! 🧬✨ 