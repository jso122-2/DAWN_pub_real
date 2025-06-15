import React, { useEffect, useRef, useState, useCallback } from 'react';

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

// Clean, minimal configuration
const METRICS_CONFIG = {
  scup: { label: 'SCUP', color: '#00ff88' },
  entropy: { label: 'Entropy', color: '#ff6b6b' },
  coherence: { label: 'Coherence', color: '#4dabf7' },
  heat: { label: 'Heat', color: '#ffd43b' },
  drift: { label: 'Drift', color: '#c084fc' },
  resonance: { label: 'Resonance', color: '#66d9ef' }
};

const NeuralPage: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  
  const [visualizationType, setVisualizationType] = useState<VisualizationType>('network');
  const [metrics, setMetrics] = useState<ProcessMetrics>({
    scup: 0.65,
    entropy: 0.18,
    coherence: 0.73,
    heat: 0.45,
    drift: 0.28,
    resonance: 0.62
  });
  
  // Smooth metric updates (less noisy)
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => {
        const newMetrics = { ...prev };
        
        // Very subtle changes for smooth visualization
        Object.keys(newMetrics).forEach(key => {
          const k = key as keyof ProcessMetrics;
          const delta = (Math.random() - 0.5) * 0.01; // Much smaller changes
          newMetrics[k] = Math.max(0, Math.min(1, prev[k] + delta));
        });
        
        return newMetrics;
      });
    }, 1000); // Slower updates
    
    return () => clearInterval(interval);
  }, []);
  
  // Simple network visualization
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
    
    // Draw connections (very subtle)
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
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
    
    // Draw center connection
    nodes.forEach(node => {
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(node.x, node.y);
      ctx.stroke();
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
      
      // Border
      ctx.strokeStyle = config.color;
      ctx.lineWidth = 2;
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
    
    // Draw center node
    ctx.fillStyle = '#00ff88';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fill();
  }, [metrics]);
  
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
  }, [metrics]);
  
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
      gap: '10px'
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
    })
  };
  
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Neural Network</h1>
        <p style={styles.subtitle}>Real-time neural activity visualization</p>
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
          </div>
        ))}
      </div>
    </div>
  );
};

export default NeuralPage; 