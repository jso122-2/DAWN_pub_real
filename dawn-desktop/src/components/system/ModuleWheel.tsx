import { useState, useEffect, useRef } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { useCosmicStore } from '../../store/cosmicStore';

interface Module {
  id: string;
  name: string;
  component: React.ComponentType;
  icon: string;
  category: string;
}

interface ModuleWheelProps {
  modules: Module[];
  onSelectModule: (module: Module) => void;
  position: 'left' | 'right' | 'bottom';
}

export const ModuleWheel: React.FC<ModuleWheelProps> = ({
  modules,
  onSelectModule,
  position = 'left'
}) => {
  const [rotation, setRotation] = useState(0);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const controls = useAnimation();
  const wheelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleWheel = (e: WheelEvent) => {
      if (!isExpanded) return;
      
      e.preventDefault();
      const delta = e.deltaY > 0 ? 1 : -1;
      const newRotation = rotation + (delta * 360 / modules.length);
      
      setRotation(newRotation);
      setSelectedIndex((prev) => {
        const newIndex = (prev + delta + modules.length) % modules.length;
        return newIndex;
      });
    };

    const wheelElement = wheelRef.current;
    if (wheelElement) {
      wheelElement.addEventListener('wheel', handleWheel, { passive: false });
    }

    return () => {
      if (wheelElement) {
        wheelElement.removeEventListener('wheel', handleWheel);
      }
    };
  }, [rotation, modules.length, isExpanded]);

  const getPositionStyles = () => {
    const positions = {
      left: 'left-8 top-1/2 -translate-y-1/2',
      right: 'right-8 top-1/2 -translate-y-1/2',
      bottom: 'bottom-8 left-1/2 -translate-x-1/2'
    };
    return positions[position];
  };

  const radius = 120;

  return (
    <div
      ref={wheelRef}
      className={`fixed ${getPositionStyles()} z-50`}
    >
      {/* Center Hub */}
      <motion.button
        className="relative w-16 h-16 rounded-full glass border border-purple-500/30 shadow-[0_0_30px_rgba(139,92,246,0.5)]"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="text-2xl">{isExpanded ? '✕' : '☰'}</span>
      </motion.button>

      {/* Module Wheel */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
        animate={{ rotate: rotation }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
      >
        {modules.map((module, index) => {
          const angle = (index * 360) / modules.length;
          const x = Math.cos((angle * Math.PI) / 180) * radius;
          const y = Math.sin((angle * Math.PI) / 180) * radius;
          const isSelected = index === selectedIndex;

          return (
            <motion.div
              key={module.id}
              className="absolute"
              initial={{ opacity: 0, scale: 0 }}
              animate={{
                opacity: isExpanded ? 1 : 0,
                scale: isExpanded ? 1 : 0,
                x: isExpanded ? x : 0,
                y: isExpanded ? y : 0,
              }}
              transition={{ delay: index * 0.05 }}
              style={{ transform: `translate(-50%, -50%)` }}
            >
              <motion.button
                className={`
                  w-14 h-14 rounded-full glass
                  ${isSelected ? 'border-2 border-purple-500' : 'border border-white/20'}
                  ${isSelected ? 'shadow-[0_0_20px_rgba(139,92,246,0.8)]' : ''}
                  flex items-center justify-center
                  hover:scale-110 transition-all
                `}
                whileHover={{ scale: 1.2 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => onSelectModule(module)}
                animate={{ rotate: -rotation }}
              >
                <span className="text-xl">{module.icon}</span>
              </motion.button>
              {isSelected && (
                <motion.div
                  className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <span className="text-xs text-purple-300 font-medium">
                    {module.name}
                  </span>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
};