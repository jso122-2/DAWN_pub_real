import React, { useRef, useState, useCallback, useEffect } from 'react';
import { motion, useAnimation, AnimatePresence } from 'framer-motion';
import { cn } from '../../lib/utils';
import { EventEmitter } from '../../lib/EventEmitter';

// Module type definition
export interface WheelModule {
  id: string;
  name: string;
  category: 'neural' | 'consciousness' | 'process' | 'monitoring' | 'diagnostic';
  description?: string;
  icon?: string;
  color?: string;
  glowIntensity?: number;
}

interface ModuleWheelProps {
  modules: WheelModule[];
  onModuleSelect?: (module: WheelModule) => void;
  onModuleSpawn?: (module: WheelModule, position: { x: number; y: number }) => void;
  emitter?: EventEmitter;
}

// Sample modules for the wheel
const defaultModules: WheelModule[] = [
  {
    id: 'neural-processor',
    name: 'Neural Processor',
    category: 'neural',
    description: 'Advanced neural network processing module',
    color: '#a78bfa',
    glowIntensity: 0.8
  },
  {
    id: 'consciousness-core',
    name: 'Consciousness Core',
    category: 'consciousness',
    description: 'Consciousness computing and entanglement module',
    color: '#60a5fa',
    glowIntensity: 0.9
  },
  {
    id: 'process-manager',
    name: 'Process Manager',
    category: 'process',
    description: 'System process orchestration and monitoring',
    color: '#34d399',
    glowIntensity: 0.7
  },
  {
    id: 'system-monitor',
    name: 'System Monitor',
    category: 'monitoring',
    description: 'Real-time system metrics and diagnostics',
    color: '#fbbf24',
    glowIntensity: 0.6
  },
  {
    id: 'diagnostic-tool',
    name: 'Diagnostic Tool',
    category: 'diagnostic',
    description: 'Advanced system diagnostics and repair',
    color: '#f87171',
    glowIntensity: 0.7
  }
];

const ModuleWheel: React.FC<ModuleWheelProps> = ({
  modules = defaultModules,
  onModuleSelect,
  onModuleSpawn,
  emitter = new EventEmitter()
}) => {
  const [rotation, setRotation] = useState(0);
  const [activeIndex, setActiveIndex] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [draggedModule, setDraggedModule] = useState<WheelModule | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [wheelScale, setWheelScale] = useState(1);

  const wheelRef = useRef<HTMLDivElement>(null);
  const rotationVelocity = useRef(0);
  const animationFrame = useRef<number>();
  const controls = useAnimation();
  
  // Motion values for smooth interactions
  const wheelScaleMotion = useAnimation();
  const particleTrails = useRef<Array<{ x: number; y: number; angle: number }>>([]);

  // Initialize particle trails
  useEffect(() => {
    particleTrails.current = Array.from({ length: 20 }, () => ({
      x: 0,
      y: 0,
      angle: Math.random() * Math.PI * 2
    }));
  }, []);

  // Handle mouse wheel rotation
  const handleWheel = useCallback((e: React.WheelEvent<HTMLDivElement>) => {
    e.preventDefault();
    const delta = e.deltaY * 0.5;
    // rotationVelocity.current += delta * 0.01;
  }, []);

  // Animation loop for smooth rotation
  useEffect(() => {
    const animate = () => {
      if (Math.abs(rotationVelocity.current) > 0.001) {
        setRotation(prev => prev + rotationVelocity.current);
        rotationVelocity.current *= 0.95; // Friction
      }
      animationFrame.current = requestAnimationFrame(animate);
    };
    animate();
    return () => {
      if (animationFrame.current) {
        cancelAnimationFrame(animationFrame.current);
      }
    };
  }, []);

  // Update active module based on rotation
  useEffect(() => {
    const moduleCount = modules.length;
    const anglePerModule = (Math.PI * 2) / moduleCount;
    const normalizedRotation = rotation % (Math.PI * 2);
    const newIndex = Math.floor((normalizedRotation + anglePerModule / 2) / anglePerModule) % moduleCount;
    setActiveIndex(newIndex >= 0 ? newIndex : newIndex + moduleCount);
  }, [rotation, modules.length]);

  // Handle module click
  const handleModuleClick = (module: WheelModule, index: number) => {
    if (index === activeIndex) {
      setIsExpanded(!isExpanded);
      if (onModuleSelect) {
        onModuleSelect(module);
      }
    } else {
      const moduleCount = modules.length;
      const anglePerModule = (Math.PI * 2) / moduleCount;
      const targetRotation = index * anglePerModule;
      setRotation(targetRotation);
      rotationVelocity.current = 0;
    }
  };

  // Handle drag start
  const handleDragStart = (module: WheelModule) => {
    setIsDragging(true);
    setDraggedModule(module);
    emitter.emit('module:dragStart', { module });
  };

  // Handle drag end
  const handleDragEnd = (e: DragEvent) => {
    if (draggedModule && onModuleSpawn) {
      const position = { x: e.clientX, y: e.clientY };
      onModuleSpawn(draggedModule, position);
    }
    setIsDragging(false);
    setDraggedModule(null);
  };

  // Filter modules based on search and category
  const filteredModules = modules.filter(module => {
    const matchesSearch = searchQuery === '' || 
      module.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      module.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = !selectedCategory || module.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <motion.div
      ref={wheelRef}
      className="relative w-full h-full flex items-center justify-center"
      onWheel={handleWheel}
      animate={controls}
    >
      {/* Energy Rim */}
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{
          background: 'conic-gradient(from 0deg, transparent, rgba(255,255,255,0.1), transparent)',
          // transform: `rotate(${rotation}rad)` // Removed rotation
        }}
      />

      {/* Module Wheel */}
      <motion.div
        className="relative w-96 h-96"
        style={{
          // transform: `rotate(${rotation}rad) scale(${wheelScale})` // Removed rotation
          transform: `scale(${wheelScale})`
        }}
      >
        {filteredModules.map((module, index) => {
          const angle = (index * (Math.PI * 2)) / filteredModules.length;
          const x = Math.cos(angle) * 150;
          const y = Math.sin(angle) * 150;
          const isActive = index === activeIndex;

          return (
            <motion.div
              key={module.id}
              className={cn(
                "absolute w-24 h-24 glass-base cursor-pointer",
                isActive && "glass-active",
                `glass-${module.category}`
              )}
              style={{
                left: `calc(50% + ${x}px)`,
                top: `calc(50% + ${y}px)`,
                transform: 'translate(-50%, -50%)',
                backgroundColor: module.color,
                boxShadow: isActive ? `0 0 20px ${module.color}` : 'none'
              }}
              onClick={() => handleModuleClick(module, index)}
              drag={!isExpanded}
              dragConstraints={wheelRef}
              onDragStart={() => handleDragStart(module)}
              onDragEnd={handleDragEnd}
              whileHover={{ scale: 1.1 }}
              animate={{
                scale: isActive ? 1.2 : 1,
                // rotate: -rotation // Removed rotation
              }}
            >
              <div className="p-2 text-center">
                <div className="text-sm font-medium text-white">{module.name}</div>
                {isActive && (
                  <motion.div
                    className="absolute inset-0 rounded-full"
                    animate={{
                      boxShadow: [
                        `0 0 10px ${module.color}`,
                        `0 0 20px ${module.color}`,
                        `0 0 10px ${module.color}`
                      ]
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity
                    }}
                  />
                )}
              </div>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Search and Controls */}
      <motion.div
        className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2"
        animate={{ opacity: isExpanded ? 1 : 0.5 }}
      >
        <input
          type="text"
          placeholder="Search modules..."
          className="px-4 py-2 rounded-full glass-base text-white"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <select
          className="px-4 py-2 rounded-full glass-base text-white"
          value={selectedCategory || ''}
          onChange={(e) => setSelectedCategory(e.target.value || null)}
        >
          <option value="">All Categories</option>
          <option value="neural">Neural</option>
          <option value="consciousness">Consciousness</option>
          <option value="process">Process</option>
          <option value="monitoring">Monitoring</option>
          <option value="diagnostic">Diagnostic</option>
        </select>
      </motion.div>

      {/* Zoom Controls */}
      <motion.div
        className="absolute right-4 top-1/2 transform -translate-y-1/2 flex flex-col gap-2"
        animate={{ opacity: isExpanded ? 1 : 0.5 }}
      >
        <button
          onClick={() => setWheelScale(prev => Math.min(2, prev + 0.1))}
          className="p-2 rounded-full glass-base hover:glass-active transition-all"
        >
          <span className="text-white">+</span>
        </button>
        <button
          onClick={() => setWheelScale(prev => Math.max(0.5, prev - 0.1))}
          className="p-2 rounded-full glass-base hover:glass-active transition-all"
        >
          <span className="text-white">-</span>
        </button>
      </motion.div>
    </motion.div>
  );
};

export default ModuleWheel; 