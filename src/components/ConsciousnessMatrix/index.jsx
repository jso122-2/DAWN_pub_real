import React, { useEffect, useRef, useState } from 'react';
import './index.css';

const ConsciousnessMatrix = () => {
  const canvasRef = useRef(null);
  const trendCanvasRef = useRef(null);
  const animationRef = useRef();
  const [isCanvasReady, setIsCanvasReady] = useState(false);
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [showTrends, setShowTrends] = useState(true);
  const [tickData, setTickData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  
  // WebSocket Connection
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001');
    
    ws.onopen = () => {
      console.log('Connected to DAWN WebSocket');
      setIsConnected(true);
    };
    
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        let data = null;
        
        if (message.type === 'tick' && message.data) {
          data = {
            scup: message.data.scup || 0.5,
            entropy: message.data.entropy || 0.5,
            heat: message.data.heat || message.data.systemLoad || 0.5,
            mood: message.data.mood || 'analytical',
            timestamp: Date.now()
          };
        }
        
        if (data) {
          setTickData(data);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };
    
    return () => {
      ws.close();
    };
  }, []);
  
  // Initialize canvas
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsCanvasReady(true);
    }, 500);
    
    return () => clearTimeout(timer);
  }, []);
  
  // Track metrics history
  useEffect(() => {
    if (tickData) {
      const timestamp = Date.now();
      const newMetric = {
        timestamp,
        scup: tickData.scup > 1 ? tickData.scup / 100 : tickData.scup,
        entropy: tickData.entropy,
        heat: tickData.heat,
        mood: tickData.mood,
        pressure: Math.min(1, tickData.entropy * tickData.heat * 1.2),
        coherence: Math.max(0, 1 - tickData.entropy * 0.8),
        temperature: tickData.heat * 0.8 + tickData.entropy * 0.2,
        neuralActivity: Math.sin(timestamp * 0.001) * 0.2 + tickData.scup * 0.8,
        resonance: Math.cos(timestamp * 0.002) * 0.15 + 0.65,
        stability: Math.max(0, 0.9 - Math.abs(tickData.entropy - 0.5) * 1.6)
      };
      
      setMetricsHistory(prev => {
        const updated = [...prev, newMetric];
        return updated.slice(-100);
      });
    }
  }, [tickData]);
  
  // Canvas animation
  useEffect(() => {
    if (!canvasRef.current || !isCanvasReady) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    
    let particles = [];
    
    // Initialize particles
    for (let i = 0; i < 50; i++) {
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
    
    const animate = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      const scup = tickData?.scup || 0.5;
      const entropy = tickData?.entropy || 0.5;
      const heat = tickData?.heat || 0.5;
      const mood = tickData?.mood || 'analytical';
      
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
      
      // Central orb
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const radius = 80 + (scup * 50);
      
      const glowRadius = radius + Math.sin(Date.now() * 0.001) * 20 * scup;
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, glowRadius);
      gradient.addColorStop(0, colors.primary);
      gradient.addColorStop(0.5, `${colors.secondary}88`);
      gradient.addColorStop(1, 'transparent');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, glowRadius, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.fillStyle = colors.primary;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius * 0.3, 0, Math.PI * 2);
      ctx.fill();
      
      // Update particles
      particles.forEach(particle => {
        particle.x += particle.vx * (1 + entropy);
        particle.y += particle.vy * (1 + entropy);
        
        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
        
        const dx = centerX - particle.x;
        const dy = centerY - particle.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist > radius) {
          particle.vx += (dx / dist) * scup * 0.1;
          particle.vy += (dy / dist) * scup * 0.1;
        }
        
        particle.pulsePhase += 0.05 * (1 + heat);
        const pulseSize = Math.sin(particle.pulsePhase) * 0.5 + 1;
        
        ctx.fillStyle = particle.active ? colors.primary : `${colors.primary}66`;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius * pulseSize, 0, Math.PI * 2);
        ctx.fill();
      });
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isCanvasReady, tickData]);
  
  // Trend lines
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
      ctx.beginPath();
      
      const yOffset = offset * 5;
      
      data.forEach((value, index) => {
        const x = (index / (data.length - 1)) * canvas.width;
        const y = canvas.height - (value * (canvas.height - yOffset - 10)) - yOffset - 5;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.stroke();
    };
    
    if (metricsHistory.length > 0) {
      const scupData = metricsHistory.map(m => m.scup);
      const entropyData = metricsHistory.map(m => m.entropy);
      const heatData = metricsHistory.map(m => m.heat);
      const pressureData = metricsHistory.map(m => m.pressure);
      const coherenceData = metricsHistory.map(m => m.coherence);
      const temperatureData = metricsHistory.map(m => m.temperature);
      const neuralData = metricsHistory.map(m => m.neuralActivity);
      const resonanceData = metricsHistory.map(m => m.resonance);
      const stabilityData = metricsHistory.map(m => m.stability);
      
      drawTrendLine(scupData, '#00ff88', 0);
      drawTrendLine(entropyData, '#ff6b6b', 1);
      drawTrendLine(heatData, '#ffa500', 2);
      drawTrendLine(pressureData, '#ff1493', 3);
      drawTrendLine(coherenceData, '#00bfff', 4);
      drawTrendLine(temperatureData, '#ffff00', 5);
      drawTrendLine(neuralData, '#9370db', 6);
      drawTrendLine(resonanceData, '#00ffff', 7);
      drawTrendLine(stabilityData, '#32cd32', 8);
    }
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
            <button className="control-btn" onClick={() => setMetricsHistory([])}>Clear History</button>
          </div>
        </div>
        
        <div className="metrics-sidebar">
          <div className="metric-card">
            <h3>SCUP</h3>
            <div className="metric-value">{((tickData?.scup || 0.5) * 100).toFixed(1)}%</div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.scup > metricsHistory[metricsHistory.length - 6]?.scup ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.scup < metricsHistory[metricsHistory.length - 6]?.scup ? '↘' : '→'
              )}
            </div>
          </div>
          
          <div className="metric-card">
            <h3>Entropy</h3>
            <div className="metric-value">{(tickData?.entropy || 0.5).toFixed(3)}</div>
            <div className="metric-trend">
              {metricsHistory.length > 5 && (
                metricsHistory[metricsHistory.length - 1]?.entropy > metricsHistory[metricsHistory.length - 6]?.entropy ? '↗' : 
                metricsHistory[metricsHistory.length - 1]?.entropy < metricsHistory[metricsHistory.length - 6]?.entropy ? '↘' : '→'
              )}
            </div>
          </div>

          <div className="metric-card">
            <h3>Heat</h3>
            <div className="metric-value">{(tickData?.heat || 0.5).toFixed(3)}</div>
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