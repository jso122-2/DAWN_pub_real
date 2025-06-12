import React, { useState, useRef } from 'react';
import { motion, useAnimation } from 'framer-motion';

interface Module {
  id: string;
  name: string;
  icon: string;
  preview?: React.ReactNode;
}

interface ModuleWheelProps {
  modules: Module[];
  onActivateModule: (id: string) => void;
}

const RADIUS = 120;

const ModuleWheel: React.FC<ModuleWheelProps> = ({ modules, onActivateModule }) => {
  const [rotation, setRotation] = useState(0);
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const wheelRef = useRef<HTMLDivElement>(null);
  const controls = useAnimation();

  // Handle mouse wheel for rotation
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 1 : -1;
    const newIndex = (selectedIndex + delta + modules.length) % modules.length;
    setSelectedIndex(newIndex);
    setRotation((prev) => prev + delta * (360 / modules.length));
  };

  // Handle click to activate
  const handleClick = (index: number) => {
    setSelectedIndex(index);
    onActivateModule(modules[index].id);
  };

  return (
    <div
      ref={wheelRef}
      className="relative w-72 h-72 flex items-center justify-center select-none"
      onWheel={handleWheel}
      style={{ perspective: 800 }}
    >
      {/* Carousel */}
      <motion.div
        animate={{ rotate: rotation }}
        transition={{ type: 'spring', stiffness: 120, damping: 18 }}
        className="absolute top-1/2 left-1/2"
        style={{ transform: 'translate(-50%, -50%)' }}
      >
        {modules.map((mod, i) => {
          const angle = (i * 360) / modules.length;
          const rad = (angle * Math.PI) / 180;
          const x = Math.cos(rad) * RADIUS;
          const y = Math.sin(rad) * RADIUS;
          const isHovered = hoveredIndex === i;
          const isSelected = selectedIndex === i;
          return (
            <motion.button
              key={mod.id}
              className={`absolute w-16 h-16 rounded-full glass flex items-center justify-center border-2 transition-all duration-300 ${
                isSelected ? 'border-purple-400 shadow-[0_0_24px_#a78bfa99]' : 'border-white/20'
              } ${isHovered ? 'scale-110 z-20' : ''}`}
              style={{
                left: x + 144,
                top: y + 144,
                zIndex: isHovered ? 2 : 1,
              }}
              onMouseEnter={() => setHoveredIndex(i)}
              onMouseLeave={() => setHoveredIndex(null)}
              onClick={() => handleClick(i)}
              whileHover={{ scale: 1.15 }}
              whileTap={{ scale: 0.95 }}
              animate={{ rotate: -rotation }}
            >
              <span className="text-2xl">{mod.icon}</span>
              {/* Preview on hover */}
              {isHovered && mod.preview && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  className="absolute left-1/2 top-full mt-2 -translate-x-1/2 z-30 min-w-[180px]"
                >
                  <div className="glass rounded-xl p-4 shadow-lg border border-purple-500/20">
                    {mod.preview}
                  </div>
                </motion.div>
              )}
            </motion.button>
          );
        })}
      </motion.div>
      {/* Center hub */}
      <motion.div
        className="absolute top-1/2 left-1/2 w-20 h-20 rounded-full glass border-2 border-purple-500 flex items-center justify-center shadow-[0_0_32px_#a78bfa55]"
        style={{ transform: 'translate(-50%, -50%)' }}
        whileHover={{ scale: 1.08 }}
      >
        <span className="text-3xl text-purple-400">☰</span>
      </motion.div>
    </div>
  );
};

export default ModuleWheel; 