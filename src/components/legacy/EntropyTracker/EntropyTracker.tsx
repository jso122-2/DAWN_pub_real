import React from 'react';
import { motion } from 'framer-motion';
import './EntropyTracker.css';

interface EntropyTrackerProps {
  entropy: number;
  size?: 'compact' | 'normal' | 'large';
  showRings?: boolean;
  showParticles?: boolean;
}

export const EntropyTracker: React.FC<EntropyTrackerProps> = ({
  entropy,
  size = 'normal',
  showRings = true,
  showParticles = false
}) => {
  const rings = [
    { radius: 80, speed: 2, opacity: 0.2 },
    { radius: 60, speed: -3, opacity: 0.3 },
    { radius: 40, speed: 4, opacity: 0.4 },
    { radius: 20, speed: -5, opacity: 0.5 }
  ];
  
  return (
    <div className={`entropy-tracker size-${size}`}>
      <div className="entropy-container">
        {/* Background glow */}
        <motion.div 
          className="entropy-glow"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.6, 0.3]
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          style={{
            background: `radial-gradient(circle, rgba(255, 0, 170, ${entropy}) 0%, transparent 70%)`
          }}
        />
        
        {/* Rotating rings */}
        {showRings && rings.map((ring, index) => (
          <motion.div
            key={index}
            className="entropy-ring"
            animate={{
              rotate: 360 * Math.sign(ring.speed)
            }}
            transition={{
              duration: Math.abs(20 / ring.speed),
              repeat: Infinity,
              ease: "linear"
            }}
            style={{
              width: ring.radius * 2,
              height: ring.radius * 2,
              opacity: ring.opacity * entropy
            }}
          />
        ))}
        
        {/* Central core */}
        <motion.div 
          className="entropy-core"
          animate={{
            scale: 0.8 + entropy * 0.4
          }}
          transition={{
            duration: 0.5,
            ease: "easeOut"
          }}
        >
          <span className="entropy-value">{entropy.toFixed(3)}</span>
          <span className="entropy-label">ENTROPY</span>
        </motion.div>
        
        {/* Chaos particles */}
        {showParticles && Array.from({ length: Math.floor(entropy * 10) }, (_, i) => (
          <motion.div
            key={i}
            className="chaos-particle"
            initial={{
              x: 0,
              y: 0,
              opacity: 0
            }}
            animate={{
              x: (Math.random() - 0.5) * 200,
              y: (Math.random() - 0.5) * 200,
              opacity: [0, 1, 0]
            }}
            transition={{
              duration: 2 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          />
        ))}
      </div>
    </div>
  );
}; 