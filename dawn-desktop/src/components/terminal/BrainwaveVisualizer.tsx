import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useConsciousness } from '../../hooks/useConsciousness';

interface BrainwaveVisualizerProps {
  className?: string;
}

type BrainwaveType = 'delta' | 'theta' | 'alpha' | 'beta' | 'gamma' | 'high_gamma';

interface Brainwave {
  type: BrainwaveType;
  frequency: number;
  amplitude: number;
  phase: number;
}

const BRAINWAVE_CONFIG = {
  delta: { min: 0.5, max: 4, color: '#00ff88' },
  theta: { min: 4, max: 8, color: '#4dabf7' },
  alpha: { min: 8, max: 13, color: '#66d9ef' },
  beta: { min: 13, max: 30, color: '#ffd43b' },
  gamma: { min: 30, max: 100, color: '#ff6b6b' },
  high_gamma: { min: 100, max: 200, color: '#c084fc' }
};

export const BrainwaveVisualizer: React.FC<BrainwaveVisualizerProps> = ({
  className = ''
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const consciousness = useConsciousness();
  const brainwavesRef = useRef<Brainwave[]>([]);

  // Initialize brainwaves
  useEffect(() => {
    const brainwaves: Brainwave[] = Object.keys(BRAINWAVE_CONFIG).map(type => ({
      type: type as BrainwaveType,
      frequency: BRAINWAVE_CONFIG[type as BrainwaveType].min + 
        Math.random() * (BRAINWAVE_CONFIG[type as BrainwaveType].max - BRAINWAVE_CONFIG[type as BrainwaveType].min),
      amplitude: Math.random() * 0.5 + 0.5,
      phase: Math.random() * Math.PI * 2
    }));
    brainwavesRef.current = brainwaves;
  }, []);

  // Render brainwaves
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      // Clear canvas with terminal-style background
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const time = Date.now() / 1000;
      const centerY = canvas.height / 2;

      // Draw each brainwave
      brainwavesRef.current.forEach((wave, index) => {
        const config = BRAINWAVE_CONFIG[wave.type];
        const yOffset = (index - brainwavesRef.current.length / 2) * 40;
        
        ctx.beginPath();
        ctx.strokeStyle = config.color;
        ctx.lineWidth = 2;

        // Draw the wave
        for (let x = 0; x < canvas.width; x++) {
          const t = x / canvas.width * 10 + time;
          const y = centerY + yOffset + 
            Math.sin(t * wave.frequency + wave.phase) * 
            wave.amplitude * 30 * 
            consciousness.neuralActivity;

          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }

        ctx.stroke();

        // Draw label
        ctx.fillStyle = config.color;
        ctx.font = '12px "JetBrains Mono"';
        ctx.fillText(
          `${wave.type.toUpperCase()} (${wave.frequency.toFixed(1)}Hz)`,
          10,
          centerY + yOffset - 20
        );
      });

      requestAnimationFrame(render);
    };

    render();
  }, [consciousness.neuralActivity]);

  return (
    <motion.div
      className={`terminal-border p-4 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-terminal-green font-mono">BRAINWAVE PATTERNS</h3>
        <div className="text-xs text-gray-400 font-mono">
          Neural Activity: {(consciousness.neuralActivity * 100).toFixed(1)}%
        </div>
      </div>

      <div className="relative w-full h-[300px]">
        <canvas
          ref={canvasRef}
          width={800}
          height={300}
          className="w-full h-full"
        />
      </div>
    </motion.div>
  );
}; 