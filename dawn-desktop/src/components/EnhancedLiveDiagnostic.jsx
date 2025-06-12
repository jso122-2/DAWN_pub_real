import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import eventBus, { emitPrediction } from './eventBus';

const EnhancedLiveDiagnostic = ({ scupData, entropyData, heatData, updateInterval = 1000, onPatternDetected, onAnomalyDetected }) => {
  const spectrogramCanvasRef = useRef(null);
  const waterfallCanvasRef = useRef(null);
  const correlationCanvasRef = useRef(null);
  const animationRef = useRef(null);
  const bufferCanvasRef = useRef(null);
  
  const [activeView, setActiveView] = useState('spectrogram');
  const [patterns, setPatterns] = useState({
    detected: [],
    anomalies: []
  });
  const [fps, setFps] = useState(0);
  
  // Data fallback
  const scup = scupData && scupData.length ? scupData : new Array(64).fill(0);
  const entropy = entropyData && entropyData.length ? entropyData : new Array(64).fill(0);
  const heat = heatData && heatData.length ? heatData : new Array(64).fill(0);
  
  // Track last data for change detection
  const lastDataRef = useRef({
    scup: [],
    entropy: [],
    heat: [],
    view: activeView
  });
  
  // FPS calculation
  const frameTimesRef = useRef([]);
  
  // Canvas buffer setup
  useEffect(() => {
    if (!bufferCanvasRef.current) {
      bufferCanvasRef.current = document.createElement('canvas');
      bufferCanvasRef.current.width = 800;
      bufferCanvasRef.current.height = 300;
    }
  }, []);
  
  // Redraw logic using requestAnimationFrame
  useEffect(() => {
    let running = true;
    let lastRedraw = 0;
    
    function arraysEqual(a, b) {
      if (a.length !== b.length) return false;
      for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
      return true;
    }
    
    const draw = () => {
      // Only redraw if data or view changed
      const last = lastDataRef.current;
      const needsRedraw =
        !arraysEqual(scup, last.scup) ||
        !arraysEqual(entropy, last.entropy) ||
        !arraysEqual(heat, last.heat) ||
        activeView !== last.view;
      
      if (needsRedraw) {
        // Update last data
        lastDataRef.current = {
          scup: [...scup],
          entropy: [...entropy],
          heat: [...heat],
          view: activeView
        };
        
        // Draw to buffer
        const buffer = bufferCanvasRef.current;
        const ctx = buffer.getContext('2d');
        if (activeView === 'spectrogram') {
          drawSpectrogram(ctx, buffer.width, buffer.height);
        } else if (activeView === 'waterfall') {
          drawWaterfall(ctx, buffer.width, buffer.height);
        } else if (activeView === 'correlation') {
          drawCorrelation(ctx, buffer.width, buffer.height);
        }
        
        // Swap buffer to visible canvas
        let targetCanvas = null;
        if (activeView === 'spectrogram') targetCanvas = spectrogramCanvasRef.current;
        if (activeView === 'waterfall') targetCanvas = waterfallCanvasRef.current;
        if (activeView === 'correlation') targetCanvas = correlationCanvasRef.current;
        if (targetCanvas) {
          const tctx = targetCanvas.getContext('2d');
          tctx.clearRect(0, 0, targetCanvas.width, targetCanvas.height);
          tctx.drawImage(buffer, 0, 0);
        }
      }
      
      // FPS calculation
      const now = performance.now();
      frameTimesRef.current.push(now);
      // Only keep last 1s of frames
      while (frameTimesRef.current.length > 0 && frameTimesRef.current[0] < now - 1000) {
        frameTimesRef.current.shift();
      }
      setFps(frameTimesRef.current.length);
      
      if (running) {
        animationRef.current = requestAnimationFrame(draw);
      }
    };
    animationRef.current = requestAnimationFrame(draw);
    return () => {
      running = false;
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [scup, entropy, heat, activeView]);
  
  // Pattern detection
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate pattern detection
      if (Math.random() > 0.8) {
        const pattern = {
          type: ['Alpha Spike', 'Beta Surge', 'Gamma Burst'][Math.floor(Math.random() * 3)],
          timestamp: new Date().toLocaleTimeString(),
          confidence: (Math.random() * 40 + 60).toFixed(1)
        };
        setPatterns(prev => ({
          detected: [...prev.detected.slice(-5), pattern],
          anomalies: prev.anomalies
        }));
        if (onPatternDetected) onPatternDetected(pattern);
        // Emit to event bus
        eventBus.dispatchEvent(new CustomEvent('pattern-detected', { detail: pattern }));
      }
      // Simulate anomaly detection
      if (Math.random() > 0.95) {
        const anomaly = {
          type: 'Phase Desync',
          severity: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
          timestamp: new Date().toLocaleTimeString()
        };
        setPatterns(prev => ({
          detected: prev.detected,
          anomalies: [...prev.anomalies.slice(-3), anomaly]
        }));
        if (onAnomalyDetected) onAnomalyDetected(anomaly);
        // Emit to event bus
        eventBus.dispatchEvent(new CustomEvent('anomaly-detected', { detail: anomaly }));
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [onPatternDetected, onAnomalyDetected]);
  
  // Predictive analysis based on historical patterns/anomalies
  useEffect(() => {
    const predictionInterval = setInterval(() => {
      if (patterns.detected.length > 3) {
        const last = patterns.detected.slice(-3);
        const confidences = last.map(p => parseFloat(p.confidence));
        const avgConfidence = confidences.reduce((a, b) => a + b, 0) / confidences.length;
        if (avgConfidence > 80) {
          emitPrediction({
            message: `Pattern activity likely to spike (avg confidence ${avgConfidence.toFixed(1)}%) in next 30s`,
            probability: avgConfidence,
            severity: avgConfidence > 90 ? 'high' : 'medium',
            type: 'pattern'
          });
        }
      }
      if (patterns.anomalies.length > 2) {
        emitPrediction({
          message: `Increased risk of phase desync anomaly in next 45s`,
          probability: 75,
          severity: 'medium',
          type: 'anomaly'
        });
      }
    }, 10000);
    return () => clearInterval(predictionInterval);
  }, [patterns]);
  
  // Draw spectrogram
  const drawSpectrogram = (ctx, width, height) => {
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);
    
    const streams = ['scup', 'entropy', 'heat'];
    const colors = ['#ec4899', '#3b82f6', '#f59e0b'];
    const sectionHeight = height / 3;
    
    streams.forEach((stream, idx) => {
      const yOffset = idx * sectionHeight;
      const data = [scup, entropy, heat][idx];
      
      // Draw frequency bars
      const barWidth = width / data.length;
      
      data.forEach((value, i) => {
        const barHeight = value * (sectionHeight - 20);
        const x = i * barWidth;
        const y = yOffset + sectionHeight - barHeight - 10;
        
        // Gradient fill
        const gradient = ctx.createLinearGradient(x, y + barHeight, x, y);
        gradient.addColorStop(0, `${colors[idx]}33`);
        gradient.addColorStop(1, colors[idx]);
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth - 1, barHeight);
      });
      
      // Label
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.fillText(stream.toUpperCase(), 10, yOffset + 20);
      
      // Frequency scale
      ctx.fillStyle = '#6b7280';
      ctx.font = '10px monospace';
      ctx.fillText('0Hz', 5, yOffset + sectionHeight - 5);
      ctx.fillText('50Hz', width - 30, yOffset + sectionHeight - 5);
    });
    
    // Draw grid
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 10; i++) {
      const x = (width / 10) * i;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
  };
  
  // Draw waterfall display
  const drawWaterfall = (ctx, width, height) => {
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);
    
    // Create time-based waterfall effect
    const timeSlices = 50;
    const sliceHeight = height / timeSlices;
    
    for (let t = 0; t < timeSlices; t++) {
      const y = t * sliceHeight;
      const intensity = Math.sin(t * 0.1) * 0.5 + 0.5;
      
      // Draw frequency spectrum for this time slice
      for (let f = 0; f < 64; f++) {
        const x = (f / 64) * width;
        const value = Math.sin(f * 0.3 + t * 0.1) * intensity;
        const color = `hsl(${200 + value * 60}, 70%, ${30 + value * 40}%)`;
        
        ctx.fillStyle = color;
        ctx.fillRect(x, y, width / 64, sliceHeight);
      }
    }
    
    // Overlay grid
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 0.5;
    
    // Time markers
    for (let i = 0; i <= 5; i++) {
      const y = (height / 5) * i;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
      
      ctx.fillStyle = '#6b7280';
      ctx.font = '10px monospace';
      ctx.fillText(`-${i}s`, 5, y + 12);
    }
  };
  
  // Draw phase correlation
  const drawCorrelation = (ctx, width, height) => {
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);
    
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;
    
    // Draw correlation circles
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    
    for (let r = radius; r > 0; r -= radius / 4) {
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.stroke();
    }
    
    // Draw axes
    ctx.beginPath();
    ctx.moveTo(centerX - radius - 20, centerY);
    ctx.lineTo(centerX + radius + 20, centerY);
    ctx.moveTo(centerX, centerY - radius - 20);
    ctx.lineTo(centerX, centerY + radius + 20);
    ctx.stroke();
    
    // Plot correlation points
    const pairs = [
      { a: 'scup', b: 'entropy', color: '#ec4899' },
      { a: 'entropy', b: 'heat', color: '#3b82f6' },
      { a: 'heat', b: 'scup', color: '#f59e0b' }
    ];
    
    pairs.forEach((pair, idx) => {
      const dataA = pair.a === 'scup' ? scup : pair.a === 'entropy' ? entropy : heat;
      const dataB = pair.b === 'scup' ? scup : pair.b === 'entropy' ? entropy : heat;
      
      // Calculate phase from data (simple sum-based approach)
      const phaseA = dataA.reduce((sum, val, i) => sum + val * i, 0) / dataA.length;
      const phaseB = dataB.reduce((sum, val, i) => sum + val * i, 0) / dataB.length;
      const correlation = Math.cos(phaseA - phaseB);
      
      const x = centerX + correlation * radius * 0.8;
      const y = centerY + Math.sin(phaseA - phaseB) * radius * 0.8;
      
      // Draw point
      ctx.fillStyle = pair.color;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw trail
      ctx.strokeStyle = `${pair.color}66`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
      
      // Label
      ctx.fillStyle = '#ffffff';
      ctx.font = '10px monospace';
      ctx.fillText(`${pair.a}-${pair.b}`, x + 10, y - 5);
    });
    
    // Correlation strength indicator
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 14px monospace';
    ctx.textAlign = 'center';
    ctx.fillText('Phase Correlation', centerX, 30);
  };
  
  return (
    <div className="glass border-0 shadow-glow-sm rounded-lg p-6 relative hover:shadow-glow-md transition-all duration-300">
      {/* FPS Counter */}
      <div className="absolute top-2 right-4 text-xs text-cyan-300 bg-gray-800/80 px-2 py-1 rounded shadow">
        FPS: {fps}
      </div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></span>
          Enhanced Live Diagnostic
        </h3>
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveView('spectrogram')}
            className={`px-3 py-1 rounded text-sm ${
              activeView === 'spectrogram' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            Spectrogram
          </button>
          <button
            onClick={() => setActiveView('waterfall')}
            className={`px-3 py-1 rounded text-sm ${
              activeView === 'waterfall' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            Waterfall
          </button>
          <button
            onClick={() => setActiveView('correlation')}
            className={`px-3 py-1 rounded text-sm ${
              activeView === 'correlation' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            Correlation
          </button>
        </div>
      </div>
      
      <div className="relative">
        <canvas 
          ref={spectrogramCanvasRef}
          width={800} 
          height={300}
          className={`w-full rounded bg-gray-950 ${activeView !== 'spectrogram' ? 'hidden' : ''}`}
        />
        <canvas 
          ref={waterfallCanvasRef}
          width={800} 
          height={300}
          className={`w-full rounded bg-gray-950 ${activeView !== 'waterfall' ? 'hidden' : ''}`}
        />
        <canvas 
          ref={correlationCanvasRef}
          width={800} 
          height={300}
          className={`w-full rounded bg-gray-950 ${activeView !== 'correlation' ? 'hidden' : ''}`}
        />
      </div>
      
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="glass-dark animate-breathe rounded p-3 hover:shadow-glow-md transition-all duration-300">
          <h4 className="text-sm font-bold text-white mb-2">Pattern Detection</h4>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {patterns.detected.length === 0 ? (
              <p className="text-xs text-gray-500">Monitoring...</p>
            ) : (
              patterns.detected.map((pattern, idx) => (
                <div key={idx} className="text-xs">
                  <span className="text-green-400">{pattern.type}</span>
                  <span className="text-gray-500 ml-2">{pattern.confidence}%</span>
                  <span className="text-gray-600 float-right">{pattern.timestamp}</span>
                </div>
              ))
            )}
          </div>
        </div>
        
        <div className="glass-dark animate-breathe rounded p-3 hover:shadow-glow-md transition-all duration-300">
          <h4 className="text-sm font-bold text-white mb-2">Anomaly Detection</h4>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {patterns.anomalies.length === 0 ? (
              <p className="text-xs text-gray-500">No anomalies detected</p>
            ) : (
              patterns.anomalies.map((anomaly, idx) => (
                <div key={idx} className="text-xs">
                  <span className={`${
                    anomaly.severity === 'High' ? 'text-red-400' :
                    anomaly.severity === 'Medium' ? 'text-yellow-400' : 'text-orange-400'
                  }`}>{anomaly.type}</span>
                  <span className="text-gray-600 float-right">{anomaly.timestamp}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

EnhancedLiveDiagnostic.propTypes = {
  scupData: PropTypes.arrayOf(PropTypes.number),
  entropyData: PropTypes.arrayOf(PropTypes.number),
  heatData: PropTypes.arrayOf(PropTypes.number),
  updateInterval: PropTypes.number,
  onPatternDetected: PropTypes.func,
  onAnomalyDetected: PropTypes.func
};

export default EnhancedLiveDiagnostic; 
