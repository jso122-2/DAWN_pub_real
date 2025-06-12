import React, { useEffect, useState } from 'react';
import ModulationConsole from './ModulationConsole';
import { useModulationStore } from '../../state/modulation';

const ModulationDemo: React.FC = () => {
  const [isConsoleEnabled, setIsConsoleEnabled] = useState(false);
  const { mood, pulse, noiseInjection } = useModulationStore();

  // Example: React to modulation changes
  useEffect(() => {
    console.log('Modulation changed:', { mood, pulse, noiseInjection });
    
    // Example integrations:
    // 1. Adjust neural visualization parameters
    // 2. Modify tick engine timing
    // 3. Change UI animation speeds
    // 4. Alter background colors/effects
  }, [mood, pulse, noiseInjection]);

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">DAWN Modulation Console Demo</h1>
        
        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Console Controls</h2>
          <button
            onClick={() => setIsConsoleEnabled(!isConsoleEnabled)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              isConsoleEnabled 
                ? 'bg-red-600 hover:bg-red-700' 
                : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            {isConsoleEnabled ? 'Hide Console' : 'Show Console'}
          </button>
          <p className="text-sm text-gray-400 mt-2">
            Or press Ctrl+Shift+M to toggle
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Mood</h3>
            <div className="text-2xl font-bold text-green-400">{mood}%</div>
            <div className="text-sm text-gray-400">
              Affects emotional tone and color schemes
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Pulse</h3>
            <div className="text-2xl font-bold text-blue-400">{pulse}%</div>
            <div className="text-sm text-gray-400">
              Controls animation speed and rhythm
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Noise Injection</h3>
            <div className="text-2xl font-bold text-yellow-400">{noiseInjection}%</div>
            <div className="text-sm text-gray-400">
              Adds randomness and chaos to systems
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Live Preview</h2>
          
          {/* Demo visualization affected by modulation */}
          <div 
            className="w-full h-32 rounded-lg transition-all duration-1000"
            style={{
              background: `linear-gradient(45deg, 
                hsl(${120 + mood * 2.4}, 70%, ${30 + mood * 0.3}%), 
                hsl(${240 - mood * 1.2}, 70%, ${20 + mood * 0.4}%))`,
              transform: `scale(${1 + pulse * 0.01})`,
              filter: `blur(${noiseInjection * 0.05}px) hue-rotate(${noiseInjection * 3.6}deg)`,
            }}
          >
            <div className="flex items-center justify-center h-full">
              <div 
                className="w-16 h-16 bg-white rounded-full animate-pulse"
                style={{
                  animationDuration: `${2 - pulse * 0.015}s`,
                  opacity: 0.7 + mood * 0.003,
                }}
              />
            </div>
          </div>
          
          <p className="text-sm text-gray-400 mt-4">
            This preview demonstrates how modulation values can affect visual elements in real-time.
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Integration Tips</h2>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>• Use <code className="bg-gray-700 px-2 py-1 rounded">useModulationStore()</code> to access values anywhere in your app</li>
            <li>• Modulation values are persisted and shared across components</li>
            <li>• The console auto-hides after 15 seconds of inactivity</li>
            <li>• Drag the console to reposition it on screen</li>
            <li>• Use Ctrl+R while focused to reset values to defaults</li>
            <li>• Sound effects provide audio feedback (requires sound files)</li>
          </ul>
        </div>
      </div>

      {/* Conditionally render the console */}
      {isConsoleEnabled && <ModulationConsole />}
    </div>
  );
};

export default ModulationDemo; 