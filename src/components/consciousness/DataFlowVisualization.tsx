import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { moduleCommunicationHub, ModuleMessage } from '../../services/ModuleCommunicationHub';

interface FlowParticle {
  id: string;
  message: ModuleMessage;
  startTime: number;
  duration: number;
  path: { x: number; y: number }[];
}

export const DataFlowVisualization: React.FC = () => {
  const [particles, setParticles] = useState<FlowParticle[]>([]);
  const [modulePositions, setModulePositions] = useState<Map<string, { x: number; y: number }>>(new Map());

  useEffect(() => {
    const updateModulePositions = () => {
      const positions = new Map();
      const moduleElements = document.querySelectorAll('[data-module-id]');
      
      moduleElements.forEach(element => {
        const moduleId = element.getAttribute('data-module-id');
        const rect = element.getBoundingClientRect();
        if (moduleId) {
          positions.set(moduleId, {
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2
          });
        }
      });
      
      setModulePositions(positions);
    };

    updateModulePositions();
    const interval = setInterval(updateModulePositions, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleMessageFlow = (message: ModuleMessage) => {
      const sourcePos = modulePositions.get(message.sourceModuleId);
      const targetPos = message.targetModuleId ? modulePositions.get(message.targetModuleId) : null;

      if (!sourcePos) return;

      const particle: FlowParticle = {
        id: message.id,
        message,
        startTime: Date.now(),
        duration: targetPos ? 2000 : 1000,
        path: targetPos ? [sourcePos, targetPos] : [sourcePos, { x: sourcePos.x, y: sourcePos.y - 50 }]
      };

      setParticles(prev => [...prev, particle]);

      setTimeout(() => {
        setParticles(prev => prev.filter(p => p.id !== particle.id));
      }, particle.duration + 500);
    };

    moduleCommunicationHub.on('messageFlow', handleMessageFlow);
    return () => {
      moduleCommunicationHub.off('messageFlow', handleMessageFlow);
    };
  }, [modulePositions]);

  const getParticleColor = (type: string) => {
    const colors = {
      consciousness_update: '#4FC3F7',
      neural_spike: '#9C27B0',
      memory_access: '#FF9800',
      process_complete: '#4CAF50',
      custom: '#9E9E9E'
    };
    return colors[type as keyof typeof colors] || colors.custom;
  };

  return (
    <div className="fixed inset-0 pointer-events-none z-10">
      <svg className="w-full h-full">
        <defs>
          <filter id="particle-glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <AnimatePresence>
          {particles.map(particle => {
            const color = getParticleColor(particle.message.type);
            const [start, end] = particle.path;
            
            return (
              <motion.circle
                key={particle.id}
                r={particle.message.priority === 'critical' ? 6 : 4}
                fill={color}
                filter="url(#particle-glow)"
                initial={{ 
                  cx: start.x, 
                  cy: start.y,
                  opacity: 0,
                  scale: 0
                }}
                animate={{ 
                  cx: end.x, 
                  cy: end.y,
                  opacity: [0, 1, 1, 0],
                  scale: [0, 1, 1, 0]
                }}
                exit={{ opacity: 0, scale: 0 }}
                transition={{ 
                  duration: particle.duration / 1000,
                  ease: "easeInOut"
                }}
              />
            );
          })}
        </AnimatePresence>
      </svg>
    </div>
  );
}; 