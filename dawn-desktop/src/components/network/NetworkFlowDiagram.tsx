import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { useCosmicStore } from '../../store/cosmic.store';
import PropTypes from 'prop-types';

interface NetworkFlowDiagramProps {
  scup: number;
  entropy: number;
  heat: number;
  mood: string;
}

const COSMIC_COLORS = {
  purple: '#a78bfa',
  cyan: '#22d3ee',
  pink: '#f472b6',
};

// Particle class for flow animation
class Particle {
  startNode: { x: number; y: number; color: string };
  endNode: { x: number; y: number; color: string };
  progress: number;
  speed: number;
  size: number;
  color: string;
  opacity: number;
  trail: { x: number; y: number; opacity: number }[];
  maxTrailLength: number;
  constructor(startNode: { x: number; y: number; color: string }, endNode: { x: number; y: number; color: string }, value: number, color: string) {
    this.startNode = startNode;
    this.endNode = endNode;
    this.progress = 0;
    this.speed = 0.5 + value * 1.5;
    this.size = 2 + value * 4;
    this.color = color;
    this.opacity = 0.3 + value * 0.7;
    this.trail = [];
    this.maxTrailLength = 10;
  }
  update(deltaTime: number) {
    this.progress += this.speed * deltaTime * 0.001;
    const currentPos = this.getCurrentPosition();
    this.trail.push({ ...currentPos, opacity: this.opacity });
    if (this.trail.length > this.maxTrailLength) {
      this.trail.shift();
    }
    return this.progress >= 1;
  }
  getCurrentPosition() {
    const t = this.easeInOutCubic(this.progress);
    return {
      x: this.startNode.x + (this.endNode.x - this.startNode.x) * t,
      y: this.startNode.y + (this.endNode.y - this.startNode.y) * t,
    };
  }
  easeInOutCubic(t: number) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }
  draw(ctx: CanvasRenderingContext2D, width: number, height: number) {
    // Draw trail with glow
    this.trail.forEach((point, index) => {
      const trailOpacity = (index / this.trail.length) * point.opacity * 0.5;
      ctx.save();
      ctx.globalAlpha = trailOpacity;
      ctx.shadowBlur = 12;
      ctx.shadowColor = this.color;
      ctx.beginPath();
      ctx.arc(point.x * width, point.y * height, this.size * 0.7, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();
      ctx.restore();
    });
    // Draw main particle with glow
    const pos = this.getCurrentPosition();
    ctx.save();
    ctx.globalAlpha = this.opacity;
    ctx.shadowBlur = 24;
    ctx.shadowColor = this.color;
    ctx.beginPath();
    ctx.arc(pos.x * width, pos.y * height, this.size, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.restore();
  }
}

const NetworkFlowDiagram: React.FC<Partial<NetworkFlowDiagramProps>> = (props) => {
  // Use real-time data from store if not provided
  const store = useCosmicStore();
  const scup = props.scup ?? store.neuralActivity;
  const entropy = props.entropy ?? store.entropy;
  const heat = props.heat ?? store.systemLoad;
  const mood = props.mood ?? 'neutral';

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationRef = useRef<number | null>(null);
  const particlesRef = useRef<Particle[]>([]);
  const [dimensions, setDimensions] = useState({ width: 800, height: 400 });

  // Node positions and cosmic colors
  const nodes = {
    scup: { x: 0.2, y: 0.3, label: 'SCUP', color: COSMIC_COLORS.purple },
    entropy: { x: 0.2, y: 0.7, label: 'ENTROPY', color: COSMIC_COLORS.cyan },
    heat: { x: 0.5, y: 0.2, label: 'HEAT', color: COSMIC_COLORS.pink },
    mood: { x: 0.5, y: 0.8, label: 'MOOD', color: COSMIC_COLORS.purple },
    core: { x: 0.8, y: 0.5, label: 'CORE', color: COSMIC_COLORS.cyan },
  };

  // Create particles based on metric values
  const createParticles = () => {
    const particles: Particle[] = [];
    // SCUP → CORE flow
    if (scup > 0.1 && Math.random() < scup * 0.1) {
      particles.push(new Particle(nodes.scup, nodes.core, scup, nodes.scup.color));
    }
    // ENTROPY → CORE flow
    if (entropy > 0.1 && Math.random() < entropy * 0.1) {
      particles.push(new Particle(nodes.entropy, nodes.core, entropy, nodes.entropy.color));
    }
    // HEAT → MOOD flow
    if (heat > 0.1 && Math.random() < heat * 0.08) {
      particles.push(new Particle(nodes.heat, nodes.mood, heat, nodes.heat.color));
    }
    // MOOD → CORE flow (bidirectional)
    if (Math.random() < 0.05) {
      const moodValue = mood === 'excited' ? 0.8 : mood === 'calm' ? 0.5 : 0.3;
      particles.push(new Particle(nodes.mood, nodes.core, moodValue, nodes.mood.color));
    }
    // CORE → SCUP feedback
    if (Math.random() < 0.03) {
      particles.push(new Particle(nodes.core, nodes.scup, 0.5, nodes.core.color));
    }
    return particles;
  };

  // Animation loop
  const animate = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const { width, height } = canvas;
    // Transparent background
    ctx.clearRect(0, 0, width, height);
    // Draw connections (cosmic theme)
    ctx.save();
    ctx.strokeStyle = COSMIC_COLORS.purple;
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    const connections: [typeof nodes[keyof typeof nodes], typeof nodes[keyof typeof nodes]][] = [
      [nodes.scup, nodes.core],
      [nodes.entropy, nodes.core],
      [nodes.heat, nodes.mood],
      [nodes.mood, nodes.core],
      [nodes.core, nodes.scup],
    ];
    connections.forEach(([start, end]) => {
      ctx.beginPath();
      ctx.moveTo(start.x * width, start.y * height);
      ctx.lineTo(end.x * width, end.y * height);
      ctx.stroke();
    });
    ctx.setLineDash([]);
    ctx.restore();
    // Update and draw particles
    const newParticles = createParticles();
    particlesRef.current.push(...newParticles);
    particlesRef.current = particlesRef.current.filter((particle) => {
      const isDone = particle.update(16);
      if (!isDone) {
        particle.draw(ctx, width, height);
      }
      return !isDone;
    });
    // Draw nodes (cosmic theme, glow)
    Object.entries(nodes).forEach(([key, node]) => {
      const x = node.x * width;
      const y = node.y * height;
      const radius = key === 'core' ? 30 : 25;
      // Node glow
      ctx.save();
      ctx.shadowBlur = 32;
      ctx.shadowColor = node.color;
      ctx.beginPath();
      ctx.arc(x, y, radius * 1.5, 0, Math.PI * 2);
      ctx.fillStyle = node.color + '22';
      ctx.fill();
      ctx.restore();
      // Node circle
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = '#18181b';
      ctx.strokeStyle = node.color;
      ctx.lineWidth = 3;
      ctx.fill();
      ctx.stroke();
      ctx.restore();
      // Node label
      ctx.save();
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 13px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(node.label, x, y - 8);
      // Value display
      let value = '';
      if (key === 'scup') value = scup.toFixed(3);
      else if (key === 'entropy') value = entropy.toFixed(3);
      else if (key === 'heat') value = heat.toFixed(3);
      else if (key === 'mood') value = mood.substring(0, 3).toUpperCase();
      else if (key === 'core') value = '∞';
      ctx.font = '11px monospace';
      ctx.fillStyle = node.color;
      ctx.fillText(value, x, y + 12);
      ctx.restore();
    });
    animationRef.current = requestAnimationFrame(animate);
  };

  // Handle resize
  useEffect(() => {
    const handleResize = () => {
      const canvas = canvasRef.current;
      if (canvas && canvas.parentElement) {
        const rect = canvas.parentElement.getBoundingClientRect();
        setDimensions({
          width: rect.width,
          height: Math.min(rect.height, 400),
        });
      }
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Start animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = dimensions.width;
      canvas.height = dimensions.height;
      animationRef.current = requestAnimationFrame(animate);
    }
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
    // eslint-disable-next-line
  }, [dimensions, scup, entropy, heat, mood]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="rounded-lg p-4 h-full bg-transparent"
    >
      <h3 className="text-lg font-semibold text-purple-300 mb-2">Network Flow Diagram</h3>
      <div className="relative w-full h-full min-h-[300px]">
        <canvas
          ref={canvasRef}
          className="w-full h-full"
          style={{ maxHeight: '400px', background: 'transparent' }}
        />
      </div>
    </motion.div>
  );
};

NetworkFlowDiagram.propTypes = {
  scup: PropTypes.number,
  entropy: PropTypes.number,
  heat: PropTypes.number,
  mood: PropTypes.string
};

export default NetworkFlowDiagram; 