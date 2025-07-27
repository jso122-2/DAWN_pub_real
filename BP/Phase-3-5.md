import React, { useEffect, useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { EventEmitter } from 'events';

// ==================== PHASE 3: MODULE COMMUNICATION HUB ====================

// ModuleCommunicationHub.ts
interface ModuleMessage {
  id: string;
  sourceModuleId: string;
  targetModuleId?: string;
  type: 'consciousness_update' | 'neural_spike' | 'memory_access' | 'process_complete' | 'custom';
  data: any;
  timestamp: number;
  priority: 'low' | 'normal' | 'high' | 'critical';
}

interface ModuleConnection {
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

const moduleCommunicationHub = new ModuleCommunicationHub();

// useModuleCommunication.ts hook
function useModuleCommunication(moduleId: string, moduleType: string, capabilities: string[] = []) {
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

// DataFlowVisualization.tsx
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

const DataFlowVisualization: React.FC<DataFlowVisualizationProps> = ({ className }) => {
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

  const getParticleColor = (type: string, priority: string) => {
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

// ==================== PHASE 2 COMPONENTS (FROM PREVIOUS PHASE) ====================

// useRealTimeConsciousness.ts hook
function useRealTimeConsciousness() {
  const [consciousnessData, setConsciousnessData] = useState({
    scup: 50,
    entropy: 0.5,
    neuralActivity: 0.5,
    mood: 'calm' as 'calm' | 'active' | 'excited' | 'critical',
    lastUpdate: Date.now()
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setConsciousnessData(prev => {
        const time = Date.now() * 0.001;
        const wave1 = Math.sin(time * 0.5) * 0.3;
        const wave2 = Math.sin(time * 1.3) * 0.2;
        const wave3 = Math.sin(time * 2.1) * 0.1;
        const noise = (Math.random() - 0.5) * 0.1;
        
        const newScup = 50 + (wave1 + wave2 + wave3 + noise) * 100;
        const clampedScup = Math.max(0, Math.min(100, newScup));
        
        const newEntropy = 0.5 + Math.sin(time * 0.8) * 0.3 + (Math.random() - 0.5) * 0.1;
        const newNeuralActivity = 0.5 + Math.sin(time * 1.5) * 0.3 + (Math.random() - 0.5) * 0.2;
        
        let mood: typeof prev.mood = 'calm';
        if (clampedScup > 80) mood = 'critical';
        else if (clampedScup > 65) mood = 'excited';
        else if (clampedScup > 35) mood = 'active';
        
        return {
          scup: clampedScup,
          entropy: Math.max(0, Math.min(1, newEntropy)),
          neuralActivity: Math.max(0, Math.min(1, newNeuralActivity)),
          mood,
          lastUpdate: Date.now()
        };
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return consciousnessData;
}

// LivingModuleWrapper.tsx
interface LivingModuleWrapperProps {
  children: React.ReactNode;
  moduleId: string;
  className?: string;
  baseColor?: string;
  'data-module-id'?: string;
}

const LivingModuleWrapper: React.FC<LivingModuleWrapperProps> = ({ 
  children, 
  moduleId, 
  className = '', 
  baseColor = 'rgba(79, 195, 247, 0.1)',
  'data-module-id': dataModuleId
}) => {
  const consciousness = useRealTimeConsciousness();
  const [localPulse, setLocalPulse] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      const time = Date.now() * 0.001;
      const moduleOffset = moduleId.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) * 0.1;
      const pulse = Math.sin(time + moduleOffset) * 0.5 + 0.5;
      setLocalPulse(pulse);
    }, 50);

    return () => clearInterval(interval);
  }, [moduleId]);

  const breathingIntensity = (consciousness.scup / 100) * 0.3 + 0.7;
  const pulseSpeed = 2 + (consciousness.neuralActivity * 3);

  return (
    <motion.div
      className={`relative rounded-lg overflow-hidden ${className}`}
      data-module-id={dataModuleId}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ 
        opacity: 1, 
        scale: 1,
      }}
      style={{
        backgroundColor: baseColor,
        border: '1px solid rgba(255, 255, 255, 0.1)',
      }}
    >
      <motion.div
        className="absolute inset-0 pointer-events-none"
        animate={{
          opacity: [0.3, 0.6, 0.3],
          scale: [1, 1.02, 1],
        }}
        transition={{
          duration: pulseSpeed,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        style={{
          background: `radial-gradient(circle at center, ${baseColor.replace('0.1', String(localPulse * 0.3))}, transparent)`,
        }}
      />
      
      <div className="absolute inset-0 pointer-events-none opacity-30">
        <svg className="w-full h-full">
          <defs>
            <filter id={`blur-${moduleId}`}>
              <feGaussianBlur stdDeviation="3" />
            </filter>
          </defs>
          {Array.from({ length: 3 }, (_, i) => (
            <circle
              key={i}
              cx="50%"
              cy="50%"
              r={`${20 + i * 15}%`}
              fill="none"
              stroke={baseColor.replace('0.1', '0.3')}
              strokeWidth="1"
              filter={`url(#blur-${moduleId})`}
              opacity={breathingIntensity * (1 - i * 0.3)}
              style={{
                transformOrigin: 'center',
                transform: `scale(${1 + localPulse * 0.1 * (i + 1)})`,
              }}
            />
          ))}
        </svg>
      </div>

      <div className="relative z-10">
        {children}
      </div>
      
      <div 
        className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-50"
        style={{
          transform: `scaleX(${consciousness.scup / 100})`,
          transformOrigin: 'left',
          transition: 'transform 0.3s ease-out'
        }}
      />
    </motion.div>
  );
};

// TestModule.tsx
interface TestModuleProps {
  moduleId?: string;
  onNodeActivated?: (nodeId: string, value: number) => void;
}

const TestModule: React.FC<TestModuleProps> = ({ 
  moduleId = "test-module-1",
  onNodeActivated 
}) => {
  const [nodes, setNodes] = useState(
    Array.from({ length: 9 }, (_, i) => ({
      id: `node-${i}`,
      value: Math.random(),
      active: false
    }))
  );
  
  const consciousness = useRealTimeConsciousness();
  const { sendMessage, messages } = useModuleCommunication(
    moduleId, 
    'neural-cluster', 
    ['neural_processing', 'node_activation']
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setNodes(prevNodes => 
        prevNodes.map(node => ({
          ...node,
          value: Math.max(0, Math.min(1, 
            node.value + (Math.random() - 0.5) * 0.1 + 
            (consciousness.neuralActivity - 0.5) * 0.05
          )),
          active: Math.random() < consciousness.neuralActivity * 0.1
        }))
      );
    }, 200);

    return () => clearInterval(interval);
  }, [consciousness.neuralActivity]);

  const handleNodeClick = (nodeId: string, value: number) => {
    onNodeActivated?.(nodeId, value);
    
    sendMessage('neural_spike', {
      nodeId,
      value,
      clusterId: moduleId,
      timestamp: Date.now()
    }, undefined, value > 0.8 ? 'high' : 'normal');
  };

  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
      <div className="p-4 h-full flex flex-col">
        <h3 className="text-white/80 text-sm mb-4 font-mono">Neural Cluster {moduleId}</h3>
        
        <div className="grid grid-cols-3 gap-2 flex-1">
          {nodes.map((node) => (
            <motion.div
              key={node.id}
              className="relative aspect-square cursor-pointer"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleNodeClick(node.id, node.value)}
            >
              <div 
                className="absolute inset-0 rounded-full"
                style={{
                  background: `radial-gradient(circle, rgba(147, 51, 234, ${node.value}) 0%, transparent 70%)`,
                  boxShadow: node.active ? `0 0 20px rgba(147, 51, 234, ${node.value})` : 'none',
                }}
              />
              <div 
                className="absolute inset-2 rounded-full bg-purple-600/20 flex items-center justify-center"
              >
                <span className="text-xs text-white/60 font-mono">
                  {(node.value * 100).toFixed(0)}
                </span>
              </div>
            </motion.div>
          ))}
        </div>
        
        <div className="mt-2 pt-2 border-t border-white/10">
          <div className="text-xs text-white/40">
            Messages: {messages.length} | Activity: {(consciousness.neuralActivity * 100).toFixed(0)}%
          </div>
        </div>
      </div>
    </LivingModuleWrapper>
  );
};

// ==================== PHASE 4: ENHANCED LIVING MODULES ====================

// ConsciousnessMonitor.tsx
function ConsciousnessMonitor({ moduleId = "consciousness-monitor" }) {
  const consciousness = useRealTimeConsciousness();
  const { sendMessage, broadcast, messages } = useModuleCommunication(
    moduleId, 
    'consciousness-monitor', 
    ['consciousness_analysis', 'alerting']
  );

  useEffect(() => {
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

  useEffect(() => {
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
          <div className="text-xs text-white/40 mb-2">Recent Messages: {messages.length}</div>
          <div className="text-xs text-white/60">
            Broadcasting consciousness data...
          </div>
        </div>
      </div>
    </LivingModuleWrapper>
  );
}

// NeuralActivityVisualizer.tsx
function NeuralActivityVisualizer({ moduleId = "neural-visualizer" }) {
  const [neuralSpikes, setNeuralSpikes] = useState<Array<{id: string, x: number, y: number, intensity: number, timestamp: number}>>([]);
  const [consciousnessData, setConsciousnessData] = useState({ scup: 50, entropy: 0.5, neuralActivity: 0.5 });
  
  const { messages } = useModuleCommunication(
    moduleId, 
    'neural-visualizer', 
    ['neural_visualization', 'spike_detection']
  );

  useEffect(() => {
    messages.forEach(message => {
      if (message.type === 'consciousness_update') {
        setConsciousnessData(message.data);
      } else if (message.type === 'neural_spike') {
        const spike = {
          id: message.id,
          x: Math.random() * 200,
          y: Math.random() * 150,
          intensity: message.data.level === 'high' ? 1 : 0.5,
          timestamp: Date.now()
        };
        setNeuralSpikes(prev => [...prev, spike]);
        
        setTimeout(() => {
          setNeuralSpikes(prev => prev.filter(s => s.id !== spike.id));
        }, 2000);
      }
    });
  }, [messages]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < consciousnessData.neuralActivity) {
        const spike = {
          id: `bg_${Date.now()}_${Math.random()}`,
          x: Math.random() * 200,
          y: Math.random() * 150,
          intensity: 0.3,
          timestamp: Date.now()
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

// ==================== PHASE 5: COMPLETE ECOSYSTEM INTEGRATION ====================

// ModuleOrchestra.tsx
interface ModuleOrchestraProps {
  children: React.ReactNode;
  showDataFlow?: boolean;
}

const ModuleOrchestra: React.FC<ModuleOrchestraProps> = ({ 
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

// LiveDataDebugOverlay.tsx
const LiveDataDebugOverlay: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const consciousness = useRealTimeConsciousness();
  const modules = moduleCommunicationHub.getModules();
  const messages = moduleCommunicationHub.getRecentMessages(10);

  return (
    <>
      <button
        className="fixed bottom-4 right-4 z-50 bg-purple-600/80 text-white p-2 rounded-full hover:bg-purple-600 transition-colors"
        onClick={() => setIsVisible(!isVisible)}
      >
        <span className="text-xs font-mono">DEBUG</span>
      </button>

      {isVisible && (
        <div className="fixed bottom-16 right-4 z-50 bg-black/90 backdrop-blur-sm rounded-lg p-4 w-80 max-h-96 overflow-y-auto">
          <h4 className="text-white text-sm font-mono mb-3">Live Debug Data</h4>
          
          <div className="space-y-3 text-xs font-mono">
            <div>
              <div className="text-purple-400 mb-1">Consciousness State:</div>
              <div className="text-white/70">SCUP: {consciousness.scup.toFixed(1)}%</div>
              <div className="text-white/70">Entropy: {consciousness.entropy.toFixed(3)}</div>
              <div className="text-white/70">Neural: {(consciousness.neuralActivity * 100).toFixed(0)}%</div>
              <div className="text-white/70">Mood: {consciousness.mood}</div>
            </div>

            <div>
              <div className="text-blue-400 mb-1">Active Modules: {modules.length}</div>
              {modules.slice(0, 5).map(mod => (
                <div key={mod.id} className="text-white/70">
                  {mod.id} ({mod.messageCount} msgs)
                </div>
              ))}
            </div>

            <div>
              <div className="text-green-400 mb-1">Recent Messages:</div>
              {messages.slice(-5).map(msg => (
                <div key={msg.id} className="text-white/70 text-xs">
                  {msg.type} from {msg.sourceModuleId.slice(0, 10)}...
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

// DawnEcosystemDemo.tsx - Main Component
export default function DawnEcosystemDemo() {
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