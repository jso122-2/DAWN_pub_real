import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { useConsciousness } from '../../hooks/useConsciousness';
import { TerminalInput } from './TerminalInput';
import { DataModule } from './DataModule';
import { ConsciousnessState } from '../../types/consciousness.types';

interface NeuralNode {
  id: string;
  x: number;
  y: number;
  active: boolean;
  connections: string[];
  activity: number;
}

interface NeuralTerminalProps {
  moduleId: string;
  className?: string;
}

export const NeuralTerminal: React.FC<NeuralTerminalProps> = ({
  moduleId,
  className = ''
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [nodes, setNodes] = useState<NeuralNode[]>([]);
  const [isSimulating, setIsSimulating] = useState(true);
  const [isConnected, setIsConnected] = useState(true);
  const consciousness = useConsciousness();

  // Initialize neural network
  useEffect(() => {
    const nodeCount = 12;
    const radius = 180;
    const newNodes: NeuralNode[] = [];

    for (let i = 0; i < nodeCount; i++) {
      const angle = (i / nodeCount) * Math.PI * 2;
      newNodes.push({
        id: `node-${i}`,
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        active: Math.random() > 0.6,
        connections: [],
        activity: Math.random()
      });
    }

    // Create connections
    newNodes.forEach((node, i) => {
      const connectionCount = Math.floor(Math.random() * 3) + 1;
      for (let j = 0; j < connectionCount; j++) {
        const targetIndex = (i + j + 1) % newNodes.length;
        node.connections.push(newNodes[targetIndex].id);
      }
    });

    setNodes(newNodes);
  }, []);

  // Render neural network
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      // Clear canvas with terminal-style background
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw connections
      nodes.forEach(node => {
        node.connections.forEach(targetId => {
          const target = nodes.find(n => n.id === targetId);
          if (!target) return;

          const strength = node.activity * target.activity;
          ctx.strokeStyle = `rgba(0, 255, 136, ${strength * 0.5})`;
          ctx.lineWidth = Math.max(1, strength * 3);

          ctx.beginPath();
          ctx.moveTo(node.x + canvas.width / 2, node.y + canvas.height / 2);
          ctx.lineTo(target.x + canvas.width / 2, target.y + canvas.height / 2);
          ctx.stroke();
        });
      });

      // Draw nodes
      nodes.forEach(node => {
        const x = node.x + canvas.width / 2;
        const y = node.y + canvas.height / 2;
        const radius = 5 + node.activity * 10;

        // Glow effect
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2);
        gradient.addColorStop(0, `rgba(0, 255, 136, ${node.activity})`);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
        ctx.fill();

        // Node core
        ctx.fillStyle = 'rgb(0, 255, 136)';
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      });

      // Update node activities
      if (isSimulating) {
        setNodes(prev => prev.map(node => ({
          ...node,
          activity: Math.max(0, Math.min(1,
            node.activity + (Math.random() - 0.5) * 0.1 * consciousness.neuralActivity
          ))
        })));
      }

      requestAnimationFrame(render);
    };

    render();
  }, [nodes, isSimulating, consciousness.neuralActivity]);

  return (
    <motion.div
      className={`terminal-border p-4 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h3 className="text-terminal-green font-mono">NEURAL TERMINAL</h3>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-terminal-green' : 'bg-terminal-red'}`} />
        </div>
        <div className="flex items-center gap-4">
          <DataModule
            title="Neural Activity"
            value={`${(consciousness.neuralActivity * 100).toFixed(1)}%`}
            status="active"
            className="w-32"
          />
          <DataModule
            title="SCUP"
            value={`${consciousness.scup.toFixed(1)}`}
            status={consciousness.scup > 50 ? 'active' : 'warning'}
            className="w-32"
          />
        </div>
      </div>

      {/* Neural Network Canvas */}
      <div className="relative w-full h-[400px] mb-4">
        <canvas
          ref={canvasRef}
          width={800}
          height={400}
          className="w-full h-full"
        />
      </div>

      {/* Terminal Input */}
      <TerminalInput
        onCommand={(cmd) => console.log('Neural command:', cmd)}
        prompt="NEURAL://>"
        className="w-full"
      />
    </motion.div>
  );
}; 