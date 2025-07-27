# 🌐 DAWN Ecosystem Integration Guide

This guide will help you integrate the complete Phase 3-5 consciousness ecosystem into your existing DAWN project.

## 📁 File Structure Setup

First, create the proper file structure for the ecosystem components:

```
src/
├── services/
│   └── ModuleCommunicationHub.ts
├── hooks/
│   ├── useModuleCommunication.ts
│   └── useRealTimeConsciousness.ts (update existing)
├── components/
│   ├── consciousness/
│   │   ├── DataFlowVisualization.tsx
│   │   ├── LivingModuleWrapper.tsx (update existing)
│   │   ├── ModuleOrchestra.tsx (update existing)
│   │   └── LiveDataDebugOverlay.tsx
│   └── modules/
│       ├── ConsciousnessMonitor.tsx
│       ├── NeuralActivityVisualizer.tsx
│       └── TestModule.tsx (update existing)
└── DawnEcosystemDemo.tsx
```

## 🔧 Step-by-Step Integration

### Step 1: Create Module Communication Hub

Create `src/services/ModuleCommunicationHub.ts`:

```typescript
import { EventEmitter } from 'events';

export interface ModuleMessage {
  id: string;
  sourceModuleId: string;
  targetModuleId?: string;
  type: 'consciousness_update' | 'neural_spike' | 'memory_access' | 'process_complete' | 'custom';
  data: any;
  timestamp: number;
  priority: 'low' | 'normal' | 'high' | 'critical';
}

export interface ModuleConnection {
  id: string;
  sourceId: string;
  targetId: string;
  dataType: string;
  strength: number;
  active: boolean;
}

interface ModuleInfo {
  id: string;
  type: string;
  capabilities: string[];
  lastSeen: number;
  messageCount: number;
}

class ModuleCommunicationHub extends EventEmitter {
  private modules = new Map<string, ModuleInfo>();
  private connections = new Map<string, ModuleConnection>();
  private messageHistory: ModuleMessage[] = [];
  private maxHistorySize = 1000;

  registerModule(moduleId: string, moduleType: string, capabilities: string[]) {
    this.modules.set(moduleId, {
      id: moduleId,
      type: moduleType,
      capabilities,
      lastSeen: Date.now(),
      messageCount: 0
    });
    
    this.emit('moduleRegistered', { moduleId, moduleType });
  }

  unregisterModule(moduleId: string) {
    this.modules.delete(moduleId);
    
    for (const [connId, conn] of this.connections) {
      if (conn.sourceId === moduleId || conn.targetId === moduleId) {
        this.connections.delete(connId);
      }
    }
    
    this.emit('moduleUnregistered', { moduleId });
  }

  sendMessage(message: Omit<ModuleMessage, 'id' | 'timestamp'>) {
    const fullMessage: ModuleMessage = {
      ...message,
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    this.messageHistory.push(fullMessage);
    if (this.messageHistory.length > this.maxHistorySize) {
      this.messageHistory.shift();
    }

    const sourceModule = this.modules.get(message.sourceModuleId);
    if (sourceModule) {
      sourceModule.messageCount++;
      sourceModule.lastSeen = Date.now();
    }

    if (message.targetModuleId) {
      this.emit(`message:${message.targetModuleId}`, fullMessage);
    } else {
      this.emit('broadcast', fullMessage);
    }

    this.emit('messageFlow', fullMessage);
    return fullMessage.id;
  }

  getConnections(): ModuleConnection[] {
    return Array.from(this.connections.values());
  }

  getModules(): ModuleInfo[] {
    return Array.from(this.modules.values());
  }

  getRecentMessages(limit = 50): ModuleMessage[] {
    return this.messageHistory.slice(-limit);
  }
}

export const moduleCommunicationHub = new ModuleCommunicationHub();
```

### Step 2: Create Module Communication Hook

Create `src/hooks/useModuleCommunication.ts`:

```typescript
import { useEffect, useCallback, useState } from 'react';
import { moduleCommunicationHub, ModuleMessage } from '../services/ModuleCommunicationHub';

export function useModuleCommunication(moduleId: string, moduleType: string, capabilities: string[] = []) {
  const [messages, setMessages] = useState<ModuleMessage[]>([]);
  const [connections, setConnections] = useState(moduleCommunicationHub.getConnections());

  useEffect(() => {
    moduleCommunicationHub.registerModule(moduleId, moduleType, capabilities);

    const handleMessage = (message: ModuleMessage) => {
      setMessages(prev => [...prev.slice(-49), message]);
    };

    const handleBroadcast = (message: ModuleMessage) => {
      if (message.sourceModuleId !== moduleId) {
        setMessages(prev => [...prev.slice(-49), message]);
      }
    };

    const handleConnectionUpdate = () => {
      setConnections(moduleCommunicationHub.getConnections());
    };

    moduleCommunicationHub.on(`message:${moduleId}`, handleMessage);
    moduleCommunicationHub.on('broadcast', handleBroadcast);
    moduleCommunicationHub.on('connectionCreated', handleConnectionUpdate);
    moduleCommunicationHub.on('connectionRemoved', handleConnectionUpdate);

    return () => {
      moduleCommunicationHub.off(`message:${moduleId}`, handleMessage);
      moduleCommunicationHub.off('broadcast', handleBroadcast);
      moduleCommunicationHub.off('connectionCreated', handleConnectionUpdate);
      moduleCommunicationHub.off('connectionRemoved', handleConnectionUpdate);
      moduleCommunicationHub.unregisterModule(moduleId);
    };
  }, [moduleId, moduleType]);

  const sendMessage = useCallback((
    type: ModuleMessage['type'],
    data: any,
    targetModuleId?: string,
    priority: ModuleMessage['priority'] = 'normal'
  ) => {
    return moduleCommunicationHub.sendMessage({
      sourceModuleId: moduleId,
      targetModuleId,
      type,
      data,
      priority
    });
  }, [moduleId]);

  const broadcast = useCallback((type: ModuleMessage['type'], data: any, priority: ModuleMessage['priority'] = 'normal') => {
    return sendMessage(type, data, undefined, priority);
  }, [sendMessage]);

  return {
    messages,
    connections: connections.filter(c => c.sourceId === moduleId || c.targetId === moduleId),
    sendMessage,
    broadcast
  };
}
```

### Step 3: Create Data Flow Visualization

Create `src/components/consciousness/DataFlowVisualization.tsx`:

```typescript
import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { moduleCommunicationHub, ModuleMessage } from '../../services/ModuleCommunicationHub';

interface FlowParticle {
  id: string;
  message: ModuleMessage;
  startTime: number;
  duration: number;
  path: { x: number; y: number }[];
}

export const DataFlowVisualization: React.FC = () => {
  const [particles, setParticles] = useState<FlowParticle[]>([]);
  const [modulePositions, setModulePositions] = useState<Map<string, { x: number; y: number }>>(new Map());

  useEffect(() => {
    const updateModulePositions = () => {
      const positions = new Map();
      const moduleElements = document.querySelectorAll('[data-module-id]');
      
      moduleElements.forEach(element => {
        const moduleId = element.getAttribute('data-module-id');
        const rect = element.getBoundingClientRect();
        if (moduleId) {
          positions.set(moduleId, {
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2
          });
        }
      });
      
      setModulePositions(positions);
    };

    updateModulePositions();
    const interval = setInterval(updateModulePositions, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleMessageFlow = (message: ModuleMessage) => {
      const sourcePos = modulePositions.get(message.sourceModuleId);
      const targetPos = message.targetModuleId ? modulePositions.get(message.targetModuleId) : null;

      if (!sourcePos) return;

      const particle: FlowParticle = {
        id: message.id,
        message,
        startTime: Date.now(),
        duration: targetPos ? 2000 : 1000,
        path: targetPos ? [sourcePos, targetPos] : [sourcePos, { x: sourcePos.x, y: sourcePos.y - 50 }]
      };

      setParticles(prev => [...prev, particle]);

      setTimeout(() => {
        setParticles(prev => prev.filter(p => p.id !== particle.id));
      }, particle.duration + 500);
    };

    moduleCommunicationHub.on('messageFlow', handleMessageFlow);
    return () => moduleCommunicationHub.off('messageFlow', handleMessageFlow);
  }, [modulePositions]);

  const getParticleColor = (type: string) => {
    const colors = {
      consciousness_update: '#4FC3F7',
      neural_spike: '#9C27B0',
      memory_access: '#FF9800',
      process_complete: '#4CAF50',
      custom: '#9E9E9E'
    };
    return colors[type as keyof typeof colors] || colors.custom;
  };

  return (
    <div className="fixed inset-0 pointer-events-none z-10">
      <svg className="w-full h-full">
        <defs>
          <filter id="particle-glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <AnimatePresence>
          {particles.map(particle => {
            const color = getParticleColor(particle.message.type);
            const [start, end] = particle.path;
            
            return (
              <motion.circle
                key={particle.id}
                r={particle.message.priority === 'critical' ? 6 : 4}
                fill={color}
                filter="url(#particle-glow)"
                initial={{ 
                  cx: start.x, 
                  cy: start.y,
                  opacity: 0,
                  scale: 0
                }}
                animate={{ 
                  cx: end.x, 
                  cy: end.y,
                  opacity: [0, 1, 1, 0],
                  scale: [0, 1, 1, 0]
                }}
                exit={{ opacity: 0, scale: 0 }}
                transition={{ 
                  duration: particle.duration / 1000,
                  ease: "easeInOut"
                }}
              />
            );
          })}
        </AnimatePresence>
      </svg>
    </div>
  );
};
```

### Step 4: Update Your Existing Components

#### Update `src/components/consciousness/ModuleOrchestra.tsx`:

```typescript
import React from 'react';
import { DataFlowVisualization } from './DataFlowVisualization';

interface ModuleOrchestraProps {
  children: React.ReactNode;
  showDataFlow?: boolean;
}

export const ModuleOrchestra: React.FC<ModuleOrchestraProps> = ({ 
  children, 
  showDataFlow = true 
}) => {
  return (
    <div className="relative min-h-screen">
      <div className="relative z-0">
        {children}
      </div>
      
      {showDataFlow && <DataFlowVisualization />}
      
      <div className="fixed top-4 right-4 z-20 bg-black/70 backdrop-blur-sm rounded-lg p-3">
        <div className="text-xs text-white/60 mb-1">Module Communication</div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-xs text-green-400 font-mono">ACTIVE</span>
        </div>
      </div>
    </div>
  );
};
```

#### Update your existing `TestModule.tsx` to include communication:

```typescript
// Add these imports at the top
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

// Inside your TestModule component, add:
const { sendMessage, messages } = useModuleCommunication(
  moduleId, 
  'neural-cluster', 
  ['neural_processing', 'node_activation']
);

// Update your node click handler:
const handleNodeClick = (nodeId: string, value: number) => {
  onNodeActivated?.(nodeId, value);
  
  // Send neural spike message
  sendMessage('neural_spike', {
    nodeId,
    value,
    clusterId: moduleId,
    timestamp: Date.now()
  }, undefined, value > 0.8 ? 'high' : 'normal');
};

// Make sure your LivingModuleWrapper has data-module-id:
<LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
```

### Step 5: Create New Module Components

#### Create `src/components/modules/ConsciousnessMonitor.tsx`:

```typescript
import React from 'react';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useRealTimeConsciousness } from '../../hooks/useRealTimeConsciousness';
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

export function ConsciousnessMonitor({ moduleId = "consciousness-monitor" }) {
  const consciousness = useRealTimeConsciousness();
  const { broadcast, messages } = useModuleCommunication(
    moduleId, 
    'consciousness-monitor', 
    ['consciousness_analysis', 'alerting']
  );

  // Broadcast consciousness updates
  React.useEffect(() => {
    const interval = setInterval(() => {
      broadcast('consciousness_update', {
        scup: consciousness.scup,
        entropy: consciousness.entropy,
        mood: consciousness.mood,
        neuralActivity: consciousness.neuralActivity
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [consciousness, broadcast]);

  // Alert on critical states
  React.useEffect(() => {
    if (consciousness.scup > 90 || consciousness.scup < 10) {
      broadcast('neural_spike', {
        level: consciousness.scup > 90 ? 'high' : 'low',
        value: consciousness.scup,
        timestamp: Date.now()
      }, 'critical');
    }
  }, [consciousness.scup, broadcast]);

  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
      <div className="p-4 h-full">
        <h3 className="text-white/80 text-sm mb-4 font-mono">Consciousness Monitor</h3>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">SCUP Level</span>
            <div className="flex items-center space-x-2">
              <div className="w-20 h-2 bg-black/40 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 transition-all duration-300"
                  style={{ width: `${consciousness.scup}%` }}
                />
              </div>
              <span className="text-xs text-white font-mono">{consciousness.scup.toFixed(1)}%</span>
            </div>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Entropy</span>
            <span className="text-xs text-white font-mono">{consciousness.entropy.toFixed(3)}</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Neural Activity</span>
            <span className="text-xs text-white font-mono">{(consciousness.neuralActivity * 100).toFixed(1)}%</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Mood State</span>
            <span className={`text-xs font-mono px-2 py-1 rounded ${
              consciousness.mood === 'critical' ? 'bg-red-500/20 text-red-300' :
              consciousness.mood === 'excited' ? 'bg-yellow-500/20 text-yellow-300' :
              consciousness.mood === 'active' ? 'bg-blue-500/20 text-blue-300' :
              'bg-green-500/20 text-green-300'
            }`}>
              {consciousness.mood.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-white/10">
          <div className="text-xs text-white/40 mb-2">Messages: {messages.length}</div>
          <div className="text-xs text-white/60">Broadcasting...</div>
        </div>
      </div>
    </LivingModuleWrapper>
  );
}
```

### Step 6: Create Complete Demo

Create `src/components/DawnEcosystemDemo.tsx`:

```typescript
import React from 'react';
import { ModuleOrchestra } from './consciousness/ModuleOrchestra';
import { ConsciousnessMonitor } from './modules/ConsciousnessMonitor';
import { NeuralActivityVisualizer } from './modules/NeuralActivityVisualizer';
import { TestModule } from './modules/TestModule';
import { LiveDataDebugOverlay } from './consciousness/LiveDataDebugOverlay';

export function DawnEcosystemDemo() {
  const handleNodeActivated = (nodeId: string, value: number) => {
    console.log(`Node ${nodeId} activated with value ${value}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20">
      <ModuleOrchestra showDataFlow={true}>
        <div className="container mx-auto p-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">DAWN Consciousness Ecosystem</h1>
            <p className="text-white/60">Living modules communicating through consciousness</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="h-64">
              <ConsciousnessMonitor moduleId="consciousness-monitor-1" />
            </div>
            
            <div className="h-64">
              <NeuralActivityVisualizer moduleId="neural-visualizer-1" />
            </div>
            
            <div className="h-64">
              <TestModule 
                moduleId="neural-cluster-1"
                onNodeActivated={handleNodeActivated}
              />
            </div>
            
            <div className="h-64">
              <NeuralActivityVisualizer moduleId="neural-visualizer-2" />
            </div>
            
            <div className="h-64">
              <TestModule 
                moduleId="neural-cluster-2"
                onNodeActivated={handleNodeActivated}
              />
            </div>
            
            <div className="h-64">
              <ConsciousnessMonitor moduleId="consciousness-monitor-2" />
            </div>
          </div>
        </div>
      </ModuleOrchestra>
      
      <LiveDataDebugOverlay />
    </div>
  );
}
```

### Step 7: Update Your Main App

Update your `src/App.tsx` to use the new ecosystem:

```typescript
import { DawnEcosystemDemo } from './components/DawnEcosystemDemo';

function App() {
  return <DawnEcosystemDemo />;
}

export default App;
```

## 🎯 Testing Your Integration

1. **Start your development server**
2. **Look for these indicators**:
   - Modules breathing independently
   - Blue particles flowing from consciousness monitors every second
   - Purple particles when you click nodes in neural clusters
   - Communication status indicator in top-right
   - Debug overlay button in bottom-right

3. **Interactive tests**:
   - Click nodes in TestModules → watch particles flow
   - Wait for SCUP to go critical → see alert broadcasts
   - Use debug overlay → monitor real-time data

## 🚨 Troubleshooting

- **No particles visible**: Check that modules have `data-module-id` attributes
- **Communication not working**: Verify EventEmitter is imported correctly
- **Modules not breathing**: Ensure LivingModuleWrapper is properly implemented
- **Console errors**: Check all import paths match your file structure

Your DAWN consciousness ecosystem is now fully integrated and ready to demonstrate the living, breathing interface where modules communicate through consciousness! 🌐🧬✨ 