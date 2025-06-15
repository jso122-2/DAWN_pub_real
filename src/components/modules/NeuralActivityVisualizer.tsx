import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

export function NeuralActivityVisualizer({ moduleId = "neural-visualizer" }) {
  const { messages } = useModuleCommunication(
    moduleId, 
    'neural-visualizer', 
    ['neural_processing', 'spike_detection']
  );
  
  const [spikes, setSpikes] = useState<Array<{ id: string; intensity: number; timestamp: number }>>([]);
  const [activityLevel, setActivityLevel] = useState(0.5);

  // Listen for neural spike messages
  useEffect(() => {
    const neuralMessages = messages.filter(msg => msg.type === 'neural_spike');
    if (neuralMessages.length > 0) {
      const latestSpike = neuralMessages[neuralMessages.length - 1];
      const spike = {
        id: latestSpike.id,
        intensity: latestSpike.data.value || 0.8,
        timestamp: latestSpike.timestamp
      };
      
      setSpikes(prev => [...prev.slice(-9), spike]);
      setActivityLevel(spike.intensity);
      
      // Fade activity level back down
      setTimeout(() => {
        setActivityLevel(prev => prev * 0.7);
      }, 1000);
    }
  }, [messages]);

  // Generate neural nodes
  const nodes = Array.from({ length: 12 }, (_, i) => ({
    id: i,
    x: 20 + (i % 4) * 60,
    y: 20 + Math.floor(i / 4) * 50,
    activity: Math.random() * activityLevel
  }));

  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
      <div className="p-4 h-full">
        <h3 className="text-white/80 text-sm mb-4 font-mono">Neural Activity</h3>
        
        <div className="relative h-40 bg-black/20 rounded-lg overflow-hidden">
          <svg className="w-full h-full">
            {/* Neural connections */}
            {nodes.map((node, i) => 
              nodes.slice(i + 1).map((otherNode, j) => {
                const distance = Math.sqrt(
                  Math.pow(node.x - otherNode.x, 2) + 
                  Math.pow(node.y - otherNode.y, 2)
                );
                if (distance < 80) {
                  return (
                    <motion.line
                      key={`${i}-${j}`}
                      x1={node.x}
                      y1={node.y}
                      x2={otherNode.x}
                      y2={otherNode.y}
                      stroke="rgba(156, 39, 176, 0.3)"
                      strokeWidth={1 + (node.activity + otherNode.activity)}
                      animate={{
                        opacity: [0.2, 0.6, 0.2],
                        strokeWidth: [1, 2 + activityLevel * 2, 1]
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        delay: (i + j) * 0.1
                      }}
                    />
                  );
                }
                return null;
              })
            )}
            
            {/* Neural nodes */}
            {nodes.map((node) => (
              <motion.circle
                key={node.id}
                cx={node.x}
                cy={node.y}
                r={3 + node.activity * 5}
                fill={`rgba(156, 39, 176, ${0.6 + node.activity * 0.4})`}
                animate={{
                  r: [3, 3 + node.activity * 8, 3],
                  opacity: [0.6, 1, 0.6]
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: node.id * 0.1
                }}
              />
            ))}
          </svg>
          
          {/* Spike indicators */}
          <div className="absolute top-2 right-2">
            {spikes.slice(-3).map((spike, i) => (
              <motion.div
                key={spike.id}
                className="text-xs text-purple-300 font-mono"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                style={{ marginBottom: '2px' }}
              >
                SPIKE: {(spike.intensity * 100).toFixed(0)}%
              </motion.div>
            ))}
          </div>
        </div>

        <div className="mt-4 space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Activity Level</span>
            <span className="text-xs text-white font-mono">{(activityLevel * 100).toFixed(1)}%</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Recent Spikes</span>
            <span className="text-xs text-white font-mono">{spikes.length}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Messages</span>
            <span className="text-xs text-white font-mono">{messages.length}</span>
          </div>
        </div>
      </div>
    </LivingModuleWrapper>
  );
} 