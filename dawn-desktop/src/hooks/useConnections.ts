import { useMemo } from 'react';

export interface ModulePosition {
  id: string;
  x: number;
  y: number;
}

export interface Connection {
  from: string;
  to: string;
}

export function useConnections(
  modules: ModulePosition[],
  connections: Connection[]
) {
  // Returns an array of SVG line/curve props for rendering connections
  return useMemo(() => {
    return connections.map((conn) => {
      const from = modules.find((m) => m.id === conn.from);
      const to = modules.find((m) => m.id === conn.to);
      if (!from || !to) return null;
      // You can use a straight line or a curve (e.g., quadratic Bezier)
      return {
        key: `${conn.from}-${conn.to}`,
        x1: from.x,
        y1: from.y,
        x2: to.x,
        y2: to.y,
        // Optionally, add animation or style props here
        stroke: 'url(#cosmic-gradient)',
        strokeWidth: 4,
        opacity: 0.7,
        filter: 'url(#glow)',
      };
    }).filter(Boolean);
  }, [modules, connections]);
} 