import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useConsciousness } from '../contexts/ConsciousnessContext';

// Types
type VisualizationType = 'network' | 'radar';

interface ProcessMetrics {
  scup: number;
  entropy: number;
  coherence: number;
  heat: number;
  drift: number;
  resonance: number;
}

interface PulseConnection {
  from: number;
  to: number;
  progress: number;
  intensity: number;
  color: string;
}

// Clean, minimal configuration
const METRICS_CONFIG = {
  scup: { label: 'SCUP', color: '#00ff88' },
  entropy: { label: 'Entropy', color: '#ff6b6b' },
  coherence: { label: 'Coherence', color: '#4dabf7' },
  heat: { label: 'Heat', color: '#ffd43b' },
  drift: { label: 'Drift', color: '#c084fc' },
  resonance: { label: 'Resonance', color: '#66d9ef' }
};

export default function NeuralNetwork() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const pulseConnectionsRef = useRef<PulseConnection[]>([]);
  const lastPulseTimeRef = useRef<number>(0);
  
  const [visualizationType, setVisualizationType] = useState<VisualizationType>('network');
  
  // 🔥 GET REAL TICK DATA FROM DAWN CONSCIOUSNESS ENGINE
  const { data: consciousnessData, isLoading } = useConsciousness();
  
  // Map real DAWN data to neural metrics
  const [metrics, setMetrics] = useState<ProcessMetrics>({
    scup: 0.65,        // Will be updated from real data
    entropy: 0.18,     // Will be updated from real data  
    coherence: 0.73,   // Derived from network health
    heat: 0.45,        // Will be updated from real data
    drift: 0.28,       // Derived from tick rate stability
    resonance: 0.62    // Derived from mood state
  });
  
  // 🎯 UPDATE METRICS FROM REAL TICK DATA
  useEffect(() => {
    if (!isLoading && consciousnessData) {
      // Map real DAWN consciousness data to neural network metrics
      const newMetrics: ProcessMetrics = {
        scup: consciousnessData.scup / 100,  // Convert from 0-100 to 0-1
        entropy: consciousnessData.entropy,   // Already 0-1
        heat: consciousnessData.heat,         // Already 0-1
        coherence: consciousnessData.networkHealth / 100, // Network health as coherence
        drift: Math.max(0, Math.min(1, (200 - consciousnessData.tickRate) / 200)), // Tick rate stability (inverted)
        resonance: moodToResonance(consciousnessData.mood) // Convert mood to resonance value
      };
      
      setMetrics(newMetrics);
    }
  }, [consciousnessData, isLoading]);
  
  // Convert mood string to resonance value (0-1)
  const moodToResonance = (mood: string): number => {
    const moodMap: { [key: string]: number } = {
      'euphoric': 0.95,
      'confident': 0.85,  
      'focused': 0.75,
      'creative': 0.80,
      'analytical': 0.70,
      'serene': 0.60,
      'contemplative': 0.50,
      'excited': 0.90,
      'active': 0.85,
      'anxious': 0.30,
      'chaotic': 0.20,
      'critical': 0.40
    };
    return moodMap[mood] || 0.50; // Default to 0.50 if mood not found
  };
  
  // Generate pulsing connections based on real metrics
  const generatePulseConnections = useCallback(() => {
    const now = Date.now();
    const metricKeys = Object.keys(METRICS_CONFIG);
    const nodeCount = metricKeys.length;
    
    // Generate pulses based on system activity
    const avgActivity = (metrics.scup + metrics.heat + metrics.coherence + metrics.resonance) / 4;
    const pulseFrequency = 500 + (1 - avgActivity) * 1500; // Higher activity = faster pulses
    
    if (now - lastPulseTimeRef.current > pulseFrequency) {
      // Create new pulse connections
      const connectionCount = Math.floor(1 + avgActivity * 3); // 1-4 connections based on activity
      
      for (let i = 0; i < connectionCount; i++) {
        const fromIndex = Math.floor(Math.random() * nodeCount);
        let toIndex = Math.floor(Math.random() * nodeCount);
        
        // Ensure different nodes
        while (toIndex === fromIndex) {
          toIndex = Math.floor(Math.random() * nodeCount);
        }
        
        // Color based on metric values and connection type
        const fromMetric = Object.values(metrics)[fromIndex];
        const toMetric = Object.values(metrics)[toIndex];
        const avgMetric = (fromMetric + toMetric) / 2;
        
        // Choose color based on dominant metric
        const colors = Object.values(METRICS_CONFIG).map(config => config.color);
        const dominantColor = colors[fromIndex];
        
        pulseConnectionsRef.current.push({
          from: fromIndex,
          to: toIndex,
          progress: 0,
          intensity: 0.3 + avgMetric * 0.7, // Intensity based on metric values
          color: dominantColor
        });
      }
      
      lastPulseTimeRef.current = now;
    }
    
    // Update existing pulses
    pulseConnectionsRef.current = pulseConnectionsRef.current.filter(pulse => {
      pulse.progress += 0.02 + avgActivity * 0.03; // Speed based on activity
      return pulse.progress < 1.0; // Remove completed pulses
    });
  }, [metrics]);
  
  // Simple network visualization with pulsing connections
  const drawNetwork = useCallback((ctx: CanvasRenderingContext2D) => {
    const width = ctx.canvas.width;
    const height = ctx.canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    
    // Clear canvas
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, width, height);
    
    // Draw minimal grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
    ctx.lineWidth = 1;
    
    // Vertical lines
    for (let x = 0; x < width; x += 50) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = 0; y < height; y += 50) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    
    // Draw core nodes in a circle
    const nodeCount = 6;
    const radius = 150;
    const nodes: Array<{x: number, y: number, metric: keyof ProcessMetrics}> = [];
    
    Object.keys(METRICS_CONFIG).forEach((metric, i) => {
      const angle = (i / nodeCount) * Math.PI * 2 - Math.PI / 2;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      nodes.push({ x, y, metric: metric as keyof ProcessMetrics });
    });
    
    // Draw static connections (very subtle)
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
    ctx.lineWidth = 1;
    
    nodes.forEach((node, i) => {
      nodes.forEach((other, j) => {
        if (i < j) {
          ctx.beginPath();
          ctx.moveTo(node.x, node.y);
          ctx.lineTo(other.x, other.y);
          ctx.stroke();
        }
      });
    });
    
    // Draw center connections
    nodes.forEach(node => {
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(node.x, node.y);
      ctx.stroke();
    });
    
    // Generate and draw pulsing connections
    generatePulseConnections();
    
    // Draw pulsing data flows
    pulseConnectionsRef.current.forEach(pulse => {
      const fromNode = nodes[pulse.from];
      const toNode = nodes[pulse.to];
      
      if (fromNode && toNode) {
        // Calculate current position along the line
        const currentX = fromNode.x + (toNode.x - fromNode.x) * pulse.progress;
        const currentY = fromNode.y + (toNode.y - fromNode.y) * pulse.progress;
        
        // Draw pulsing line segment
        const segmentLength = 30;
        const startProgress = Math.max(0, pulse.progress - 0.2);
        const startX = fromNode.x + (toNode.x - fromNode.x) * startProgress;
        const startY = fromNode.y + (toNode.y - fromNode.y) * startProgress;
        
        // Fade effect based on progress
        const fadeAlpha = Math.sin(pulse.progress * Math.PI) * pulse.intensity;
        
        // Draw glowing line
        ctx.strokeStyle = pulse.color + Math.floor(fadeAlpha * 255).toString(16).padStart(2, '0');
        ctx.lineWidth = 2 + pulse.intensity * 2;
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(currentX, currentY);
        ctx.stroke();
        
        // Draw pulse head (bright dot)
        ctx.fillStyle = pulse.color + Math.floor(fadeAlpha * 255).toString(16).padStart(2, '0');
        ctx.beginPath();
        ctx.arc(currentX, currentY, 3 + pulse.intensity * 2, 0, Math.PI * 2);
        ctx.fill();
      }
    });
    
    // Draw nodes
    nodes.forEach(node => {
      const value = metrics[node.metric];
      const config = METRICS_CONFIG[node.metric];
      const size = 20 + value * 20; // Node size based on metric
      
      // Simple circle, no glow
      ctx.fillStyle = config.color + '20'; // Very transparent
      ctx.beginPath();
      ctx.arc(node.x, node.y, size, 0, Math.PI * 2);
      ctx.fill();
      
      // Border with activity pulse
      const pulseSize = size + Math.sin(Date.now() * 0.003 + value * 10) * 2;
      ctx.strokeStyle = config.color + Math.floor((0.5 + value * 0.5) * 255).toString(16).padStart(2, '0');
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(node.x, node.y, pulseSize, 0, Math.PI * 2);
      ctx.stroke();
      
      // Center dot
      ctx.fillStyle = config.color;
      ctx.beginPath();
      ctx.arc(node.x, node.y, 3, 0, Math.PI * 2);
      ctx.fill();
      
      // Label
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(config.label, node.x, node.y - size - 15);
      ctx.fillText(`${(value * 100).toFixed(0)}%`, node.x, node.y - size - 30);
    });
    
    // Draw center node with activity pulse
    const centerPulse = 5 + Math.sin(Date.now() * 0.005) * 2;
    ctx.fillStyle = '#00ff88';
    ctx.beginPath();
    ctx.arc(centerX, centerY, centerPulse, 0, Math.PI * 2);
    ctx.fill();
    
    // Show connection status
    if (!consciousnessData.isConnected) {
      ctx.fillStyle = 'rgba(255, 68, 68, 0.8)';
      ctx.font = '14px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('DISCONNECTED', centerX, centerY + 40);
    }
  }, [metrics, consciousnessData, generatePulseConnections]);
  
  // Clean radar visualization
  const drawRadar = useCallback((ctx: CanvasRenderingContext2D) => {
    const width = ctx.canvas.width;
    const height = ctx.canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const maxRadius = Math.min(width, height) * 0.35;
    
    // Clear canvas
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, width, height);
    
    // Draw minimal rings
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    
    [0.25, 0.5, 0.75, 1].forEach(scale => {
      ctx.beginPath();
      ctx.arc(centerX, centerY, maxRadius * scale, 0, Math.PI * 2);
      ctx.stroke();
    });
    
    // Draw axes
    const metricKeys = Object.keys(METRICS_CONFIG) as Array<keyof ProcessMetrics>;
    metricKeys.forEach((_, i) => {
      const angle = (i / metricKeys.length) * Math.PI * 2 - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(
        centerX + Math.cos(angle) * maxRadius,
        centerY + Math.sin(angle) * maxRadius
      );
      ctx.stroke();
    });
    
    // Plot metrics
    const points: Array<{x: number, y: number}> = [];
    
    metricKeys.forEach((key, i) => {
      const angle = (i / metricKeys.length) * Math.PI * 2 - Math.PI / 2;
      const value = metrics[key];
      const r = value * maxRadius;
      
      points.push({
        x: centerX + Math.cos(angle) * r,
        y: centerY + Math.sin(angle) * r
      });
    });
    
    // Draw shape
    ctx.beginPath();
    points.forEach((point, i) => {
      if (i === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    });
    ctx.closePath();
    
    // Fill
    ctx.fillStyle = 'rgba(0, 255, 136, 0.05)';
    ctx.fill();
    
    // Stroke
    ctx.strokeStyle = 'rgba(0, 255, 136, 0.5)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw points and labels
    metricKeys.forEach((key, i) => {
      const angle = (i / metricKeys.length) * Math.PI * 2 - Math.PI / 2;
      const value = metrics[key];
      const r = value * maxRadius;
      const config = METRICS_CONFIG[key];
      
      // Point
      const x = centerX + Math.cos(angle) * r;
      const y = centerY + Math.sin(angle) * r;
      
      ctx.fillStyle = config.color;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
      
      // Label
      const labelR = maxRadius + 30;
      const labelX = centerX + Math.cos(angle) * labelR;
      const labelY = centerY + Math.sin(angle) * labelR;
      
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(config.label, labelX, labelY);
      ctx.fillText(`${(value * 100).toFixed(0)}%`, labelX, labelY + 15);
    });
    
    // Show connection status
    if (!consciousnessData.isConnected) {
      ctx.fillStyle = 'rgba(255, 68, 68, 0.8)';
      ctx.font = '14px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('DISCONNECTED', centerX, centerY);
    }
  }, [metrics, consciousnessData]);
  
  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const draw = () => {
      if (visualizationType === 'network') {
        drawNetwork(ctx);
      } else {
        drawRadar(ctx);
      }
      
      animationRef.current = requestAnimationFrame(draw);
    };
    
    draw();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [visualizationType, drawNetwork, drawRadar]);
  
  const styles = {
    container: {
      backgroundColor: '#0a0a0a',
      color: '#ffffff',
      minHeight: '100vh',
      fontFamily: 'monospace'
    },
    header: {
      padding: '20px',
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
    },
    title: {
      fontSize: '24px',
      fontWeight: '300',
      color: '#00ff88',
      marginBottom: '8px'
    },
    subtitle: {
      fontSize: '14px',
      color: 'rgba(255, 255, 255, 0.5)'
    },
    controls: {
      padding: '20px',
      display: 'flex',
      gap: '10px',
      alignItems: 'center'
    },
    button: (isActive: boolean) => ({
      padding: '8px 20px',
      backgroundColor: isActive ? 'rgba(0, 255, 136, 0.1)' : 'transparent',
      border: `1px solid ${isActive ? '#00ff88' : 'rgba(255, 255, 255, 0.2)'}`,
      borderRadius: '4px',
      color: isActive ? '#00ff88' : 'rgba(255, 255, 255, 0.8)',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
      fontSize: '14px'
    }),
    status: {
      marginLeft: 'auto',
      fontSize: '12px',
      color: consciousnessData.isConnected ? '#00ff88' : '#ff4444'
    },
    canvas: {
      display: 'block',
      width: '100%',
      maxWidth: '800px',
      height: '600px',
      margin: '0 auto'
    },
    metrics: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
      gap: '10px',
      padding: '20px',
      maxWidth: '800px',
      margin: '0 auto'
    },
    metric: {
      padding: '15px',
      backgroundColor: 'rgba(255, 255, 255, 0.02)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: '4px'
    },
    metricLabel: {
      fontSize: '12px',
      color: 'rgba(255, 255, 255, 0.5)',
      marginBottom: '4px'
    },
    metricValue: (color: string) => ({
      fontSize: '20px',
      color: color,
      fontWeight: 'bold'
    }),
    tickInfo: {
      fontSize: '11px',
      color: 'rgba(255, 255, 255, 0.4)',
      marginTop: '4px'
    }
  };
  
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Neural Network</h1>
        <p style={styles.subtitle}>
          Real-time neural activity visualization • Tick Rate: {consciousnessData.tickRate}/s • Mood: {consciousnessData.mood}
        </p>
      </div>
      
      <div style={styles.controls}>
        <button
          style={styles.button(visualizationType === 'network')}
          onClick={() => setVisualizationType('network')}
        >
          Network View
        </button>
        <button
          style={styles.button(visualizationType === 'radar')}
          onClick={() => setVisualizationType('radar')}
        >
          Radar View
        </button>
        <div style={styles.status}>
          {consciousnessData.isConnected ? 
            `🟢 Connected • ${consciousnessData.nodes} nodes • ${consciousnessData.connections} connections` : 
            '🔴 Disconnected from tick engine'
          }
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        style={styles.canvas}
      />
      
      <div style={styles.metrics}>
        {Object.entries(METRICS_CONFIG).map(([key, config]) => (
          <div key={key} style={styles.metric}>
            <div style={styles.metricLabel}>{config.label}</div>
            <div style={styles.metricValue(config.color)}>
              {(metrics[key as keyof ProcessMetrics] * 100).toFixed(0)}%
            </div>
            <div style={styles.tickInfo}>
              {key === 'scup' && `Raw: ${consciousnessData.scup.toFixed(1)}`}
              {key === 'entropy' && `Raw: ${consciousnessData.entropy.toFixed(3)}`}
              {key === 'heat' && `Raw: ${consciousnessData.heat.toFixed(3)}`}
              {key === 'coherence' && `Health: ${consciousnessData.networkHealth}%`}
              {key === 'drift' && `Tick: ${consciousnessData.tickRate}/s`}
              {key === 'resonance' && `Mood: ${consciousnessData.mood}`}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}