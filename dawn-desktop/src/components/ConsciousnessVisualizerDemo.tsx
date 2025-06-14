import React from 'react';
import { ConsciousnessVisualizer } from './modules/ConsciousnessVisualizer/ConsciousnessVisualizer';

export const ConsciousnessVisualizerDemo: React.FC = () => {
  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <div style={{
        width: '90%',
        height: '90%',
        maxWidth: '1200px',
        maxHeight: '800px'
      }}>
        <ConsciousnessVisualizer 
          moduleId="consciousness-demo"
          position={{ x: 0, y: 0, z: 0 }}
        />
      </div>
    </div>
  );
}; 