import React, { useState, useEffect, useRef } from 'react';

const EnhancedLiveDiagnostic = () => {
  const spectrogramCanvasRef = useRef(null);
  const waterfallCanvasRef = useRef(null);
  const correlationCanvasRef = useRef(null);
  const animationRef = useRef(null);
  
  const [activeView, setActiveView] = useState('spectrogram');
  const [patterns, setPatterns] = useState({
    detected: [],
    anomalies: []
  });
  
  const [dataStreams] = useState({
    scup: { 
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: 0
    },
    entropy: {
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: Math.PI / 4
    },
    heat: {
      frequency: new Array(64).fill(0),
      amplitude: new Array(128).fill(0),
      phase: Math.PI / 2
    }
  });
  
  // Generate FFT-like data
  const generateFrequencyData = (baseFreq, harmonics) => {
    const data = new Array(64).fill(0);
    for (let i = 0; i < harmonics; i++) {
      const freq = baseFreq * (i + 1);
      if (freq < 64) {
        data[freq] = Math.random() * 0.8 + 0.2;
      }
    }
    return data;
  };
  
  // Draw spectrogram
  const drawSpectrogram = (ctx, width, height) => {
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);
    
    const streams = ['scup', 'entropy', 'heat'];
    const colors = ['#ec4899', '#3b82f6', '#f59e0b'];
    const sectionHeight = height / 3;
    
    streams.forEach((stream, idx) => {
      const yOffset = idx * sectionHeight;
      const data = dataStreams[stream].frequency;
      
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
  };
  
  // Animation loop
  useEffect(() => {
    const animate = () => {
      // Update data
      Object.keys(dataStreams).forEach(stream => {
        dataStreams[stream].frequency = generateFrequencyData(
          Math.floor(Math.random() * 10) + 5,
          Math.floor(Math.random() * 5) + 3
        );
        dataStreams[stream].phase += 0.05;
      });
      
      // Draw active view
      if (activeView === 'spectrogram' && spectrogramCanvasRef.current) {
        const ctx = spectrogramCanvasRef.current.getContext('2d');
        drawSpectrogram(ctx, spectrogramCanvasRef.current.width, spectrogramCanvasRef.current.height);
      } else if (activeView === 'waterfall' && waterfallCanvasRef.current) {
        const ctx = waterfallCanvasRef.current.getContext('2d');
        drawWaterfall(ctx, waterfallCanvasRef.current.width, waterfallCanvasRef.current.height);
      } else if (activeView === 'correlation' && correlationCanvasRef.current) {
        const ctx = correlationCanvasRef.current.getContext('2d');
        drawCorrelation(ctx, correlationCanvasRef.current.width, correlationCanvasRef.current.height);
      }
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [activeView]);
  
  // Pattern detection
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate pattern detection
      if (Math.random() > 0.8) {
        setPatterns(prev => ({
          detected: [...prev.detected.slice(-5), {
            type: ['Alpha Spike', 'Beta Surge', 'Gamma Burst'][Math.floor(Math.random() * 3)],
            timestamp: new Date().toLocaleTimeString(),
            confidence: (Math.random() * 40 + 60).toFixed(1)
          }],
          anomalies: prev.anomalies
        }));
      }
      
      // Simulate anomaly detection
      if (Math.random() > 0.95) {
        setPatterns(prev => ({
          detected: prev.detected,
          anomalies: [...prev.anomalies.slice(-3), {
            type: 'Phase Desync',
            severity: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
            timestamp: new Date().toLocaleTimeString()
          }]
        }));
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700">
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
        <div className="bg-gray-800 rounded p-3">
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
        
        <div className="bg-gray-800 rounded p-3">
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

export default EnhancedLiveDiagnostic;