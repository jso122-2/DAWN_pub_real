import { useMemo } from 'react';

export function useFloating() {
  return useMemo(() => ({
    float: {
      y: [0, -10, 0],
      x: [0, 5, -5, 0],
      transition: {
        duration: 6,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
  }), []);
} 