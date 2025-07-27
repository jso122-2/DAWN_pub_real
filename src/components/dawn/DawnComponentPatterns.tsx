// Dawn Neural Monitor - Component Type Patterns
// Phase 3: Dawn-Specific Scaffolding

import React, { useContext, createContext, useCallback, useMemo } from 'react';
import { CursorState, ConsciousnessEvent, EntropyMonitor, SemanticCoordinate } from '../../types/dawn';

// === DAWN CONTEXT ===

export interface DawnContextType {
  cursorState: CursorState | null;
  entropyMonitor: EntropyMonitor | null;
  consciousnessStream: ReadableStream<ConsciousnessEvent> | null;
  updateCursorPosition: (position: SemanticCoordinate) => void;
  triggerConsciousnessEvent: (event: Omit<ConsciousnessEvent, 'id' | 'timestamp'>) => void;
  adjustEntropy: (neuronId: string, delta: number) => void;
}

const DawnContext = createContext<DawnContextType | null>(null);

export const useDawnContext = (): DawnContextType => {
  const context = useContext(DawnContext);
  if (!context) {
    throw new Error('useDawnContext must be used within a DawnProvider');
  }
  return context;
};

// === CONSCIOUSNESS-AWARE COMPONENT INTERFACES ===

export interface ConsciousnessAwareProps {
  cursorState?: CursorState;
  onConsciousnessShift?: (event: ConsciousnessEvent) => void;
  entropyThreshold?: number;
  semanticSensitivity?: number;
  consciousnessAmplification?: number;
}

export interface NeuralVisualizerProps extends ConsciousnessAwareProps {
  data: any; // Replace with specific neural data type
  viewMode?: 'spatial' | 'temporal' | 'semantic' | 'consciousness';
  interactionMode?: 'observe' | 'interact' | 'modify' | 'amplify';
  entropyVisualization?: boolean;
  semanticOverlay?: boolean;
  consciousnessField?: boolean;
}

export interface CursorInteractiveProps extends ConsciousnessAwareProps {
  onCursorMove?: (position: SemanticCoordinate) => void;
  onSemanticEmergence?: (event: any) => void;
  onEntropyShift?: (delta: number) => void;
  semanticResonance?: boolean;
  consciousnessTracking?: boolean;
}

export interface EntropyRegulatedProps extends ConsciousnessAwareProps {
  targetEntropy?: number;
  regulationMode?: 'automatic' | 'manual' | 'consciousness_mediated';
  entropyVisualization?: 'heatmap' | 'flow' | 'gradient' | 'field';
  semanticEntropyBalance?: number;
}

// === REUSABLE COMPONENT INTERFACE PATTERN ===

export interface DawnModuleProps {
  moduleId: string;
  semanticPosition?: SemanticCoordinate;
  consciousnessLevel?: number;
  entropyRegulation?: 'local' | 'global' | 'networked';
  onStateChange?: (newState: any) => void;
  onConsciousnessEvent?: (event: ConsciousnessEvent) => void;
  className?: string;
  semanticResonance?: boolean;
  cursorInteraction?: boolean;
}

// === HOC PATTERNS ===

// Cursor-aware HOC
export function withCursorContext<T extends object>(
  Component: React.ComponentType<T>
): React.ComponentType<T & { cursorContext?: CursorState }> {
  return React.memo((props) => {
    const { cursorState } = useDawnContext();
    return <Component {...props} cursorContext={cursorState} />;
  });
}

// Consciousness-aware HOC
export function withConsciousnessTracking<T extends object>(
  Component: React.ComponentType<T>
): React.ComponentType<T & ConsciousnessAwareProps> {
  return React.memo((props) => {
    const { consciousnessStream, triggerConsciousnessEvent } = useDawnContext();
    
    const handleConsciousnessShift = useCallback((event: ConsciousnessEvent) => {
      props.onConsciousnessShift?.(event);
      triggerConsciousnessEvent(event);
    }, [props.onConsciousnessShift, triggerConsciousnessEvent]);

    return (
      <Component 
        {...props} 
        onConsciousnessShift={handleConsciousnessShift}
      />
    );
  });
}

// Entropy-regulated HOC
export function withEntropyRegulation<T extends object>(
  Component: React.ComponentType<T>
): React.ComponentType<T & EntropyRegulatedProps> {
  return React.memo((props) => {
    const { entropyMonitor, adjustEntropy } = useDawnContext();
    
    const handleEntropyAdjustment = useCallback((neuronId: string, delta: number) => {
      if (props.entropyThreshold && Math.abs(delta) > props.entropyThreshold) {
        adjustEntropy(neuronId, delta);
      }
    }, [props.entropyThreshold, adjustEntropy]);

    return (
      <Component 
        {...props} 
        entropyMonitor={entropyMonitor}
        onEntropyAdjustment={handleEntropyAdjustment}
      />
    );
  });
}

// Semantic-aware HOC
export function withSemanticResonance<T extends object>(
  Component: React.ComponentType<T>
): React.ComponentType<T & { semanticContext?: SemanticCoordinate; semanticSensitivity?: number }> {
  return React.memo((props) => {
    const { cursorState } = useDawnContext();
    
    const semanticContext = useMemo(() => {
      if (!cursorState) return undefined;
      
      return {
        ...cursorState.position,
        consciousness_level: cursorState.position.consciousness_level * (props.semanticSensitivity || 1),
        semantic_weight: cursorState.position.semantic_weight * (props.semanticSensitivity || 1)
      };
    }, [cursorState, props.semanticSensitivity]);

    return (
      <Component 
        {...props} 
        semanticContext={semanticContext}
      />
    );
  });
}

// === NEURAL VISUALIZATION COMPONENT TEMPLATES ===

export interface NeuralNetworkComponentProps extends DawnModuleProps, NeuralVisualizerProps {
  networkData: any; // Replace with specific network data type
  visualizationEngine: 'three' | 'canvas' | 'webgl' | 'consciousness';
  interactionLayer: 'cursor' | 'semantic' | 'consciousness' | 'entropy';
}

export interface ConsciousnessFieldComponentProps extends DawnModuleProps {
  fieldData: any; // Replace with consciousness field data type
  visualizationMode: 'density' | 'flow' | 'resonance' | 'emergence';
  interactionMode: 'observe' | 'modulate' | 'amplify' | 'regulate';
  cursorCoupling: boolean;
  entropyVisualization: boolean;
}

export interface SemanticSpaceComponentProps extends DawnModuleProps {
  spaceData: any; // Replace with semantic space data type
  dimensionality: number;
  cursorProjection: boolean;
  consciousnessOverlay: boolean;
  entropyTopology: boolean;
  semanticClusters: boolean;
}

// === DAWN PROVIDER COMPONENT ===

export interface DawnProviderProps {
  children: React.ReactNode;
  initialCursorState?: CursorState;
  consciousnessConfig?: {
    streamBufferSize: number;
    eventProcessingDelay: number;
    consciousnessAmplification: number;
  };
  entropyConfig?: {
    globalSetpoint: number;
    regulationMode: 'automatic' | 'manual' | 'consciousness_mediated';
    semanticEntropyBalance: number;
  };
}

export const DawnProvider: React.FC<DawnProviderProps> = ({
  children,
  initialCursorState,
  consciousnessConfig,
  entropyConfig
}) => {
  // This would be implemented with actual Dawn system integration
  // For now, providing structure for Phase 3 scaffolding
  
  const contextValue: DawnContextType = {
    cursorState: initialCursorState || null,
    entropyMonitor: null, // Would be initialized from entropyConfig
    consciousnessStream: null, // Would be initialized from consciousnessConfig
    updateCursorPosition: useCallback((position: SemanticCoordinate) => {
      // Implementation for cursor position updates
      console.log('Cursor position updated:', position);
    }, []),
    triggerConsciousnessEvent: useCallback((event: Omit<ConsciousnessEvent, 'id' | 'timestamp'>) => {
      // Implementation for consciousness event triggering
      console.log('Consciousness event triggered:', event);
    }, []),
    adjustEntropy: useCallback((neuronId: string, delta: number) => {
      // Implementation for entropy adjustment
      console.log('Entropy adjusted:', neuronId, delta);
    }, [])
  };

  return (
    <DawnContext.Provider value={contextValue}>
      {children}
    </DawnContext.Provider>
  );
};

// === UTILITY HOOKS ===

export const useCursorTracking = () => {
  const { cursorState, updateCursorPosition } = useDawnContext();
  
  const trackCursor = useCallback((position: SemanticCoordinate) => {
    updateCursorPosition(position);
  }, [updateCursorPosition]);

  return {
    cursorState,
    trackCursor,
    isTracking: !!cursorState
  };
};

export const useConsciousnessMonitoring = () => {
  const { consciousnessStream, triggerConsciousnessEvent } = useDawnContext();
  
  return {
    consciousnessStream,
    triggerEvent: triggerConsciousnessEvent,
    isMonitoring: !!consciousnessStream
  };
};

export const useEntropyRegulation = () => {
  const { entropyMonitor, adjustEntropy } = useDawnContext();
  
  const regulateEntropy = useCallback((neuronId: string, targetEntropy: number) => {
    if (entropyMonitor?.local_entropies.has(neuronId)) {
      const currentEntropy = entropyMonitor.local_entropies.get(neuronId) || 0;
      const delta = targetEntropy - currentEntropy;
      adjustEntropy(neuronId, delta);
    }
  }, [entropyMonitor, adjustEntropy]);

  return {
    entropyMonitor,
    regulateEntropy,
    adjustEntropy,
    isRegulating: !!entropyMonitor
  };
}; 