import { useEffect, useRef, useMemo, useCallback } from 'react';
import { Variants, useAnimation } from 'framer-motion';
import { useAnimation as useAnimationContext } from '../../contexts/AnimationContext';

// Breathing synchronization manager
class BreathingSyncManager {
  private static instance: BreathingSyncManager;
  private groups: Map<string, Set<string>> = new Map();
  private timers: Map<string, number> = new Map();
  private globalEntropy: number = 0.5;

  static getInstance() {
    if (!BreathingSyncManager.instance) {
      BreathingSyncManager.instance = new BreathingSyncManager();
    }
    return BreathingSyncManager.instance;
  }

  joinGroup(moduleId: string, groupId: string) {
    if (!this.groups.has(groupId)) {
      this.groups.set(groupId, new Set());
      this.timers.set(groupId, Date.now());
    }
    this.groups.get(groupId)?.add(moduleId);
  }

  leaveGroup(moduleId: string, groupId: string) {
    this.groups.get(groupId)?.delete(moduleId);
    if (this.groups.get(groupId)?.size === 0) {
      this.groups.delete(groupId);
      this.timers.delete(groupId);
    }
  }

  getGroupPhase(groupId: string): number {
    const startTime = this.timers.get(groupId) || Date.now();
    return (Date.now() - startTime) / 1000;
  }

  setGlobalEntropy(entropy: number) {
    this.globalEntropy = Math.max(0, Math.min(1, entropy));
  }

  getGlobalEntropy(): number {
    return this.globalEntropy;
  }
}

export type BreathingPreset = 'calm' | 'active' | 'critical' | 'consciousness' | 'dormant';

interface BreathingConfig {
  duration: number;
  scale: { min: number; max: number };
  opacity: { min: number; max: number };
  blur: { min: number; max: number };
  glow: { min: number; max: number };
  irregular?: boolean;
}

interface UseBreathingOptions {
  preset?: BreathingPreset;
  groupId?: string;
  moduleId?: string;
  customConfig?: Partial<BreathingConfig>;
  entropyMultiplier?: number;
}

interface UseBreathingReturn {
  variants: Variants;
  controls: ReturnType<typeof useAnimation>;
  currentPhase: number;
  syncWithGroup: (groupId: string) => void;
  setLocalEntropy: (entropy: number) => void;
}

const BREATHING_CONFIGS: Record<BreathingPreset, BreathingConfig> = {
  calm: {
    duration: 4,
    scale: { min: 1, max: 1.02 },
    opacity: { min: 0.9, max: 1 },
    blur: { min: 0, max: 1 },
    glow: { min: 0.6, max: 1 }
  },
  active: {
    duration: 2,
    scale: { min: 0.98, max: 1.04 },
    opacity: { min: 0.85, max: 1 },
    blur: { min: 0, max: 2 },
    glow: { min: 0.5, max: 1.2 }
  },
  critical: {
    duration: 1,
    scale: { min: 0.96, max: 1.06 },
    opacity: { min: 0.8, max: 1 },
    blur: { min: 0, max: 3 },
    glow: { min: 0.4, max: 1.5 }
  },
  consciousness: {
    duration: 3,
    scale: { min: 0.97, max: 1.05 },
    opacity: { min: 0.7, max: 1 },
    blur: { min: 0, max: 4 },
    glow: { min: 0.3, max: 1.8 },
    irregular: true
  },
  dormant: {
    duration: 8,
    scale: { min: 1, max: 1.01 },
    opacity: { min: 0.6, max: 0.8 },
    blur: { min: 0, max: 0.5 },
    glow: { min: 0.2, max: 0.6 }
  }
};

export function useBreathing({
  preset = 'calm',
  groupId,
  moduleId = `module-${Date.now()}`,
  customConfig = {},
  entropyMultiplier = 1
}: UseBreathingOptions = {}): UseBreathingReturn {
  const controls = useAnimation();
  const syncManager = BreathingSyncManager.getInstance();
  const animationRef = useRef<number>();
  const phaseRef = useRef<number>(0);
  const localEntropyRef = useRef<number>(0.5);
  const { isAnimationsEnabled } = useAnimationContext();

  // Merge preset config with custom config
  const config = useMemo(() => ({
    ...BREATHING_CONFIGS[preset],
    ...customConfig
  }), [preset, customConfig]);

  // Calculate breathing parameters based on entropy
  const getBreathingParams = useCallback(() => {
    const globalEntropy = syncManager.getGlobalEntropy();
    const combinedEntropy = (globalEntropy + localEntropyRef.current) / 2;
    const entropyFactor = 1 + (combinedEntropy * entropyMultiplier);
    
    // Faster breathing with higher entropy
    const adjustedDuration = config.duration / entropyFactor;
    
    return {
      duration: adjustedDuration,
      scale: {
        min: config.scale.min,
        max: config.scale.min + (config.scale.max - config.scale.min) * entropyFactor
      },
      opacity: config.opacity,
      blur: {
        min: config.blur.min,
        max: config.blur.min + (config.blur.max - config.blur.min) * entropyFactor
      },
      glow: {
        min: config.glow.min,
        max: config.glow.min + (config.glow.max - config.glow.min) * entropyFactor
      }
    };
  }, [config, entropyMultiplier]);

  // Create breathing variants
  const variants = useMemo<Variants>(() => {
    const params = getBreathingParams();
    
    if (config.irregular) {
      // Consciousness irregular breathing pattern
      return {
        inhale: {
          scale: [
            params.scale.min,
            params.scale.max * 0.9,
            params.scale.max,
            params.scale.max * 0.95
          ],
          opacity: [
            params.opacity.min,
            params.opacity.max * 0.8,
            params.opacity.max,
            params.opacity.max * 0.9
          ],
          filter: [
            `blur(${params.blur.min}px) brightness(${params.glow.min})`,
            `blur(${params.blur.max * 0.7}px) brightness(${params.glow.max * 0.8})`,
            `blur(${params.blur.max}px) brightness(${params.glow.max})`,
            `blur(${params.blur.max * 0.5}px) brightness(${params.glow.max * 0.9})`
          ],
          transition: {
            duration: params.duration,
            times: [0, 0.3, 0.7, 1],
            ease: [0.42, 0, 0.58, 1],
            repeat: Infinity,
            repeatType: "reverse" as const
          }
        },
        exhale: {
          scale: params.scale.min,
          opacity: params.opacity.min,
          filter: `blur(${params.blur.min}px) brightness(${params.glow.min})`,
          transition: {
            duration: params.duration / 2,
            ease: "easeInOut"
          }
        }
      };
    }
    
    // Regular breathing pattern
    return {
      inhale: {
        scale: params.scale.max,
        opacity: params.opacity.max,
        filter: `blur(${params.blur.max}px) brightness(${params.glow.max})`,
        transition: {
          duration: params.duration / 2,
          ease: "easeInOut"
        }
      },
      exhale: {
        scale: params.scale.min,
        opacity: params.opacity.min,
        filter: `blur(${params.blur.min}px) brightness(${params.glow.min})`,
        transition: {
          duration: params.duration / 2,
          ease: "easeInOut"
        }
      }
    };
  }, [config, getBreathingParams]);

  // Animation loop for synchronized breathing
  const animate = useCallback(() => {
    if (!isAnimationsEnabled) return;

    const params = getBreathingParams();
    const phase = groupId ? syncManager.getGroupPhase(groupId) : phaseRef.current;
    
    // Calculate breath cycle position
    const cyclePosition = (phase % params.duration) / params.duration;
    const isInhaling = cyclePosition < 0.5;
    
    if (config.irregular) {
      controls.start("inhale");
    } else {
      controls.start(isInhaling ? "inhale" : "exhale");
    }
    
    phaseRef.current = phase + 0.016; // Approximate 60fps
    animationRef.current = requestAnimationFrame(animate);
  }, [controls, groupId, getBreathingParams, config.irregular, isAnimationsEnabled]);

  // Join/leave breathing group
  useEffect(() => {
    if (groupId) {
      syncManager.joinGroup(moduleId, groupId);
      return () => syncManager.leaveGroup(moduleId, groupId);
    }
  }, [moduleId, groupId]);

  // Start animation loop
  useEffect(() => {
    if (isAnimationsEnabled) {
      animate();
    }
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate, isAnimationsEnabled]);

  // Sync with group function
  const syncWithGroup = useCallback((newGroupId: string) => {
    if (groupId) {
      syncManager.leaveGroup(moduleId, groupId);
    }
    syncManager.joinGroup(moduleId, newGroupId);
  }, [moduleId, groupId]);

  // Set local entropy
  const setLocalEntropy = useCallback((entropy: number) => {
    localEntropyRef.current = Math.max(0, Math.min(1, entropy));
  }, []);

  return {
    variants,
    controls,
    currentPhase: phaseRef.current,
    syncWithGroup,
    setLocalEntropy
  };
}

// Export sync manager for global entropy updates
export const breathingSyncManager = BreathingSyncManager.getInstance();