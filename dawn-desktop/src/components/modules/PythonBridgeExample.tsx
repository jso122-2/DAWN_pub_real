import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Play, Square, Activity, Zap } from 'lucide-react';
import PythonBridge from './TickLoopIntergration';
import { EventEmitter } from '@/lib/EventEmitter';

interface TickData {
  id: string;
  timestamp: number;
  type: 'neural' | 'quantum' | 'genomic' | 'system';
  value: number;
  metadata?: Record<string, any>;
}

interface VisualizationData {
  neural: number[];
  quantum: number[];
  genomic: number[];
  system: number[];
}

const PythonBridgeExample: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [tickData, setTickData] = useState<TickData[]>([]);
  const [visualization, setVisualization] = useState<VisualizationData>({
    neural: [],
    quantum: [],
    genomic: [],
    system: []
  });
  const [globalEntropy, setGlobalEntropy] = useState(0.5);
  const [emitter] = useState(() => new EventEmitter());

  // Handle incoming tick data from Python Bridge
  const handleTickData = (data: TickData[]) => {
    setTickData(prev => [...prev.slice(-99), ...data].slice(-100)); // Keep last 100 items
    
    // Update visualization data
    setVisualization(prev => {
      const newViz = { ...prev };
      
      data.forEach(tick => {
        const values = newViz[tick.type];
        values.push(tick.value);
        if (values.length > 50) values.shift(); // Keep last 50 values
      });
      
      return newViz;
    });

    // Update global entropy based on data variance
    const avgValue = data.reduce((sum, tick) => sum + tick.value, 0) / data.length;
    setGlobalEntropy(Math.min(1, Math.max(0, avgValue)));
  };

  // Start a sample Python process
  const startSampleProcess = () => {
    setIsRunning(true);
    
    // Emit event to start a sample neural network process
    emitter.emit('python:execute', {
      script: `
import time
import json
import random

# Simulate neural network training
for epoch in range(100):
    # Simulate neural activity
    neural_value = random.random() * 0.8 + 0.1
    print(json.dumps({
        "type": "neural",
        "value": neural_value,
        "neurons": 128,
        "epoch": epoch
    }))
    
    # Simulate quantum measurements
    if epoch % 5 == 0:
        quantum_value = random.random()
        print(json.dumps({
            "type": "quantum",
            "value": quantum_value,
            "qubits": 8,
            "coherence": 0.95
        }))
    
    # Progress indicator
    print(f"Progress: {(epoch + 1) * 100 / 100:.1f}")
    
    time.sleep(0.1)

print("Training completed!")
      `,
      args: {
        epochs: 100,
        learning_rate: 0.001
      }
    });
  };

  const stopProcess = () => {
    setIsRunning(false);
    emitter.emit('python:stop-all');
  };

  // Data type colors
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'neural': return 'text-blue-400';
      case 'quantum': return 'text-purple-400';
      case 'genomic': return 'text-green-400';
      case 'system': return 'text-yellow-400';
      default: return 'text-white';
    }
  };

  const getTypeGradient = (type: string) => {
    switch (type) {
      case 'neural': return 'from-blue-500 to-cyan-400';
      case 'quantum': return 'from-purple-500 to-pink-400';
      case 'genomic': return 'from-green-500 to-emerald-400';
      case 'system': return 'from-yellow-500 to-orange-400';
      default: return 'from-gray-500 to-gray-400';
    }
  };

  return (
    <div className="w-full h-full flex flex-col space-y-4 p-6">
      {/* Header Controls */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">Python Bridge Demo</h2>
          <p className="text-white/70">Real-time Python process integration with tick loop</p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="text-xs text-white/50">
            Entropy: {(globalEntropy * 100).toFixed(0)}%
          </div>
          
          {!isRunning ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={startSampleProcess}
              className="flex items-center gap-2 px-4 py-2 bg-green-500/20 hover:bg-green-500/30 rounded-lg border border-green-500/30 text-green-400 transition-colors"
            >
              <Play className="w-4 h-4" />
              Start Demo
            </motion.button>
          ) : (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={stopProcess}
              className="flex items-center gap-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg border border-red-500/30 text-red-400 transition-colors"
            >
              <Square className="w-4 h-4" />
              Stop Demo
            </motion.button>
          )}
        </div>
      </div>

      <div className="flex-1 grid grid-cols-2 gap-4">
        {/* Python Bridge Component */}
        <div className="glass-panel glass-depth-2 rounded-lg overflow-hidden">
          <PythonBridge
            emitter={emitter}
            globalEntropy={globalEntropy}
            tickRate={60}
            onTickData={handleTickData}
          />
        </div>

        {/* Data Visualization */}
        <div className="space-y-4">
          {/* Recent Tick Data */}
          <div className="glass-panel glass-depth-1 rounded-lg p-4">
            <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
              <Activity className="w-4 h-4" />
              Live Tick Data
            </h3>
            
            <div className="max-h-48 overflow-y-auto space-y-1">
              {tickData.slice(-10).map((tick) => (
                <motion.div
                  key={tick.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center justify-between p-2 bg-white/5 rounded text-xs"
                >
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${getTypeGradient(tick.type)}`} />
                    <span className={getTypeColor(tick.type)}>{tick.type}</span>
                  </div>
                  <div className="text-white/70">
                    {tick.value.toFixed(3)}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Data Type Charts */}
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(visualization).map(([type, values]) => (
              <div key={type} className="glass-panel glass-depth-1 rounded-lg p-3">
                <h4 className={`text-sm font-medium mb-2 ${getTypeColor(type)}`}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </h4>
                
                                 <div className="h-16 flex items-end justify-between gap-1">
                   {values.slice(-20).map((value: number, index: number) => (
                     <motion.div
                       key={index}
                       initial={{ height: 0 }}
                       animate={{ height: `${value * 100}%` }}
                       className={`w-1 bg-gradient-to-t ${getTypeGradient(type)} rounded-sm`}
                       style={{ minHeight: '2px' }}
                     />
                   ))}
                 </div>
                
                                 <div className="text-xs text-white/50 mt-1">
                   Latest: {(visualization[type as keyof VisualizationData][values.length - 1])?.toFixed(3) || '0.000'}
                 </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer Status */}
      <div className="flex items-center justify-between text-xs text-white/50 px-2">
        <div className="flex items-center gap-4">
          <span>Total Ticks: {tickData.length}</span>
          <span>Types Active: {Object.keys(visualization).filter(type => visualization[type].length > 0).length}</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Zap className="w-3 h-3" />
          <span>60 Hz Tick Rate</span>
        </div>
      </div>
    </div>
  );
};

export default PythonBridgeExample; 