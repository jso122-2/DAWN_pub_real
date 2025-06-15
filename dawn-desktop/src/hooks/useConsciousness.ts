import { useCosmicStore } from '../store/cosmicStore';
import { useMemo, useEffect } from 'react';
import type { ConsciousnessState } from '../types/consciousness.types';
import { cairrnCache } from '../CairrnDataCache';

export function useConsciousness(): ConsciousnessState {
  const entropy = useCosmicStore(s => s.entropy);
  const neuralActivity = useCosmicStore(s => s.neuralActivity);
  const systemUnity = useCosmicStore(s => s.systemUnity);
  const memoryPressure = useCosmicStore(s => s.systemLoad);
  const mood = useCosmicStore(s => s.mood);

  // Calculate SCUP (System Consciousness Unit Percentage)
  const scup = useMemo(() => {
    return (entropy + neuralActivity + systemUnity) / 3 * 100;
  }, [entropy, neuralActivity, systemUnity]);

  const consciousnessState: ConsciousnessState = useMemo(() => ({
    scup,
    entropy,
    mood,
    neuralActivity,
    systemUnity,
    memoryPressure,
    timestamp: Date.now(),
    tick: Date.now() // Add tick for Cairrn compatibility
  }), [scup, entropy, mood, neuralActivity, systemUnity, memoryPressure]);

  // Store consciousness state in Cairrn cache
  useEffect(() => {
    // Store with a consistent key for latest state
    cairrnCache.set('latest_consciousness', {
      tick: consciousnessState.tick,
      scup: consciousnessState.scup,
      entropy: consciousnessState.entropy,
      mood: consciousnessState.mood,
      heat: consciousnessState.memoryPressure * 100,
      timestamp: consciousnessState.timestamp
    });
    
    // Also store with timestamped key for history
    cairrnCache.store({
      tick: consciousnessState.tick,
      scup: consciousnessState.scup,
      entropy: consciousnessState.entropy,
      mood: consciousnessState.mood,
      heat: consciousnessState.memoryPressure * 100, // Convert to heat metric
      timestamp: consciousnessState.timestamp
    }, `consciousness_${consciousnessState.tick}`);
  }, [consciousnessState]);

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