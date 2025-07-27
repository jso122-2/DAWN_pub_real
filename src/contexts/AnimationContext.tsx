import React, { createContext, useContext, useState, useEffect } from 'react';

interface AnimationContextType {
  rotationsEnabled: boolean;
  setRotationsEnabled: (enabled: boolean) => void;
  animationsEnabled: boolean;
  setAnimationsEnabled: (enabled: boolean) => void;
  particlesEnabled: boolean;
  setParticlesEnabled: (enabled: boolean) => void;
}

const AnimationContext = createContext<AnimationContextType | null>(null);

export const AnimationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [rotationsEnabled, setRotationsEnabled] = useState(false); // Start OFF
  const [animationsEnabled, setAnimationsEnabled] = useState(true);
  const [particlesEnabled, setParticlesEnabled] = useState(true);
  
  useEffect(() => {
    // Apply body classes
    document.body.classList.toggle('no-rotations', !rotationsEnabled);
    document.body.classList.toggle('no-animations', !animationsEnabled);
    document.body.classList.toggle('no-particles', !particlesEnabled);
  }, [rotationsEnabled, animationsEnabled, particlesEnabled]);
  
  return (
    <AnimationContext.Provider value={{
      rotationsEnabled,
      setRotationsEnabled,
      animationsEnabled,
      setAnimationsEnabled,
      particlesEnabled,
      setParticlesEnabled
    }}>
      {children}
    </AnimationContext.Provider>
  );
};

export const useAnimationControls = () => {
  const context = useContext(AnimationContext);
  if (!context) {
    throw new Error('useAnimationControls must be used within AnimationProvider');
  }
  return context;
}; 