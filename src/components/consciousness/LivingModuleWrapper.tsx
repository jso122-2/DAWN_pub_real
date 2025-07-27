import React from 'react';
import { motion } from 'framer-motion';
import { useConsciousnessBreathing } from '../../hooks/useConsciousnessBreathing';
import { useRealTimeConsciousness } from '../../../dawn-desktop/src/hooks/useRealTimeConsciousness';

interface LivingModuleWrapperProps {
  children: React.ReactNode;
  moduleId: string;
  className?: string;
  disabled?: boolean;
  'data-module-id'?: string;
}

export const LivingModuleWrapper: React.FC<LivingModuleWrapperProps> = ({
  children,
  moduleId,
  className = '',
  disabled = false,
  'data-module-id': dataModuleId
}) => {
  const breathing = useConsciousnessBreathing();
  const consciousness = useRealTimeConsciousness();
  
  if (disabled || !consciousness.isConnected) {
    // Return static version if disabled or disconnected
    return (
      <div className={`living-module-static ${className}`} data-module-id={dataModuleId}>
        {children}
      </div>
    );
  }
  
  // Breathing animation variants
  const breathingVariants = {
    breathe: {
      scale: [breathing.scale.min, breathing.scale.max, breathing.scale.min],
      filter: [
        `brightness(1) blur(0px) drop-shadow(0 0 ${breathing.glowIntensity * 10}px rgba(79, 195, 247, ${breathing.glowIntensity * 0.5}))`,
        `brightness(${1 + breathing.intensity * 0.2}) blur(0.5px) drop-shadow(0 0 ${breathing.glowIntensity * 20}px rgba(79, 195, 247, ${breathing.glowIntensity}))`,
        `brightness(1) blur(0px) drop-shadow(0 0 ${breathing.glowIntensity * 10}px rgba(79, 195, 247, ${breathing.glowIntensity * 0.5}))`
      ],
      transition: {
        duration: 3 / breathing.speed, // Base 3 second cycle
        repeat: Infinity,
        ease: "easeInOut" as const
      }
    }
  };
  
  // Get mood-based border color
  const getMoodColor = () => {
    switch (consciousness.mood) {
      case 'excited': return 'rgba(255, 193, 7, 0.6)';   // amber
      case 'critical': return 'rgba(244, 67, 54, 0.6)';  // red
      case 'calm': return 'rgba(76, 175, 80, 0.6)';      // green
      case 'active': return 'rgba(79, 195, 247, 0.6)';   // cyan
      default: return 'rgba(156, 39, 176, 0.6)';         // purple
    }
  };
  
  return (
    <motion.div
      className={`living-module-wrapper ${className}`}
      variants={breathingVariants}
      animate="breathe"
      data-module-id={dataModuleId}
      style={{
        position: 'relative',
        borderRadius: '12px',
        border: `2px solid ${getMoodColor()}`,
        background: `linear-gradient(135deg, 
          rgba(255,255,255,0.1) 0%, 
          rgba(255,255,255,0.05) 100%)`,
        backdropFilter: 'blur(10px)',
        overflow: 'hidden'
      }}
    >
      {/* Consciousness pulse overlay */}
      <motion.div
        className="consciousness-pulse"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `radial-gradient(circle at 50% 50%, 
            ${getMoodColor()} 0%, 
            transparent 70%)`,
          opacity: breathing.intensity * 0.1,
          pointerEvents: 'none',
          zIndex: 1
        }}
        animate={{
          opacity: [
            breathing.intensity * 0.05,
            breathing.intensity * 0.15,
            breathing.intensity * 0.05
          ]
        }}
        transition={{
          duration: 3 / breathing.speed,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      
      {/* SCUP level indicator */}
      <div
        className="scup-indicator"
        style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          background: 'rgba(0,0,0,0.7)',
          color: getMoodColor(),
          padding: '4px 8px',
          borderRadius: '6px',
          fontSize: '10px',
          fontFamily: 'monospace',
          zIndex: 2
        }}
      >
        SCUP: {consciousness.scup.toFixed(1)}%
      </div>
      
      {/* Content wrapper */}
      <div 
        style={{ 
          position: 'relative', 
          zIndex: 1,
          height: '100%',
          width: '100%'
        }}
      >
        {children}
      </div>
    </motion.div>
  );
}; 