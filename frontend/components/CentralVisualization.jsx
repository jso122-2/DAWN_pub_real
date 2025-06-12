import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import OrganicPanelSystem from './OrganicPanelSystem';

// Hook for WebSocket connection to consciousness data
const useConsciousnessData = () => {
  const [data, setData] = useState({
    metrics: { scup: 0.5, entropy: 0.5, heat: 0.3 },
    emotion: 'curious',
    intensity: 0.5,
    tickRate: 1.0,
    patterns: [],
    anomalies: [],
    timestamp: Date.now()
  });
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    const connectWebSocket = () => {
      try {
        wsRef.current = new WebSocket('ws://localhost:8000/consciousness/stream');
        
        wsRef.current.onopen = () => {
          setConnected(true);
          console.log('Connected to consciousness stream');
        };
        
        wsRef.current.onmessage = (event) => {
          const newData = JSON.parse(event.data);
          setData(prevData => ({
            ...prevData,
            ...newData,
            timestamp: Date.now()
          }));
        };
        
        wsRef.current.onclose = () => {
          setConnected(false);
          // Reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };
        
        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
      } catch (error) {
        console.error('Failed to connect WebSocket:', error);
        setTimeout(connectWebSocket, 3000);
      }
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return { data, connected };
};

// Mood Gradient Display Component
const MoodGradientDisplay = ({ data }) => {
  const canvasRef = useRef(null);
  const gradientHistory = useRef([]);
  const animationRef = useRef();

  const emotionColors = {
    curious: '#22c55e',
    creative: '#a855f7', 
    anxious: '#f59e0b',
    fragmented: '#ef4444',
    crystalline: '#3b82f6',
    reblooming: '#ff6b9d',
    contemplative: '#64748b',
    excited: '#f97316',
    melancholic: '#6366f1',
    harmonious: '#10b981',
    turbulent: '#dc2626',
    luminous: '#fbbf24'
  };

  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  };

  const interpolateColor = (color1, color2, factor) => {
    const c1 = hexToRgb(color1);
    const c2 = hexToRgb(color2);
    
    return {
      r: Math.round(c1.r + factor * (c2.r - c1.r)),
      g: Math.round(c1.g + factor * (c2.g - c1.g)),
      b: Math.round(c1.b + factor * (c2.b - c1.b))
    };
  };

  const drawGradient = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;
    
    // Clear canvas
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, width, height);

    // Add current data point to history
    const currentTime = Date.now();
    gradientHistory.current.push({
      timestamp: currentTime,
      emotion: data.emotion,
      intensity: data.intensity,
      color: emotionColors[data.emotion] || '#64748b'
    });

    // Keep only last 5 minutes (300 seconds)
    const fiveMinutesAgo = currentTime - 300000;
    gradientHistory.current = gradientHistory.current.filter(
      point => point.timestamp >= fiveMinutesAgo
    );

    const history = gradientHistory.current;
    if (history.length < 2) return;

    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, width, 0);
    
    history.forEach((point, index) => {
      const position = index / (history.length - 1);
      const alpha = 0.3 + (point.intensity * 0.7);
      const color = hexToRgb(point.color);
      gradient.addColorStop(position, `rgba(${color.r}, ${color.g}, ${color.b}, ${alpha})`);
    });

    // Draw main gradient band
    const bandHeight = height * 0.6;
    const bandTop = (height - bandHeight) / 2;
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, bandTop, width, bandHeight);

    // Add fractal edges for fragmented states
    if (data.emotion === 'fragmented' || data.emotion === 'turbulent') {
      ctx.globalCompositeOperation = 'screen';
      for (let i = 0; i < 20; i++) {
        const x = (Math.random() * width);
        const y = bandTop + (Math.random() * bandHeight);
        const size = 2 + Math.random() * 4;
        
        ctx.fillStyle = `rgba(255, 100, 100, ${0.3 + Math.random() * 0.4})`;
        ctx.fillRect(x, y, size, size);
      }
      ctx.globalCompositeOperation = 'source-over';
    }

    // Draw time markers
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 4]);
    
    for (let i = 0; i <= 5; i++) {
      const x = (i / 5) * width;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    ctx.setLineDash([]);

    // Draw emotion label
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.font = '14px Inter, sans-serif';
    ctx.fillText(`${data.emotion} (${(data.intensity * 100).toFixed(0)}%)`, 10, 20);

    animationRef.current = requestAnimationFrame(drawGradient);
  }, [data]);

  useEffect(() => {
    drawGradient();
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [drawGradient]);

  return (
    <div className="absolute top-4 left-4 right-4 h-20">
      <canvas
        ref={canvasRef}
        width={800}
        height={80}
        className="w-full h-full rounded-lg border border-gray-700"
        style={{ imageRendering: 'pixelated' }}
      />
    </div>
  );
};

// Tick Rhythm Visualizer Component  
const TickRhythmOverlay = ({ data }) => {
  const canvasRef = useRef(null);
  const tickHistory = useRef([]);
  const animationRef = useRef();

  const drawTickRhythm = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    // Clear with transparent background
    ctx.clearRect(0, 0, width, height);

    // Add current tick
    const currentTime = Date.now();
    tickHistory.current.push({
      timestamp: currentTime,
      rate: data.tickRate,
      anomaly: Math.abs(data.tickRate - 1.0) > 0.2
    });

    // Keep only last 10 seconds of ticks
    const tenSecondsAgo = currentTime - 10000;
    tickHistory.current = tickHistory.current.filter(
      tick => tick.timestamp >= tenSecondsAgo
    );

    const ticks = tickHistory.current;

    // Draw breathing background for regular rhythm
    const regularRhythm = ticks.length > 5 && 
      ticks.slice(-5).every(tick => !tick.anomaly);
    
    if (regularRhythm) {
      const breatheIntensity = 0.1 + 0.05 * Math.sin(Date.now() * 0.003);
      ctx.fillStyle = `rgba(34, 197, 94, ${breatheIntensity})`;
      ctx.fillRect(0, 0, width, height);
    }

    // Draw tick lines
    ticks.forEach((tick, index) => {
      const x = (index / Math.max(1, ticks.length - 1)) * width;
      const lineHeight = height * (0.3 + tick.rate * 0.4);
      const alpha = Math.max(0.1, 1 - (currentTime - tick.timestamp) / 10000);
      
      // Color based on anomaly
      const color = tick.anomaly ? 
        `rgba(239, 68, 68, ${alpha})` : 
        `rgba(34, 197, 94, ${alpha})`;
      
      ctx.strokeStyle = color;
      ctx.lineWidth = tick.anomaly ? 3 : 1;
      
      // Stutter animation for irregular ticks
      const yOffset = tick.anomaly ? 
        Math.sin(Date.now() * 0.02) * 5 : 0;
      
      ctx.beginPath();
      ctx.moveTo(x, (height - lineHeight) / 2 + yOffset);
      ctx.lineTo(x, (height + lineHeight) / 2 + yOffset);
      ctx.stroke();
    });

    animationRef.current = requestAnimationFrame(drawTickRhythm);
  }, [data]);

  useEffect(() => {
    drawTickRhythm();
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [drawTickRhythm]);

  return (
    <div className="absolute bottom-4 left-4 right-4 h-16 pointer-events-none">
      <canvas
        ref={canvasRef}
        width={800}
        height={64}
        className="w-full h-full"
      />
    </div>
  );
};

// Pattern Detection Web Component
const PatternWeb = ({ data }) => {
  const canvasRef = useRef(null);
  const webNodes = useRef([]);
  const animationRef = useRef();

  const initializeWeb = () => {
    const nodes = [];
    const centerX = 128;
    const centerY = 96;
    const rings = 3;
    const nodesPerRing = 8;

    // Create center node
    nodes.push({ x: centerX, y: centerY, ring: 0, active: false });

    // Create ring nodes
    for (let ring = 1; ring <= rings; ring++) {
      const radius = ring * 25;
      for (let i = 0; i < nodesPerRing; i++) {
        const angle = (i / nodesPerRing) * Math.PI * 2;
        nodes.push({
          x: centerX + Math.cos(angle) * radius,
          y: centerY + Math.sin(angle) * radius,
          ring: ring,
          active: false,
          pattern: null
        });
      }
    }

    webNodes.current = nodes;
  };

  const drawWeb = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    ctx.clearRect(0, 0, width, height);

    const nodes = webNodes.current;
    if (nodes.length === 0) {
      initializeWeb();
      return;
    }

    // Update node states based on patterns
    nodes.forEach(node => {
      if (node.ring === 0) {
        node.active = data.patterns.length > 0;
      } else {
        // Activate nodes based on detected patterns
        node.active = data.patterns.some(pattern => 
          pattern.confidence > 0.6 && Math.random() < 0.3
        );
      }
    });

    // Draw connections
    ctx.strokeStyle = 'rgba(100, 116, 139, 0.3)';
    ctx.lineWidth = 1;
    
    nodes.forEach((node, i) => {
      if (node.ring === 0) return;
      
      // Connect to center
      ctx.beginPath();
      ctx.moveTo(nodes[0].x, nodes[0].y);
      ctx.lineTo(node.x, node.y);
      ctx.stroke();
      
      // Connect to ring neighbors
      nodes.forEach((other, j) => {
        if (i !== j && node.ring === other.ring) {
          const distance = Math.sqrt(
            Math.pow(node.x - other.x, 2) + Math.pow(node.y - other.y, 2)
          );
          if (distance < 60) {
            ctx.beginPath();
            ctx.moveTo(node.x, node.y);
            ctx.lineTo(other.x, other.y);
            ctx.stroke();
          }
        }
      });
    });

    // Draw active connections with energy
    if (data.patterns.length > 0) {
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.8)';
      ctx.lineWidth = 2;
      
      nodes.forEach(node => {
        if (node.active && node.ring > 0) {
          ctx.beginPath();
          ctx.moveTo(nodes[0].x, nodes[0].y);
          ctx.lineTo(node.x, node.y);
          ctx.stroke();
        }
      });
    }

    // Draw nodes
    nodes.forEach(node => {
      const size = node.ring === 0 ? 4 : 2;
      const glowSize = node.active ? size * 2 : size;
      
      if (node.active) {
        // Glow effect
        const gradient = ctx.createRadialGradient(
          node.x, node.y, 0,
          node.x, node.y, glowSize
        );
        gradient.addColorStop(0, 'rgba(168, 85, 247, 0.8)');
        gradient.addColorStop(1, 'rgba(168, 85, 247, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(node.x, node.y, glowSize, 0, Math.PI * 2);
        ctx.fill();
      }
      
      // Node core
      ctx.fillStyle = node.active ? '#a855f7' : '#64748b';
      ctx.beginPath();
      ctx.arc(node.x, node.y, size, 0, Math.PI * 2);
      ctx.fill();
    });

    animationRef.current = requestAnimationFrame(drawWeb);
  }, [data]);

  useEffect(() => {
    initializeWeb();
    drawWeb();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [drawWeb]);

  return (
    <div className="absolute top-24 right-4 w-64 h-48">
      <canvas
        ref={canvasRef}
        width={256}
        height={192}
        className="w-full h-full"
      />
    </div>
  );
};

// Composite Health Orb Component
const HealthOrb = ({ data }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef();

  const getOrbColor = () => {
    const emotionColors = {
      curious: [34, 197, 94],
      creative: [168, 85, 247], 
      anxious: [245, 158, 11],
      fragmented: [239, 68, 68],
      crystalline: [59, 130, 246],
      reblooming: [255, 107, 157],
      contemplative: [100, 116, 139],
      excited: [249, 115, 22],
      melancholic: [99, 102, 241],
      harmonious: [16, 185, 129],
      turbulent: [220, 38, 38],
      luminous: [251, 191, 36]
    };
    
    return emotionColors[data.emotion] || [100, 116, 139];
  };

  const drawOrb = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;
    
    ctx.clearRect(0, 0, width, height);

    const centerX = width / 2;
    const centerY = height / 2;
    const baseRadius = 40;
    
    // Calculate orb properties
    const healthScore = (data.metrics.scup + (1 - data.metrics.entropy) + (1 - data.metrics.heat)) / 3;
    const orbRadius = baseRadius * (0.7 + healthScore * 0.3);
    const [r, g, b] = getOrbColor();
    
    // Pulsing effect based on tick rate
    const pulsePhase = Date.now() * 0.001 * data.tickRate;
    const pulseFactor = 1 + Math.sin(pulsePhase) * 0.1;
    const currentRadius = orbRadius * pulseFactor;

    // Draw main orb with gradient
    const gradient = ctx.createRadialGradient(
      centerX - currentRadius * 0.3, 
      centerY - currentRadius * 0.3, 
      0,
      centerX, 
      centerY, 
      currentRadius
    );
    
    const alpha = 0.3 + data.intensity * 0.7;
    gradient.addColorStop(0, `rgba(${r + 50}, ${g + 50}, ${b + 50}, ${alpha})`);
    gradient.addColorStop(0.7, `rgba(${r}, ${g}, ${b}, ${alpha})`);
    gradient.addColorStop(1, `rgba(${Math.max(0, r - 50)}, ${Math.max(0, g - 50)}, ${Math.max(0, b - 50)}, 0.1)`);

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, currentRadius, 0, Math.PI * 2);
    ctx.fill();

    // Add cracks for fragmented state
    if (data.emotion === 'fragmented' || data.emotion === 'turbulent') {
      ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, 0.8)`;
      ctx.lineWidth = 2;
      
      const numCracks = 3 + Math.floor(data.metrics.entropy * 5);
      for (let i = 0; i < numCracks; i++) {
        const angle = (i / numCracks) * Math.PI * 2;
        const startX = centerX + Math.cos(angle) * (currentRadius * 0.3);
        const startY = centerY + Math.sin(angle) * (currentRadius * 0.3);
        const endX = centerX + Math.cos(angle) * currentRadius;
        const endY = centerY + Math.sin(angle) * currentRadius;
        
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
      }
    }

    // Outer ring for system status
    ctx.strokeStyle = healthScore > 0.7 ? 
      'rgba(34, 197, 94, 0.6)' : 
      healthScore > 0.4 ? 
      'rgba(245, 158, 11, 0.6)' : 
      'rgba(239, 68, 68, 0.6)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(centerX, centerY, currentRadius + 10, 0, Math.PI * 2);
    ctx.stroke();

    // Draw metrics text
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.font = '10px Inter, sans-serif';
    ctx.textAlign = 'center';
    
    ctx.fillText(`SCUP: ${(data.metrics.scup * 100).toFixed(0)}%`, centerX, centerY - 5);
    ctx.fillText(`Health: ${(healthScore * 100).toFixed(0)}%`, centerX, centerY + 8);

    animationRef.current = requestAnimationFrame(drawOrb);
  }, [data]);

  useEffect(() => {
    drawOrb();
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [drawOrb]);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32">
      <canvas
        ref={canvasRef}
        width={128}
        height={128}
        className="w-full h-full"
      />
    </div>
  );
};

// Hologram shader text effect
function HologramShaderText({ children, className = '', ...props }) {
  return (
    <span
      className={`text-glow font-dawn drop-shadow-[0_0_8px_#00ffff] drop-shadow-[0_0_16px_#ff00ff] drop-shadow-[0_0_32px_#ffaa00] ${className}`}
      style={{
        filter: 'blur(0.5px) contrast(1.2)',
        letterSpacing: '0.02em',
        WebkitTextStroke: '0.5px #00ffff',
      }}
      {...props}
    >
      {children}
    </span>
  );
}

// Animated gradient mesh background
function AnimatedGradientMesh() {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let running = true;
    const w = window.innerWidth;
    const h = window.innerHeight;
    canvas.width = w;
    canvas.height = h;
    // Mesh points
    const points = Array.from({ length: 8 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      dx: (Math.random() - 0.5) * 0.5,
      dy: (Math.random() - 0.5) * 0.5,
      color: [
        ['#00ffff', '#ff00ff', '#ffaa00'][Math.floor(Math.random() * 3)],
        Math.random() * 0.7 + 0.3
      ]
    }));
    function draw() {
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < points.length; i++) {
        const p = points[i];
        // Animate
        p.x += p.dx;
        p.y += p.dy;
        if (p.x < 0 || p.x > w) p.dx *= -1;
        if (p.y < 0 || p.y > h) p.dy *= -1;
        // Draw radial gradient
        const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, w * 0.5);
        grad.addColorStop(0, `${p.color[0]}${Math.floor(p.color[1]*255).toString(16)}`);
        grad.addColorStop(1, 'transparent');
        ctx.globalAlpha = 0.5;
        ctx.beginPath();
        ctx.arc(p.x, p.y, w * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = grad;
        ctx.fill();
      }
      if (running) requestAnimationFrame(draw);
    }
    draw();
    return () => { running = false; };
  }, []);
  return <canvas ref={canvasRef} style={{ position: 'fixed', left: 0, top: 0, width: '100vw', height: '100vh', zIndex: 0, pointerEvents: 'none' }} />;
}

// Blur layers for depth
function BlurLayers() {
  return (
    <>
      <div style={{ position: 'fixed', left: 0, top: 0, width: '100vw', height: '100vh', zIndex: 2, pointerEvents: 'none', backdropFilter: 'blur(8px) brightness(1.1)', opacity: 0.12 }} />
      <div style={{ position: 'fixed', left: 0, top: 0, width: '100vw', height: '100vh', zIndex: 3, pointerEvents: 'none', backdropFilter: 'blur(24px) brightness(1.2)', opacity: 0.08 }} />
    </>
  );
}

// Main Central Visualization Component
const CentralVisualization = () => {
  const { data, connected } = useConsciousnessData();
  const [organicMode, setOrganicMode] = useState(false);

  return (
    <div className="relative h-full w-full min-h-screen min-w-screen overflow-hidden" style={{ background: 'transparent', fontFamily: 'dawn, monospace' }}>
      {/* Animated mesh background */}
      <AnimatedGradientMesh />
      {/* Blur layers for depth */}
      <BlurLayers />
      {/* Scanline and static overlays */}
      <div className="scanlines" />
      <div className="static-noise" />
      <button
        className="absolute top-2 left-2 z-20 px-4 py-2 rounded-lg font-bold text-white bg-gradient-to-r from-dawn-cyan to-dawn-magenta shadow-dawn-glow hover:scale-105 transition-all text-glow font-dawn"
        onClick={() => setOrganicMode(m => !m)}
      >
        {organicMode ? 'Switch to Classic' : 'Switch to Organic'}
      </button>
      {organicMode ? (
        <OrganicPanelSystem
          renderPanel={panel => (
            <HologramShaderText>{panel.label}</HologramShaderText>
          )}
        />
      ) : (
        <React.Fragment>
          {/* Connection Status Indicator */}
          <div className="absolute top-2 right-2 z-10">
            <div className={`w-3 h-3 rounded-full ${connected ? 'bg-dawn-cyan' : 'bg-dawn-amber'} shadow-dawn-glow`}>
              {connected && (
                <div className="w-3 h-3 rounded-full bg-dawn-cyan animate-ping"></div>
              )}
            </div>
          </div>

          {/* Visualization Components */}
          <div className="absolute inset-0 pointer-events-none">
            <MoodGradientDisplay data={data} />
            <TickRhythmOverlay data={data} />
            <PatternWeb data={data} />
            <HealthOrb data={data} />
          </div>

          {/* Status Panel */}
          <div className="absolute bottom-4 right-4 bg-[#0a0a0aee] rounded-lg p-3 min-w-48 shadow-dawn-glow border border-dawn-cyan/30">
            <h3 className="text-dawn-cyan text-sm font-semibold mb-2 text-glow font-dawn">DAWN Status</h3>
            <div className="space-y-1 text-xs">
              <div className="flex justify-between">
                <span className="text-dawn-magenta">Emotion:</span>
                <HologramShaderText>{data.emotion}</HologramShaderText>
              </div>
              <div className="flex justify-between">
                <span className="text-dawn-magenta">Intensity:</span>
                <HologramShaderText>{(data.intensity * 100).toFixed(0)}%</HologramShaderText>
              </div>
              <div className="flex justify-between">
                <span className="text-dawn-magenta">Tick Rate:</span>
                <HologramShaderText>{data.tickRate.toFixed(2)}x</HologramShaderText>
              </div>
              <div className="flex justify-between">
                <span className="text-dawn-magenta">Patterns:</span>
                <HologramShaderText>{data.patterns.length}</HologramShaderText>
              </div>
              {data.anomalies.length > 0 && (
                <div className="mt-2 p-2 bg-dawn-amber/20 rounded text-dawn-amber text-xs text-glow font-dawn shadow-holo-glow">
                  {data.anomalies.length} anomal{data.anomalies.length === 1 ? 'y' : 'ies'} detected
                </div>
              )}
            </div>
          </div>
        </React.Fragment>
      )}
    </div>
  );
};

export default CentralVisualization; 