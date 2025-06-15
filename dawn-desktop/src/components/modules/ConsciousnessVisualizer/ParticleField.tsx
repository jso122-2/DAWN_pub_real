import React, { useRef, useEffect } from 'react';
import { useParticleSystem } from '../../../hooks/useParticleSystem';
import * as styles from './ConsciousnessVisualizer.styles';

interface ParticleFieldProps {
  fullscreen?: boolean;
}

export const ParticleField: React.FC<ParticleFieldProps> = ({ fullscreen }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { particleSystem } = useParticleSystem();
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      // Clear with trails
      ctx.fillStyle = 'rgba(15, 23, 42, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw connections
      ctx.strokeStyle = 'rgba(148, 163, 184, 0.1)';
      ctx.lineWidth = 1;
      
      particleSystem.particles.forEach(particle => {
        particle.connections.forEach(connectedId => {
          const connected = particleSystem.particles.find(p => p.id === connectedId);
          if (!connected) return;

          ctx.beginPath();
          ctx.moveTo(
            particle.position.x + canvas.width / 2,
            particle.position.y + canvas.height / 2
          );
          ctx.lineTo(
            connected.position.x + canvas.width / 2,
            connected.position.y + canvas.height / 2
          );
          ctx.stroke();
        });
      });

      // Draw particles
      particleSystem.particles.forEach(particle => {
        const x = particle.position.x + canvas.width / 2;
        const y = particle.position.y + canvas.height / 2;
        const radius = 2 + particle.charge * 3;

        // Glow effect
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 3);
        gradient.addColorStop(0, particle.color);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius * 3, 0, Math.PI * 2);
        ctx.fill();

        // Core particle
        ctx.fillStyle = particle.color;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw center mass indicator
      if (particleSystem.particles.length > 0) {
        const centerX = particleSystem.centerMass.x + canvas.width / 2;
        const centerY = particleSystem.centerMass.y + canvas.height / 2;

        ctx.strokeStyle = 'rgba(251, 191, 36, 0.5)';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.arc(centerX, centerY, 20, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      animationFrameRef.current = requestAnimationFrame(render);
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
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [particleSystem]);

  return (
    <div className={styles.particleContainer(fullscreen)}>
      <canvas ref={canvasRef} className={styles.canvas} />
      <div className={styles.particleInfo}>
        <span>Particles: {particleSystem.particles.length}</span>
        <span>Coherence: {(particleSystem.unity * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
}; 