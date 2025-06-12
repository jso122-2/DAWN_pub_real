import React, { useState, useEffect, useRef } from 'react';

const NeuralActivityVisualizer = ({ 
  brainwaveData: propBrainwaveData,
  samplingInfo = { sampling: 1000, window: 5, fft: 512 },
  onPatternDetected,
  onAnomalyDetected 
}) => {
  const canvasRef = useRef(null);
  const spectrogramCanvasRef = useRef(null);
  const waterfallCanvasRef = useRef(null);
  const correlationCanvasRef = useRef(null);
  const animationRef = useRef(null);
  
  const [activeView, setActiveView] = useState('waveforms');
  const [showDiagnostics, setShowDiagnostics] = useState(false);
  
  const [brainwaveData, setBrainwaveData] = useState(propBrainwaveData || {
    delta: [],
    theta: [],
    alpha: [],
    beta: [],
    gamma: []
  });
  
  const [patterns, setPatterns] = useState({
    detected: [],
    anomalies: []
  });
  
  const [dataStreams, setDataStreams] = useState({
    delta: { 
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: 0
    },
    theta: {
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: Math.PI / 4
    },
    alpha: {
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: Math.PI / 2
    },
    beta: {
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: Math.PI / 3
    },
    gamma: {
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: Math.PI / 6
    }
  });
  
  // Update brainwave data from props or generate random data
  useEffect(() => {
    if (propBrainwaveData) {
      setBrainwaveData(propBrainwaveData);
    } else {
    const interval = setInterval(() => {
      setBrainwaveData(prev => ({
        delta: [...prev.delta.slice(-100), Math.random() * 30 + 10],
        theta: [...prev.theta.slice(-100), Math.random() * 20 + 30],
        alpha: [...prev.alpha.slice(-100), Math.random() * 25 + 20],
        beta: [...prev.beta.slice(-100), Math.random() * 35 + 15],
        gamma: [...prev.gamma.slice(-100), Math.random() * 40 + 5]
      }));
    }, 50);
    
    return () => clearInterval(interval);
    }
  }, [propBrainwaveData]);

  // Update frequency domain data streams
  useEffect(() => {
    const updateInterval = setInterval(() => {
      setDataStreams(prev => ({
        delta: {
          ...prev.delta,
          frequency: generateFrequencyData(2, 3),
          phase: prev.delta.phase + 0.02
        },
        theta: {
          ...prev.theta,
          frequency: generateFrequencyData(6, 4),
          phase: prev.theta.phase + 0.03
        },
        alpha: {
          ...prev.alpha,
          frequency: generateFrequencyData(10, 5),
          phase: prev.alpha.phase + 0.04
        },
        beta: {
          ...prev.beta,
          frequency: generateFrequencyData(20, 6),
          phase: prev.beta.phase + 0.05
        },
        gamma: {
          ...prev.gamma,
          frequency: generateFrequencyData(40, 8),
          phase: prev.gamma.phase + 0.06
        }
      }));
    }, 100);
    
    return () => clearInterval(updateInterval);
  }, []);

  // Generate FFT-like data for frequency domain analysis
  const generateFrequencyData = (baseFreq, harmonics) => {
    const data = new Array(64).fill(0);
    for (let i = 0; i < harmonics; i++) {
      const freq = Math.floor(baseFreq * (i + 1));
      if (freq < 64) {
        data[freq] = Math.random() * 0.8 + 0.2;
        // Add some noise to adjacent bins
        if (freq > 0) data[freq - 1] += Math.random() * 0.3;
        if (freq < 63) data[freq + 1] += Math.random() * 0.3;
      }
    }
    return data;
  };
  
  // Draw waveforms with animation
  const drawWaveforms = (ctx, width, height) => {
      // Clear with fade effect
      ctx.fillStyle = 'rgba(10, 15, 27, 0.1)';
      ctx.fillRect(0, 0, width, height);
      
      const waves = [
        { data: brainwaveData.delta, color: '#ff6b6b', label: 'Delta (0.5-4 Hz)', offset: 60 },
        { data: brainwaveData.theta, color: '#4ecdc4', label: 'Theta (4-8 Hz)', offset: 120 },
        { data: brainwaveData.alpha, color: '#45b7d1', label: 'Alpha (8-13 Hz)', offset: 180 },
        { data: brainwaveData.beta, color: '#96ceb4', label: 'Beta (13-30 Hz)', offset: 240 },
        { data: brainwaveData.gamma, color: '#dda0dd', label: 'Gamma (30-100 Hz)', offset: 300 }
      ];
      
      waves.forEach((wave, waveIndex) => {
        // Draw glow
        ctx.shadowBlur = 10;
        ctx.shadowColor = wave.color;
        
        ctx.strokeStyle = wave.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        wave.data.forEach((value, index) => {
          const x = (index / wave.data.length) * width;
          const y = wave.offset + Math.sin(index * 0.1 + Date.now() * 0.001) * value * 0.5;
          
          if (index === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        });
        
        ctx.stroke();
        ctx.shadowBlur = 0;
        
        // Draw label with background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(8, wave.offset - 20, 150, 18);
        ctx.fillStyle = wave.color;
        ctx.font = '12px monospace';
        ctx.fillText(wave.label, 10, wave.offset - 5);
      });
  };

  // Draw spectrogram
  const drawSpectrogram = (ctx, width, height) => {
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);
    
    const bands = ['delta', 'theta', 'alpha', 'beta', 'gamma'];
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#dda0dd'];
    const sectionHeight = height / 5;
    
    bands.forEach((band, idx) => {
      const yOffset = idx * sectionHeight;
      const data = dataStreams[band].frequency;
      
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
      ctx.fillText(band.toUpperCase(), 10, yOffset + 20);
      
      // Frequency scale
      ctx.fillStyle = '#6b7280';
      ctx.font = '10px monospace';
      ctx.fillText('0Hz', 5, yOffset + sectionHeight - 5);
      ctx.fillText('100Hz', width - 35, yOffset + sectionHeight - 5);
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
      { a: 'delta', b: 'theta', color: '#ff6b6b' },
      { a: 'alpha', b: 'beta', color: '#45b7d1' },
      { a: 'beta', b: 'gamma', color: '#96ceb4' }
    ];
    
    pairs.forEach(pair => {
      const phaseA = dataStreams[pair.a].phase;
      const phaseB = dataStreams[pair.b].phase;
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
    ctx.textAlign = 'left';
  };

  // Animation loop with proper rendering
  useEffect(() => {
    let animationId;
    
    const animate = () => {
      // Draw active view
      if (activeView === 'waveforms' && canvasRef.current) {
        const ctx = canvasRef.current.getContext('2d');
        drawWaveforms(ctx, canvasRef.current.width, canvasRef.current.height);
      } else if (activeView === 'spectrogram' && spectrogramCanvasRef.current) {
        const ctx = spectrogramCanvasRef.current.getContext('2d');
        drawSpectrogram(ctx, spectrogramCanvasRef.current.width, spectrogramCanvasRef.current.height);
      } else if (activeView === 'waterfall' && waterfallCanvasRef.current) {
        const ctx = waterfallCanvasRef.current.getContext('2d');
        drawWaterfall(ctx, waterfallCanvasRef.current.width, waterfallCanvasRef.current.height);
      } else if (activeView === 'correlation' && correlationCanvasRef.current) {
        const ctx = correlationCanvasRef.current.getContext('2d');
        drawCorrelation(ctx, correlationCanvasRef.current.width, correlationCanvasRef.current.height);
      }
      
      animationId = requestAnimationFrame(animate);
    };
    
    // Start animation after component mounts
    const timeoutId = setTimeout(() => {
    animate();
    }, 100);
    
    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
      clearTimeout(timeoutId);
    };
  }, [activeView, brainwaveData, dataStreams]);

  // Pattern detection
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate pattern detection based on brainwave data
      if (Math.random() > 0.85) {
        const detectedPattern = {
          type: ['Alpha Spike', 'Beta Surge', 'Gamma Burst', 'Delta Wave', 'Theta Rhythm'][Math.floor(Math.random() * 5)],
          timestamp: new Date().toLocaleTimeString(),
          confidence: (Math.random() * 40 + 60).toFixed(1),
          frequency: Math.floor(Math.random() * 100) + 'Hz'
        };
        
        setPatterns(prev => ({
          ...prev,
          detected: [...prev.detected.slice(-5), detectedPattern]
        }));
        
        // Call callback if provided
        if (onPatternDetected) {
          onPatternDetected(detectedPattern);
        }
      }
      
      // Simulate anomaly detection
      if (Math.random() > 0.95) {
        const anomaly = {
          type: 'Phase Desync',
          severity: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
          timestamp: new Date().toLocaleTimeString(),
          bands: ['Delta-Theta', 'Alpha-Beta', 'Beta-Gamma'][Math.floor(Math.random() * 3)]
        };
        
        setPatterns(prev => ({
          ...prev,
          anomalies: [...prev.anomalies.slice(-3), anomaly]
        }));
        
        // Call callback if provided
        if (onAnomalyDetected) {
          onAnomalyDetected(anomaly);
        }
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [onPatternDetected, onAnomalyDetected]);
  
  return (
    <div className="dawn-panel cognitive-breathing p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></span>
          Neural Activity Visualizer
        </h3>
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveView('waveforms')}
            className={`dawn-button text-sm ${activeView === 'waveforms' ? 'primary' : ''}`}
          >
            Waveforms
          </button>
          <button
            onClick={() => setActiveView('spectrogram')}
            className={`dawn-button text-sm ${activeView === 'spectrogram' ? 'primary' : ''}`}
          >
            Spectrogram
          </button>
          <button
            onClick={() => setActiveView('waterfall')}
            className={`dawn-button text-sm ${activeView === 'waterfall' ? 'primary' : ''}`}
          >
            Waterfall
          </button>
          <button
            onClick={() => setActiveView('correlation')}
            className={`dawn-button text-sm ${activeView === 'correlation' ? 'primary' : ''}`}
          >
            Correlation
          </button>
          <button
            onClick={() => setShowDiagnostics(!showDiagnostics)}
            className={`dawn-button text-sm ${showDiagnostics ? 'primary' : ''}`}
          >
            Diagnostics
          </button>
        </div>
      </div>
      
      <div className="relative dendritic-bg rounded-lg overflow-hidden">
        <canvas 
          ref={canvasRef} 
          width={800} 
          height={400} 
          className={`w-full rounded ${activeView !== 'waveforms' ? 'hidden' : ''}`}
          style={{ background: 'rgba(10, 15, 27, 0.8)' }}
        />
        <canvas 
          ref={spectrogramCanvasRef}
          width={800} 
          height={400}
          className={`w-full rounded ${activeView !== 'spectrogram' ? 'hidden' : ''}`}
          style={{ background: 'rgba(10, 15, 27, 0.8)' }}
        />
        <canvas 
          ref={waterfallCanvasRef}
          width={800} 
          height={400}
          className={`w-full rounded ${activeView !== 'waterfall' ? 'hidden' : ''}`}
          style={{ background: 'rgba(10, 15, 27, 0.8)' }}
        />
        <canvas 
          ref={correlationCanvasRef}
          width={800} 
          height={400}
          className={`w-full rounded ${activeView !== 'correlation' ? 'hidden' : ''}`}
          style={{ background: 'rgba(10, 15, 27, 0.8)' }}
        />
      </div>
      
      {/* Pattern Detection and Diagnostics */}
      {showDiagnostics && (
        <div className="mt-4 grid grid-cols-2 gap-4">
          <div className="dawn-panel p-3">
            <h4 className="text-sm font-bold text-white mb-2 flex items-center">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
              Pattern Detection
            </h4>
            <div className="space-y-1 max-h-32 overflow-y-auto">
              {patterns.detected.length === 0 ? (
                <p className="text-xs text-gray-500">Monitoring neural patterns...</p>
              ) : (
                patterns.detected.map((pattern, idx) => (
                  <div key={idx} className="text-xs neural-impulse">
                    <span className="text-green-400">{pattern.type}</span>
                    <span className="text-blue-400 ml-2">{pattern.frequency}</span>
                    <span className="text-gray-500 ml-2">{pattern.confidence}%</span>
                    <span className="text-gray-600 float-right">{pattern.timestamp}</span>
                  </div>
                ))
              )}
            </div>
          </div>
          
          <div className="dawn-panel p-3">
            <h4 className="text-sm font-bold text-white mb-2 flex items-center">
              <span className="w-2 h-2 bg-red-400 rounded-full mr-2"></span>
              Anomaly Detection
            </h4>
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
                    <span className="text-gray-500 ml-2">{anomaly.bands}</span>
                    <span className="text-gray-600 float-right">{anomaly.timestamp}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
      
      <div className="mt-4 grid grid-cols-5 gap-2">
        <div className="text-center">
          <div className="w-full h-2 bg-red-500/50 rounded-full neural-glow"></div>
          <p className="text-xs text-gray-400 mt-1">Delta</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-teal-400/50 rounded-full neural-glow"></div>
          <p className="text-xs text-gray-400 mt-1">Theta</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-blue-400/50 rounded-full neural-glow"></div>
          <p className="text-xs text-gray-400 mt-1">Alpha</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-green-400/50 rounded-full neural-glow"></div>
          <p className="text-xs text-gray-400 mt-1">Beta</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-purple-400/50 rounded-full neural-glow"></div>
          <p className="text-xs text-gray-400 mt-1">Gamma</p>
        </div>
      </div>
      
      <div className="mt-4 flex justify-between text-xs text-gray-500">
        <span>Sampling: {samplingInfo.sampling} Hz</span>
        <span>Window: {samplingInfo.window}s</span>
        <span>FFT: {samplingInfo.fft} points</span>
        <span>View: {activeView}</span>
      </div>
    </div>
  );
};

export default NeuralActivityVisualizer;