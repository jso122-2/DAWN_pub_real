// src/components/CognitiveVector.tsx
//! Cognitive state vector visualization

import React from 'react';
import { useConsciousnessMonitor } from '../hooks/useConsciousnessMonitor';

export const CognitiveVector: React.FC = () => {
  const { consciousness, cognitiveLoad } = useConsciousnessMonitor();

  if (!consciousness) {
    return (
      <div className="blueprint-window">
        <div className="tech-label">COGNITIVE VECTORS</div>
        <div className="tech-value warning">NO COGNITIVE DATA</div>
      </div>
    );
  }

  const cognitiveMetrics = [
    {
      label: 'SEMANTIC ALIGN',
      value: consciousness.semantic_alignment,
      color: 'var(--neural-accent)'
    },
    {
      label: 'ENTROPY GRAD',
      value: consciousness.entropy_gradient,
      color: 'var(--neural-warning)'
    },
    {
      label: 'DRIFT MAGN',
      value: consciousness.drift_magnitude,
      color: 'var(--neural-secondary)'
    },
    {
      label: 'REBLOOM INT',
      value: consciousness.rebloom_intensity,
      color: 'var(--emotion-positive)'
    }
  ];

  return (
    <div className="blueprint-window">
      <div className="tech-label">COGNITIVE STATE VECTORS</div>
      <div className="tech-value">LOAD: {(cognitiveLoad * 100).toFixed(1)}%</div>
      
      {/* Cognitive vector bars */}
      <div className="cognitive-vectors">
        {cognitiveMetrics.map((metric, index) => (
          <div key={index} className="cognitive-vector-item">
            <div className="vector-label">
              <span className="tech-label">{metric.label}</span>
              <span className="tech-value">{metric.value.toFixed(3)}</span>
            </div>
            <div className="vector-bar">
              <div 
                className="vector-fill"
                style={{ 
                  width: `${metric.value * 100}%`,
                  backgroundColor: metric.color,
                  boxShadow: `0 0 6px ${metric.color}`
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Overall cognitive load meter */}
      <div className="cognitive-load-meter">
        <div className="tech-label">OVERALL COGNITIVE LOAD</div>
        <div className="load-meter">
          <div 
            className="load-fill"
            style={{ 
              width: `${cognitiveLoad * 100}%`,
              backgroundColor: cognitiveLoad > 0.7 ? 'var(--neural-critical)' : 'var(--neural-primary)'
            }}
          ></div>
        </div>
        <div className="tech-value">{(cognitiveLoad * 100).toFixed(1)}%</div>
      </div>
    </div>
  );
};