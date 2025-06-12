import React, { useState, useEffect, useRef } from 'react';

const NeuralActivityVisualizer = () => {
  const canvasRef = useRef(null);
  const [brainwaveData, setBrainwaveData] = useState({
    delta: [],
    theta: [],
    alpha: [],
    beta: [],
    gamma: []
  });
  
  // Generate random brainwave data
  useEffect(() => {
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
  }, []);
  
  // Draw waveforms
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);
    
    const waves = [
      { data: brainwaveData.delta, color: '#ff6b6b', label: 'Delta (0.5-4 Hz)', offset: 0 },
      { data: brainwaveData.theta, color: '#4ecdc4', label: 'Theta (4-8 Hz)', offset: 60 },
      { data: brainwaveData.alpha, color: '#45b7d1', label: 'Alpha (8-13 Hz)', offset: 120 },
      { data: brainwaveData.beta, color: '#96ceb4', label: 'Beta (13-30 Hz)', offset: 180 },
      { data: brainwaveData.gamma, color: '#dda0dd', label: 'Gamma (30-100 Hz)', offset: 240 }
    ];
    
    waves.forEach(wave => {
      ctx.strokeStyle = wave.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      
      wave.data.forEach((value, index) => {
        const x = (index / wave.data.length) * width;
        const y = wave.offset + (value / 100) * 50;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.stroke();
      
      // Draw label
      ctx.fillStyle = wave.color;
      ctx.font = '12px monospace';
      ctx.fillText(wave.label, 10, wave.offset - 5);
    });
  }, [brainwaveData]);
  
  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></span>
          Live Neural Activity
        </h3>
        <div className="flex space-x-2">
          <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
            3D View
          </button>
          <button className="px-3 py-1 bg-gray-700 text-white rounded text-sm hover:bg-gray-600">
            Spike View
          </button>
        </div>
      </div>
      
      <canvas 
        ref={canvasRef} 
        width={800} 
        height={300} 
        className="w-full rounded bg-gray-950"
      />
      
      <div className="mt-4 grid grid-cols-5 gap-2">
        <div className="text-center">
          <div className="w-full h-2 bg-red-500 rounded"></div>
          <p className="text-xs text-gray-400 mt-1">Delta</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-teal-400 rounded"></div>
          <p className="text-xs text-gray-400 mt-1">Theta</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-blue-400 rounded"></div>
          <p className="text-xs text-gray-400 mt-1">Alpha</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-green-400 rounded"></div>
          <p className="text-xs text-gray-400 mt-1">Beta</p>
        </div>
        <div className="text-center">
          <div className="w-full h-2 bg-purple-400 rounded"></div>
          <p className="text-xs text-gray-400 mt-1">Gamma</p>
        </div>
      </div>
      
      <div className="mt-4 flex justify-between text-xs text-gray-500">
        <span>Sampling: 1000 Hz</span>
        <span>Window: 5s</span>
        <span>FFT: 512 points</span>
      </div>
    </div>
  );
};

export default NeuralActivityVisualizer;