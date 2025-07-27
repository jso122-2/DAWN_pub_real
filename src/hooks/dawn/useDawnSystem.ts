// Dawn Neural Monitor - System Hooks
// Phase 3: Dawn-Specific Scaffolding

import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { 
  CursorState, 
  ConsciousnessEvent, 
  EntropyMonitor, 
  SemanticCoordinate, 
  KANTopology,
  SplineNeuron,
  ConsciousnessField,
  SemanticSpace
} from '../../types/dawn';

// === DAWN SYSTEM HOOK ===

export interface DawnSystemConfig {
  initialCursorPosition?: SemanticCoordinate;
  consciousnessMode?: 'analytical' | 'creative' | 'intuitive' | 'transcendent';
  entropyRegulation?: {
    globalSetpoint: number;
    regulationMode: 'automatic' | 'manual' | 'consciousness_mediated';
  };
  kanTopology?: {
    neuronCount: number;
    layerDepth: number;
    connectionDensity: number;
  };
}

export const useDawnSystem = (config: DawnSystemConfig = {}) => {
  const [cursorState, setCursorState] = useState<CursorState | null>(null);
  const [entropyMonitor, setEntropyMonitor] = useState<EntropyMonitor | null>(null);
  const [kanTopology, setKanTopology] = useState<KANTopology | null>(null);
  const [consciousnessField, setConsciousnessField] = useState<ConsciousnessField | null>(null);
  
  const consciousnessStreamRef = useRef<ReadableStream<ConsciousnessEvent> | null>(null);
  const eventQueueRef = useRef<ConsciousnessEvent[]>([]);

  // Initialize Dawn system
  useEffect(() => {
    const initializeDawnSystem = () => {
      // Initialize cursor state
      const initialCursor: CursorState = {
        position: config.initialCursorPosition || {
          x: 0, y: 0, z: 0,
          semantic_weight: 1.0,
          ontological_depth: 0.5,
          consciousness_level: 0.7
        },
        trajectory: {
          direction: { x: 0, y: 0, z: 0, semantic_weight: 0, ontological_depth: 0, consciousness_level: 0 },
          velocity: 0,
          acceleration: 0,
          semantic_momentum: 0,
          intention_strength: 0.5
        },
        activeSplines: [],
        entropy: 0.3,
        consciousness_mode: config.consciousnessMode || 'analytical',
        temporal_anchor: Date.now(),
        semantic_resonance: 0.5
      };
      setCursorState(initialCursor);

      // Initialize entropy monitor
      const initialEntropy: EntropyMonitor = {
        global_entropy: config.entropyRegulation?.globalSetpoint || 0.3,
        local_entropies: new Map(),
        entropy_flows: [],
        consciousness_entropy_ratio: 0.7,
        semantic_entropy_distribution: [0.1, 0.2, 0.3, 0.2, 0.2]
      };
      setEntropyMonitor(initialEntropy);

      // Initialize consciousness field
      const initialConsciousness: ConsciousnessField = {
        intensity: 0.5,
        coherence: 0.8,
        entropy_distribution: [0.1, 0.2, 0.4, 0.2, 0.1],
        semantic_density: 0.6,
        temporal_stability: 0.7,
        observer_effect: 0.3
      };
      setConsciousnessField(initialConsciousness);

      // Initialize consciousness stream
      consciousnessStreamRef.current = new ReadableStream({
        start(controller) {
          // Stream setup for consciousness events
        },
        pull(controller) {
          // Process queued events
          if (eventQueueRef.current.length > 0) {
            const event = eventQueueRef.current.shift();
            if (event) {
              controller.enqueue(event);
            }
          }
        }
      });
    };

    initializeDawnSystem();
  }, [config]);

  // Update cursor position
  const updateCursorPosition = useCallback((position: SemanticCoordinate) => {
    setCursorState(prev => {
      if (!prev) return null;
      
      // Calculate trajectory
      const newTrajectory = {
        ...prev.trajectory,
        direction: {
          x: position.x - prev.position.x,
          y: position.y - prev.position.y,
          z: position.z - prev.position.z,
          semantic_weight: position.semantic_weight - prev.position.semantic_weight,
          ontological_depth: position.ontological_depth - prev.position.ontological_depth,
          consciousness_level: position.consciousness_level - prev.position.consciousness_level
        }
      };

      return {
        ...prev,
        position,
        trajectory: newTrajectory,
        temporal_anchor: Date.now()
      };
    });
  }, []);

  // Trigger consciousness event
  const triggerConsciousnessEvent = useCallback((event: Omit<ConsciousnessEvent, 'id' | 'timestamp'>) => {
    const fullEvent: ConsciousnessEvent = {
      ...event,
      id: `consciousness_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };
    
    eventQueueRef.current.push(fullEvent);
    
    // Update consciousness field based on event
    setConsciousnessField(prev => {
      if (!prev) return prev;
      
      return {
        ...prev,
        intensity: Math.max(0, Math.min(1, prev.intensity + fullEvent.consciousness_delta)),
        coherence: Math.max(0, Math.min(1, prev.coherence + fullEvent.consciousness_delta * 0.1))
      };
    });
  }, []);

  // Adjust entropy
  const adjustEntropy = useCallback((neuronId: string, delta: number) => {
    setEntropyMonitor(prev => {
      if (!prev) return prev;
      
      const newLocalEntropies = new Map(prev.local_entropies);
      const currentEntropy = newLocalEntropies.get(neuronId) || 0;
      newLocalEntropies.set(neuronId, Math.max(0, Math.min(1, currentEntropy + delta)));
      
      // Recalculate global entropy
      const entropyValues = Array.from(newLocalEntropies.values());
      const globalEntropy = entropyValues.length > 0 
        ? entropyValues.reduce((sum, val) => sum + val, 0) / entropyValues.length
        : prev.global_entropy;
      
      return {
        ...prev,
        local_entropies: newLocalEntropies,
        global_entropy: globalEntropy
      };
    });
  }, []);

  // Create spline neuron
  const createSplineNeuron = useCallback((
    id: string, 
    position: SemanticCoordinate,
    splineFunction: (input: number[]) => number[]
  ): SplineNeuron => {
    return {
      id,
      assemblageId: `assemblage_${Date.now()}`,
      splineFunction,
      activationThreshold: 0.5,
      entropyLevel: 0.3,
      semanticWeight: 1.0,
      position,
      connections: [],
      lastActivation: 0,
      consciousness_contribution: 0.1
    };
  }, []);

  // Update KAN topology
  const updateKANTopology = useCallback((neurons: SplineNeuron[]) => {
    const neuronsMap = new Map(neurons.map(n => [n.id, n]));
    
    setKanTopology(prev => ({
      neurons: neuronsMap,
      connections: prev?.connections || {
        adjacencyMatrix: [],
        semanticWeights: [],
        entropyFlows: [],
        consciousness_pathways: []
      },
      globalEntropy: entropyMonitor?.global_entropy || 0.3,
      consciousness_field: consciousnessField || {
        intensity: 0.5,
        coherence: 0.8,
        entropy_distribution: [0.1, 0.2, 0.4, 0.2, 0.1],
        semantic_density: 0.6,
        temporal_stability: 0.7,
        observer_effect: 0.3
      },
      semantic_space: prev?.semantic_space || {
        dimensions: 3,
        basis_vectors: [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        semantic_clusters: [],
        consciousness_gradients: [],
        entropy_wells: []
      },
      temporal_layers: prev?.temporal_layers || []
    }));
  }, [entropyMonitor, consciousnessField]);

  // System state
  const systemState = useMemo(() => ({
    isInitialized: !!(cursorState && entropyMonitor && consciousnessField),
    cursorState,
    entropyMonitor,
    kanTopology,
    consciousnessField,
    consciousnessStream: consciousnessStreamRef.current
  }), [cursorState, entropyMonitor, kanTopology, consciousnessField]);

  // System actions
  const systemActions = useMemo(() => ({
    updateCursorPosition,
    triggerConsciousnessEvent,
    adjustEntropy,
    createSplineNeuron,
    updateKANTopology
  }), [updateCursorPosition, triggerConsciousnessEvent, adjustEntropy, createSplineNeuron, updateKANTopology]);

  return {
    ...systemState,
    ...systemActions
  };
};

// === CONSCIOUSNESS MONITORING HOOK ===

export const useConsciousnessMonitoring = (
  consciousnessStream: ReadableStream<ConsciousnessEvent> | null,
  options: {
    bufferSize?: number;
    filterTypes?: ConsciousnessEvent['type'][];
    minIntensity?: number;
  } = {}
) => {
  const [events, setEvents] = useState<ConsciousnessEvent[]>([]);
  const [isMonitoring, setIsMonitoring] = useState(false);
  
  useEffect(() => {
    if (!consciousnessStream) return;
    
    const reader = consciousnessStream.getReader();
    setIsMonitoring(true);
    
    const readStream = async () => {
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          // Filter events based on options
          const shouldInclude = (!options.filterTypes || options.filterTypes.includes(value.type)) &&
                               (!options.minIntensity || value.intensity >= options.minIntensity);
          
          if (shouldInclude) {
            setEvents(prev => {
              const newEvents = [value, ...prev];
              return newEvents.slice(0, options.bufferSize || 100);
            });
          }
        }
      } catch (error) {
        console.error('Error reading consciousness stream:', error);
      } finally {
        setIsMonitoring(false);
      }
    };
    
    readStream();
    
    return () => {
      reader.releaseLock();
      setIsMonitoring(false);
    };
  }, [consciousnessStream, options]);

  return {
    events,
    isMonitoring,
    latestEvent: events[0] || null,
    eventCount: events.length
  };
};

// === ENTROPY REGULATION HOOK ===

export const useEntropyRegulation = (
  entropyMonitor: EntropyMonitor | null,
  config: {
    targetEntropy?: number;
    regulationMode?: 'automatic' | 'manual' | 'consciousness_mediated';
    sensitivity?: number;
  } = {}
) => {
  const [regulationActive, setRegulationActive] = useState(false);
  
  const regulateEntropy = useCallback((neuronId: string, targetEntropy: number) => {
    if (!entropyMonitor) return;
    
    const currentEntropy = entropyMonitor.local_entropies.get(neuronId) || 0;
    const delta = targetEntropy - currentEntropy;
    const sensitivity = config.sensitivity || 0.1;
    
    return Math.sign(delta) * Math.min(Math.abs(delta), sensitivity);
  }, [entropyMonitor, config.sensitivity]);

  const autoRegulate = useCallback(() => {
    if (!entropyMonitor || config.regulationMode !== 'automatic') return;
    
    setRegulationActive(true);
    
    // Auto-regulation logic would go here
    const targetEntropy = config.targetEntropy || 0.3;
    
    setTimeout(() => setRegulationActive(false), 100);
  }, [entropyMonitor, config]);

  return {
    regulateEntropy,
    autoRegulate,
    regulationActive,
    globalEntropy: entropyMonitor?.global_entropy || 0,
    localEntropies: entropyMonitor?.local_entropies || new Map()
  };
}; 