import React, { useEffect, useRef, useState, useMemo } from 'react';

// Types
type ProcessType = 'scup' | 'entropy' | 'coherence' | 'heat' | 'drift' | 'resonance';

interface ProcessMetrics {
  [key: string]: number; // 0-1 normalized values
}

interface RadarPoint {
  angle: number;
  radius: number;
  value: number;
  label: string;
  color: string;
}

interface HistoricalSpiral {
  points: Array<{
    timestamp: number;
    metrics: ProcessMetrics;
  }>;
  decay: number;
}

// Configuration
const PROCESS_CONFIG = {
  scup: {
    label: 'SCUP',
    color: '#00ffff',
    glow: 'rgba(0, 255, 255, 0.6)',
    optimal: [0.6, 0.8]
  },
  entropy: {
    label: 'Entropy',
    color: '#ff00ff',
    glow: 'rgba(255, 0, 255, 0.6)',
    optimal: [0.3, 0.7]
  },
  coherence: {
    label: 'Coherence',
    color: '#00ff88',
    glow: 'rgba(0, 255, 136, 0.6)',
    optimal: [0.7, 0.9]
  },
  heat: {
    label: 'Heat',
    color: '#ffaa00',
    glow: 'rgba(255, 170, 0, 0.6)',
    optimal: [0.4, 0.6]
  },
  drift: {
    label: 'Drift',
    color: '#ff4466',
    glow: 'rgba(255, 68, 102, 0.6)',
    optimal: [0.2, 0.4]
  },
  resonance: {
    label: 'Resonance',
    color: '#8844ff',
    glow: 'rgba(136, 68, 255, 0.6)',
    optimal: [0.5, 0.8]
  }
};

export default function NeuralRadarSystem() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  
  const [metrics, setMetrics] = useState<ProcessMetrics>({
    scup: 0.75,
    entropy: 0.45,
    coherence: 0.8,
    heat: 0.5,
    drift: 0.3,
    resonance: 0.65
  });
  
  const [historical, setHistorical] = useState<HistoricalSpiral>({
    points: [],
    decay: 0.98
  });
  
  const [selectedProcess, setSelectedProcess] = useState<ProcessType | null>(null);
  const [showSpiral, setShowSpiral] = useState(false);
  const [showOptimalZones, setShowOptimalZones] = useState(true);
  
  // Update metrics with mock data (replace with real consciousness data)
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => {
        const newMetrics: ProcessMetrics = {};
        
        Object.keys(prev).forEach(key => {
          // Smooth random walk
          const delta = (Math.random() - 0.5) * 0.05;
          newMetrics[key] = Math.max(0, Math.min(1, prev[key] + delta));
        });
        
        return newMetrics;
      });
      
      // Add to historical data
      setHistorical(prev => ({
        ...prev,
        points: [...prev.points.slice(-100), {
          timestamp: Date.now(),
          metrics: { ...metrics }
        }]
      }));
    }, 100);
    
    return () => clearInterval(interval);
  }, [metrics]);
  
  // Calculate radar points
  const radarPoints = useMemo(() => {
    const processes = Object.keys(PROCESS_CONFIG) as ProcessType[];
    const angleStep = (Math.PI * 2) / processes.length;
    
    return processes.map((process, index) => ({
      angle: index * angleStep - Math.PI / 2,
      radius: metrics[process] || 0,
      value: metrics[process] || 0,
      label: PROCESS_CONFIG[process].label,
      color: PROCESS_CONFIG[process].color
    }));
  }, [metrics]);
  
  // Animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const maxRadius = Math.min(centerX, centerY) - 100;
    
    let time = 0;
    
    const animate = () => {
      // Clear with fade effect
      ctx.fillStyle = 'rgba(0, 8, 20, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw grid
      drawRadarGrid(ctx, centerX, centerY, maxRadius);
      
      // Draw optimal zones if enabled
      if (showOptimalZones) {
        drawOptimalZones(ctx, centerX, centerY, maxRadius);
      }
      
      // Draw historical spiral if enabled
      if (showSpiral && historical.points.length > 1) {
        drawHistoricalSpiral(ctx, centerX, centerY, maxRadius, historical, time);
      }
      
      // Draw main radar
      drawRadar(ctx, centerX, centerY, maxRadius, radarPoints, selectedProcess);
      
      // Draw process labels
      drawLabels(ctx, centerX, centerY, maxRadius, radarPoints);
      
      // Draw center glow
      const glowSize = 20 + Math.sin(time * 0.02) * 10;
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, glowSize);
      gradient.addColorStop(0, 'rgba(0, 255, 255, 0.3)');
      gradient.addColorStop(1, 'transparent');
      ctx.fillStyle = gradient;
      ctx.fillRect(centerX - glowSize, centerY - glowSize, glowSize * 2, glowSize * 2);
      
      time++;
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [radarPoints, selectedProcess, showSpiral, showOptimalZones, historical]);
  
  // Drawing functions
  const drawRadarGrid = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    maxRadius: number
  ) => {
    const rings = 5;
    const processes = Object.keys(PROCESS_CONFIG);
    
    // Draw concentric rings
    for (let i = 1; i <= rings; i++) {
      const radius = (maxRadius / rings) * i;
      
      ctx.strokeStyle = `rgba(0, 255, 255, ${0.1 - i * 0.015})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.stroke();
      
      // Ring value labels
      if (i % 2 === 0) {
        ctx.fillStyle = 'rgba(0, 255, 255, 0.3)';
        ctx.font = '10px monospace';
        ctx.fillText(`${(i / rings * 100).toFixed(0)}%`, centerX + 5, centerY - radius + 5);
      }
    }
    
    // Draw spokes
    processes.forEach((_, index) => {
      const angle = (index * Math.PI * 2) / processes.length - Math.PI / 2;
      const x = centerX + Math.cos(angle) * maxRadius;
      const y = centerY + Math.sin(angle) * maxRadius;
      
      ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    });
  };
  
  const drawOptimalZones = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    maxRadius: number
  ) => {
    const processes = Object.keys(PROCESS_CONFIG) as ProcessType[];
    
    processes.forEach((process, index) => {
      const config = PROCESS_CONFIG[process];
      const angle = (index * Math.PI * 2) / processes.length - Math.PI / 2;
      const nextAngle = ((index + 1) * Math.PI * 2) / processes.length - Math.PI / 2;
      
      const innerRadius = config.optimal[0] * maxRadius;
      const outerRadius = config.optimal[1] * maxRadius;
      
      ctx.fillStyle = `${config.color}10`;
      ctx.strokeStyle = `${config.color}30`;
      ctx.lineWidth = 1;
      
      // Draw arc section
      ctx.beginPath();
      ctx.arc(centerX, centerY, innerRadius, angle, nextAngle);
      ctx.arc(centerX, centerY, outerRadius, nextAngle, angle, true);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    });
  };
  
  const drawRadar = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    maxRadius: number,
    points: RadarPoint[],
    selected: ProcessType | null
  ) => {
    // Draw filled area
    ctx.beginPath();
    points.forEach((point, index) => {
      const x = centerX + Math.cos(point.angle) * point.radius * maxRadius;
      const y = centerY + Math.sin(point.angle) * point.radius * maxRadius;
      
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    ctx.closePath();
    
    // Gradient fill
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, maxRadius);
    gradient.addColorStop(0, 'rgba(0, 255, 255, 0.1)');
    gradient.addColorStop(1, 'rgba(0, 255, 255, 0.05)');
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Draw outline
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.8)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw points
    points.forEach((point, index) => {
      const process = Object.keys(PROCESS_CONFIG)[index] as ProcessType;
      const config = PROCESS_CONFIG[process];
      const x = centerX + Math.cos(point.angle) * point.radius * maxRadius;
      const y = centerY + Math.sin(point.angle) * point.radius * maxRadius;
      
      // Point glow
      const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, 15);
      glowGradient.addColorStop(0, config.glow);
      glowGradient.addColorStop(1, 'transparent');
      ctx.fillStyle = glowGradient;
      ctx.fillRect(x - 15, y - 15, 30, 30);
      
      // Point core
      ctx.fillStyle = config.color;
      ctx.beginPath();
      ctx.arc(x, y, selected === process ? 8 : 5, 0, Math.PI * 2);
      ctx.fill();
      
      // Inner dot
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, Math.PI * 2);
      ctx.fill();
    });
  };
  
  const drawHistoricalSpiral = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    maxRadius: number,
    history: HistoricalSpiral,
    time: number
  ) => {
    const spiralTightness = 0.02;
    
    history.points.forEach((point, index) => {
      const age = history.points.length - index;
      const opacity = Math.pow(history.decay, age);
      
      if (opacity < 0.01) return;
      
      const processes = Object.keys(PROCESS_CONFIG) as ProcessType[];
      
      ctx.strokeStyle = `rgba(136, 68, 255, ${opacity * 0.3})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      
      processes.forEach((process, pIndex) => {
        const angle = (pIndex * Math.PI * 2) / processes.length - Math.PI / 2 + (age * spiralTightness);
        const radius = (point.metrics[process] || 0) * maxRadius * (1 - age * 0.002);
        
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        if (pIndex === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.closePath();
      ctx.stroke();
    });
  };
  
  const drawLabels = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    maxRadius: number,
    points: RadarPoint[]
  ) => {
    points.forEach((point, index) => {
      const process = Object.keys(PROCESS_CONFIG)[index] as ProcessType;
      const config = PROCESS_CONFIG[process];
      const labelRadius = maxRadius + 30;
      
      const x = centerX + Math.cos(point.angle) * labelRadius;
      const y = centerY + Math.sin(point.angle) * labelRadius;
      
      ctx.fillStyle = config.color;
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Label background
      const labelWidth = ctx.measureText(config.label).width + 20;
      ctx.fillStyle = 'rgba(0, 8, 20, 0.8)';
      ctx.fillRect(x - labelWidth / 2, y - 10, labelWidth, 20);
      
      // Label text
      ctx.fillStyle = config.color;
      ctx.fillText(config.label, x, y);
      
      // Value
      ctx.font = '10px monospace';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.fillText(`${(point.value * 100).toFixed(0)}%`, x, y + 15);
    });
  };
  
  const styles = {
    container: {
      position: 'relative' as const,
      width: '100%',
      maxWidth: '800px',
      margin: '0 auto',
      background: 'radial-gradient(ellipse at center, rgba(0, 20, 40, 0.9) 0%, rgba(0, 8, 20, 0.95) 100%)',
      borderRadius: '20px',
      overflow: 'hidden',
      boxShadow: '0 0 60px rgba(0, 255, 255, 0.1), inset 0 0 120px rgba(0, 0, 0, 0.5)'
    },
    header: {
      padding: '20px',
      background: 'rgba(0, 0, 0, 0.3)',
      borderBottom: '1px solid rgba(0, 255, 255, 0.1)',
      backdropFilter: 'blur(20px)'
    },
    title: {
      margin: 0,
      fontSize: '1.5rem',
      fontWeight: '300',
      color: '#00ffff',
      letterSpacing: '2px',
      textTransform: 'uppercase' as const,
      fontFamily: 'monospace'
    },
    controls: {
      display: 'flex',
      gap: '16px',
      marginTop: '16px',
      flexWrap: 'wrap' as const
    },
    toggle: (active: boolean) => ({
      padding: '8px 16px',
      background: active ? 'rgba(0, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.05)',
      border: `1px solid ${active ? 'rgba(0, 255, 255, 0.5)' : 'rgba(255, 255, 255, 0.1)'}`,
      borderRadius: '20px',
      color: active ? '#00ffff' : '#ffffff',
      fontSize: '0.875rem',
      fontFamily: 'monospace',
      cursor: 'pointer',
      transition: 'all 0.3s ease'
    }),
    canvas: {
      display: 'block',
      width: '100%',
      height: '600px'
    },
    metrics: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
      gap: '12px',
      padding: '20px',
      background: 'rgba(0, 0, 0, 0.3)',
      borderTop: '1px solid rgba(0, 255, 255, 0.1)'
    },
    metric: (color: string, inOptimal: boolean) => ({
      padding: '12px',
      background: 'rgba(255, 255, 255, 0.02)',
      border: `1px solid ${inOptimal ? color : 'rgba(255, 255, 255, 0.1)'}`,
      borderRadius: '8px',
      textAlign: 'center' as const,
      transition: 'all 0.3s ease',
      boxShadow: inOptimal ? `0 0 20px ${color}40` : 'none'
    }),
    metricLabel: {
      fontSize: '0.75rem',
      color: 'rgba(255, 255, 255, 0.6)',
      textTransform: 'uppercase' as const,
      letterSpacing: '0.5px'
    },
    metricValue: (color: string) => ({
      fontSize: '1.25rem',
      fontWeight: 'bold',
      color: color,
      fontFamily: 'monospace',
      textShadow: `0 0 10px ${color}80`
    }),
    processButton: (color: string, selected: boolean) => ({
      padding: '6px 12px',
      background: selected ? `${color}20` : 'transparent',
      border: `1px solid ${selected ? color : 'rgba(255, 255, 255, 0.2)'}`,
      borderRadius: '4px',
      color: selected ? color : '#ffffff',
      fontSize: '0.75rem',
      fontFamily: 'monospace',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    })
  };
  
  const isInOptimalRange = (process: ProcessType, value: number) => {
    const optimal = PROCESS_CONFIG[process].optimal;
    return value >= optimal[0] && value <= optimal[1];
  };
  
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Neural Performance Matrix</h2>
        
        <div style={styles.controls}>
          <button
            style={styles.toggle(showSpiral)}
            onClick={() => setShowSpiral(!showSpiral)}
          >
            Historical Spiral
          </button>
          
          <button
            style={styles.toggle(showOptimalZones)}
            onClick={() => setShowOptimalZones(!showOptimalZones)}
          >
            Optimal Zones
          </button>
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        style={styles.canvas}
      />
      
      <div style={styles.metrics}>
        {(Object.keys(PROCESS_CONFIG) as ProcessType[]).map(process => {
          const config = PROCESS_CONFIG[process];
          const value = metrics[process] || 0;
          const inOptimal = isInOptimalRange(process, value);
          
          return (
            <div key={process} style={styles.metric(config.color, inOptimal)}>
              <div style={styles.metricLabel}>{config.label}</div>
              <div style={styles.metricValue(config.color)}>
                {(value * 100).toFixed(0)}%
              </div>
              <button
                style={styles.processButton(config.color, selectedProcess === process)}
                onClick={() => setSelectedProcess(
                  selectedProcess === process ? null : process
                )}
              >
                {selectedProcess === process ? 'SELECTED' : 'SELECT'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
} 