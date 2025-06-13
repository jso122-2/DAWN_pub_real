import React from 'react';
import { useAnimation } from '../contexts/AnimationContext';

export function AnimationControlPanel() {
  const {
    isAnimationsEnabled,
    toggleAnimations,
    animationSpeed,
    setAnimationSpeed,
    particleCount,
    setParticleCount,
    glowIntensity,
    setGlowIntensity,
  } = useAnimation();

  return (
    <div className="fixed bottom-4 right-4 z-50 p-4 bg-black/50 backdrop-blur rounded-lg border border-purple-500/20">
      <h3 className="text-purple-400 font-medium mb-4">Animation Controls</h3>
      
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <button
            onClick={toggleAnimations}
            className={`px-3 py-1 rounded ${
              isAnimationsEnabled
                ? 'bg-green-500/20 text-green-400 border border-green-400/50'
                : 'bg-red-500/20 text-red-400 border border-red-400/50'
            }`}
          >
            {isAnimationsEnabled ? 'Enabled' : 'Disabled'}
          </button>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-purple-300">Animation Speed</label>
          <input
            type="range"
            min="0.1"
            max="2"
            step="0.1"
            value={animationSpeed}
            onChange={(e) => setAnimationSpeed(parseFloat(e.target.value))}
            className="w-full"
          />
          <span className="text-xs text-purple-300">{animationSpeed}x</span>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-purple-300">Particle Count</label>
          <input
            type="range"
            min="0"
            max="500"
            step="10"
            value={particleCount}
            onChange={(e) => setParticleCount(parseInt(e.target.value))}
            className="w-full"
          />
          <span className="text-xs text-purple-300">{particleCount} particles</span>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-purple-300">Glow Intensity</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={glowIntensity}
            onChange={(e) => setGlowIntensity(parseFloat(e.target.value))}
            className="w-full"
          />
          <span className="text-xs text-purple-300">{Math.round(glowIntensity * 100)}%</span>
        </div>
      </div>
    </div>
  );
} 