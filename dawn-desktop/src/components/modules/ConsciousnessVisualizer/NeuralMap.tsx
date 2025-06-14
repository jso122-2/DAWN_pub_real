import React, { useRef, useEffect } from 'react';
import { useConsciousness } from '../../../hooks/useConsciousness';
import * as styles from './ConsciousnessVisualizer.styles';

interface NeuralMapProps {
  fullscreen?: boolean;
}

export const NeuralMap: React.FC<NeuralMapProps> = ({ fullscreen }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const consciousness = useConsciousness();
  const nodesRef = useRef<any[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Initialize neural network if needed
    if (nodesRef.current.length === 0) {
      const layers = 5;
      const nodesPerLayer = [3, 5, 7, 5, 3];
      
      nodesPerLayer.forEach((count, layer) => {
        for (let i = 0; i < count; i++) {
          nodesRef.current.push({
            id: `node-${layer}-${i}`,
            layer,
            position: {
              x: (layer / (layers - 1)) * 0.8 + 0.1,
              y: (i / (count - 1)) * 0.8 + 0.1
            },
            activation: Math.random(),
            connections: []
          });
        }
      });

      // Create connections
      for (let l = 0; l < layers - 1; l++) {
        const currentLayer = nodesRef.current.filter(n => n.layer === l);
        const nextLayer = nodesRef.current.filter(n => n.layer === l + 1);
        
        currentLayer.forEach(node => {
          nextLayer.forEach(next => {
            if (Math.random() > 0.3) {
              node.connections.push({
                to: next.id,
                weight: Math.random() * 2 - 1
              });
            }
          });
        });
      }
    }

    const render = () => {
      // Clear canvas
      ctx.fillStyle = 'rgba(15, 23, 42, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update activations based on consciousness
      nodesRef.current.forEach(node => {
        node.activation = Math.max(0, Math.min(1,
          node.activation + (Math.random() - 0.5) * 0.1 * consciousness.neuralActivity
        ));
      });

      // Draw connections
      nodesRef.current.forEach(node => {
        node.connections.forEach((conn: any) => {
          const target = nodesRef.current.find(n => n.id === conn.to);
          if (!target) return;

          const startX = node.position.x * canvas.width;
          const startY = node.position.y * canvas.height;
          const endX = target.position.x * canvas.width;
          const endY = target.position.y * canvas.height;

          const strength = node.activation * target.activation;
          ctx.strokeStyle = `rgba(59, 130, 246, ${strength * 0.5})`;
          ctx.lineWidth = Math.abs(conn.weight) * 2;

          ctx.beginPath();
          ctx.moveTo(startX, startY);
          ctx.lineTo(endX, endY);
          ctx.stroke();
        });
      });

      // Draw nodes
      nodesRef.current.forEach(node => {
        const x = node.position.x * canvas.width;
        const y = node.position.y * canvas.height;
        const radius = 5 + node.activation * 10;

        // Glow
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2);
        gradient.addColorStop(0, `hsla(${200 + node.activation * 60}, 70%, 50%, ${node.activation})`);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
        ctx.fill();

        // Core
        ctx.fillStyle = `hsl(${200 + node.activation * 60}, 70%, 50%)`;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      });

      requestAnimationFrame(render);
    };

    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    render();

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [consciousness]);

  return (
    <div className={styles.particleContainer(fullscreen)}>
      <canvas ref={canvasRef} className={styles.canvas} />
      <div className={styles.particleInfo}>
        <span>Neural Activity: {(consciousness.neuralActivity * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
}; 