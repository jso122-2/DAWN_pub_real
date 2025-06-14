import { useState, useEffect } from 'react';
import { useAnimationFrame } from './useAnimationFrame';

interface FloatingConfig {
  amplitude: number;
  speed: number;
  pattern: 'lissajous' | 'orbital' | 'random' | 'magnetic';
}

export function useFloatingOptimized(config: FloatingConfig) {
  const [position, setPosition] = useState({ x: 0, y: 0, rotate: 0 });
  const { amplitude, speed, pattern } = config;
  
  useAnimationFrame((time: number) => {
    const t = time * 0.001 * speed;
    
    let x = 0, y = 0, rotate = 0;
    
    switch (pattern) {
      case 'lissajous':
        x = amplitude * Math.sin(t * 1.3);
        y = amplitude * Math.sin(t * 2.1);
        rotate = Math.sin(t * 0.5) * 5;
        break;
        
      case 'orbital':
        x = amplitude * Math.cos(t);
        y = amplitude * Math.sin(t);
        rotate = t * 10 % 360;
        break;
        
      case 'random':
        x = amplitude * (Math.sin(t * 1.3) + Math.sin(t * 2.7) * 0.5);
        y = amplitude * (Math.sin(t * 2.1) + Math.sin(t * 3.2) * 0.5);
        rotate = Math.sin(t * 0.7) * 10;
        break;
        
      case 'magnetic':
        x = amplitude * Math.sin(t) * Math.cos(t * 0.7);
        y = amplitude * Math.cos(t) * Math.sin(t * 0.7);
        rotate = Math.sin(t * 0.3) * 3;
        break;
    }
    
    setPosition({ x, y, rotate });
  });
  
  return {
    transform: `translate(${position.x}px, ${position.y}px) rotate(${position.rotate}deg)`,
  };
} 