import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import eventBus from '../../lib/eventBus';
import { ModuleContainer } from '../system/ModuleContainer';

interface NeuralEvent {
  type: string;
  source: string;
  time: number;
}

interface NeuralProcessorProps {
  onEvent?: (event: NeuralEvent) => void;
}

const NeuralProcessor: React.FC<NeuralProcessorProps> = ({ onEvent }) => {
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
      
      // Draw neural network visualization
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const radius = Math.min(canvas.width, canvas.height) * 0.4;
      
      // Draw nodes
      const numNodes = 8;
      for (let i = 0; i < numNodes; i++) {
        const angle = (i / numNodes) * Math.PI * 2;
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(139, 92, 246, 0.8)';
        ctx.fill();
      }
      
      // Draw connections
      ctx.strokeStyle = 'rgba(139, 92, 246, 0.3)';
      ctx.lineWidth = 1;
      for (let i = 0; i < numNodes; i++) {
        const angle1 = (i / numNodes) * Math.PI * 2;
        const x1 = centerX + Math.cos(angle1) * radius;
        const y1 = centerY + Math.sin(angle1) * radius;
        
        for (let j = i + 1; j < numNodes; j++) {
          const angle2 = (j / numNodes) * Math.PI * 2;
          const x2 = centerX + Math.cos(angle2) * radius;
          const y2 = centerY + Math.sin(angle2) * radius;
          
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.stroke();
        }
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

    eventBus.addEventListener('neural:spike', handleEvent as EventListener);
    eventBus.addEventListener('neural:pattern', handleEvent as EventListener);

    return () => {
      eventBus.removeEventListener('neural:spike', handleEvent as EventListener);
      eventBus.removeEventListener('neural:pattern', handleEvent as EventListener);
    };
  }, [onEvent]);

  const emitSpike = () => {
    const event = { type: 'neural:spike', source: 'NeuralProcessor', time: Date.now() };
    eventBus.dispatchEvent(new CustomEvent('neural:spike', { detail: event }));
    if (onEvent) onEvent(event);
  };

  useEffect(() => {
    // Example: listen for quantum:collapse event
    const handler = (data: CustomEvent) => {
      if (data.type === 'quantum:collapse') {
        // Could trigger a visual effect
      }
    };
    eventBus.addEventListener('quantum:collapse', handler as EventListener);
    return () => eventBus.removeEventListener('quantum:collapse', handler as EventListener);
  }, []);

  return (
    <ModuleContainer
      config={{
        id: 'neural-processor',
        title: 'Neural Processor',
        category: 'neural',
        size: 'md',
        breathingSpeed: 4,
        draggable: true,
        minimizable: true,
      }}
    >
      <div className="flex flex-col items-center justify-center gap-4">
        <motion.canvas
          ref={canvasRef}
          width={300}
          height={200}
          className="rounded-xl glass-neural shadow-lg animate-breathe"
        />
        <button
          className="glass-neural px-4 py-2 rounded-lg text-white font-bold shadow-glow-md hover:bg-neural-700/40 transition"
          onClick={emitSpike}
        >
          Emit Neural Spike
        </button>
      </div>
    </ModuleContainer>
  );
};

export default NeuralProcessor; 