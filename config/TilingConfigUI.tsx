import React from 'react';
import { useTilingAwareUI } from './uiMode';

const TilingConfigUI: React.FC = () => {
  const { 
    wmType, 
    isEnabled, 
    isLocked, 
    toggle, 
    toggleLock, 
    recommendations 
  } = useTilingAwareUI();

  return (
    <div className="fixed bottom-4 right-4 glass-dark animate-breathe rounded-lg p-4 shadow-glow-sm border-0 min-w-[300px] hover:shadow-glow-md transition-all duration-300">
      <h3 className="text-lg font-semibold text-gray-100 mb-4">Tiling Mode Configuration</h3>
      
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Window Manager</span>
          <span className="text-sm font-mono text-cyan-400">{wmType}</span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Tiling Mode</span>
          <button
            onClick={toggle}
            className={`px-3 py-1 text-xs rounded-full transition-all ${
              isEnabled 
                ? 'bg-green-500/20 text-green-400 border border-green-500/50' 
                : 'bg-gray-700/50 text-gray-400 border border-gray-600/50'
            }`}
          >
            {isEnabled ? 'Enabled' : 'Disabled'}
          </button>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-300">Panel Lock</span>
          <button
            onClick={toggleLock}
            disabled={!isEnabled}
            className={`px-3 py-1 text-xs rounded-full transition-all ${
              isLocked 
                ? 'bg-orange-500/20 text-orange-400 border border-orange-500/50' 
                : 'bg-gray-700/50 text-gray-400 border border-gray-600/50'
            } ${!isEnabled && 'opacity-50 cursor-not-allowed'}`}
          >
            {isLocked ? 'Locked' : 'Floating'}
          </button>
        </div>
      </div>
      
      {wmType !== 'none' && (
        <div className="mt-4 pt-4 border-t border-gray-700/50">
          <p className="text-xs text-gray-400 mb-2">Keyboard Shortcuts:</p>
          <div className="space-y-1">
            {Object.entries(recommendations.keybindings || {}).map(([action, key]) => (
              <div key={action} className="flex items-center justify-between text-xs">
                <span className="text-gray-500">{action}</span>
                <kbd className="px-2 py-0.5 bg-gray-800 rounded text-gray-300">{key as string}</kbd>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TilingConfigUI; 