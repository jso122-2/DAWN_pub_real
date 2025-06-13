import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Brain, Zap, Activity, Monitor, Cog, X } from 'lucide-react';

interface Module {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  preview?: React.ReactNode;
  category: 'neural' | 'quantum' | 'process' | 'monitoring' | 'diagnostic';
  color: string;
  description: string;
}

interface ModuleWheelProps {
  modules: Module[];
  onActivateModule: (id: string) => void;
  onSpawnModule?: (module: Module, position: { x: number; y: number }) => void;
  className?: string;
}

const defaultModules: Module[] = [
  {
    id: 'neural-network',
    name: 'Neural Network',
    icon: Brain,
    category: 'neural',
    color: '#a855f7',
    description: 'Consciousness processing network'
  },
  {
    id: 'quantum-core',
    name: 'Quantum Core',
    icon: Zap,
    category: 'quantum',
    color: '#06b6d4',
    description: 'Quantum state processor'
  },
  {
    id: 'process-engine',
    name: 'Process Engine',
    icon: Activity,
    category: 'process',
    color: '#22c55e',
    description: 'System process orchestrator'
  },
  {
    id: 'system-monitor',
    name: 'System Monitor',
    icon: Monitor,
    category: 'monitoring',
    color: '#f59e0b',
    description: 'Real-time system monitoring'
  },
  {
    id: 'diagnostics',
    name: 'Diagnostics',
    icon: Cog,
    category: 'diagnostic',
    color: '#ec4899',
    description: 'System diagnostics and health'
  }
];

const ModuleWheel: React.FC<ModuleWheelProps> = ({ 
  modules = defaultModules, 
  onActivateModule,
  onSpawnModule,
  className = ''
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [rotation, setRotation] = useState(0);
  const [hoveredModule, setHoveredModule] = useState<string | null>(null);
  const wheelRef = useRef<HTMLButtonElement>(null);
  const animationRef = useRef<number>();

  // Auto rotation when open
  useEffect(() => {
    if (isOpen) {
      const animate = () => {
        setRotation(prev => prev + 0.5);
        animationRef.current = requestAnimationFrame(animate);
      };
      animate();
    } else {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    }

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isOpen]);

  const handleModuleClick = (module: Module, index: number) => {
    onActivateModule(module.id);
    
    if (onSpawnModule && wheelRef.current) {
      const rect = wheelRef.current.getBoundingClientRect();
      const angle = (index / modules.length) * 2 * Math.PI + (rotation * Math.PI / 180);
      const radius = 120;
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      const spawnX = centerX + Math.cos(angle) * radius;
      const spawnY = centerY + Math.sin(angle) * radius;
      
      onSpawnModule(module, { x: spawnX, y: spawnY });
    }
    
    setIsOpen(false);
  };

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    if (isOpen) {
      setRotation(prev => prev + e.deltaY * 0.1);
    }
  };

  return (
    <div className={`fixed bottom-8 left-8 z-50 ${className}`}>
      {/* Main wheel button */}
      <motion.button
        ref={wheelRef}
        onClick={() => setIsOpen(!isOpen)}
        onWheel={handleWheel}
        className="relative w-16 h-16 rounded-full glass-neural flex items-center justify-center group"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        animate={{
          rotate: isOpen ? rotation : 0,
        }}
        transition={{
          rotate: { duration: 0, ease: "linear" }
        }}
      >
        <motion.div
          animate={{
            rotate: isOpen ? 45 : 0,
            scale: isOpen ? 1.2 : 1
          }}
          transition={{ duration: 0.3 }}
        >
          {isOpen ? (
            <X className="w-6 h-6 text-purple-300" />
          ) : (
            <Plus className="w-6 h-6 text-purple-300" />
          )}
        </motion.div>
        
        {/* Pulsing ring */}
        <motion.div
          className="absolute inset-0 rounded-full border-2 border-purple-400/30"
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.5, 0.2, 0.5]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </motion.button>

      {/* Module options */}
      <AnimatePresence>
        {isOpen && (
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-4">
            {modules.map((module, index) => {
              const angle = (index / modules.length) * 2 * Math.PI + (rotation * Math.PI / 180);
              const radius = 120;
              const x = Math.cos(angle) * radius;
              const y = Math.sin(angle) * radius;
              
              return (
                <motion.div
                  key={module.id}
                  className="absolute"
                  style={{
                    left: `${x}px`,
                    top: `${y}px`,
                    transform: 'translate(-50%, -50%)'
                  }}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ 
                    opacity: 1, 
                    scale: hoveredModule === module.id ? 1.2 : 1
                  }}
                  exit={{ opacity: 0, scale: 0 }}
                  transition={{ 
                    delay: index * 0.1,
                    duration: 0.3
                  }}
                  onMouseEnter={() => setHoveredModule(module.id)}
                  onMouseLeave={() => setHoveredModule(null)}
                >
                  <motion.button
                    onClick={() => handleModuleClick(module, index)}
                    className="relative w-12 h-12 rounded-full flex items-center justify-center glass-base group"
                    style={{
                      backgroundColor: `${module.color}20`,
                      borderColor: `${module.color}40`
                    }}
                    whileHover={{ 
                      scale: 1.1,
                      boxShadow: `0 0 20px ${module.color}60`
                    }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <div style={{ color: module.color }}>
                      <module.icon className="w-5 h-5" />
                    </div>
                    
                    {/* Rotating ring */}
                    <motion.div
                      className="absolute inset-0 rounded-full border border-current opacity-30"
                      style={{ borderColor: module.color }}
                      animate={{ rotate: 360 }}
                      transition={{
                        duration: 3 + index,
                        repeat: Infinity,
                        ease: "linear"
                      }}
                    />
                  </motion.button>
                  
                  {/* Module tooltip */}
                  <AnimatePresence>
                    {hoveredModule === module.id && (
                      <motion.div
                        className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-1 bg-black/80 backdrop-blur rounded text-white text-xs whitespace-nowrap"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                      >
                        <div className="font-medium">{module.name}</div>
                        <div className="text-gray-400 text-xs">{module.description}</div>
                        <div 
                          className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-2 border-r-2 border-t-4 border-transparent border-t-black/80"
                        />
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              );
            })}
          </div>
        )}
      </AnimatePresence>

      {/* Instruction text */}
      <AnimatePresence>
        {!isOpen && (
          <motion.div
            className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 text-xs text-purple-300/70 whitespace-nowrap"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            Spawn Modules
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ModuleWheel; 