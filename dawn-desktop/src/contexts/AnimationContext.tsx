import React, { createContext, useContext, useState, useCallback } from 'react';

interface AnimationContextType {
  isAnimationsEnabled: boolean;
  toggleAnimations: () => void;
  animationSpeed: number;
  setAnimationSpeed: (speed: number) => void;
  particleCount: number;
  setParticleCount: (count: number) => void;
  glowIntensity: number;
  setGlowIntensity: (intensity: number) => void;
}

const AnimationContext = createContext<AnimationContextType | undefined>(undefined);

export function AnimationProvider({ children }: { children: React.ReactNode }) {
  const [isAnimationsEnabled, setIsAnimationsEnabled] = useState(true);
  const [animationSpeed, setAnimationSpeed] = useState(1);
  const [particleCount, setParticleCount] = useState(100);
  const [glowIntensity, setGlowIntensity] = useState(0.5);

  const toggleAnimations = useCallback(() => {
    setIsAnimationsEnabled(prev => !prev);
  }, []);

  const value = {
    isAnimationsEnabled,
    toggleAnimations,
    animationSpeed,
    setAnimationSpeed,
    particleCount,
    setParticleCount,
    glowIntensity,
    setGlowIntensity,
  };

  return (
    <AnimationContext.Provider value={value}>
      {children}
    </AnimationContext.Provider>
  );
}

export function useAnimation() {
  const context = useContext(AnimationContext);
  if (context === undefined) {
    throw new Error('useAnimation must be used within an AnimationProvider');
  }
  return context;
} 