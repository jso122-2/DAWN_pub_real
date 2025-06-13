import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface AudioVisualizerProps {
  isActive?: boolean;
  barCount?: number;
  className?: string;
}

export function AudioVisualizer({ isActive = true, barCount = 32, className = '' }: AudioVisualizerProps) {
  const [frequencies, setFrequencies] = useState<number[]>(new Array(barCount).fill(0));

  // Simulate audio frequencies
  useEffect(() => {
    if (!isActive) {
      setFrequencies(new Array(barCount).fill(0));
      return;
    }

    const animate = () => {
      const time = Date.now() * 0.001;
      
      const newFrequencies = Array.from({ length: barCount }, (_, i) => {
        // Create different frequency bands with varying intensities
        const bassFreq = Math.sin(time * 3 + i * 0.1) * 0.7 + 0.3;
        const midFreq = Math.sin(time * 4 + i * 0.2) * 0.5 + 0.5;
        const highFreq = Math.sin(time * 8 + i * 0.15) * 0.4 + 0.4;
        
        // Mix frequencies based on position in spectrum
        const bassWeight = Math.max(0, 1 - (i / barCount) * 3);
        const midWeight = Math.max(0, 1 - Math.abs((i / barCount) - 0.5) * 2);
        const highWeight = Math.max(0, (i / barCount) - 0.6) * 2;
        
        const mixed = (bassFreq * bassWeight + midFreq * midWeight + highFreq * highWeight) / (bassWeight + midWeight + highWeight + 0.1);
        
        // Add some randomness for realism
        return Math.max(0.1, mixed + (Math.random() - 0.5) * 0.2);
      });
      
      setFrequencies(newFrequencies);
    };

    const interval = setInterval(animate, 50); // 20 FPS for smooth animation
    return () => clearInterval(interval);
  }, [isActive, barCount]);

  if (!isActive) {
    return (
      <div className={`flex items-end gap-1 h-16 ${className}`}>
        {Array.from({ length: barCount }).map((_, index) => (
          <div
            key={index}
            className="w-2 h-1 rounded-t-sm bg-gray-600/30"
          />
        ))}
      </div>
    );
  }

  return (
    <div className={`flex items-end gap-1 h-16 ${className}`}>
      {frequencies.map((freq, index) => {
        const height = Math.max(4, freq * 60);
        const intensity = freq;
        
        // Color based on frequency position (bass = purple, mid = cyan, high = pink)
        let color;
        if (index < barCount * 0.3) {
          // Bass frequencies - purple
          color = `rgba(168, 85, 247, ${0.5 + intensity * 0.5})`;
        } else if (index < barCount * 0.7) {
          // Mid frequencies - cyan
          color = `rgba(6, 182, 212, ${0.5 + intensity * 0.5})`;
        } else {
          // High frequencies - pink
          color = `rgba(236, 72, 153, ${0.5 + intensity * 0.5})`;
        }
        
        return (
          <motion.div
            key={index}
            className="w-2 rounded-t-sm"
            style={{
              height: `${height}px`,
              backgroundColor: color,
              boxShadow: `0 0 ${intensity * 10}px ${color}`,
            }}
            animate={{ 
              height: `${height}px`,
              boxShadow: `0 0 ${intensity * 10}px ${color}`
            }}
            transition={{ 
              duration: 0.1,
              ease: "easeOut"
            }}
          />
        );
      })}
    </div>
  );
} 