import { useEffect, useState, useRef } from 'react';

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
}

interface Particle {
  x: number;
  y: number;
  size: number;
  speedX: number;
  speedY: number;
  opacity: number;
}

const ConsciousnessVisualizer = () => {
  const [state, setState] = useState<ConsciousnessState>({
    scup: 0,
    entropy: 0,
    mood: 'neutral'
  });
  const [particles, setParticles] = useState<Particle[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>();

  // Generate particles based on entropy
  useEffect(() => {
    const generateParticles = () => {
      const count = Math.floor(state.entropy * 50); // Scale entropy to particle count
      const newParticles: Particle[] = [];
      
      for (let i = 0; i < count; i++) {
        const angle = (Math.random() * Math.PI * 2);
        const distance = 100 + Math.random() * 50;
        newParticles.push({
          x: Math.cos(angle) * distance,
          y: Math.sin(angle) * distance,
          size: 2 + Math.random() * 3,
          speedX: (Math.random() - 0.5) * 2,
          speedY: (Math.random() - 0.5) * 2,
          opacity: 0.3 + Math.random() * 0.7
        });
      }
      
      setParticles(newParticles);
    };

    generateParticles();
  }, [state.entropy]);

  // Animate particles
  useEffect(() => {
    const animateParticles = () => {
      setParticles(prev => prev.map(particle => ({
        ...particle,
        x: particle.x + particle.speedX,
        y: particle.y + particle.speedY,
        opacity: particle.opacity * 0.99
      })).filter(p => p.opacity > 0.1));

      animationFrameRef.current = requestAnimationFrame(animateParticles);
    };

    animationFrameRef.current = requestAnimationFrame(animateParticles);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  // WebSocket connection
  useEffect(() => {
    wsRef.current = new WebSocket('ws://localhost:8000/ws');

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'consciousness_state') {
          setState({
            scup: data.scup,
            entropy: data.entropy,
            mood: data.mood
          });
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const getMoodColor = (mood: string): string => {
    switch (mood.toLowerCase()) {
      case 'calm':
        return '#3b82f6'; // blue
      case 'energetic':
        return '#f97316'; // orange
      case 'chaotic':
        return '#ef4444'; // red
      default:
        return '#00ff88'; // default green
    }
  };

  const orbSize = 100 + (state.scup * 100); // Scale SCUP to size
  const moodColor = getMoodColor(state.mood);

  return (
    <div style={{ 
      position: 'relative',
      width: '400px',
      height: '400px',
      margin: '2rem auto'
    }}>
      {/* Particles */}
      <div style={{ position: 'absolute', width: '100%', height: '100%' }}>
        {particles.map((particle, index) => (
          <div
            key={index}
            style={{
              position: 'absolute',
              left: '50%',
              top: '50%',
              width: particle.size,
              height: particle.size,
              background: moodColor,
              borderRadius: '50%',
              transform: `translate(${particle.x}px, ${particle.y}px)`,
              opacity: particle.opacity,
              transition: 'opacity 0.3s ease'
            }}
          />
        ))}
      </div>

      {/* Orb */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          width: orbSize,
          height: orbSize,
          background: `radial-gradient(circle at 30% 30%, ${moodColor}, rgba(0,0,0,0.8))`,
          borderRadius: '50%',
          transform: 'translate(-50%, -50%)',
          boxShadow: `0 0 50px ${moodColor}`,
          transition: 'all 0.5s ease',
          animation: 'pulse 2s infinite'
        }}
      />

      {/* Labels */}
      <div style={{
        position: 'absolute',
        bottom: '1rem',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '2rem',
        background: 'rgba(0, 0, 0, 0.5)',
        padding: '0.5rem 1rem',
        borderRadius: '0.5rem',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>SCUP</div>
          <div style={{ color: '#00ff88', fontFamily: 'var(--font-mono)' }}>
            {Math.round(state.scup * 100)}%
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Entropy</div>
          <div style={{ color: '#00ff88', fontFamily: 'var(--font-mono)' }}>
            {Math.round(state.entropy * 100)}%
          </div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Mood</div>
          <div style={{ 
            color: moodColor, 
            fontFamily: 'var(--font-mono)',
            textTransform: 'capitalize'
          }}>
            {state.mood}
          </div>
        </div>
      </div>

      <style>
        {`
          @keyframes pulse {
            0% {
              box-shadow: 0 0 50px ${moodColor};
            }
            50% {
              box-shadow: 0 0 70px ${moodColor};
            }
            100% {
              box-shadow: 0 0 50px ${moodColor};
            }
          }
        `}
      </style>
    </div>
  );
};

export default ConsciousnessVisualizer; 