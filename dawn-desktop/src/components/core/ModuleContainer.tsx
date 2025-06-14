import React, { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useBreathing } from '@/hooks/useBreathing';
import { useFloatingOptimized } from '@/hooks/useFloatingOptimized';
import * as styles from './ModuleContainer.styles';

export interface ModuleContainerProps {
  children: React.ReactNode;
  moduleId: string;
  category: 'neural' | 'quantum' | 'chaos' | 'process' | 'monitor';
  position?: { x: number; y: number; z: number };
  breathingIntensity?: number;
  floatingSpeed?: number;
  glowIntensity?: number;
  onClose?: () => void;
  className?: string;
}

export const ModuleContainer: React.FC<ModuleContainerProps> = ({
  children,
  moduleId,
  category,
  position = { x: 0, y: 0, z: 0 },
  breathingIntensity = 0.5,
  floatingSpeed = 1,
  glowIntensity = 0.5,
  onClose,
  className,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  const breathing = useBreathing({
    intensity: breathingIntensity,
    baseRate: 4000,
  });
  
  const floating = useFloatingOptimized({
    amplitude: 20,
    speed: floatingSpeed,
    pattern: 'lissajous',
  });

  // Module-specific glow colors
  const glowColors = {
    neural: 'rgba(147, 51, 234, 0.5)',
    quantum: 'rgba(59, 130, 246, 0.5)',
    chaos: 'rgba(239, 68, 68, 0.5)',
    process: 'rgba(34, 197, 94, 0.5)',
    monitor: 'rgba(251, 191, 36, 0.5)',
  };

  const glowColor = glowColors[category];

  return (
    <AnimatePresence>
      <motion.div
        ref={containerRef}
        className={`${styles.container} ${className || ''}`}
        data-module-id={moduleId}
        data-category={category}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ 
          opacity: 1, 
          x: position.x,
          y: position.y,
          ...breathing.animate,
        }}
        exit={{ opacity: 0, scale: 0.9 }}
        transition={breathing.transition}
        style={{
          ...floating,
          boxShadow: `0 0 ${30 * glowIntensity}px ${glowColor}`,
        }}
      >
        <div className={styles.glassLayer} />
        <div className={styles.contentLayer}>
          {onClose && (
            <motion.button
              className={styles.closeButton}
              onClick={onClose}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <X size={16} />
            </motion.button>
          )}
          {children}
        </div>
        <div 
          className={styles.glowBorder} 
          style={{ 
            background: `linear-gradient(135deg, ${glowColor}, transparent)`,
            opacity: glowIntensity,
          }} 
        />
      </motion.div>
    </AnimatePresence>
  );
}; 