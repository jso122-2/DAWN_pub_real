import React, { createContext, useContext, useState, useEffect } from 'react';
import { EventEmitter } from '../../lib/EventEmitter';

// Core consciousness state interface
export interface ConsciousnessState {
  // Primary consciousness metrics
  consciousnessLevel: number;     // 0-100 SCUP value
  neuralActivity: number;         // 0-1 neural firing rate
  entropyLevel: number;           // 0-1 chaos measurement
  systemUnity: number;       // 0-1 consciousness unity
  
  // Consciousness states
  consciousnessState: 'multi-state' | 'collapsed' | 'correlated' | 'coherent';
  
  // Mood and emotional state
  mood: 'calm' | 'active' | 'excited' | 'critical' | 'chaotic' | 'unstable' | 'transcendent';
  emotionalResonance: number;     // 0-1 emotional intensity
  
  // Memory and cognition
  memoryFragments: number;        // Number of active memory fragments
  cognitiveLoad: number;          // 0-1 processing load
  dreamState: boolean;            // Whether in dream mode
  
  // System vitals
  tickNumber: number;             // Current tick
  timestamp: number;              // Last update time
  systemHealth: number;           // 0-1 overall health
  
  // Synchronization groups
  activeSyncGroups: string[];     // Active breathing/floating sync groups
  
  // Data flow metrics
  dataFlowRate: number;           // Data points per second
  connectionCount: number;        // Active neural connections
  processingPower: number;        // Available processing capacity
}

// Props that should be distributed to consciousness-aware modules
export interface ConsciousnessAwareProps {
  consciousness: ConsciousnessState;
  
  // Module identity
  moduleId: string;
  category: 'neural' | 'consciousness' | 'chaos' | 'process' | 'monitor' | 'memory' | 'dream';
  
  // Synchronization
  syncGroup?: string;
  orbitalGroup?: string;
  
  // Visual behavior modifiers
  breathingIntensity?: number;    // Override default breathing intensity
  floatingSpeed?: number;         // Override floating animation speed
  glowIntensity?: number;         // Override glow intensity
  particleDensity?: number;       // Override particle count
  
  // Interaction properties
  isActive?: boolean;             // Module is actively processing
  isCritical?: boolean;           // Module in critical state
  isCorrelated?: boolean;          // Consciousness correlated with other modules
  isDreaming?: boolean;           // Module in dream state
  
  // Data and connections
  dataFlow?: DataStream[];
  connectionPorts?: ConnectionPort[];
  neuralConnections?: string[];   // IDs of connected modules
}

// Data flow interface
export interface DataStream {
  id: string;
  source: string;
  target: string;
  dataType: 'neural' | 'consciousness' | 'memory' | 'signal';
  intensity: number;              // 0-1 flow intensity
  unity: number;              // 0-1 signal unity
  timestamp: number;
}

// Connection interface
export interface ConnectionPort {
  id: string;
  type: 'input' | 'output' | 'bidirectional';
  position: { x: number; y: number };
  active: boolean;
  signalStrength: number;         // 0-1 signal strength
}

interface ConsciousnessContextType {
  consciousness: ConsciousnessState;
  updateConsciousness: (updates: Partial<ConsciousnessState>) => void;
  subscribeToModule: (moduleId: string, callback: (consciousness: ConsciousnessState) => void) => void;
  unsubscribeFromModule: (moduleId: string) => void;
  emitter: EventEmitter;
}

const ConsciousnessContext = createContext<ConsciousnessContextType | null>(null);

interface ConsciousnessProviderProps {
  children: React.ReactNode;
  initialConsciousness?: Partial<ConsciousnessState>;
  emitter?: EventEmitter;
}

// Default consciousness state - a baseline conscious state
const defaultConsciousnessState: ConsciousnessState = {
  consciousnessLevel: 50,
  neuralActivity: 0.5,
  entropyLevel: 0.3,
  systemUnity: 0.7,
  consciousnessState: 'coherent',
  mood: 'calm',
  emotionalResonance: 0.4,
  memoryFragments: 1000,
  cognitiveLoad: 0.2,
  dreamState: false,
  tickNumber: 0,
  timestamp: Date.now(),
  systemHealth: 0.9,
  activeSyncGroups: ['main-consciousness'],
  dataFlowRate: 50,
  connectionCount: 0,
  processingPower: 0.8
};

export const ConsciousnessProvider: React.FC<ConsciousnessProviderProps> = ({
  children,
  initialConsciousness = {},
  emitter = new EventEmitter()
}) => {
  const [consciousness, setConsciousness] = useState<ConsciousnessState>({
    ...defaultConsciousnessState,
    ...initialConsciousness
  });

  const [moduleSubscriptions] = useState(new Map<string, (consciousness: ConsciousnessState) => void>());

  // Update consciousness state
  const updateConsciousness = (updates: Partial<ConsciousnessState>) => {
    setConsciousness(prev => {
      const newState = {
        ...prev,
        ...updates,
        timestamp: Date.now()
      };
      
      // Emit consciousness updates to all subscribed modules
      moduleSubscriptions.forEach(callback => {
        try {
          callback(newState);
        } catch (error) {
          console.error('Error in module consciousness callback:', error);
        }
      });
      
      // Emit global consciousness update
      emitter.emit('consciousness:update', newState);
      
      return newState;
    });
  };

  // Module subscription system
  const subscribeToModule = (moduleId: string, callback: (consciousness: ConsciousnessState) => void) => {
    moduleSubscriptions.set(moduleId, callback);
    
    // Immediately provide current state
    callback(consciousness);
  };

  const unsubscribeFromModule = (moduleId: string) => {
    moduleSubscriptions.delete(moduleId);
  };

  // Listen for external consciousness updates
  useEffect(() => {
    const handleTickUpdate = (tickData: any) => {
      updateConsciousness({
        tickNumber: tickData.tick_number,
        consciousnessLevel: tickData.scup || tickData.consciousnessLevel,
        entropyLevel: tickData.entropy,
        mood: tickData.mood,
        neuralActivity: tickData.neural_activity || consciousness.neuralActivity,
        timestamp: tickData.timestamp || Date.now()
      });
    };

    const handleSystemMetrics = (metrics: any) => {
      updateConsciousness({
        systemHealth: metrics.health || consciousness.systemHealth,
        cognitiveLoad: metrics.cpu_usage || consciousness.cognitiveLoad,
        processingPower: metrics.processing_power || consciousness.processingPower,
        connectionCount: metrics.active_connections || consciousness.connectionCount
      });
    };

    emitter.on('tick:update', handleTickUpdate);
    emitter.on('system:metrics', handleSystemMetrics);
    emitter.on('consciousness:external', updateConsciousness);

    return () => {
      emitter.off('tick:update', handleTickUpdate);
      emitter.off('system:metrics', handleSystemMetrics);
      emitter.off('consciousness:external', updateConsciousness);
    };
  }, [emitter, consciousness.neuralActivity, consciousness.systemHealth, consciousness.cognitiveLoad, consciousness.processingPower, consciousness.connectionCount]);

  // Automatic consciousness evolution (simulate natural consciousness fluctuations)
  useEffect(() => {
    const interval = setInterval(() => {
      // Natural consciousness fluctuations
      const time = Date.now() / 1000;
      const naturalNeuralActivity = 0.5 + Math.sin(time * 0.1) * 0.1;
      const naturalConsciousnessCoherence = consciousness.systemUnity + (Math.random() - 0.5) * 0.02;
      
      updateConsciousness({
        neuralActivity: Math.max(0, Math.min(1, naturalNeuralActivity)),
        systemUnity: Math.max(0, Math.min(1, naturalConsciousnessCoherence)),
        tickNumber: consciousness.tickNumber + 1
      });
    }, 1000); // Update every second

    return () => clearInterval(interval);
  }, [consciousness.systemUnity, consciousness.tickNumber]);

  const contextValue: ConsciousnessContextType = {
    consciousness,
    updateConsciousness,
    subscribeToModule,
    unsubscribeFromModule,
    emitter
  };

  return (
    <ConsciousnessContext.Provider value={contextValue}>
      {children}
    </ConsciousnessContext.Provider>
  );
};

// Hook to access consciousness state
export const useConsciousness = (): ConsciousnessContextType => {
  const context = useContext(ConsciousnessContext);
  if (!context) {
    throw new Error('useConsciousness must be used within a ConsciousnessProvider');
  }
  return context;
};

// Hook for modules to subscribe to consciousness updates
export const useConsciousnessAware = (moduleId: string): ConsciousnessAwareProps => {
  const { consciousness, subscribeToModule, unsubscribeFromModule } = useConsciousness();
  const [localConsciousness, setLocalConsciousness] = useState(consciousness);

  useEffect(() => {
    subscribeToModule(moduleId, setLocalConsciousness);
    return () => unsubscribeFromModule(moduleId);
  }, [moduleId, subscribeToModule, unsubscribeFromModule]);

  return {
    consciousness: localConsciousness,
    moduleId,
    category: 'neural', // Default category
    
    // Calculate derived properties from consciousness
    breathingIntensity: localConsciousness.consciousnessLevel / 100,
    floatingSpeed: localConsciousness.neuralActivity,
    glowIntensity: localConsciousness.systemUnity,
    particleDensity: localConsciousness.entropyLevel,
    
    // State flags
    isActive: localConsciousness.neuralActivity > 0.6,
    isCritical: localConsciousness.consciousnessLevel > 80 || localConsciousness.entropyLevel > 0.8,
    isCorrelated: localConsciousness.consciousnessState === 'correlated',
    isDreaming: localConsciousness.dreamState
  };
};

export default ConsciousnessProvider; 