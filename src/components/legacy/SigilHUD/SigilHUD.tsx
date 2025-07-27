import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import './SigilHUD.css';

interface SigilHUDProps {
  consciousness: number;
  entropy: number;
  mood?: string;
  fullscreen?: boolean;
}

export const SigilHUD: React.FC<SigilHUDProps> = ({ 
  consciousness, 
  entropy, 
  mood = 'neutral',
  fullscreen = false 
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw mystical sigil based on consciousness
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 50;
    
    // Outer circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(0, 255, 136, ${consciousness})`;
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Inner geometric patterns
    const points = Math.floor(3 + consciousness * 6); // 3-9 points
    for (let i = 0; i < points; i++) {
      const angle = (i / points) * Math.PI * 2 - Math.PI / 2;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      // Connect to opposite points
      for (let j = i + 1; j < points; j++) {
        const angle2 = (j / points) * Math.PI * 2 - Math.PI / 2;
        const x2 = centerX + Math.cos(angle2) * radius;
        const y2 = centerY + Math.sin(angle2) * radius;
        
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = `rgba(0, 255, 136, ${consciousness * 0.3})`;
        ctx.stroke();
      }
    }
    
    // Central symbol based on mood
    const moodSymbols = {
      analytical: '◊',
      confident: '▲',
      focused: '●',
      creative: '✦',
      neutral: '◉'
    };
    
    ctx.font = `${radius / 3}px Arial`;
    ctx.fillStyle = `rgba(0, 255, 136, ${consciousness})`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(moodSymbols[mood as keyof typeof moodSymbols] || '◉', centerX, centerY);
    
    // Rotating entropy indicators
    const time = Date.now() * 0.001;
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2 + time * entropy;
      const dist = radius * 0.7;
      const x = centerX + Math.cos(angle) * dist;
      const y = centerY + Math.sin(angle) * dist;
      const size = 3 + entropy * 5;
      
      ctx.beginPath();
      ctx.arc(x, y, size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 0, 170, ${entropy})`;
      ctx.fill();
    }
  }, [consciousness, entropy, mood]);
  
  return (
    <motion.div 
      className={`sigil-hud ${fullscreen ? 'fullscreen' : ''}`}
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <canvas 
        ref={canvasRef}
        width={fullscreen ? 800 : 400}
        height={fullscreen ? 800 : 400}
        className="sigil-canvas"
      />
      
      <div className="sigil-metrics">
        <div className="metric">
          <span className="label">Consciousness</span>
          <span className="value">{(consciousness * 100).toFixed(1)}%</span>
        </div>
        <div className="metric">
          <span className="label">Entropy</span>
          <span className="value">{entropy.toFixed(3)}</span>
        </div>
      </div>
    </motion.div>
  );
}; 