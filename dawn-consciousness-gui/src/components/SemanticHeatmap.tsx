// src/components/SemanticHeatmap.tsx
//! 256-node semantic network visualization

import React from 'react';
import { useConsciousnessMonitor } from '../hooks/useConsciousnessMonitor';

export const SemanticHeatmap: React.FC = () => {
  const { consciousness } = useConsciousnessMonitor();

  if (!consciousness) {
    return (
      <div className="blueprint-window">
        <div className="tech-label">SEMANTIC NETWORK</div>
        <div className="tech-value warning">NO SEMANTIC DATA</div>
      </div>
    );
  }

  const averageActivation = consciousness.semantic_heatmap.reduce((sum, val) => sum + val, 0) / 256;
  const hotNodes = consciousness.semantic_heatmap.filter(val => val > 0.8).length;

  return (
    <div className="blueprint-window">
      <div className="tech-label">SEMANTIC ACTIVATION HEATMAP</div>
      <div className="tech-value">{hotNodes} HOT NODES</div>
      
      {/* Semantic heatmap grid */}
      <div className="semantic-heatmap">
        {consciousness.semantic_heatmap.map((activation, index) => {
          const intensity = Math.min(Math.max(activation, 0), 1);
          const isHot = activation > 0.8;
          
          return (
            <div
              key={index}
              className={`semantic-node ${isHot ? 'hot' : ''}`}
              style={{
                backgroundColor: `hsl(${240 - intensity * 60}, 100%, ${20 + intensity * 60}%)`
              }}
              title={`Node ${index}: ${activation.toFixed(3)}`}
            ></div>
          );
        })}
      </div>
      
      {/* Semantic metrics */}
      <div className="semantic-metrics">
        <div className="semantic-metric">
          <span className="tech-label">AVG ACTIVATION</span>
          <span className="tech-value">{averageActivation.toFixed(3)}</span>
        </div>
        <div className="semantic-metric">
          <span className="tech-label">HOT NODES</span>
          <span className="tech-value">{hotNodes}/256</span>
        </div>
      </div>
    </div>
  );
};