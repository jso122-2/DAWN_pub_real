import React, { useState, useEffect } from 'react';
import GlassPanel from '../ui/GlassPanel';
import MetricCard from '../ui/MetricCard';

export default function GlassDemo() {
  const [tick, setTick] = useState(0);
  const [entropy, setEntropy] = useState(0.756);
  const [scup, setScup] = useState(0.842);
  const [heat, setHeat] = useState(0.634);

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setTick(prev => prev + 1);
      setEntropy(prev => Math.max(0, Math.min(1, prev + (Math.random() - 0.5) * 0.1)));
      setScup(prev => Math.max(0, Math.min(1, prev + (Math.random() - 0.5) * 0.05)));
      setHeat(prev => Math.max(0, Math.min(1, prev + (Math.random() - 0.5) * 0.08)));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-800 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            🔮 DAWN Glass Morphism System
          </h1>
          <p className="text-gray-300 text-lg">
            Migrated from your old repository - signature glass effects & neural aesthetics!
          </p>
        </div>

        {/* Glass Panel Variants */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <GlassPanel glow="cyan" className="text-center">
            <h3 className="text-xl font-bold text-cyan-300 mb-2">🌊 Cyan Glow</h3>
            <p className="text-gray-300">
              Neural network vibes with that signature cyan glow from your consciousness visualizers.
            </p>
            <div className="mt-4 p-3 bg-black/20 rounded-lg font-mono text-sm text-cyan-400">
              glow="cyan"
            </div>
          </GlassPanel>

          <GlassPanel glow="purple" className="text-center">
            <h3 className="text-xl font-bold text-purple-300 mb-2">🚀 Purple Glow</h3>
            <p className="text-gray-300">
              That mystical purple energy from your quantum consciousness modules.
            </p>
            <div className="mt-4 p-3 bg-black/20 rounded-lg font-mono text-sm text-purple-400">
              glow="purple"
            </div>
          </GlassPanel>

          <GlassPanel glow="mixed" className="text-center">
            <h3 className="text-xl font-bold text-white mb-2">✨ Mixed Glow</h3>
            <p className="text-gray-300">
              The perfect fusion - cyan and purple harmonizing like your old DAWN aesthetic.
            </p>
            <div className="mt-4 p-3 bg-black/20 rounded-lg font-mono text-sm text-gray-300">
              glow="mixed" (default)
            </div>
          </GlassPanel>
        </div>

        {/* Metrics Dashboard */}
        <GlassPanel glow="mixed" className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            📊 Enhanced Metric Cards
            <span className="ml-2 text-sm text-gray-400 font-mono">
              (with real-time animations!)
            </span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="Tick Count"
              value={tick}
              colorScheme="blue"
              icon="⚡"
              subtitle="Processing cycles"
              isConnected={true}
              lastUpdate={Date.now()}
              glow="cyan"
            />
            
            <MetricCard
              title="Entropy"
              value={entropy}
              colorScheme="purple"
              icon="🌀"
              subtitle="System chaos level"
              isConnected={true}
              lastUpdate={Date.now()}
              glow="purple"
            />
            
            <MetricCard
              title="SCUP Index"
              value={scup}
              colorScheme="green"
              icon="🧠"
              subtitle="Consciousness metric"
              isConnected={true}
              lastUpdate={Date.now()}
              glow="mixed"
            />
            
            <MetricCard
              title="Heat"
              value={heat}
              colorScheme="orange"
              icon="🔥"
              subtitle="Neural activity"
              isConnected={tick > 0}
              lastUpdate={Date.now()}
              glow="mixed"
            />
          </div>
        </GlassPanel>

        {/* Neural Terminal Style */}
        <GlassPanel glow="cyan" className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">
            🖥️ Neural Terminal Aesthetics
          </h2>
          <div className="neural-terminal">
            <div className="text-cyan-400 mb-2">
              DAWN@consciousness:~$ ./neural_process --mode=active
            </div>
            <div className="text-purple-400 mb-2">
              [INIT] Loading consciousness modules...
            </div>
            <div className="text-cyan-300 mb-2">
              [OK] Glass morphism system: ACTIVE
            </div>
            <div className="text-purple-300 mb-2">
              [OK] Neon glow effects: INITIALIZED
            </div>
            <div className="text-green-400 mb-2">
              [STATUS] Neural network online. Tick #{tick}
            </div>
            <div className="text-cyan-400 animate-pulse">
              █
            </div>
          </div>
        </GlassPanel>

        {/* Features List */}
        <GlassPanel glow="mixed">
          <h2 className="text-2xl font-bold text-white mb-6">
            🎯 Successfully Migrated Features
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-bold text-cyan-300 mb-3">
                ✅ Glass Morphism System
              </h3>
              <ul className="space-y-2 text-gray-300">
                <li>• Backdrop blur effects</li>
                <li>• Multiple glow variants (cyan, purple, mixed)</li>
                <li>• Hover animations & transforms</li>
                <li>• Responsive glass panels</li>
                <li>• Neural terminal styling</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-bold text-purple-300 mb-3">
                ✅ Enhanced Metric Cards
              </h3>
              <ul className="space-y-2 text-gray-300">
                <li>• Real-time value updates</li>
                <li>• Trend indicators (↗️↘️➡️)</li>
                <li>• Progress bars for numeric values</li>
                <li>• Connection status indicators</li>
                <li>• Smooth animations & transitions</li>
              </ul>
            </div>
          </div>
        </GlassPanel>

        {/* Next Steps */}
        <div className="mt-12 text-center">
          <p className="text-gray-400 text-lg mb-4">
            🚀 Ready to integrate more components from your old repository?
          </p>
          <p className="text-gray-500">
            Next: 3D visualizations, particle systems, consciousness orbs, and WebSocket implementations!
          </p>
        </div>
      </div>
    </div>
  );
} 