/ src/components/PredictionVector.tsx
//! 32-dimensional future state prediction visualization

import React from 'react';
import { useConsciousnessMonitor } from '../hooks/useConsciousnessMonitor';

export const PredictionVector: React.FC = () => {
  const { consciousness } = useConsciousnessMonitor();

  if (!consciousness) {
    return (
      <div className="blueprint-window">
        <div className="tech-label">PREDICTION VECTOR</div>
        <div className="tech-value warning">NO PREDICTION DATA</div>
      </div>
    );
  }

  const averageConfidence = consciousness.prediction_vector.reduce((sum, val) => sum + Math.abs(val), 0) / 32;
  const significantPredictions = consciousness.prediction_vector.filter(val => Math.abs(val) > 0.5).length;

  return (
    <div className="blueprint-window">
      <div className="tech-label">FUTURE STATE PREDICTIONS</div>
      <div className="tech-value">{significantPredictions}/32 SIGNIFICANT</div>
      
      {/* Prediction vector bars */}
      <div className="prediction-vector">
        {consciousness.prediction_vector.map((prediction, index) => {
          const magnitude = Math.abs(prediction);
          const height = magnitude * 100;
          const isSignificant = magnitude > 0.5;
          const isPositive = prediction >= 0;
          
          return (
            <div
              key={index}
              className={`prediction-bar ${isSignificant ? 'significant' : ''} ${isPositive ? 'positive' : 'negative'}`}
              style={{
                height: `${height}%`,
                backgroundColor: isPositive ? 'var(--neural-accent)' : 'var(--neural-critical)'
              }}
              title={`Dimension ${index}: ${prediction.toFixed(3)}`}
            ></div>
          );
        })}
      </div>
      
      {/* Prediction metrics */}
      <div className="prediction-metrics">
        <div className="prediction-metric">
          <span className="tech-label">AVG CONFIDENCE</span>
          <span className="tech-value">{averageConfidence.toFixed(3)}</span>
        </div>
        <div className="prediction-metric">
          <span className="tech-label">SIGNIFICANT</span>
          <span className="tech-value">{significantPredictions}/32</span>
        </div>
      </div>
    </div>
  );
};