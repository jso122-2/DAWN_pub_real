import React, { useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export interface ModuleContainerProps {
  children: React.ReactNode;
  moduleId?: string;
  category?: 'neural' | 'consciousness' | 'chaos' | 'process' | 'monitor';
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
  category = 'neural',
  position = { x: 0, y: 0, z: 0 },
  breathingIntensity = 0.5,
  floatingSpeed = 1,
  glowIntensity = 0.5,
  onClose,
  className,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Module-specific glow colors
  const glowColors = {
    neural: 'rgba(147, 51, 234, 0.5)',
    consciousness: 'rgba(59, 130, 246, 0.5)',
    chaos: 'rgba(239, 68, 68, 0.5)',
    process: 'rgba(34, 197, 94, 0.5)',
    monitor: 'rgba(251, 191, 36, 0.5)',
  };

  const glowColor = glowColors[category];

  return (
    <AnimatePresence>
      <motion.div
        ref={containerRef}
        className={`relative glass-base p-6 rounded-xl border border-white/10 ${className || ''}`}
        data-module-id={moduleId}
        data-category={category}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ 
          opacity: 1, 
          x: position.x,
          y: position.y,
          scale: [1, 1.01, 1],
        }}
        exit={{ opacity: 0, scale: 0.9 }}
        transition={{
          duration: 2,
          repeat: Infinity,
          repeatType: "reverse",
          ease: "easeInOut"
        }}
        style={{
          boxShadow: `0 0 ${30 * glowIntensity}px ${glowColor}`,
        }}
      >
        <div className="relative z-10">
          {onClose && (
            <motion.button
              className="absolute top-2 right-2 w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white/60 hover:text-white/80"
              onClick={onClose}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              ×
            </motion.button>
          )}
          {children}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}; 