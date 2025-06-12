import React, { useEffect, useRef, useState, useMemo } from 'react';

// Custom hook to track entropy state from DAWN system
const useEntropyState = () => {
  const [entropy, setEntropy] = useState(45); // 0-100
  const [coherence, setCoherence] = useState(0.8); // 0-1
  
  useEffect(() => {
    // Simulate entropy fluctuations for demo
    // In production, this would connect to DAWN system metrics
    const interval = setInterval(() => {
      setEntropy(prev => {
        const change = (Math.random() - 0.5) * 10;
        return Math.max(0, Math.min(100, prev + change));
      });
      setCoherence(prev => {
        const change = (Math.random() - 0.5) * 0.1;
        return Math.max(0, Math.min(1, prev + change));
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  return { entropy, coherence };
};

const EntropyRingHUD: React.FC = () => {
  const { entropy, coherence } = useEntropyState();
  const [isHovered, setIsHovered] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const svgRef = useRef<SVGSVGElement>(null);
  
  // Determine visibility
  useEffect(() => {
    setIsVisible(isHovered || entropy > 75);
  }, [isHovered, entropy]);
  
  // Calculate coherence color
  const coherenceColor = useMemo(() => {
    if (coherence > 0.7) return '#14b8a6'; // teal
    if (coherence > 0.3) return '#f59e0b'; // amber
    return '#ef4444'; // red
  }, [coherence]);
  
  // Calculate ring dimensions
  const size = 120;
  const center = size / 2;
  const innerRadius = 35;
  const outerRadius = 45;
  const pulseRadius = 50 + (entropy / 100) * 15;
  
  // Create arc path
  const createArc = (radius: number, startAngle: number, endAngle: number) => {
    const start = polarToCartesian(center, center, radius, endAngle);
    const end = polarToCartesian(center, center, radius, startAngle);
    const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
    
    return [
      "M", start.x, start.y,
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
    ].join(" ");
  };
  
  const polarToCartesian = (centerX: number, centerY: number, radius: number, angleInDegrees: number) => {
    const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    };
  };
  
  return (
    <div
      className={`fixed top-20 right-20 transition-opacity duration-500 pointer-events-none ${
        isVisible ? 'opacity-100' : 'opacity-0'
      }`}
      style={{ zIndex: 9999 }}
    >
      <div 
        className="relative pointer-events-auto"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <svg
          ref={svgRef}
          width={size}
          height={size}
          className="transform-gpu"
        >
          <defs>
            {/* Glow filter */}
            <filter id="entropy-glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            
            {/* Gradient for pulse ring */}
            <radialGradient id="pulse-gradient">
              <stop offset="0%" stopColor={coherenceColor} stopOpacity="0.3"/>
              <stop offset="100%" stopColor={coherenceColor} stopOpacity="0"/>
            </radialGradient>
          </defs>
          
          {/* Background circle */}
          <circle
            cx={center}
            cy={center}
            r={outerRadius + 10}
            fill="rgba(0, 0, 0, 0.5)"
            strokeWidth="0"
          />
          
          {/* Outer pulse ring */}
          <circle
            cx={center}
            cy={center}
            r={pulseRadius}
            fill="none"
            stroke="url(#pulse-gradient)"
            strokeWidth="2"
            opacity="0.6"
            className="animate-pulse"
            style={{
              filter: 'url(#entropy-glow)',
              transformOrigin: 'center',
              animation: 'pulse 2s ease-in-out infinite'
            }}
          />
          
          {/* Inner coherence ring */}
          <path
            d={createArc(innerRadius, 0, coherence * 360)}
            fill="none"
            stroke={coherenceColor}
            strokeWidth="4"
            strokeLinecap="round"
            style={{
              filter: 'url(#entropy-glow)',
              transition: 'all 0.5s ease-out'
            }}
          />
          
          {/* Center metrics */}
          <text
            x={center}
            y={center - 5}
            textAnchor="middle"
            fill="white"
            fontSize="18"
            fontWeight="bold"
            opacity="0.9"
          >
            {entropy.toFixed(0)}%
          </text>
          <text
            x={center}
            y={center + 10}
            textAnchor="middle"
            fill={coherenceColor}
            fontSize="11"
            opacity="0.7"
          >
            entropy
          </text>
          
          {/* Warning indicator for critical entropy */}
          {entropy > 85 && (
            <circle
              cx={center}
              cy={center}
              r={innerRadius - 5}
              fill="none"
              stroke="#ef4444"
              strokeWidth="2"
              opacity="0.8"
              className="animate-ping"
            />
          )}
        </svg>
        
        {/* Tooltip on hover */}
        {isHovered && (
          <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-black/80 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
            Coherence: {(coherence * 100).toFixed(0)}%
          </div>
        )}
      </div>
      
      <style jsx>{`
        @keyframes pulse {
          0% {
            transform: scale(1);
            opacity: 0.6;
          }
          50% {
            transform: scale(1.05);
            opacity: 0.3;
          }
          100% {
            transform: scale(1);
            opacity: 0.6;
          }
        }
        
        @keyframes ping {
          75%, 100% {
            transform: scale(1.2);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default EntropyRingHUD; 