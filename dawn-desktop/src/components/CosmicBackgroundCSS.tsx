import React, { useEffect, useState } from 'react';
import './CosmicBackground.css';

interface Star {
  id: number;
  x: number;
  y: number;
  size: number;
  duration: number;
  delay: number;
}

export const CosmicBackgroundCSS: React.FC = () => {
  const [stars, setStars] = useState<Star[]>([]);
  
  useEffect(() => {
    // Generate random stars
    const generatedStars = Array.from({ length: 100 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 3 + 1,
      duration: Math.random() * 20 + 10,
      delay: Math.random() * 20
    }));
    setStars(generatedStars);
  }, []);
  
  return (
    <div className="cosmic-background-css">
      {/* Gradient background */}
      <div className="cosmic-gradient" />
      
      {/* Animated stars */}
      <div className="stars-container">
        {stars.map(star => (
          <div
            key={star.id}
            className="star"
            style={{
              left: `${star.x}%`,
              top: `${star.y}%`,
              width: `${star.size}px`,
              height: `${star.size}px`,
              animationDuration: `${star.duration}s`,
              animationDelay: `${star.delay}s`
            }}
          />
        ))}
      </div>
      
      {/* Floating orbs */}
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />
    </div>
  );
}; 