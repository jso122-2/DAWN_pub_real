import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { useConsciousness } from '../../../hooks/useConsciousness';
import { waveformGenerator } from '../../../utils/consciousness/waveformGenerator';
import { WaveformData } from '../../../types/visualization.types';
import * as styles from './ConsciousnessVisualizer.styles';

interface WaveformDisplayProps {
  fullscreen?: boolean;
}

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
    <div className={styles.waveformContainer(fullscreen)}>
      <canvas ref={canvasRef} className={styles.canvas} />
      {waveformData && (
        <div className={styles.waveformInfo}>
          <span>Frequency: {waveformData.frequency.toFixed(2)} Hz</span>
          <span>Harmonics: {waveformData.harmonics.length}</span>
        </div>
      )}
    </div>
  );
}; 