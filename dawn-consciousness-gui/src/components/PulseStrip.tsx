import React, { useEffect, useState } from 'react';
import './PulseStrip.css';

interface PulseStripProps {
  isActive: boolean;
  scup?: number;
  mood?: number;
  entropy?: number;
  tickNumber?: number;
}

export const PulseStrip: React.FC<PulseStripProps> = ({ 
  isActive, 
  scup = 0.5, 
  mood = 0.5, 
  entropy = 0.5,
  tickNumber = 0
}) => {
  const [pulseIntensity, setPulseIntensity] = useState(0.5);
  const [hueShift, setHueShift] = useState(0);

  useEffect(() => {
    if (isActive) {
      // Calculate pulse intensity based on consciousness metrics
      const intensity = (scup + Math.abs(mood) + entropy) / 3;
      setPulseIntensity(Math.max(0.1, intensity));
      
      // Calculate hue shift based on mood (red=negative, blue=positive, green=neutral)
      const hue = mood >= 0 
        ? 200 + (mood * 80)  // Blue to cyan for positive mood
        : 0 + (Math.abs(mood) * 60); // Red to orange for negative mood
      setHueShift(hue);
    }
  }, [isActive, scup, mood, entropy, tickNumber]);

  return (
    <div className={`pulse-strip ${isActive ? 'active' : 'inactive'}`}>
      <div 
        className="pulse-wave"
        style={{
          '--pulse-intensity': pulseIntensity,
          '--hue-shift': `${hueShift}deg`,
          '--tick-animation': isActive ? 'pulse 62.5ms ease-in-out infinite' : 'none'
        } as React.CSSProperties}
      >
        <div className="pulse-core" />
        <div className="pulse-ring" />
        <div className="pulse-outer" />
      </div>
      
      {isActive && (
        <div className="pulse-metrics">
          <span className="metric">
            SCUP: {(scup * 100).toFixed(1)}%
          </span>
          <span className="metric">
            Mood: {mood >= 0 ? '+' : ''}{(mood * 100).toFixed(1)}%
          </span>
          <span className="metric">
            Entropy: {(entropy * 100).toFixed(1)}%
          </span>
          <span className="tick-counter">
            Tick #{tickNumber}
          </span>
        </div>
      )}
    </div>
  );
}; 