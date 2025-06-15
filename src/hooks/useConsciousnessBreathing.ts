import { useRealTimeConsciousness } from '../../dawn-desktop/src/hooks/useRealTimeConsciousness';
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