import { useMemo } from 'react';

export function useBreathing(entropy: number) {
  // Map entropy (0-100) to animation intensity
  const intensity = Math.min(1, Math.max(0, entropy / 100));
  return useMemo(() => ({
    calm: {
      scale: [1, 1 + 0.01 * (1 - intensity), 1],
      opacity: [0.8, 1, 0.8],
      transition: {
        duration: 4 - 2 * intensity,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
    active: {
      scale: [1, 1 + 0.03 * intensity, 1],
      opacity: [0.7, 1, 0.7],
      transition: {
        duration: 2 - intensity,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
  }), [intensity]);
} 