import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

// Types
interface LayoutPosition {
  x: number;
  y: number;
  w: number;
  h: number;
}

// Example module definitions
const MODULES = [
  { id: 'neural', name: 'Neural Core', color: 'var(--color-neural-primary)' },
  { id: 'quantum', name: 'Quantum Interface', color: 'var(--color-quantum-primary)' },
  { id: 'entropy', name: 'Entropy Visualizer', color: 'var(--color-chaos-primary)' },
  { id: 'metrics', name: 'Metrics Panel', color: 'var(--color-process-primary)' },
  { id: 'radar', name: 'Cognitive Radar', color: 'var(--color-neural-accent)' },
  { id: 'events', name: 'Event Stream', color: 'var(--color-chaos-accent)' },
];

const PRESET_LAYOUTS: Record<string, Record<string, LayoutPosition>> = {
  Focus: {
    neural: { x: 1, y: 1, w: 2, h: 2 },
    metrics: { x: 3, y: 1, w: 1, h: 1 },
    radar: { x: 3, y: 2, w: 1, h: 1 },
  },
  Dashboard: {
    neural: { x: 1, y: 1, w: 2, h: 2 },
    quantum: { x: 3, y: 1, w: 1, h: 1 },
    entropy: { x: 3, y: 2, w: 1, h: 1 },
    metrics: { x: 1, y: 3, w: 1, h: 1 },
    radar: { x: 2, y: 3, w: 1, h: 1 },
    events: { x: 3, y: 3, w: 1, h: 1 },
  },
  Monitoring: {
    entropy: { x: 1, y: 1, w: 1, h: 2 },
    metrics: { x: 2, y: 1, w: 1, h: 1 },
    radar: { x: 2, y: 2, w: 1, h: 1 },
    events: { x: 3, y: 1, w: 1, h: 2 },
  },
};

const LOCAL_STORAGE_KEY = 'cosmic-layout';

function getInitialLayout(): Record<string, LayoutPosition> {
  const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
  if (saved) return JSON.parse(saved);
  return PRESET_LAYOUTS.Dashboard;
}

export const LayoutManager = () => {
  const [activeModules, setActiveModules] = useState<string[]>(Object.keys(getInitialLayout()));
  const [positions, setPositions] = useState<Record<string, LayoutPosition>>(getInitialLayout());
  const [preset, setPreset] = useState('Dashboard');
  const gridRef = useRef<HTMLDivElement>(null);

  // Save layout to localStorage
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(positions));
  }, [positions]);

  // Handle preset change
  const handlePreset = (name: string) => {
    setPositions(PRESET_LAYOUTS[name]);
    setActiveModules(Object.keys(PRESET_LAYOUTS[name]));
    setPreset(name);
  };

  // Handle module activation
  const activateModule = (id: string) => {
    if (!activeModules.includes(id)) {
      setActiveModules([...activeModules, id]);
      setPositions({ ...positions, [id]: { x: 2, y: 2, w: 1, h: 1 } });
    }
  };

  // Handle module drag (simple demo, not pixel-perfect)
  const handleDrag = (id: string, dx: number, dy: number) => {
    setPositions((pos: Record<string, LayoutPosition>) => ({
      ...pos,
      [id]: {
        ...pos[id],
        x: Math.max(1, pos[id].x + dx),
        y: Math.max(1, pos[id].y + dy),
      },
    }));
  };

  // Draw data flow connections (example: neural → metrics, entropy → radar)
  const connections = [
    ['neural', 'metrics'],
    ['entropy', 'radar'],
    ['metrics', 'events'],
  ];

  // Get module center positions for SVG lines
  const getModuleCenter = (id: string) => {
    const pos = positions[id];
    if (!pos || !gridRef.current) return { x: 0, y: 0 };
    const gridW = gridRef.current.offsetWidth / 4;
    const gridH = gridRef.current.offsetHeight / 4;
    return {
      x: (pos.x - 0.5 + pos.w / 2) * gridW,
      y: (pos.y - 0.5 + pos.h / 2) * gridH,
    };
  };

  return (
    <div className="relative w-full h-[700px] glass rounded-2xl p-6 bg-white/5 backdrop-blur-xl border border-purple-500/20 shadow-glow-md">
      {/* Preset Layout Buttons */}
      <div className="flex gap-2 mb-4">
        {Object.keys(PRESET_LAYOUTS).map(name => (
          <button
            key={name}
            onClick={() => handlePreset(name)}
            className={`px-4 py-1 rounded-full font-semibold border transition-all duration-300 ${preset === name ? 'bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-400 text-white' : 'bg-white/10 text-purple-200 border-white/10'}`}
          >
            {name}
          </button>
        ))}
        <button
          onClick={() => {
            localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(positions));
          }}
          className="ml-4 px-4 py-1 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-400/20"
        >Save Custom</button>
      </div>
      {/* Module Wheel */}
      <div className="absolute top-8 right-8 z-20">
        <div className="glass rounded-full p-4 shadow-glow-md flex flex-col items-center gap-2 bg-white/10">
          <span className="text-xs text-purple-200 mb-1">Module Wheel</span>
          {MODULES.map(m => (
            <button
              key={m.id}
              onClick={() => activateModule(m.id)}
              className="w-10 h-10 rounded-full flex items-center justify-center mb-1 border border-white/10 hover:scale-110 transition-all"
              style={{ background: m.color }}
              title={m.name}
            >
              <span className="text-xs font-bold text-white drop-shadow">{m.name[0]}</span>
            </button>
          ))}
        </div>
      </div>
      {/* Grid Layout */}
      <div ref={gridRef} className="relative w-full h-full grid grid-cols-4 grid-rows-4 gap-4">
        {/* SVG Connections */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0" style={{ overflow: 'visible' }}>
          {connections.map(([from, to], i) => {
            if (!positions[from] || !positions[to]) return null;
            const start = getModuleCenter(from);
            const end = getModuleCenter(to);
            return (
              <motion.line
                key={i}
                x1={start.x}
                y1={start.y}
                x2={end.x}
                y2={end.y}
                stroke="url(#cosmic-gradient)"
                strokeWidth={4}
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.7 }}
                transition={{ duration: 1, delay: i * 0.2 }}
                strokeLinecap="round"
                filter="url(#glow)"
              />
            );
          })}
          <defs>
            <linearGradient id="cosmic-gradient" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="var(--color-neural-primary)" />
              <stop offset="50%" stopColor="var(--color-chaos-primary)" />
              <stop offset="100%" stopColor="var(--color-quantum-primary)" />
            </linearGradient>
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="6" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
        </svg>
        {/* Module Panels */}
        {activeModules.map(id => {
          const m = MODULES.find(mod => mod.id === id);
          const pos = positions[id];
          if (!m || !pos) return null;
          return (
            <motion.div
              key={id}
              drag
              dragMomentum={false}
              dragConstraints={gridRef}
              onDragEnd={(_, info) => {
                // Snap to grid (simple)
                const dx = Math.round(info.point.x / (gridRef.current!.offsetWidth / 4)) - pos.x + 1;
                const dy = Math.round(info.point.y / (gridRef.current!.offsetHeight / 4)) - pos.y + 1;
                handleDrag(id, dx, dy);
              }}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="absolute shadow-glow-md glass rounded-xl p-6 flex flex-col items-center justify-center cursor-move select-none"
              style={{
                left: `calc((100% / 4) * ${pos.x - 1})`,
                top: `calc((100% / 4) * ${pos.y - 1})`,
                width: `calc((100% / 4) * ${pos.w})`,
                height: `calc((100% / 4) * ${pos.h})`,
                background: m.color,
                zIndex: 10 + pos.y,
                border: '2px solid var(--color-border-glass)',
                boxShadow: '0 0 32px 4px ' + m.color,
              }}
            >
              <span className="text-lg font-bold text-white drop-shadow mb-2">{m.name}</span>
              <span className="text-xs text-white/70">({id})</span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};