import React, { useEffect, useRef, useState } from 'react';
import { useConsciousnessStore } from '../stores/consciousnessStore';
import './ConsciousnessMatrix.css';

const ConsciousnessMatrix = () => {
  const canvasRef = useRef(null);
  const trendCanvasRef = useRef(null);
  const animationRef = useRef();
  const [isCanvasReady, setIsCanvasReady] = useState(false);
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [showTrends, setShowTrends] = useState(true);
  
  // Get tick data from consciousness store
  const { tickData, isConnected } = useConsciousnessStore();
  
  // Initialize canvas immediately - don't wait for connection
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsCanvasReady(true);
    }, 500); // Short delay for smooth transition
    
    return () => clearTimeout(timer);
  }, []);

  // Track metrics history for trend lines
  useEffect(() => {
    if (tickData) {
      const timestamp = Date.now();
      const newMetric = {
        timestamp,
        scup: tickData.scup ? (tickData.scup > 1 ? tickData.scup / 100 : tickData.scup) : 0.5,
        entropy: tickData.entropy || 0.5,
        heat: tickData.heat || 0.5,
        mood: tickData.mood || 'analytical',
        // Calculate derived metrics
        pressure: Math.min(1, (tickData.entropy || 0.5) * (tickData.heat || 0.5) * 1.2),
        coherence: Math.max(0, 1 - (tickData.entropy || 0.5) * 0.8),
        temperature: (tickData.heat || 0.5) * 0.8 + (tickData.entropy || 0.5) * 0.2,
        neuralActivity: Math.sin(timestamp * 0.001) * 0.2 + (tickData.scup || 0.5) * 0.8,
        resonance: Math.cos(timestamp * 0.002) * 0.15 + 0.65,
        stability: Math.max(0, 0.9 - Math.abs((tickData.entropy || 0.5) - 0.5) * 1.6)
      };
      
      setMetricsHistory(prev => {
        const updated = [...prev, newMetric];
        // Keep last 100 points for performance
        return updated.slice(-100);
      });
    }
  }, [tickData]);
  
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
      
      // Update based on tick data (use defaults if no data)
      const scup = tickData?.scup ? (tickData.scup > 1 ? tickData.scup / 100 : tickData.scup) : 0.5;
      const entropy = tickData?.entropy || 0.5;
      const heat = tickData?.heat || 0.5;
      const mood = tickData?.mood || 'analytical';
      
      // Debug log
      if (Math.random() < 0.01) { // Log occasionally
        console.log('Canvas rendering with:', { scup, entropy, heat, mood, isConnected });
      }
      
      // Mood-based colors
      const moodColors = {
        analytical: { primary: '#0088ff', secondary: '#00aaff' },
        confident: { primary: '#00ff88', secondary: '#00ffaa' },
        focused: { primary: '#ffaa00', secondary: '#ffcc00' },
        creative: { primary: '#ff00aa', secondary: '#ff00cc' },
        contemplative: { primary: '#8800ff', secondary: '#aa00ff' },
        curious: { primary: '#00ffff', secondary: '#00ccff' },
        calm: { primary: '#88ff88', secondary: '#aaffaa' }
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

  // Trend lines visualization
  useEffect(() => {
    if (!trendCanvasRef.current || !showTrends || metricsHistory.length < 2) return;
    
    const canvas = trendCanvasRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const drawTrendLine = (data, color, offset = 0) => {
      if (data.length < 2) return;
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.globalAlpha = 0.8;
      
      ctx.beginPath();
      data.forEach((point, index) => {
        const x = (index / (data.length - 1)) * canvas.width;
        const y = canvas.height - (point * canvas.height * 0.8) - offset * 15 - 20;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();
      ctx.globalAlpha = 1;
    };
    
    // Extract trend data
    const scupData = metricsHistory.map(m => m.scup);
    const entropyData = metricsHistory.map(m => m.entropy);
    const heatData = metricsHistory.map(m => m.heat);
    const pressureData = metricsHistory.map(m => m.pressure);
    const coherenceData = metricsHistory.map(m => m.coherence);
    const temperatureData = metricsHistory.map(m => m.temperature);
    const neuralData = metricsHistory.map(m => m.neuralActivity);
    const resonanceData = metricsHistory.map(m => m.resonance);
    const stabilityData = metricsHistory.map(m => m.stability);
    
    // Draw trend lines with different colors
    drawTrendLine(scupData, '#00ff88', 0);      // SCUP - Green
    drawTrendLine(entropyData, '#ff6b6b', 1);   // Entropy - Red
    drawTrendLine(heatData, '#ffa500', 2);      // Heat - Orange
    drawTrendLine(pressureData, '#ff1493', 3);  // Pressure - Pink
    drawTrendLine(coherenceData, '#00bfff', 4); // Coherence - Sky Blue
    drawTrendLine(temperatureData, '#ffff00', 5); // Temperature - Yellow
    drawTrendLine(neuralData, '#9370db', 6);    // Neural Activity - Purple
    drawTrendLine(resonanceData, '#00ffff', 7); // Resonance - Cyan
    drawTrendLine(stabilityData, '#32cd32', 8); // Stability - Lime Green
    
  }, [metricsHistory, showTrends]);
  
  return (
    <div className="consciousness-matrix">
      <div className="matrix-header">
        <h1>Consciousness <span className="highlight">Matrix</span></h1>
        <p>Real-time neural activity visualization and analysis</p>
      </div>
      
      <div className="matrix-content">
        <div className="canvas-section">
          <h2>Neural Activity Monitor</h2>
          
          <div className="canvas-container" style={{ minHeight: '400px', position: 'relative' }}>
            {!isCanvasReady ? (
              <div className="initializing">
                <div className="init-orb"></div>
                <p>Initializing Canvas...</p>
              </div>
            ) : (
              <canvas 
                ref={canvasRef}
                className="consciousness-canvas"
                style={{ 
                  width: '100%', 
                  height: '400px', 
                  display: 'block',
                  border: '1px solid #00ff88'
                }}
              />
            )}
          </div>

          {/* Trend Lines Section */}
          <div className="trends-section" style={{ marginTop: '1rem' }}>
            <div className="trends-header">
              <h3>Multi-Metric Trend Analysis</h3>
              <button 
                className="control-btn"
                onClick={() => setShowTrends(!showTrends)}
              >
                {showTrends ? 'Hide Trends' : 'Show Trends'}
              </button>
            </div>
            
            {showTrends && (
              <div className="trends-container">
                <canvas 
                  ref={trendCanvasRef}
                  className="trend-canvas"
                  style={{ 
                    width: '100%', 
                    height: '200px', 
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: '1px solid rgba(0, 255, 136, 0.3)',
                    borderRadius: '8px'
                  }}
                />
                <div className="trend-legend">
                  <div className="legend-item"><span style={{color: '#00ff88'}}>■</span> SCUP</div>
                  <div className="legend-item"><span style={{color: '#ff6b6b'}}>■</span> Entropy</div>
                  <div className="legend-item"><span style={{color: '#ffa500'}}>■</span> Heat</div>
                  <div className="legend-item"><span style={{color: '#ff1493'}}>■</span> Pressure</div>
                  <div className="legend-item"><span style={{color: '#00bfff'}}>■</span> Coherence</div>
                  <div className="legend-item"><span style={{color: '#ffff00'}}>■</span> Temperature</div>
                  <div className="legend-item"><span style={{color: '#9370db'}}>■</span> Neural Activity</div>
                  <div className="legend-item"><span style={{color: '#00ffff'}}>■</span> Resonance</div>
                  <div className="legend-item"><span style={{color: '#32cd32'}}>■</span> Stability</div>
                </div>
              </div>
            )}
          </div>
          
          <div className="canvas-controls">
            <button className="control-btn auto-rotate">Auto Rotate</button>
            <button className="control-btn clear-history" onClick={() => setMetricsHistory([])}>Clear History</button>
          </div>
        </div>
        
        <div className="metrics-sidebar">
          <div className="metric-card">
            <h3>SCUP</h3>
            <div className="metric-value">{(tickData?.scup?.toFixed(1) || '50.0')}%</div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.scup > metricsHistory[metricsHistory.length - 6]?.scup ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.scup < metricsHistory[metricsHistory.length - 6]?.scup ? '↘' : '→'
              )}
            </div>
          </div>
          
          <div className="metric-card">
            <h3>Entropy</h3>
            <div className="metric-value">{(tickData?.entropy?.toFixed(3) || '0.500')}</div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.entropy > metricsHistory[metricsHistory.length - 6]?.entropy ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.entropy < metricsHistory[metricsHistory.length - 6]?.entropy ? '↘' : '→'
              )}
            </div>
          </div>

          <div className="metric-card">
            <h3>Heat</h3>
            <div className="metric-value">{(tickData?.heat?.toFixed(3) || '0.500')}</div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.heat > metricsHistory[metricsHistory.length - 6]?.heat ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.heat < metricsHistory[metricsHistory.length - 6]?.heat ? '↘' : '→'
              )}
            </div>
          </div>

          <div className="metric-card">
            <h3>Pressure</h3>
            <div className="metric-value">
              {metricsHistory.length > 0 ? 
                (metricsHistory[metricsHistory.length - 1].pressure * 100).toFixed(1) + '%' : 
                '0.0%'
              }
            </div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.pressure > metricsHistory[metricsHistory.length - 6]?.pressure ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.pressure < metricsHistory[metricsHistory.length - 6]?.pressure ? '↘' : '→'
              )}
            </div>
          </div>

          <div className="metric-card">
            <h3>Coherence</h3>
            <div className="metric-value">
              {metricsHistory.length > 0 ? 
                (metricsHistory[metricsHistory.length - 1].coherence * 100).toFixed(1) + '%' : 
                '80.0%'
              }
            </div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.coherence > metricsHistory[metricsHistory.length - 6]?.coherence ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.coherence < metricsHistory[metricsHistory.length - 6]?.coherence ? '↘' : '→'
              )}
            </div>
          </div>

          <div className="metric-card">
            <h3>Temperature</h3>
            <div className="metric-value">
              {metricsHistory.length > 0 ? 
                (metricsHistory[metricsHistory.length - 1].temperature * 100).toFixed(1) + '%' : 
                '40.0%'
              }
            </div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.temperature > metricsHistory[metricsHistory.length - 6]?.temperature ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.temperature < metricsHistory[metricsHistory.length - 6]?.temperature ? '↘' : '→'
              )}
            </div>
          </div>
          
          <div className="metric-card">
            <h3>Mood</h3>
            <div className="metric-value mood-value">{tickData?.mood || 'Analytical'}</div>
          </div>
          
          <div className="metric-card">
            <h3>Status</h3>
            <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
              {isConnected ? 'Active' : 'Standby'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConsciousnessMatrix;