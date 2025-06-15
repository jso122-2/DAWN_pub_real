import React from 'react';
import { motion } from 'framer-motion';

interface Connection {
  from: string;
  to: string;
  type?: 'consciousness' | 'neural';
}

interface ConnectionLayerProps {
  positions: Record<string, { x: number; y: number }>;
  connections: Connection[];
  width?: number;
  height?: number;
}

const COLOR_MAP = {
  consciousness: 'var(--consciousness-400)',
  neural: 'var(--neural-400)',
  default: 'var(--consciousness-400)',
};

const PULSE_ANIMATION = {
  animate: {
    strokeDashoffset: [0, 40, 0],
    opacity: [0.7, 1, 0.7],
  },
  transition: {
    duration: 1.6,
    repeat: Infinity,
    ease: 'easeInOut',
  },
};

export const ConnectionLayer: React.FC<ConnectionLayerProps> = ({ positions, connections, width = 1600, height = 900 }) => {
  // Helper to get control points for bezier
  const getCurve = (from: { x: number; y: number }, to: { x: number; y: number }) => {
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const curve = Math.max(60, Math.abs(dx) * 0.4);
    const c1 = { x: from.x + curve, y: from.y };
    const c2 = { x: to.x - curve, y: to.y };
    return `M${from.x},${from.y} C${c1.x},${c1.y} ${c2.x},${c2.y} ${to.x},${to.y}`;
  };

  return (
    <svg className="absolute inset-0 w-full h-full pointer-events-none z-0" width={width} height={height} style={{ overflow: 'visible' }}>
      {connections.map((conn, i) => {
        const from = positions[conn.from];
        const to = positions[conn.to];
        if (!from || !to) return null;
        const color = COLOR_MAP[conn.type || 'default'] || COLOR_MAP.default;
        const path = getCurve(
          { x: from.x + 180, y: from.y + 40 },
          { x: to.x + 40, y: to.y + 40 }
        );
        return (
          <motion.path
            key={i}
            d={path}
            stroke={color}
            strokeWidth={4}
            fill="none"
            strokeDasharray="20 20"
            initial={{ strokeDashoffset: 0, opacity: 0.7 }}
            animate={PULSE_ANIMATION.animate}
            transition={PULSE_ANIMATION.transition}
            style={{ filter: `drop-shadow(0 0 12px ${color})` }}
          />
        );
      })}
    </svg>
  );
};

export default ConnectionLayer; 