import { useCosmicStore } from '../store/cosmicStore';
import { useMemo } from 'react';

export function useConsciousnessLevel({ critical = 0.8, active = 0.5 } = {}) {
  const entropy = useCosmicStore(s => s.entropy);
  const neural = useCosmicStore(s => s.neuralActivity);
  const quantum = useCosmicStore(s => s.quantumCoherence);
  const system = useCosmicStore(s => s.systemLoad);

  // Compute consciousness level (weighted average)
  const level = useMemo(() => (
    (entropy + neural + quantum + system) / 4
  ), [entropy, neural, quantum, system]);

  let status: 'idle' | 'active' | 'critical' = 'idle';
  if (level >= critical) status = 'critical';
  else if (level >= active) status = 'active';

  return { level, status };
} 