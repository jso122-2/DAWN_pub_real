import React, { useEffect, useRef } from 'react';
import { useConsciousnessStore } from '../stores/consciousnessStore';

const SimpleConsciousnessCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const { tickData, isConnected } = useConsciousnessStore();
  
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth * window.devicePixelRatio;
      canvas.height = canvas.offsetHeight * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    };
    
    resizeCanvas();
    
    interface Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      pulsePhase: number;
      active: boolean;
    }
    
    let particles: Particle[] = [];
    
    // Initialize particles
    const initParticles = () => {
      particles = [];
      const numParticles = 30;
      
      for (let i = 0; i < numParticles; i++) {
        particles.push({
          x: Math.random() * canvas.offsetWidth,
          y: Math.random() * canvas.offsetHeight,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          radius: Math.random() * 3 + 2,
          pulsePhase: Math.random() * Math.PI * 2,
          active: Math.random() > 0.3
        });
      }
    };
    
    initParticles();
    
    // Animation loop
    const animate = () => {
      const width = canvas.offsetWidth;
      const height = canvas.offsetHeight;
      
      // Clear canvas with fade
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, width, height);
      
      // Get data with defaults
      const scup = tickData?.scup ? (tickData.scup > 1 ? tickData.scup / 100 : tickData.scup) : 0.5;
      const entropy = tickData?.entropy || 0.5;
      const heat = tickData?.heat || 0.5;
      const mood = tickData?.mood || 'analytical';
      
      // Colors based on mood
      const colors: Record<string, string> = {
        analytical: '#0088ff',
        confident: '#00ff88',
        focused: '#ffaa00',
        creative: '#ff00aa'
      };
      const color = colors[mood.toLowerCase()] || colors.analytical;
      
      // Draw central orb
      const centerX = width / 2;
      const centerY = height / 2;
      const baseRadius = 60;
      const radius = baseRadius + (scup * 40);
      
      // Animated glow
      const glowRadius = radius + Math.sin(Date.now() * 0.001) * 15 * scup;
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, glowRadius);
      gradient.addColorStop(0, color);
      gradient.addColorStop(0.5, `${color}66`);
      gradient.addColorStop(1, 'transparent');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, glowRadius, 0, Math.PI * 2);
      ctx.fill();
      
      // Core orb
      ctx.fillStyle = color;
      ctx.globalAlpha = 0.8;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius * 0.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
      
      // Update and draw particles
      particles.forEach((particle, i) => {
        // Update position
        particle.x += particle.vx * (1 + entropy * 0.5);
        particle.y += particle.vy * (1 + entropy * 0.5);
        
        // Bounce off walls
        if (particle.x < 0 || particle.x > width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > height) particle.vy *= -1;
        
        // Attraction to center
        const dx = centerX - particle.x;
        const dy = centerY - particle.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist > radius) {
          particle.vx += (dx / dist) * scup * 0.05;
          particle.vy += (dy / dist) * scup * 0.05;
        }
        
        // Pulse animation
        particle.pulsePhase += 0.03 * (1 + heat);
        const pulseSize = Math.sin(particle.pulsePhase) * 0.3 + 1;
        
        // Draw particle
        ctx.fillStyle = particle.active ? color : `${color}44`;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius * pulseSize, 0, Math.PI * 2);
        ctx.fill();
      });
      
      // Draw connections
      ctx.strokeStyle = `${color}22`;
      ctx.lineWidth = 1;
      
      particles.forEach((p1, i) => {
        particles.slice(i + 1).forEach(p2 => {
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < 80 && p1.active && p2.active) {
            ctx.globalAlpha = (1 - dist / 80) * 0.5;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        });
      });
      
      ctx.globalAlpha = 1;
      
      // Connection status indicator
      ctx.fillStyle = isConnected ? '#00ff88' : '#ff4444';
      ctx.beginPath();
      ctx.arc(width - 20, 20, 6, 0, Math.PI * 2);
      ctx.fill();
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    // Handle resize
    const handleResize = () => {
      resizeCanvas();
      initParticles();
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      window.removeEventListener('resize', handleResize);
    };
  }, [tickData, isConnected]);
  
  return (
    <div style={{ width: '100%', height: '100%', minHeight: '400px', position: 'relative' }}>
      <canvas 
        ref={canvasRef}
        style={{ 
          width: '100%', 
          height: '100%', 
          background: 'radial-gradient(ellipse at center, #0a0a1a 0%, #000000 100%)',
          borderRadius: '8px',
          border: '2px solid #00ff88' // Temporary debug border
        }}
      />
      {/* Debug overlay */}
      <div style={{
        position: 'absolute',
        top: '10px',
        left: '10px',
        color: '#00ff88',
        fontSize: '12px',
        background: 'rgba(0,0,0,0.5)',
        padding: '5px',
        borderRadius: '3px'
      }}>
        Canvas Active ✅
      </div>
    </div>
  );
};

export default SimpleConsciousnessCanvas; 