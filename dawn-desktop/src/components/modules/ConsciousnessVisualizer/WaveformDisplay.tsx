import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { waveformGenerator } from '@/utils/consciousness/waveformGenerator';
import { WaveformData } from '@/types/visualization.types';

interface WaveformDisplayProps {
  fullscreen?: boolean;
}

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
}

// Mock consciousness hook - replace with actual implementation
function useConsciousness(): ConsciousnessState {
  const [consciousness, setConsciousness] = useState<ConsciousnessState>({
    scup: 75,
    entropy: 0.5,
    mood: 'active',
    neuralActivity: 0.6
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const moods = ['active', 'contemplative', 'excited', 'serene', 'anxious', 'euphoric', 'chaotic'];
      setConsciousness(prev => ({
        ...prev,
        scup: Math.max(0, Math.min(100, prev.scup + (Math.random() - 0.5) * 10)),
        entropy: Math.max(0, Math.min(1, prev.entropy + (Math.random() - 0.5) * 0.2)),
        neuralActivity: Math.max(0, Math.min(1, prev.neuralActivity + (Math.random() - 0.5) * 0.3)),
        mood: Math.random() > 0.9 ? moods[Math.floor(Math.random() * moods.length)] : prev.mood
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return consciousness;
}

const waveformContainerStyle = (fullscreen?: boolean) => ({
  position: 'relative' as const,
  width: '100%',
  height: '100%',
  minHeight: fullscreen ? '500px' : '150px'
});

const canvasStyle = {
  width: '100%',
  height: '100%'
};

const waveformInfoStyle = {
  position: 'absolute' as const,
  bottom: '1rem',
  left: '1rem',
  display: 'flex',
  gap: '1rem',
  fontSize: '0.75rem',
  color: 'rgba(148, 163, 184, 0.7)',
  background: 'rgba(15, 23, 42, 0.8)',
  padding: '0.5rem 1rem',
  borderRadius: '6px',
  backdropFilter: 'blur(10px)'
};

export const WaveformDisplay: React.FC<WaveformDisplayProps> = ({ fullscreen }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const consciousness = useConsciousness();
  const [waveformData, setWaveformData] = useState<WaveformData | null>(null);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      // Generate new waveform data
      const data = waveformGenerator.generateWaveform(consciousness);
      setWaveformData(data);

      // Clear canvas
      ctx.fillStyle = 'rgba(15, 23, 42, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw waveform
      ctx.strokeStyle = `hsla(${180 + consciousness.scup * 1.8}, 70%, 50%, 0.8)`;
      ctx.lineWidth = 2;
      ctx.shadowBlur = 10;
      ctx.shadowColor = ctx.strokeStyle;

      ctx.beginPath();
      data.points.forEach((point, index) => {
        const x = point.x * canvas.width;
        const y = (0.5 + point.y * 0.4) * canvas.height;

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();

      // Draw harmonics
      data.harmonics.forEach((harmonic, index) => {
        ctx.strokeStyle = `hsla(${200 + index * 30}, 60%, 50%, 0.3)`;
        ctx.lineWidth = 1;
        ctx.beginPath();
        
        data.points.forEach((point, i) => {
          const x = point.x * canvas.width;
          const y = (0.5 + Math.sin(point.time * harmonic.frequency * Math.PI * 2) * harmonic.amplitude * 0.3) * canvas.height;
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        });
        ctx.stroke();
      });

      // Draw Lissajous pattern overlay
      const lissajousPoints = waveformGenerator.generateLissajous(consciousness, Date.now() / 1000);
      ctx.strokeStyle = `hsla(${260 + consciousness.entropy * 60}, 70%, 50%, 0.5)`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      
      lissajousPoints.forEach((point, index) => {
        const x = point.x * canvas.width;
        const y = point.y * canvas.height;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();

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
  }, [consciousness]);

  return (
    <div style={waveformContainerStyle(fullscreen)}>
      <canvas ref={canvasRef} style={canvasStyle} />
      {waveformData && (
        <div style={waveformInfoStyle}>
          <span>Frequency: {waveformData.frequency.toFixed(2)} Hz</span>
          <span>Harmonics: {waveformData.harmonics.length}</span>
        </div>
      )}
    </div>
  );
}; 