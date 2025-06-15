import { useMemo } from 'react';

export function useGlassEffect({
  category = 'base',
  intensity = 0.5,
  isActive = false,
  isCritical = false,
}: {
  category?: 'base' | 'neural' | 'consciousness' | 'process' | 'diagnostic' | string;
  intensity?: number;
  isActive?: boolean;
  isCritical?: boolean;
} = {}) {
  // Map category to glass class
  const glassClass = useMemo(() => {
    if (isCritical) return 'glass-critical';
    if (isActive) return 'glass-active';
    switch (category) {
      case 'neural': return 'glass-neural';
      case 'consciousness': return 'glass-consciousness';
      case 'process': return 'glass-active';
      case 'diagnostic': return 'glass-critical';
      default: return 'glass-base';
    }
  }, [category, isActive, isCritical]);

  // Dynamic glow style
  const style = useMemo(() => ({
    boxShadow: `0 0 ${30 * intensity}px rgba(147, 51, 234, ${0.3 * intensity}), 0 0 ${60 * intensity}px rgba(147, 51, 234, ${0.2 * intensity}), inset 0 0 ${20 * intensity}px rgba(147, 51, 234, ${0.1 * intensity})`,
  }), [intensity]);

  return { className: glassClass, style };
} 