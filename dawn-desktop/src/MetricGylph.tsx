import React, { useEffect, useRef, useState, memo } from 'react';
import { cairrnCache } from './CairrnDataCache';
import './MetricGlyph.css'; // Assumes you'll create corresponding styles

interface MetricGlyphProps {
  type: 'scup' | 'entropy' | 'mood' | 'heat';
  value: number | string;
  label?: string;
  showTrend?: boolean;
  showSparkline?: boolean;
  showMemoryGhosts?: boolean;
  size?: 'small' | 'medium' | 'large';
  glowIntensity?: number; // 0-1, tied to consciousness state
  pulseRate?: number; // Milliseconds between pulses
}

interface TrendData {
  direction: 'up' | 'down' | 'stable';
  magnitude: number; // 0-1
  velocity: number; // Rate of change
}

interface MemoryGhost {
  value: number | string;
  age: number; // How many ticks ago
  opacity: number;
}

export const MetricGlyph: React.FC<MetricGlyphProps> = memo(({
  type,
  value,
  label,
  showTrend = true,
  showSparkline = false,
  showMemoryGhosts = false,
  size = 'medium',
  glowIntensity = 0.5,
  pulseRate = 2000
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [trend, setTrend] = useState<TrendData>({ direction: 'stable', magnitude: 0, velocity: 0 });
  const [history, setHistory] = useState<(number | string)[]>([]);
  const [ghosts, setGhosts] = useState<MemoryGhost[]>([]);
  const [isHovered, setIsHovered] = useState(false);
  
  // Fetch historical data from Cairrn cache
  useEffect(() => {
    const currentTick = Date.now();
    const historicalStates = cairrnCache.getTemporalSlice(currentTick - 10000, currentTick);
    
    if (historicalStates.length > 0) {
      const values = historicalStates.map(glyph => {
        switch (type) {
          case 'scup': return glyph.state.scup;
          case 'entropy': return glyph.state.entropy;
          case 'mood': return glyph.state.mood;
          case 'heat': return glyph.state.heat;
        }
      });
      
      setHistory(values);
      
      // Calculate trend
      if (values.length >= 2 && typeof value === 'number' && typeof values[values.length - 2] === 'number') {
        const prevValue = values[values.length - 2] as number;
        const currentValue = value as number;
        const delta = currentValue - prevValue;
        const magnitude = Math.abs(delta) / (type === 'scup' || type === 'heat' ? 100 : 1);
        
        setTrend({
          direction: delta > 0.01 ? 'up' : delta < -0.01 ? 'down' : 'stable',
          magnitude: Math.min(magnitude, 1),
          velocity: delta / (pulseRate / 1000)
        });
      }
      
      // Extract memory ghosts
      if (showMemoryGhosts && values.length > 3) {
        const recentGhosts = values.slice(-5, -1).map((val, idx) => ({
          value: val,
          age: values.length - idx - 1,
          opacity: 1 - (idx / 5)
        }));
        setGhosts(recentGhosts);
      }
    }
  }, [value, type, showMemoryGhosts, pulseRate]);
  
  // Render sparkline
  useEffect(() => {
    if (!showSparkline || !canvasRef.current || history.length < 2) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Filter numeric values for sparkline
    const numericHistory = history.filter(v => typeof v === 'number') as number[];
    if (numericHistory.length < 2) return;
    
    // Calculate bounds
    const min = Math.min(...numericHistory);
    const max = Math.max(...numericHistory);
    const range = max - min || 1;
    
    // Draw sparkline
    ctx.strokeStyle = `rgba(0, 255, 255, ${0.3 + glowIntensity * 0.7})`;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    
    numericHistory.forEach((val, idx) => {
      const x = (idx / (numericHistory.length - 1)) * canvas.width;
      const y = canvas.height - ((val - min) / range) * canvas.height;
      
      if (idx === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    ctx.stroke();
    
    // Add glow effect
    ctx.shadowBlur = 10 * glowIntensity;
    ctx.shadowColor = 'rgba(0, 255, 255, 0.8)';
    ctx.stroke();
    
  }, [history, showSparkline, glowIntensity]);
  
  // Format display value
  const formatValue = (val: number | string): string => {
    if (typeof val === 'string') return val;
    
    switch (type) {
      case 'scup':
      case 'heat':
        return `${Math.round(val)}%`;
      case 'entropy':
        return val.toFixed(2);
      default:
        return String(val);
    }
  };
  
  // Get icon based on type
  const getIcon = () => {
    switch (type) {
      case 'scup': return '🧠';
      case 'entropy': return '🌀';
      case 'mood': return '🎭';
      case 'heat': return '🔥';
    }
  };
  
  // Size configurations
  const sizeConfig = {
    small: { width: 80, height: 60, fontSize: '0.9rem' },
    medium: { width: 120, height: 80, fontSize: '1.1rem' },
    large: { width: 160, height: 100, fontSize: '1.3rem' }
  };
  
  const config = sizeConfig[size];
  
  return (
    <div 
      className={`metric-glyph metric-glyph--${size} metric-glyph--${type}`}
      style={{
        '--glow-intensity': glowIntensity,
        '--pulse-rate': `${pulseRate}ms`,
        width: config.width,
        minHeight: config.height
      } as React.CSSProperties}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Background glass effect */}
      <div className="metric-glyph__glass" />
      
      {/* Memory ghosts */}
      {showMemoryGhosts && ghosts.map((ghost, idx) => (
        <div 
          key={idx}
          className="metric-glyph__ghost"
          style={{
            opacity: ghost.opacity * 0.3,
            transform: `translateY(-${ghost.age * 5}px)`
          }}
        >
          {formatValue(ghost.value)}
        </div>
      ))}
      
      {/* Main content */}
      <div className="metric-glyph__content">
        <div className="metric-glyph__header">
          <span className="metric-glyph__icon">{getIcon()}</span>
          {label && <span className="metric-glyph__label">{label}</span>}
          {showTrend && trend.direction !== 'stable' && (
            <span className={`metric-glyph__trend metric-glyph__trend--${trend.direction}`}>
              {trend.direction === 'up' ? '↑' : '↓'}
              <span className="metric-glyph__trend-magnitude">
                {Math.round(trend.magnitude * 100)}%
              </span>
            </span>
          )}
        </div>
        
        <div className="metric-glyph__value" style={{ fontSize: config.fontSize }}>
          {formatValue(value)}
        </div>
        
        {/* Sparkline canvas */}
        {showSparkline && (
          <canvas 
            ref={canvasRef}
            className="metric-glyph__sparkline"
            width={config.width - 20}
            height={20}
          />
        )}
        
        {/* Hover details */}
        {isHovered && history.length > 0 && (
          <div className="metric-glyph__tooltip">
            <div className="metric-glyph__tooltip-content">
              <div>Avg: {formatValue(
                typeof value === 'number' 
                  ? history.filter(v => typeof v === 'number').reduce((a, b) => (a as number) + (b as number), 0) as number / history.filter(v => typeof v === 'number').length
                  : value
              )}</div>
              <div>Samples: {history.length}</div>
              {trend.velocity !== 0 && (
                <div>Velocity: {trend.velocity.toFixed(2)}/s</div>
              )}
            </div>
          </div>
        )}
      </div>
      
      {/* Pulse animation overlay */}
      <div className="metric-glyph__pulse" />
      
      {/* Edge glow based on value */}
      <div 
        className="metric-glyph__edge-glow"
        style={{
          opacity: glowIntensity,
          animationDuration: `${pulseRate}ms`
        }}
      />
    </div>
  );
});

MetricGlyph.displayName = 'MetricGlyph';

// Compound component for grouped metrics
export const MetricGlyphGroup: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="metric-glyph-group">
      {children}
    </div>
  );
};

// Hook for using cached metric data
export const useCachedMetric = (type: MetricGlyphProps['type']) => {
  const [cachedValue, setCachedValue] = useState<number | string | null>(null);
  const [pattern, setPattern] = useState<string | null>(null);
  
  useEffect(() => {
    // Get latest cached value
    const patterns = {
      scup: 'high-consciousness',
      entropy: 'chaotic',
      mood: 'mood:curious',
      heat: 'overheated'
    };
    
    const glyphs = cairrnCache.getByPattern(patterns[type]);
    if (glyphs.length > 0) {
      const latest = glyphs[glyphs.length - 1];
      setCachedValue(latest.state[type]);
      setPattern(latest.patterns[0]);
    }
  }, [type]);
  
  return { cachedValue, pattern };
};