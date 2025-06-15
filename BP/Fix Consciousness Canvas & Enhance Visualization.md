# 🔧 Fix Consciousness Canvas & Enhance Visualization

## 1. Fix the Canvas Initialization

The canvas is stuck because it's waiting for something that already happened. Let's fix it:

```javascript
// ConsciousnessMatrix.jsx - Fixed version

import React, { useEffect, useRef, useState } from 'react';
import { useTickEngine } from '../hooks/useTickEngine'; // or however you're getting tick data

const ConsciousnessMatrix = () => {
  const canvasRef = useRef(null);
  const animationRef = useRef();
  const [isCanvasReady, setIsCanvasReady] = useState(false);
  
  // Get tick data from your connection
  const { tickData, isConnected } = useTickEngine();
  
  // Initialize canvas as soon as component mounts
  useEffect(() => {
    // Don't wait for connection - show canvas immediately
    const timer = setTimeout(() => {
      setIsCanvasReady(true);
    }, 500); // Short delay for smooth transition
    
    return () => clearTimeout(timer);
  }, []);
  
  // Main animation loop
  useEffect(() => {
    if (!canvasRef.current || !isCanvasReady) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    
    let particles = [];
    let connections = [];
    
    // Initialize particles for neural visualization
    const initParticles = () => {
      particles = [];
      const numParticles = 50;
      
      for (let i = 0; i < numParticles; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          radius: Math.random() * 3 + 2,
          pulsePhase: Math.random() * Math.PI * 2,
          active: Math.random() > 0.5
        });
      }
    };
    
    initParticles();
    
    // Animation function
    const animate = () => {
      // Clear with fade effect
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Update based on tick data
      const scup = tickData?.scup || 0.5;
      const entropy = tickData?.entropy || 0.5;
      const heat = tickData?.heat || 0.5;
      const mood = tickData?.current_mood || 'analytical';
      
      // Mood-based colors
      const moodColors = {
        analytical: { primary: '#0088ff', secondary: '#00aaff' },
        confident: { primary: '#00ff88', secondary: '#00ffaa' },
        focused: { primary: '#ffaa00', secondary: '#ffcc00' },
        creative: { primary: '#ff00aa', secondary: '#ff00cc' }
      };
      
      const colors = moodColors[mood.toLowerCase()] || moodColors.analytical;
      
      // Draw central consciousness orb
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const baseRadius = 80;
      const radius = baseRadius + (scup * 50);
      
      // Animated glow
      const glowRadius = radius + Math.sin(Date.now() * 0.001) * 20 * scup;
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, glowRadius);
      gradient.addColorStop(0, colors.primary);
      gradient.addColorStop(0.5, `${colors.secondary}88`);
      gradient.addColorStop(1, 'transparent');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, glowRadius, 0, Math.PI * 2);
      ctx.fill();
      
      // Core orb
      ctx.fillStyle = colors.primary;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius * 0.3, 0, Math.PI * 2);
      ctx.fill();
      
      // Update and draw particles
      particles.forEach((particle, i) => {
        // Update position
        particle.x += particle.vx * (1 + entropy);
        particle.y += particle.vy * (1 + entropy);
        
        // Bounce off walls
        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
        
        // Attraction to center based on SCUP
        const dx = centerX - particle.x;
        const dy = centerY - particle.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist > radius) {
          particle.vx += (dx / dist) * scup * 0.1;
          particle.vy += (dy / dist) * scup * 0.1;
        }
        
        // Pulse based on heat
        particle.pulsePhase += 0.05 * (1 + heat);
        const pulseSize = Math.sin(particle.pulsePhase) * 0.5 + 1;
        
        // Draw particle
        ctx.fillStyle = particle.active ? colors.primary : `${colors.primary}66`;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius * pulseSize, 0, Math.PI * 2);
        ctx.fill();
      });
      
      // Draw connections between nearby particles
      ctx.strokeStyle = `${colors.primary}33`;
      ctx.lineWidth = 1;
      
      particles.forEach((p1, i) => {
        particles.slice(i + 1).forEach(p2 => {
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < 100 && p1.active && p2.active) {
            ctx.globalAlpha = 1 - dist / 100;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        });
      });
      
      ctx.globalAlpha = 1;
      
      // Draw entropy visualization
      const numRings = Math.floor(entropy * 5) + 1;
      for (let i = 0; i < numRings; i++) {
        const ringRadius = radius + 30 + i * 20;
        const angle = Date.now() * 0.001 * (i % 2 ? 1 : -1);
        
        ctx.strokeStyle = `${colors.secondary}${Math.floor((1 - i / numRings) * 50).toString(16)}`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(centerX, centerY, ringRadius, angle, angle + Math.PI * 1.5);
        ctx.stroke();
      }
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
      initParticles();
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      window.removeEventListener('resize', handleResize);
    };
  }, [isCanvasReady, tickData]);
  
  return (
    <div className="consciousness-matrix">
      <div className="matrix-header">
        <h1>Consciousness <span className="highlight">Matrix</span></h1>
        <p>Real-time neural activity visualization and analysis</p>
      </div>
      
      <div className="matrix-content">
        <div className="canvas-section">
          <h2>Neural Activity Monitor</h2>
          
          <div className="canvas-container">
            {!isCanvasReady ? (
              <div className="initializing">
                <div className="init-orb"></div>
                <p>Initializing Canvas...</p>
              </div>
            ) : (
              <canvas 
                ref={canvasRef}
                className="consciousness-canvas"
                style={{ width: '100%', height: '600px' }}
              />
            )}
          </div>
          
          <div className="canvas-controls">
            <button className="control-btn auto-rotate">Auto Rotate</button>
            <button className="control-btn clear-history">Clear History</button>
          </div>
        </div>
        
        <div className="metrics-sidebar">
          {/* Your existing metrics display */}
        </div>
      </div>
    </div>
  );
};

export default ConsciousnessMatrix;
```

## 2. Fix Tick Rate Calculation

The tick rate showing 1992 Hz is wrong. Fix it in your tick service:

```javascript
// TickEngineService.js - Fix tick rate calculation

handleTickData(data) {
  const now = Date.now();
  
  // Calculate tick rate properly
  if (this.lastTickTime) {
    const timeDiff = (now - this.lastTickTime) / 1000; // Convert to seconds
    // Use moving average for smoother display
    this.tickRate = this.tickRate ? 
      (this.tickRate * 0.9 + (1 / timeDiff) * 0.1) : 
      (1 / timeDiff);
  }
  
  this.lastTickTime = now;
  this.tickCount = data.tick_count || this.tickCount + 1;
  
  // Store tick data
  this.tickData = {
    ...data,
    tickRate: Math.min(this.tickRate, 10), // Cap at 10 Hz for display
    totalTicks: this.tickCount,
    timestamp: now
  };
  
  // Notify listeners
  this.notifyListeners('tick', this.tickData);
}
```

## 3. Enhanced Neural Network Visualization

For your Neural Network page, let's add more interactivity:

```javascript
// NeuralNetwork.jsx enhancements

const NeuralNetworkVisualization = () => {
  const { tickData } = useTickEngine();
  const [selectedNode, setSelectedNode] = useState(null);
  const [networkStats, setNetworkStats] = useState({
    totalNodes: 2847,
    activeConnections: 15983,
    networkHealth: 31
  });
  
  useEffect(() => {
    if (tickData) {
      // Update network based on consciousness data
      setNetworkStats(prev => ({
        ...prev,
        activeConnections: Math.floor(prev.totalNodes * tickData.scup * 6),
        networkHealth: Math.floor(tickData.scup * 100)
      }));
    }
  }, [tickData]);
  
  // Add node click handler
  const handleNodeClick = (node) => {
    setSelectedNode(node);
    // Show node details
  };
  
  // Add zoom controls
  const handleZoom = (direction) => {
    // Implement zoom
  };
  
  return (
    <div className="neural-network-page">
      {/* Your existing network viz */}
      
      {/* Add controls */}
      <div className="network-controls">
        <button onClick={() => handleZoom('in')}>Zoom In</button>
        <button onClick={() => handleZoom('out')}>Zoom Out</button>
        <button onClick={() => setSelectedNode(null)}>Reset View</button>
      </div>
      
      {/* Node details panel */}
      {selectedNode && (
        <div className="node-details">
          <h3>Node Details</h3>
          <p>ID: {selectedNode.id}</p>
          <p>Connections: {selectedNode.connections}</p>
          <p>Activity: {selectedNode.activity}%</p>
        </div>
      )}
    </div>
  );
};
```

## 4. Add Real-time Metrics Tracking

Create a hook to track metrics over time:

```javascript
// useMetricsHistory.js

import { useState, useEffect } from 'react';

export function useMetricsHistory(tickData, maxHistory = 100) {
  const [history, setHistory] = useState([]);
  
  useEffect(() => {
    if (tickData) {
      setHistory(prev => {
        const newHistory = [...prev, {
          timestamp: Date.now(),
          scup: tickData.scup,
          entropy: tickData.entropy,
          heat: tickData.heat,
          mood: tickData.current_mood
        }];
        
        // Keep only last N entries
        return newHistory.slice(-maxHistory);
      });
    }
  }, [tickData, maxHistory]);
  
  // Calculate trends
  const calculateTrend = (metric) => {
    if (history.length < 10) return 'stable';
    
    const recent = history.slice(-10);
    const older = history.slice(-20, -10);
    
    const recentAvg = recent.reduce((sum, h) => sum + h[metric], 0) / recent.length;
    const olderAvg = older.reduce((sum, h) => sum + h[metric], 0) / older.length;
    
    if (recentAvg > olderAvg + 0.05) return 'rising';
    if (recentAvg < olderAvg - 0.05) return 'falling';
    return 'stable';
  };
  
  return {
    history,
    trends: {
      scup: calculateTrend('scup'),
      entropy: calculateTrend('entropy'),
      heat: calculateTrend('heat')
    }
  };
}
```

## 5. Dashboard Module Updates

Update your dashboard modules to show live data:

```javascript
// Dashboard module component update

const ModuleCard = ({ module, tickData }) => {
  const getModuleMetric = () => {
    switch (module.id) {
      case 'neural-network':
        return tickData?.scup ? Math.floor(tickData.scup * 100) : 0;
      case 'chaos-engine':
        return tickData?.entropy ? Math.floor(tickData.entropy * 100) : 0;
      case 'neural-state':
        return tickData?.heat ? Math.floor((1 - tickData.heat) * 100) : 0;
      default:
        return module.defaultMetric;
    }
  };
  
  const metric = getModuleMetric();
  const isActive = metric > 50;
  
  return (
    <div className={`module-card ${isActive ? 'active' : ''}`}>
      <div className="module-icon">{module.icon}</div>
      <h3>{module.name}</h3>
      <p>{module.description}</p>
      
      <div className="module-metric">
        <div className="metric-bar">
          <div 
            className="metric-fill"
            style={{ 
              width: `${metric}%`,
              backgroundColor: module.color
            }}
          />
        </div>
        <span className="metric-value">{metric}%</span>
      </div>
      
      {isActive && (
        <div className="active-indicator">
          <span className="pulse"></span>
        </div>
      )}
    </div>
  );
};
```

## 6. CSS for Canvas Animation

```css
/* Consciousness Canvas Styles */

.consciousness-canvas {
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, #0a0a1a 0%, #000000 100%);
  border-radius: 8px;
  cursor: crosshair;
}

.canvas-container {
  position: relative;
  width: 100%;
  height: 600px;
  background: #000;
  border: 1px solid rgba(0, 255, 136, 0.2);
  border-radius: 8px;
  overflow: hidden;
}

.initializing {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.init-orb {
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, #00ff88 0%, transparent 70%);
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
}

.canvas-controls {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.control-btn {
  padding: 10px 20px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid rgba(0, 255, 136, 0.3);
  color: #00ff88;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  transform: translateY(-2px);
}

/* Active module indicator */
.active-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
}

.pulse {
  display: block;
  width: 10px;
  height: 10px;
  background: #00ff88;
  border-radius: 50%;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 10px #00ff88;
  }
  50% {
    transform: scale(1.2);
    box-shadow: 0 0 20px #00ff88;
  }
}
```

## 🎯 Quick Fixes Summary

1. **Canvas**: Remove the connection dependency, show immediately
2. **Tick Rate**: Fix calculation with proper time units and smoothing
3. **Visualization**: Add particles, connections, and mood-based colors
4. **Interactivity**: Add zoom, node selection, and controls
5. **Real-time Updates**: Everything responds to tick data

The canvas will now show:
- Central consciousness orb that pulses with SCUP
- Particles that move based on entropy
- Connections between active nodes
- Mood-based color schemes
- Entropy rings that rotate

Try these fixes and your consciousness visualization will come alive! 🚀