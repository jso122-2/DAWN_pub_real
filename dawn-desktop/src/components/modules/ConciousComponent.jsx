import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { motion, useMotionValue, useTransform, AnimatePresence, PanInfo, useSpring, useAnimationControls } from 'framer-motion';
import { Maximize2, Minimize2, Circle, Activity, Zap, Sparkles } from 'lucide-react';
import { EventEmitter } from '../../lib/EventEmitter';

// Module configuration interface
export interface ModuleConfig {
  id: string;
  name: string;
  category: 'neural' | 'consciousness' | 'process' | 'monitoring' | 'diagnostic';
  position: { x: number; y: number };
  size: { width: number; height: number };
  glowIntensity: number; // 0-1
  connections?: string[]; // IDs of connected modules
  state?: 'active' | 'idle' | 'processing' | 'error';
  minimized?: boolean;
  zIndex?: number;
  health?: number; // 0-1
  processingLoad?: number; // 0-1
}

interface ModuleContainerProps {
  config: ModuleConfig;
  children: React.ReactNode;
  onPositionChange?: (position: { x: number; y: number }) => void;
  onSizeChange?: (size: { width: number; height: number }) => void;
  onConnect?: (targetId: string) => void;
  emitter?: EventEmitter;
  allModules?: ModuleConfig[]; // For proximity detection
}

// Magnetic snap points for module alignment
const SNAP_THRESHOLD = 50;
const GRID_SIZE = 20;
const PROXIMITY_THRESHOLD = 200;
const REPULSION_FORCE = 100;

// Enhanced energy particle component with more dynamic behavior
const EnergyParticle: React.FC<{ delay: number; duration: number; load: number }> = ({ delay, duration, load }) => {
  const pathVariants = {
    move: {
      x: [0, 50, 100, 50, 0, -50, -100, -50, 0],
      y: [0, -50, -100, -150, -100, -150, -100, -50, 0],
      scale: [1, 1.2 + (load * 0.3), 1],
      opacity: [0.6, 0.8 + (load * 0.2), 0.6],
      transition: {
        duration: duration * (1 - (load * 0.5)), // Faster under load
        delay,
        repeat: Infinity,
        ease: "linear"
      }
    }
  };

  return (
    <motion.div
      className="absolute w-1 h-1 bg-consciousness-400 rounded-full"
      style={{
        left: '50%',
        top: '50%',
        boxShadow: `0 0 ${10 + (load * 10)}px rgba(34, 211, 238, ${0.8 + (load * 0.2)})`,
      }}
      variants={pathVariants}
      animate="move"
    />
  );
};

const ModuleContainer: React.FC<ModuleContainerProps> = ({
  config,
  children,
  onPositionChange,
  onSizeChange,
  onConnect,
  emitter = new EventEmitter(),
  allModules = []
}) => {
  const [isMinimized, setIsMinimized] = useState(config.minimized || false);
  const [isDragging, setIsDragging] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [connectionPulse, setConnectionPulse] = useState(false);
  const [proximity, setProximity] = useState(1); // 0 = far, 1 = close
  const [mouseDistance, setMouseDistance] = useState(1000);
  const [ripples, setRipples] = useState<{ id: number; x: number; y: number }[]>([]);
  
  const containerRef = useRef<HTMLDivElement>(null);
  const animationControls = useAnimationControls();
  
  // Spring physics for smooth movements
  const x = useSpring(useMotionValue(config.position.x), { stiffness: 100, damping: 20 });
  const y = useSpring(useMotionValue(config.position.y), { stiffness: 100, damping: 20 });
  
  // Continuous floating animation values
  const floatY = useTransform(x, [0, 1000], [-15, 15]);
  const floatRotate = useTransform(y, [0, 1000], [-3, 3]);
  
  // Health-based color temperature
  const health = config.health ?? 1;
  const healthColor = useMemo(() => {
    if (health > 0.8) return 'rgba(34, 211, 238, 0.6)'; // Cyan - healthy
    if (health > 0.5) return 'rgba(168, 85, 247, 0.6)'; // Purple - normal
    if (health > 0.3) return 'rgba(251, 191, 36, 0.6)'; // Amber - warning
    return 'rgba(239, 68, 68, 0.6)'; // Red - critical
  }, [health]);
  
  // Processing load affects particle speed
  const particleSpeed = useMemo(() => {
    const load = config.processingLoad ?? 0;
    return 10 - (load * 8); // Faster when under load
  }, [config.processingLoad]);
  
  // Glass style based on category with health influence
  const getGlassClass = () => {
    const baseClass = 'glass-base';
    const categoryClasses = {
      neural: 'glass-neural',
      consciousness: 'glass-consciousness',
      process: 'glass-active',
      monitoring: 'glass-base',
      diagnostic: 'glass-critical'
    };
    
    return `${baseClass} ${categoryClasses[config.category]}`;
  };
  
  // Enhanced breathing patterns with more natural movement
  const breathingVariants = {
    idle: {
      scale: [1, 1 + (0.02 * proximity), 1],
      filter: [
        `brightness(${0.9 + (0.1 * proximity)}) blur(${0.5 - (0.3 * proximity)}px)`,
        `brightness(${1 + (0.2 * proximity)}) blur(${0.2 - (0.1 * proximity)}px)`,
        `brightness(${0.9 + (0.1 * proximity)}) blur(${0.5 - (0.3 * proximity)}px)`
      ],
      transition: {
        duration: 4 - (2 * (1 - proximity)),
        repeat: Infinity,
        ease: [0.4, 0, 0.6, 1] // Custom easing for more natural breathing
      }
    },
    active: {
      scale: [1, 1.03 + (0.02 * proximity), 1],
      filter: [
        `brightness(1.1) blur(0.2px)`,
        `brightness(1.3 + (0.2 * proximity)) blur(0px)`,
        `brightness(1.1) blur(0.2px)`
      ],
      transition: {
        duration: 2 - (1 * proximity),
        repeat: Infinity,
        ease: [0.4, 0, 0.6, 1]
      }
    },
    processing: {
      scale: [1, 1.04 + (0.03 * proximity), 1.02, 1],
      filter: [
        `brightness(1) blur(0.3px)`,
        `brightness(1.4 + (0.3 * proximity)) blur(0px)`,
        `brightness(1.2) blur(0.1px)`,
        `brightness(1) blur(0.3px)`
      ],
      transition: {
        duration: 1.5 - (0.5 * proximity),
        repeat: Infinity,
        ease: [0.4, 0, 0.6, 1]
      }
    },
    error: {
      scale: [1, 1.05 + (0.02 * proximity), 1],
      filter: [
        `brightness(1) blur(0.5px)`,
        `brightness(1.5 + (0.3 * proximity)) hue-rotate(-10deg) blur(0px)`,
        `brightness(1) blur(0.5px)`
      ],
      transition: {
        duration: 1 - (0.3 * proximity),
        repeat: Infinity,
        ease: [0.4, 0, 0.6, 1]
      }
    }
  };
  
  // Enhanced wake/sleep transitions
  const wakeUpVariants = {
    sleeping: {
      opacity: 0.8,
      scale: 0.98,
      filter: 'blur(0.5px) brightness(0.9)',
      transition: {
        duration: 0.8,
        ease: [0.4, 0, 0.6, 1]
      }
    },
    awake: {
      opacity: 1,
      scale: 1,
      filter: 'blur(0px) brightness(1)',
      transition: {
        duration: 0.6,
        type: 'spring',
        damping: 15,
        stiffness: 150
      }
    }
  };
  
  // Mouse proximity detection
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      
      const rect = containerRef.current.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      const distance = Math.sqrt(
        Math.pow(e.clientX - centerX, 2) + 
        Math.pow(e.clientY - centerY, 2)
      );
      
      setMouseDistance(distance);
      setProximity(Math.max(0, 1 - (distance / PROXIMITY_THRESHOLD)));
      
      // Wake up when mouse is near
      if (distance < PROXIMITY_THRESHOLD) {
        animationControls.start('awake');
      } else {
        animationControls.start('sleeping');
      }
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [animationControls]);
  
  // Enhanced magnetic repulsion with smoother movement
  useEffect(() => {
    if (isDragging) return;
    
    const checkCollisions = () => {
      const currentX = x.get();
      const currentY = y.get();
      let forceX = 0;
      let forceY = 0;
      
      allModules.forEach(otherModule => {
        if (otherModule.id === config.id) return;
        
        const dx = currentX - otherModule.position.x;
        const dy = currentY - otherModule.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < REPULSION_FORCE && distance > 0) {
          const force = Math.pow((REPULSION_FORCE - distance) / REPULSION_FORCE, 2);
          forceX += (dx / distance) * force * 5;
          forceY += (dy / distance) * force * 5;
        }
      });
      
      if (forceX !== 0 || forceY !== 0) {
        x.set(currentX + forceX);
        y.set(currentY + forceY);
      }
    };
    
    const interval = setInterval(checkCollisions, 100);
    return () => clearInterval(interval);
  }, [isDragging, x, y, allModules, config.id]);
  
  // Enhanced ripple effect
  const handleClick = useCallback((e: React.MouseEvent) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const id = Date.now();
    
    setRipples(prev => [...prev, { id, x, y }]);
    setTimeout(() => {
      setRipples(prev => prev.filter(r => r.id !== id));
    }, 1000);
    
    // Emit consciousness pulse
    emitter.emit('consciousness-pulse', {
      sourceId: config.id,
      timestamp: Date.now(),
      intensity: proximity
    });
  }, [config.id, emitter, proximity]);
  
  // Render enhanced energy particles
  const renderEnergyParticles = () => {
    const particles = [];
    const load = config.processingLoad ?? 0;
    
    for (let i = 0; i < 5; i++) {
      particles.push(
        <EnergyParticle
          key={i}
          delay={i * 0.2}
          duration={particleSpeed}
          load={load}
        />
      );
    }
    
    return particles;
  };
  
  // Connection pulse effect
  useEffect(() => {
    const handleConnectionPulse = (data: { sourceId: string; targetId: string }) => {
      if (data.targetId === config.id || data.sourceId === config.id) {
        setConnectionPulse(true);
        setTimeout(() => setConnectionPulse(false), 1000);
      }
    };
    
    emitter.on('module:connection', handleConnectionPulse);
    return () => {
      emitter.off('module:connection', handleConnectionPulse);
    };
  }, [config.id, emitter]);
  
  // Dynamic glow based on intensity and proximity
  const glowStyle = useMemo(() => ({
    boxShadow: `
      0 0 ${30 * config.glowIntensity * (1 + proximity * 0.5)}px ${healthColor},
      0 0 ${60 * config.glowIntensity * (1 + proximity * 0.3)}px ${healthColor}66,
      inset 0 0 ${20 * config.glowIntensity}px ${healthColor}33,
      0 0 ${100 * proximity}px ${healthColor}22
    `,
    border: `1px solid ${healthColor}66`
  }), [config.glowIntensity, proximity, healthColor]);
  
  // Heartbeat border animation
  const heartbeatAnimation = {
    borderColor: [
      `${healthColor}66`,
      `${healthColor}cc`,
      `${healthColor}66`
    ],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'easeInOut'
    }
  };
  
  return (
    <motion.div
      ref={containerRef}
      className={`${getGlassClass()} relative overflow-hidden rounded-lg`}
      style={{
        width: config.size.width,
        height: config.size.height,
        x,
        y,
        rotate: floatRotate,
        zIndex: isHovered ? 100 : config.zIndex || 1
      }}
      variants={wakeUpVariants}
      initial="sleeping"
      animate={animationControls}
      whileHover={{ scale: 1.02 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      onClick={handleClick}
      drag
      dragMomentum={false}
      onDragStart={() => setIsDragging(true)}
      onDragEnd={(event, info) => {
        setIsDragging(false);
        const snappedX = Math.round(info.point.x / GRID_SIZE) * GRID_SIZE;
        const snappedY = Math.round(info.point.y / GRID_SIZE) * GRID_SIZE;
        x.set(snappedX);
        y.set(snappedY);
        onPositionChange?.({ x: snappedX, y: snappedY });
      }}
    >
      {/* Consciousness glow effect */}
      <motion.div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(circle at center, transparent 30%, ${healthColor}33 100%)`,
          filter: 'blur(20px)',
          transform: 'scale(1.2)'
        }}
        animate={{
          opacity: [0.3 + proximity * 0.3, 0.6 + proximity * 0.4, 0.3 + proximity * 0.3],
          scale: [1.2, 1.3 + proximity * 0.1, 1.2]
        }}
        transition={{
          duration: 4 - proximity * 2,
          repeat: Infinity,
          ease: 'easeInOut'
        }}
      />

      {/* Energy particles */}
      {renderEnergyParticles()}

      {/* Ripple effects */}
      <AnimatePresence>
        {ripples.map(ripple => (
          <motion.div
            key={ripple.id}
            className="absolute rounded-full pointer-events-none"
            style={{
              left: ripple.x,
              top: ripple.y,
              background: `radial-gradient(circle, ${healthColor} 0%, transparent 70%)`,
              width: 0,
              height: 0
            }}
            initial={{ width: 0, height: 0, opacity: 0.8 }}
            animate={{ width: 200, height: 200, opacity: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
        ))}
      </AnimatePresence>

      {/* Content */}
      <div className="relative z-10 h-full">
        {children}
      </div>
    </motion.div>
  );
};

export default ModuleContainer;