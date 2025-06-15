import React, { useEffect, useRef } from 'react';
import eventBus from '../../lib/eventBus';
import { motion } from 'framer-motion';
import { ModuleContainer } from '../system/ModuleContainer';

interface ConsciousnessEvent {
  type: string;
  source: string;
  time: number;
  state?: string;
}

interface ConsciousnessCoreProps {
  onEvent?: (event: ConsciousnessEvent) => void;
}

const ConsciousnessCore: React.FC<ConsciousnessCoreProps> = ({ onEvent }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    function draw() {
      if (!ctx || !canvas) return;
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw consciousness visualization
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const radius = Math.min(canvas.width, canvas.height) * 0.4;
      
      // Draw consciousness field
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
      gradient.addColorStop(0, 'rgba(147, 51, 234, 0.8)');
      gradient.addColorStop(1, 'rgba(147, 51, 234, 0)');
      
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
      
      // Draw consciousness particles
      const time = Date.now() / 1000;
      const numParticles = 12;
      for (let i = 0; i < numParticles; i++) {
        const angle = (i / numParticles) * Math.PI * 2 + time;
        const x = centerX + Math.cos(angle) * radius * 0.7;
        const y = centerY + Math.sin(angle) * radius * 0.7;
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fill();
      }
    }

    const animate = () => {
      draw();
      requestAnimationFrame(animate);
    };

    animate();

    // Event handling
    const handleEvent = (e: CustomEvent) => {
      if (onEvent) onEvent(e.detail);
    };

    eventBus.addEventListener('consciousness:fluctuation', handleEvent as EventListener);
    eventBus.addEventListener('consciousness:collapse', handleEvent as EventListener);

    return () => {
      eventBus.removeEventListener('consciousness:fluctuation', handleEvent as EventListener);
      eventBus.removeEventListener('consciousness:collapse', handleEvent as EventListener);
    };
  }, [onEvent]);

  const emitFluctuation = () => {
    const event = { 
      type: 'consciousness:fluctuation', 
      source: 'ConsciousnessCore', 
      time: Date.now(),
      state: 'multi-state'
    };
    eventBus.dispatchEvent(new CustomEvent('consciousness:fluctuation', { detail: event }));
    if (onEvent) onEvent(event);
  };

  return (
    <ModuleContainer
      config={{
        id: 'consciousness-core',
        title: 'Consciousness Core',
        category: 'consciousness',
        size: 'md',
        breathingSpeed: 6,
        draggable: true,
        minimizable: true,
      }}
    >
      <div className="flex flex-col items-center justify-center gap-4">
        <motion.canvas
          ref={canvasRef}
          width={300}
          height={200}
          className="rounded-full glass-consciousness shadow-lg animate-breathe"
        />
        <button
          className="glass-consciousness px-4 py-2 rounded-lg text-white font-bold shadow-glow-md hover:bg-consciousness-700/40 transition"
          onClick={emitFluctuation}
        >
          Emit Fluctuation
        </button>
      </div>
    </ModuleContainer>
  );
};

export default ConsciousnessCore; 