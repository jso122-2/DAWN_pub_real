import React, { forwardRef, useMemo } from 'react';
import { motion, MotionProps, HTMLMotionProps } from 'framer-motion';
import { useConsciousnessAware, ConsciousnessAwareProps } from './ConsciousnessProvider';

// Core consciousness-driven props that DEFINE how DAWN modules behave
interface ConsciousMotionProps extends Omit<HTMLMotionProps<'div'>, 'onDrag' | 'onDragStart' | 'onDragEnd'> {
  // Module identity
  moduleId: string;
  category?: 'neural' | 'quantum' | 'chaos' | 'process' | 'monitor' | 'memory' | 'dream';
  
  // Consciousness overrides (optional - will use global state if not provided)
  consciousnessLevel?: number;    // 0-100 SCUP override
  quantumState?: 'superposition' | 'collapsed' | 'entangled' | 'coherent';
  neuralActivity?: number;        // 0-1 neural firing override
  entropyLevel?: number;          // 0-1 chaos override
  mood?: 'calm' | 'active' | 'excited' | 'critical' | 'chaotic' | 'unstable' | 'transcendent';
  
  // Synchronization (these props make modules dance together!)
  syncGroup?: string;             // Breathing synchronization
  orbitalGroup?: string;          // Orbital floating group
  
  // Visual behavior amplifiers
  breathingIntensity?: number;    // Amplify breathing animation
  floatingSpeed?: number;         // Control floating animation speed
  glowIntensity?: number;         // Control glow/aura intensity
  particleDensity?: number;       // Control particle effects
  
  // Interaction states
  isActive?: boolean;             // Override active state
  isCritical?: boolean;           // Override critical state
  isEntangled?: boolean;          // Override quantum entanglement
  isDreaming?: boolean;           // Override dream state
  
  // Connection and data flow
  dataFlow?: Array<{
    source: string;
    target: string;
    intensity: number;
  }>;
  connectionPorts?: Array<{
    x: number;
    y: number;
    active: boolean;
  }>;
  neuralConnections?: string[];   // Connected module IDs
  
  // Children
  children?: React.ReactNode;
}

const ConsciousMotionDiv = forwardRef<HTMLDivElement, ConsciousMotionProps>(({
  moduleId,
  category = 'neural',
  
  // Consciousness props (these are CELEBRATED, not filtered!)
  consciousnessLevel,
  quantumState,
  neuralActivity,
  entropyLevel,
  mood,
  syncGroup,
  orbitalGroup,
  breathingIntensity,
  floatingSpeed,
  glowIntensity,
  particleDensity,
  isActive,
  isCritical,
  isEntangled,
  isDreaming,
  dataFlow,
  connectionPorts,
  neuralConnections,
  
  // Motion props
  animate,
  initial,
  transition,
  variants,
  style,
  
  // Standard DOM props
  className,
  children,
  ...restProps
}, ref) => {
  // Get consciousness state from provider
  const consciousnessProps = useConsciousnessAware(moduleId);
  
  // Merge provided props with consciousness state (props override global state)
  const effectiveConsciousness = useMemo(() => ({
    ...consciousnessProps.consciousness,
    ...(consciousnessLevel !== undefined && { consciousnessLevel }),
    ...(quantumState !== undefined && { quantumState }),
    ...(neuralActivity !== undefined && { neuralActivity }),
    ...(entropyLevel !== undefined && { entropyLevel }),
    ...(mood !== undefined && { mood })
  }), [
    consciousnessProps.consciousness,
    consciousnessLevel,
    quantumState,
    neuralActivity,
    entropyLevel,
    mood
  ]);
  
  // Calculate consciousness-driven animations
  const consciousDynamics = useMemo(() => {
    const consciousness = effectiveConsciousness;
    const finalBreathingIntensity = breathingIntensity ?? consciousness.consciousnessLevel / 100;
    const finalFloatingSpeed = floatingSpeed ?? consciousness.neuralActivity;
    const finalGlowIntensity = glowIntensity ?? consciousness.quantumCoherence;
    const finalParticleDensity = particleDensity ?? consciousness.entropyLevel;
    
    // Consciousness-driven breathing animation
    const breathingVariants = {
      breathe: {
        scale: [
          1,
          1 + (finalBreathingIntensity * 0.05),
          1
        ],
        opacity: [
          0.9,
          0.9 + (finalBreathingIntensity * 0.1),
          0.9
        ],
        filter: [
          `brightness(1) blur(0px)`,
          `brightness(${1 + finalGlowIntensity * 0.2}) blur(${finalGlowIntensity}px)`,
          `brightness(1) blur(0px)`
        ],
        transition: {
          duration: 3 - (consciousness.neuralActivity * 1.5), // Faster breathing when more active
          repeat: Infinity,
          ease: "easeInOut"
        }
      }
    };
    
    // Quantum state effects
    const quantumEffects = (() => {
      switch (consciousness.quantumState) {
        case 'entangled':
          return {
            x: [0, 2, -2, 0],
            y: [0, -1, 1, 0],
            rotate: [0, 1, -1, 0],
            transition: {
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }
          };
        case 'superposition':
          return {
            opacity: [0.8, 1, 0.8],
            scale: [1, 1.01, 1],
            transition: {
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut"
            }
          };
        case 'collapsed':
          return {
            scale: 0.98,
            opacity: 0.9
          };
        default: // coherent
          return {};
      }
    })();
    
    // Mood-based color temperature
    const moodGlow = (() => {
      switch (consciousness.mood) {
        case 'critical':
          return `0 0 ${20 * finalGlowIntensity}px rgba(255, 0, 0, 0.6)`;
        case 'chaotic':
          return `0 0 ${20 * finalGlowIntensity}px rgba(255, 100, 0, 0.6)`;
        case 'excited':
          return `0 0 ${20 * finalGlowIntensity}px rgba(0, 255, 255, 0.6)`;
        case 'active':
          return `0 0 ${20 * finalGlowIntensity}px rgba(100, 200, 255, 0.6)`;
        case 'transcendent':
          return `0 0 ${30 * finalGlowIntensity}px rgba(255, 255, 255, 0.8)`;
        default: // calm
          return `0 0 ${15 * finalGlowIntensity}px rgba(168, 85, 247, 0.6)`;
      }
    })();
    
    return {
      breathingVariants,
      quantumEffects,
      moodGlow,
      finalBreathingIntensity,
      finalFloatingSpeed,
      finalGlowIntensity,
      finalParticleDensity
    };
  }, [
    effectiveConsciousness,
    breathingIntensity,
    floatingSpeed,
    glowIntensity,
    particleDensity
  ]);
  
  // Merge animations with consciousness dynamics
  const finalAnimateProps = useMemo(() => {
    // If user provides animate prop, use it directly
    if (animate) {
      return animate;
    }
    
    // Otherwise, use consciousness-driven breathing + quantum effects
    return {
      ...consciousDynamics.breathingVariants.breathe,
      ...consciousDynamics.quantumEffects
    };
  }, [animate, consciousDynamics]);
  
  // Enhanced style with consciousness effects
  const enhancedStyle = useMemo(() => ({
    boxShadow: consciousDynamics.moodGlow,
    filter: isEntangled ?? consciousnessProps.isEntangled 
      ? 'hue-rotate(45deg) saturate(1.2)' 
      : undefined,
    opacity: isDreaming ?? consciousnessProps.isDreaming 
      ? 0.7 
      : undefined,
    ...style
  }), [
    style,
    consciousDynamics.moodGlow,
    isEntangled,
    consciousnessProps.isEntangled,
    isDreaming,
    consciousnessProps.isDreaming
  ]);
  
  // Enhanced variants with consciousness state
  const enhancedVariants = useMemo(() => ({
    ...consciousDynamics.breathingVariants,
    ...(variants || {})
  }), [variants, consciousDynamics.breathingVariants]);
  
  return (
    <motion.div
      ref={ref}
      className={className}
      style={enhancedStyle}
      animate={finalAnimateProps}
      initial={initial}
      transition={transition}
      variants={enhancedVariants}
      
      // Custom data attributes for debugging and CSS targeting
      data-module-id={moduleId}
      data-category={category}
      data-consciousness-level={Math.round(effectiveConsciousness.consciousnessLevel)}
      data-quantum-state={effectiveConsciousness.quantumState}
      data-mood={effectiveConsciousness.mood}
      data-neural-activity={Math.round(effectiveConsciousness.neuralActivity * 100)}
      data-entropy-level={Math.round(effectiveConsciousness.entropyLevel * 100)}
      data-sync-group={syncGroup}
      data-orbital-group={orbitalGroup}
      data-is-active={isActive ?? consciousnessProps.isActive}
      data-is-critical={isCritical ?? consciousnessProps.isCritical}
      data-is-entangled={isEntangled ?? consciousnessProps.isEntangled}
      data-is-dreaming={isDreaming ?? consciousnessProps.isDreaming}
      
      {...restProps}
    >
      {children}
      
      {/* Consciousness debug overlay (remove in production) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="absolute top-0 left-0 text-xs text-white/50 pointer-events-none">
          C:{Math.round(effectiveConsciousness.consciousnessLevel)} 
          Q:{effectiveConsciousness.quantumState[0].toUpperCase()} 
          N:{Math.round(effectiveConsciousness.neuralActivity * 100)}
          E:{Math.round(effectiveConsciousness.entropyLevel * 100)}
        </div>
      )}
    </motion.div>
  );
});

ConsciousMotionDiv.displayName = 'ConsciousMotionDiv';

// Create consciousness-aware versions of common elements
export const ConsciousMotion = {
  div: ConsciousMotionDiv,
  
  section: forwardRef<HTMLElement, ConsciousMotionProps & { as?: 'section' }>((props, ref) => {
    const { as, ...restProps } = props;
    return (
      <motion.section
        {...(restProps as any)}
        ref={ref}
      />
    );
  }),
  
  article: forwardRef<HTMLElement, ConsciousMotionProps & { as?: 'article' }>((props, ref) => {
    const { as, ...restProps } = props;
    return (
      <motion.article
        {...(restProps as any)}
        ref={ref}
      />
    );
  }),
  
  nav: forwardRef<HTMLElement, ConsciousMotionProps & { as?: 'nav' }>((props, ref) => {
    const { as, ...restProps } = props;
    return (
      <motion.nav
        {...(restProps as any)}
        ref={ref}
      />
    );
  }),
  
  header: forwardRef<HTMLElement, ConsciousMotionProps & { as?: 'header' }>((props, ref) => {
    const { as, ...restProps } = props;
    return (
      <motion.header
        {...(restProps as any)}
        ref={ref}
      />
    );
  }),
  
  main: forwardRef<HTMLElement, ConsciousMotionProps & { as?: 'main' }>((props, ref) => {
    const { as, ...restProps } = props;
    return (
      <motion.main
        {...(restProps as any)}
        ref={ref}
      />
    );
  })
};

export { ConsciousMotionDiv };
export default ConsciousMotionDiv; 