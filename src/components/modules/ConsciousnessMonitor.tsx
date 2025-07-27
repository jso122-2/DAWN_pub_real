import React from 'react';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useRealTimeConsciousness } from '../../../dawn-desktop/src/hooks/useRealTimeConsciousness';
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

export function ConsciousnessMonitor({ moduleId = "consciousness-monitor" }) {
  const consciousness = useRealTimeConsciousness();
  const { broadcast, messages } = useModuleCommunication(
    moduleId, 
    'consciousness-monitor', 
    ['consciousness_analysis', 'alerting']
  );

  // Broadcast consciousness updates
  React.useEffect(() => {
    const interval = setInterval(() => {
      broadcast('consciousness_update', {
        scup: consciousness.scup,
        entropy: consciousness.entropy,
        mood: consciousness.mood,
        neuralActivity: consciousness.neuralActivity
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [consciousness, broadcast]);

  // Alert on critical states
  React.useEffect(() => {
    if (consciousness.scup > 90 || consciousness.scup < 10) {
      broadcast('neural_spike', {
        level: consciousness.scup > 90 ? 'high' : 'low',
        value: consciousness.scup,
        timestamp: Date.now()
      }, 'critical');
    }
  }, [consciousness.scup, broadcast]);

  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
      <div className="p-4 h-full">
        <h3 className="text-white/80 text-sm mb-4 font-mono">Consciousness Monitor</h3>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">SCUP Level</span>
            <div className="flex items-center space-x-2">
              <div className="w-20 h-2 bg-black/40 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 transition-all duration-300"
                  style={{ width: `${consciousness.scup}%` }}
                />
              </div>
              <span className="text-xs text-white font-mono">{consciousness.scup.toFixed(1)}%</span>
            </div>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Entropy</span>
            <span className="text-xs text-white font-mono">{consciousness.entropy.toFixed(3)}</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Neural Activity</span>
            <span className="text-xs text-white font-mono">{(consciousness.neuralActivity * 100).toFixed(1)}%</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Mood State</span>
            <span className={`text-xs font-mono px-2 py-1 rounded ${
              consciousness.mood === 'critical' ? 'bg-red-500/20 text-red-300' :
              consciousness.mood === 'excited' ? 'bg-yellow-500/20 text-yellow-300' :
              consciousness.mood === 'active' ? 'bg-blue-500/20 text-blue-300' :
              'bg-green-500/20 text-green-300'
            }`}>
              {consciousness.mood.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-white/10">
          <div className="text-xs text-white/40 mb-2">Messages: {messages.length}</div>
          <div className="text-xs text-white/60">Broadcasting...</div>
        </div>
      </div>
    </LivingModuleWrapper>
  );
} 