import { motion, useMotionValue, useTransform } from 'framer-motion';
import React, { ReactNode, useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { useCosmicStore } from '../../store/cosmicStore';
import eventBus, { emitEvent } from '../../lib/eventBus';

interface ModuleConfig {
  id: string;
  title: string;
  category: 'neural' | 'quantum' | 'process' | 'timeline' | 'monitor' | 'diagnostic';
  size: 'sm' | 'md' | 'lg' | 'xl' | 'fluid';
  glowColor?: string;
  breathingSpeed?: number;
  draggable?: boolean;
  minimizable?: boolean;
}

interface ModuleContainerProps {
  config: ModuleConfig;
  children: ReactNode;
  onClose?: () => void;
  onMinimize?: () => void;
  connections?: string[]; // IDs of connected modules
}

// Simple throttle util
function throttle<T extends (...args: any[]) => void>(fn: T, wait: number): T {
  let last = 0;
  let timeout: any;
  return function(this: any, ...args: any[]) {
    const now = Date.now();
    if (now - last >= wait) {
      last = now;
      fn.apply(this, args);
    } else {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        last = Date.now();
        fn.apply(this, args);
      }, wait - (now - last));
    }
  } as T;
}

const ModuleContainerComponent: React.FC<ModuleContainerProps> = React.memo(({
  config,
  children,
  onClose,
  onMinimize,
  connections = []
}) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [isOffscreen, setIsOffscreen] = useState(false);
  const dragRef = useRef<HTMLDivElement>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);

  // Get glow intensity from store based on system state
  const { entropy, neuralActivity } = useCosmicStore();
  const glowIntensity = (entropy + neuralActivity) / 2;

  const breathingVariants = useMemo(() => ({
    calm: {
      scale: [1, 1.02, 1],
      opacity: [0.8, 1, 0.8],
    },
    active: {
      scale: [1, 1.03, 1],
      opacity: [0.7, 1, 0.7],
    }
  }), []);

  const floatingVariants = useMemo(() => ({
    float: {
      y: [0, -2, 0],
      transition: {
        duration: 8,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }), []);

  const getSizeClasses = useCallback(() => {
    const sizes = {
      sm: 'w-64 h-48',
      md: 'w-96 h-64',
      lg: 'w-[32rem] h-96',
      xl: 'w-[48rem] h-[32rem]',
      fluid: 'w-full h-full'
    };
    return sizes[config.size] || sizes.md;
  }, [config.size]);

  const getCategoryStyles = useCallback(() => {
    const styles = {
      neural: {
        border: 'border-purple-500/20',
        glow: 'shadow-[0_0_30px_rgba(139,92,246,0.3)]',
        header: 'bg-gradient-to-r from-purple-500/20 to-purple-600/20'
      },
      quantum: {
        border: 'border-cyan-500/20',
        glow: 'shadow-[0_0_30px_rgba(34,211,238,0.3)]',
        header: 'bg-gradient-to-r from-cyan-500/20 to-cyan-600/20'
      },
      process: {
        border: 'border-green-500/20',
        glow: 'shadow-[0_0_30px_rgba(16,185,129,0.3)]',
        header: 'bg-gradient-to-r from-green-500/20 to-green-600/20'
      },
      timeline: {
        border: 'border-pink-500/20',
        glow: 'shadow-[0_0_30px_rgba(244,114,182,0.3)]',
        header: 'bg-gradient-to-r from-pink-500/20 to-pink-600/20'
      },
      monitor: {
        border: 'border-amber-500/20',
        glow: 'shadow-[0_0_30px_rgba(245,158,11,0.3)]',
        header: 'bg-gradient-to-r from-amber-500/20 to-amber-600/20'
      },
      diagnostic: {
        border: 'border-pink-500/20',
        glow: 'shadow-[0_0_30px_rgba(244,114,182,0.3)]',
        header: 'bg-gradient-to-r from-pink-500/20 to-pink-600/20'
      }
    };
    return styles[config.category] || styles.neural;
  }, [config.category]);

  const style = getCategoryStyles();

  // Throttled event handlers
  const handleDragStart = useCallback(throttle(() => {
    setIsDragging(true);
    emitModuleEvent('drag', { dragging: true });
  }, 60), [config.id]);

  const handleDragEnd = useCallback(throttle(() => {
    setIsDragging(false);
    emitModuleEvent('drag', { dragging: false });
  }, 60), [config.id]);

  const handleMinimize = useCallback(() => {
    setIsMinimized(!isMinimized);
    onMinimize?.();
    emitModuleEvent('minimize', { minimized: !isMinimized });
  }, [isMinimized, onMinimize, config.id]);

  const handleClose = useCallback(() => {
    onClose?.();
    emitModuleEvent('close');
  }, [onClose, config.id]);

  // Emit custom events for module interactions
  const emitModuleEvent = useCallback((action: 'drag' | 'minimize' | 'close', extra?: any) => {
    eventBus.dispatchEvent(
      new CustomEvent('module-interaction', {
        detail: {
          id: config.id,
          action,
          ...extra,
        },
      })
    );
  }, [config.id]);

  // Intersection observer for offscreen detection
  useEffect(() => {
    if (!dragRef.current) return;
    if (observerRef.current) observerRef.current.disconnect();
    observerRef.current = new window.IntersectionObserver(
      ([entry]) => {
        setIsOffscreen(!entry.isIntersecting);
      },
      { root: null, threshold: 0.01 }
    );
    observerRef.current.observe(dragRef.current);
    return () => observerRef.current?.disconnect();
  }, []);

  return (
    <motion.div
      ref={dragRef}
      className={`
        relative
        ${getSizeClasses()}
        ${isMinimized ? 'h-12' : ''}
        glass
        ${style.border}
        ${style.glow}
        rounded-xl
        overflow-hidden
        ${config.draggable ? 'cursor-move' : ''}
        ${isDragging ? 'z-50' : 'z-10'}
        transition-all duration-300
        ${isOffscreen ? 'offscreen' : ''}
      `}
      style={{
        opacity: glowIntensity * 0.3 + 0.7,
        contain: 'layout paint style',
      }}
      drag={config.draggable}
      dragMomentum={false}
      dragElastic={0.1}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      animate={breathingVariants.calm}
      variants={floatingVariants}
      whileHover={{ scale: 1.02 }}
      transition={{
        duration: config.breathingSpeed || 4,
        repeat: Infinity,
        repeatType: "reverse"
      }}
    >
      {/* Module Header */}
      <div className={`
        absolute top-0 left-0 right-0 h-10
        ${style.header}
        backdrop-blur-xl
        border-b border-white/10
        flex items-center justify-between px-4
        z-20
      `}>
        <h3 className="text-sm font-medium text-white/80">{config.title}</h3>
        <div className="flex gap-2">
          {config.minimizable && (
            <button
              onClick={handleMinimize}
              className="w-5 h-5 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center"
            >
              <span className="text-xs">−</span>
            </button>
          )}
          {onClose && (
            <button
              onClick={handleClose}
              className="w-5 h-5 rounded-full bg-white/10 hover:bg-red-500/50 flex items-center justify-center"
            >
              <span className="text-xs">×</span>
            </button>
          )}
        </div>
      </div>

      {/* Module Content */}
      {!isMinimized && (
        <div className="pt-10 h-full overflow-auto">
          {children}
        </div>
      )}

      {/* Connection Indicators */}
      {connections.length > 0 && (
        <div className="absolute -top-2 -right-2 w-4 h-4 rounded-full bg-purple-500 animate-pulse" />
      )}
    </motion.div>
  );
});

export const ModuleContainer = ModuleContainerComponent;