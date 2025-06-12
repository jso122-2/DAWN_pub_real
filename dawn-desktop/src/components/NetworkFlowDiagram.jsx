import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';

const NetworkFlowDiagram = ({ scup = 0, entropy = 0, heat = 0, mood = "neutral" }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const particlesRef = useRef([]);
  const [dimensions, setDimensions] = useState({ width: 800, height: 400 });

  // Node positions
  const nodes = {
    scup: { x: 0.2, y: 0.3, label: 'SCUP', color: '#3B82F6' },
    entropy: { x: 0.2, y: 0.7, label: 'ENTROPY', color: '#10B981' },
    heat: { x: 0.5, y: 0.2, label: 'HEAT', color: '#EF4444' },
    mood: { x: 0.5, y: 0.8, label: 'MOOD', color: '#8B5CF6' },
    core: { x: 0.8, y: 0.5, label: 'CORE', color: '#F59E0B' }
  };

  // Particle class
  class Particle {
    constructor(startNode, endNode, value, color) {
      this.startNode = startNode;
      this.endNode = endNode;
      this.progress = 0;
      this.speed = 0.5 + value * 1.5; // Speed based on metric value
      this.size = 2 + value * 4;
      this.color = color;
      this.opacity = 0.3 + value * 0.7;
      this.trail = [];
      this.maxTrailLength = 10;
    }

    update(deltaTime) {
      this.progress += this.speed * deltaTime * 0.001;
      
      // Add current position to trail
      const currentPos = this.getCurrentPosition();
      this.trail.push({ ...currentPos, opacity: this.opacity });
      
      // Limit trail length
      if (this.trail.length > this.maxTrailLength) {
        this.trail.shift();
      }
      
      return this.progress >= 1;
    }

    getCurrentPosition() {
      const t = this.easeInOutCubic(this.progress);
      return {
        x: this.startNode.x + (this.endNode.x - this.startNode.x) * t,
        y: this.startNode.y + (this.endNode.y - this.startNode.y) * t
      };
    }

    easeInOutCubic(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    draw(ctx, width, height) {
      // Draw trail
      this.trail.forEach((point, index) => {
        const trailOpacity = (index / this.trail.length) * point.opacity * 0.5;
        ctx.fillStyle = this.color + Math.floor(trailOpacity * 255).toString(16).padStart(2, '0');
        ctx.beginPath();
        ctx.arc(point.x * width, point.y * height, this.size * 0.5, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw particle
      const pos = this.getCurrentPosition();
      ctx.fillStyle = this.color + Math.floor(this.opacity * 255).toString(16).padStart(2, '0');
      ctx.beginPath();
      ctx.arc(pos.x * width, pos.y * height, this.size, 0, Math.PI * 2);
      ctx.fill();

      // Glow effect
      const gradient = ctx.createRadialGradient(
        pos.x * width, pos.y * height, 0,
        pos.x * width, pos.y * height, this.size * 3
      );
      gradient.addColorStop(0, this.color + '40');
      gradient.addColorStop(1, this.color + '00');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(pos.x * width, pos.y * height, this.size * 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Create particles based on metric values
  const createParticles = () => {
    const particles = [];
    const time = Date.now();

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
  const animate = (timestamp) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    // Clear canvas with fade effect
    ctx.fillStyle = 'rgba(17, 24, 39, 0.1)';
    ctx.fillRect(0, 0, width, height);

    // Draw connections
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);

    // Draw lines between nodes
    const connections = [
      [nodes.scup, nodes.core],
      [nodes.entropy, nodes.core],
      [nodes.heat, nodes.mood],
      [nodes.mood, nodes.core],
      [nodes.core, nodes.scup]
    ];

    connections.forEach(([start, end]) => {
      ctx.beginPath();
      ctx.moveTo(start.x * width, start.y * height);
      ctx.lineTo(end.x * width, end.y * height);
      ctx.stroke();
    });

    ctx.setLineDash([]);

    // Update and draw particles
    const newParticles = createParticles();
    particlesRef.current.push(...newParticles);

    particlesRef.current = particlesRef.current.filter(particle => {
      const isDone = particle.update(16); // Assume 60fps
      if (!isDone) {
        particle.draw(ctx, width, height);
      }
      return !isDone;
    });

    // Draw nodes
    Object.entries(nodes).forEach(([key, node]) => {
      const x = node.x * width;
      const y = node.y * height;
      const radius = key === 'core' ? 30 : 25;

      // Node glow
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2);
      gradient.addColorStop(0, node.color + '40');
      gradient.addColorStop(1, node.color + '00');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
      ctx.fill();

      // Node circle
      ctx.fillStyle = '#1F2937';
      ctx.strokeStyle = node.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Node label
      ctx.fillStyle = '#E5E7EB';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(node.label, x, y - 5);

      // Value display
      let value = '';
      if (key === 'scup') value = scup.toFixed(3);
      else if (key === 'entropy') value = entropy.toFixed(3);
      else if (key === 'heat') value = heat.toFixed(3);
      else if (key === 'mood') value = mood.substring(0, 3).toUpperCase();
      else if (key === 'core') value = '∞';

      ctx.font = '10px monospace';
      ctx.fillStyle = node.color;
      ctx.fillText(value, x, y + 8);
    });

    // Flow percentages
    ctx.fillStyle = '#9CA3AF';
    ctx.font = '10px monospace';
    ctx.textAlign = 'center';

    // Display flow rates
    const flowRates = {
      'SCUP→CORE': (scup * 100).toFixed(0) + '%',
      'ENTROPY→CORE': (entropy * 100).toFixed(0) + '%',
      'HEAT→MOOD': (heat * 100).toFixed(0) + '%'
    };

    let yOffset = 20;
    Object.entries(flowRates).forEach(([label, rate]) => {
      ctx.fillText(`${label}: ${rate}`, width - 80, yOffset);
      yOffset += 15;
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
          height: Math.min(rect.height, 400)
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
  }, [dimensions, scup, entropy, heat, mood]);

  return (
    <div className="bg-gray-800 rounded-lg p-4 h-full">
      <h3 className="text-lg font-semibold text-gray-200 mb-2">Network Flow Diagram</h3>
      <div className="relative w-full h-full min-h-[300px]">
        <canvas
          ref={canvasRef}
          className="w-full h-full"
          style={{ maxHeight: '400px' }}
        />
      </div>
    </div>
  );
};

NetworkFlowDiagram.propTypes = {
  scup: PropTypes.number,
  entropy: PropTypes.number,
  heat: PropTypes.number,
  mood: PropTypes.string
};

export default NetworkFlowDiagram; 