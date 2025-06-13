import React, { useRef, useEffect } from 'react';
import { useParticleSystem } from '@/hooks/useParticleSystem';

interface ParticleFieldProps {
  fullscreen?: boolean;
}

const particleContainerStyle = (fullscreen?: boolean) => ({
  position: 'relative' as const,
  width: '100%',
  height: '100%',
  minHeight: fullscreen ? '500px' : '150px'
});

const canvasStyle = {
  width: '100%',
  height: '100%'
};

const particleInfoStyle = {
  position: 'absolute' as const,
  bottom: '1rem',
  right: '1rem',
  display: 'flex',
  gap: '1rem',
  fontSize: '0.75rem',
  color: 'rgba(148, 163, 184, 0.7)',
  background: 'rgba(15, 23, 42, 0.8)',
  padding: '0.5rem 1rem',
  borderRadius: '6px',
  backdropFilter: 'blur(10px)'
};

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
    <div style={particleContainerStyle(fullscreen)}>
      <canvas ref={canvasRef} style={canvasStyle} />
      <div style={particleInfoStyle}>
        <span>Particles: {particleSystem.particles.length}</span>
        <span>Coherence: {(particleSystem.coherence * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
}; 