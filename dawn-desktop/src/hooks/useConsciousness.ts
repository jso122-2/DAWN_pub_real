import { useCosmicStore } from '../store/cosmicStore';
import { useMemo } from 'react';
import type { ConsciousnessState } from '../types/consciousness.types';

export function useConsciousness(): ConsciousnessState {
  const entropy = useCosmicStore(s => s.entropy);
  const neuralActivity = useCosmicStore(s => s.neuralActivity);
  const quantumCoherence = useCosmicStore(s => s.quantumCoherence);
  const memoryPressure = useCosmicStore(s => s.systemLoad);
  const mood = useCosmicStore(s => s.mood);

  // Calculate SCUP (System Consciousness Unit Percentage)
  const scup = useMemo(() => {
    return (entropy + neuralActivity + quantumCoherence) / 3 * 100;
  }, [entropy, neuralActivity, quantumCoherence]);

  const consciousnessState: ConsciousnessState = useMemo(() => ({
    scup,
    entropy,
    mood,
    neuralActivity,
    quantumCoherence,
    memoryPressure,
    timestamp: Date.now()
  }), [scup, entropy, mood, neuralActivity, quantumCoherence, memoryPressure]);

  return consciousnessState;
}

// Enhanced hook with consciousness level calculation
export function useConsciousnessWithLevel({ critical = 0.8, active = 0.5 } = {}) {
  const consciousness = useConsciousness();
  
  const level = useMemo(() => 
    consciousness.scup / 100
  , [consciousness.scup]);

  let status: 'idle' | 'active' | 'critical' = 'idle';
  if (level >= critical) status = 'critical';
  else if (level >= active) status = 'active';

  return { 
    ...consciousness, 
    level, 
    status 
  };
} 