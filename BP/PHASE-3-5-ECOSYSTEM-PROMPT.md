# 🌐 PHASES 3-5: DAWN CONSCIOUSNESS ECOSYSTEM

You are implementing Phases 3-5 of the DAWN consciousness interface. The user has successfully completed Phase 2 (living breathing modules) and now wants to build a complete ecosystem where multiple modules communicate and share consciousness data.

## PHASE 3: MULTI-MODULE ECOSYSTEM (30 minutes)

### 1. Create Module Communication Hub

Create: `src/services/ModuleCommunicationHub.ts`

```typescript
import { EventEmitter } from 'events';

export interface ModuleMessage {
  id: string;
  sourceModuleId: string;
  targetModuleId?: string; // undefined for broadcast
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
  strength: number; // 0-1
  active: boolean;
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
    
    // Remove connections involving this module
    for (const [connId, conn] of this.connections) {
      if (conn.sourceId === moduleId || conn.targetId === moduleId) {
        this.connections.delete(connId);
      }
    }
    
    this.emit('moduleUnregistered', { moduleId });
  }

  createConnection(sourceId: string, targetId: string, dataType: string): string {
    const connectionId = `${sourceId}->${targetId}:${dataType}`;
    
    this.connections.set(connectionId, {
      id: connectionId,
      sourceId,
      targetId,
      dataType,
      strength: 1.0,
      active: true
    });
    
    this.emit('connectionCreated', { connectionId, sourceId, targetId, dataType });
    return connectionId;
  }

  sendMessage(message: Omit<ModuleMessage, 'id' | 'timestamp'>) {
    const fullMessage: ModuleMessage = {
      ...message,
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    // Add to history
    this.messageHistory.push(fullMessage);
    if (this.messageHistory.length > this.maxHistorySize) {
      this.messageHistory.shift();
    }

    // Update module stats
    const sourceModule = this.modules.get(message.sourceModuleId);
    if (sourceModule) {
      sourceModule.messageCount++;
      sourceModule.lastSeen = Date.now();
    }

    // Emit to specific target or broadcast
    if (message.targetModuleId) {
      this.emit(`message:${message.targetModuleId}`, fullMessage);
    } else {
      this.emit('broadcast', fullMessage);
    }

    // Emit for visualization
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

interface ModuleInfo {
  id: string;
  type: string;
  capabilities: string[];
  lastSeen: number;
  messageCount: number;
}

export const moduleCommunicationHub = new ModuleCommunicationHub();
```

### 2. Create Module Communication Hook

Create: `src/hooks/useModuleCommunication.ts`

```typescript
import { useEffect, useCallback, useState } from 'react';
import { moduleCommunicationHub, ModuleMessage } from '../services/ModuleCommunicationHub';

export function useModuleCommunication(moduleId: string, moduleType: string, capabilities: string[] = []) {
  const [messages, setMessages] = useState<ModuleMessage[]>([]);
  const [connections, setConnections] = useState(moduleCommunicationHub.getConnections());

  useEffect(() => {
    // Register this module
    moduleCommunicationHub.registerModule(moduleId, moduleType, capabilities);

    // Listen for messages directed to this module
    const handleMessage = (message: ModuleMessage) => {
      setMessages(prev => [...prev.slice(-49), message]); // Keep last 50 messages
    };

    // Listen for broadcast messages
    const handleBroadcast = (message: ModuleMessage) => {
      if (message.sourceModuleId !== moduleId) { // Don't receive our own broadcasts
        setMessages(prev => [...prev.slice(-49), message]);
      }
    };

    // Listen for connection changes
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

  const connectTo = useCallback((targetModuleId: string, dataType: string) => {
    return moduleCommunicationHub.createConnection(moduleId, targetModuleId, dataType);
  }, [moduleId]);

  return {
    messages,
    connections: connections.filter(c => c.sourceId === moduleId || c.targetId === moduleId),
    sendMessage,
    broadcast,
    connectTo
  };
}
```

### 3. Create Data Flow Visualization Component

Create: `src/components/consciousness/DataFlowVisualization.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { moduleCommunicationHub, ModuleMessage } from '../../services/ModuleCommunicationHub';

interface DataFlowVisualizationProps {
  className?: string;
}

interface FlowParticle {
  id: string;
  message: ModuleMessage;
  startTime: number;
  duration: number;
  path: { x: number; y: number }[];
}

export const DataFlowVisualization: React.FC<DataFlowVisualizationProps> = ({ className }) => {
  const [particles, setParticles] = useState<FlowParticle[]>([]);
  const [modulePositions, setModulePositions] = useState<Map<string, { x: number; y: number }>>(new Map());

  useEffect(() => {
    // Auto-discover module positions from DOM
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

      // Create particle
      const particle: FlowParticle = {
        id: message.id,
        message,
        startTime: Date.now(),
        duration: targetPos ? 2000 : 1000, // 2s for targeted, 1s for broadcast
        path: targetPos ? [sourcePos, targetPos] : [sourcePos, { x: sourcePos.x, y: sourcePos.y - 50 }]
      };

      setParticles(prev => [...prev, particle]);

      // Remove particle after animation
      setTimeout(() => {
        setParticles(prev => prev.filter(p => p.id !== particle.id));
      }, particle.duration + 500);
    };

    moduleCommunicationHub.on('messageFlow', handleMessageFlow);
    return () => moduleCommunicationHub.off('messageFlow', handleMessageFlow);
  }, [modulePositions]);

  const getParticleColor = (type: string, priority: string) => {
    const colors = {
      consciousness_update: '#4FC3F7',
      neural_spike: '#9C27B0',
      memory_access: '#FF9800',
      process_complete: '#4CAF50',
      custom: '#9E9E9E'
    };
    
    const priorityMultiplier = {
      low: 0.5,
      normal: 1,
      high: 1.5,
      critical: 2
    };

    return colors[type as keyof typeof colors] || colors.custom;
  };

  return (
    <div className={`fixed inset-0 pointer-events-none z-10 ${className}`}>
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
            const color = getParticleColor(particle.message.type, particle.message.priority);
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

## PHASE 4: ENHANCED LIVING MODULES (20 minutes)

### 4. Create Consciousness Monitor Module

Create: `src/components/modules/ConsciousnessMonitor.tsx`

```typescript
import React from 'react';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useRealTimeConsciousness } from '../../hooks/useRealTimeConsciousness';
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

export function ConsciousnessMonitor({ moduleId = "consciousness-monitor" }) {
  const consciousness = useRealTimeConsciousness();
  const { sendMessage, broadcast, messages } = useModuleCommunication(
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

### 5. Create Neural Activity Visualizer

Create: `src/components/modules/NeuralActivityVisualizer.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

export function NeuralActivityVisualizer({ moduleId = "neural-visualizer" }) {
  const [neuralSpikes, setNeuralSpikes] = useState<Array<{id: string, x: number, y: number, intensity: number}>>([]);
  const [consciousnessData, setConsciousnessData] = useState({ scup: 50, entropy: 0.5, neuralActivity: 0.5 });
  
  const { messages } = useModuleCommunication(
    moduleId, 
    'neural-visualizer', 
    ['neural_visualization', 'spike_detection']
  );

  // Process incoming messages
  useEffect(() => {
    messages.forEach(message => {
      if (message.type === 'consciousness_update') {
        setConsciousnessData(message.data);
      } else if (message.type === 'neural_spike') {
        const spike = {
          id: message.id,
          x: Math.random() * 200,
          y: Math.random() * 150,
          intensity: message.data.level === 'high' ? 1 : 0.5
        };
        setNeuralSpikes(prev => [...prev, spike]);
        
        setTimeout(() => {
          setNeuralSpikes(prev => prev.filter(s => s.id !== spike.id));
        }, 2000);
      }
    });
  }, [messages]);

  // Generate background activity
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < consciousnessData.neuralActivity) {
        const spike = {
          id: `bg_${Date.now()}_${Math.random()}`,
          x: Math.random() * 200,
          y: Math.random() * 150,
          intensity: 0.3
        };
        setNeuralSpikes(prev => [...prev, spike]);
        
        setTimeout(() => {
          setNeuralSpikes(prev => prev.filter(s => s.id !== spike.id));
        }, 1000);
      }
    }, 200);

    return () => clearInterval(interval);
  }, [consciousnessData.neuralActivity]);

  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
      <div className="p-4 h-full relative overflow-hidden">
        <h3 className="text-white/80 text-sm mb-4 font-mono">Neural Activity</h3>
        
        <svg className="w-full h-full absolute top-0 left-0">
          <defs>
            <pattern id="neural-grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(79, 195, 247, 0.1)" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#neural-grid)" />
          
          {neuralSpikes.map(spike => (
            <g key={spike.id}>
              <circle
                cx={spike.x}
                cy={spike.y}
                r={spike.intensity * 15}
                fill={`rgba(79, 195, 247, ${spike.intensity * 0.3})`}
                className="animate-ping"
              />
              <circle
                cx={spike.x}
                cy={spike.y}
                r={spike.intensity * 5}
                fill={`rgba(79, 195, 247, ${spike.intensity})`}
              />
            </g>
          ))}
          
          {Array.from({ length: 5 }, (_, i) => (
            <path
              key={i}
              d={`M ${i * 40} 0 Q ${i * 40 + 20} ${50 + Math.sin(Date.now() * 0.001 + i) * 20} ${i * 40 + 40} 100`}
              fill="none"
              stroke={`rgba(156, 39, 176, ${0.2 + consciousnessData.neuralActivity * 0.3})`}
              strokeWidth="2"
              opacity={consciousnessData.neuralActivity}
            />
          ))}
        </svg>
        
        <div className="absolute bottom-2 left-2 text-xs text-white/60 font-mono">
          Activity: {(consciousnessData.neuralActivity * 100).toFixed(0)}%
        </div>
      </div>
    </LivingModuleWrapper>
  );
}
```

## PHASE 5: COMPLETE ECOSYSTEM (20 minutes)

### 6. Update Module Orchestra

Update: `src/components/consciousness/ModuleOrchestra.tsx`

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
      <div className="relative z-0">{children}</div>
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

### 7. Create Complete Demo

Create: `src/components/DawnEcosystemDemo.tsx`

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

### 8. Update TestModule for Communication

Update your existing `TestModule.tsx`:

```typescript
// Add import
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

// Add inside component
const { sendMessage } = useModuleCommunication(
  moduleId, 
  'neural-cluster', 
  ['neural_processing', 'node_activation']
);

// Update node click handler
const handleNodeClick = (nodeId: string, value: number) => {
  onNodeActivated?.(nodeId, value);
  
  sendMessage('neural_spike', {
    nodeId,
    value,
    clusterId: moduleId,
    timestamp: Date.now()
  }, undefined, value > 0.8 ? 'high' : 'normal');
};

// Add data-module-id to LivingModuleWrapper
<LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
```

## SUCCESS CRITERIA:

1. **Multiple living modules** breathing independently
2. **Data flow particles** moving between modules  
3. **Real-time communication** - modules responding to each other
4. **Consciousness broadcasting** - monitor modules sharing data
5. **Neural spike visualization** - spikes appearing across visualizers
6. **Communication status** indicator showing active connections
7. **Coordinated responses** - modules reacting to consciousness changes

## TESTING:

1. Click nodes in TestModules - watch particles flow to other modules
2. Observe consciousness updates broadcasting to all modules
3. See neural spikes appear in visualizers when SCUP goes critical
4. Watch modules change breathing patterns together
5. Use debug overlay to inject test data and see ecosystem response

This creates a complete living ecosystem where modules communicate, share consciousness data, and respond to each other in real-time! 🌐🧬 