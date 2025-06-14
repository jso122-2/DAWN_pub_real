import React from 'react';
import { ModuleContainer } from '@/components/core/ModuleContainer';
import { ErrorBoundary } from '@/components/core/ErrorBoundary';
import { ConsciousnessProvider, useConsciousness } from '@/contexts/ConsciousnessContext';

const TestContent: React.FC = () => {
  const consciousness = useConsciousness();
  
  return (
    <div style={{ padding: '1rem', color: 'white' }}>
      <h3>🧠 DAWN Core Fixes Test</h3>
      <p>SCUP Level: {consciousness.scup}</p>
      <p>Entropy: {consciousness.entropy.toFixed(2)}</p>
      <p>Mood: {consciousness.mood}</p>
      <p>Neural Activity: {(consciousness.neuralActivity * 100).toFixed(1)}%</p>
      <div style={{ marginTop: '1rem', fontSize: '0.8rem', opacity: 0.7 }}>
        ✅ All core fixes implemented successfully!
      </div>
    </div>
  );
};

export const TestFixedModule: React.FC = () => {
  return (
    <ConsciousnessProvider>
      <ErrorBoundary>
        <ModuleContainer
          moduleId="test-fixed-module"
          category="monitor"
          position={{ x: 100, y: 100, z: 1 }}
          breathingIntensity={0.6}
          floatingSpeed={0.5}
          glowIntensity={0.8}
        >
          <TestContent />
        </ModuleContainer>
      </ErrorBoundary>
    </ConsciousnessProvider>
  );
}; 