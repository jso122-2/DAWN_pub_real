import React from 'react';
import { TickState } from '../types/dawn';

interface ForecastVectorProps {
  tickState: TickState | null;
}

const ForecastVector: React.FC<ForecastVectorProps> = ({ tickState }) => {
  if (!tickState || !tickState.forecast_vector) {
    return (
      <div className="forecast-vector">
        <div className="no-forecast-data">
          <div className="tech-label">⚠️ No Forecast Data</div>
        </div>
      </div>
    );
  }

  const { forecast_vector } = tickState;
  
  // Calculate forecast statistics
  const maxValue = Math.max(...forecast_vector);
  const minValue = Math.min(...forecast_vector);
  const avgValue = forecast_vector.reduce((a, b) => a + b, 0) / forecast_vector.length;
  const variance = forecast_vector.reduce((acc, val) => acc + Math.pow(val - avgValue, 2), 0) / forecast_vector.length;
  const confidence = Math.max(0, 1 - variance); // Higher variance = lower confidence

  // Group vectors into categories for better visualization
  const vectorGroups = [
    { name: 'Short-term', vectors: forecast_vector.slice(0, 8), color: 'var(--blueprint-primary)' },
    { name: 'Medium-term', vectors: forecast_vector.slice(8, 16), color: 'var(--blueprint-secondary)' },
    { name: 'Long-term', vectors: forecast_vector.slice(16, 24), color: 'var(--blueprint-accent)' },
    { name: 'Meta', vectors: forecast_vector.slice(24, 32), color: 'var(--blueprint-warning)' }
  ];

  return (
    <div className="forecast-vector">
      <div className="forecast-stats">
        <div className="stat">
          <span className="tech-label">Confidence</span>
          <span className={`tech-value ${confidence > 0.7 ? 'positive' : confidence > 0.4 ? 'warning' : 'critical'}`}>
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>
        <div className="stat">
          <span className="tech-label">Range</span>
          <span className="tech-value">{(maxValue - minValue).toFixed(3)}</span>
        </div>
        <div className="stat">
          <span className="tech-label">Variance</span>
          <span className="tech-value">{variance.toFixed(3)}</span>
        </div>
      </div>

      <div className="forecast-groups">
        {vectorGroups.map((group, groupIndex) => {
          const groupAvg = group.vectors.reduce((a, b) => a + b, 0) / group.vectors.length;
          const groupMax = Math.max(...group.vectors);
          
          return (
            <div key={groupIndex} className="forecast-group">
              <div className="group-header">
                <span className="tech-label">{group.name}</span>
                <span className="tech-value">{groupAvg.toFixed(2)}</span>
              </div>
              
              <div className="vector-bars">
                {group.vectors.map((value, index) => {
                  const normalizedValue = (value - minValue) / (maxValue - minValue || 1);
                  
                  return (
                    <div 
                      key={index}
                      className="vector-bar"
                      title={`${group.name} Vector ${index}: ${value.toFixed(4)}`}
                    >
                      <div 
                        className="bar-fill"
                        style={{
                          height: `${normalizedValue * 100}%`,
                          backgroundColor: group.color,
                          opacity: Math.max(0.3, normalizedValue)
                        }}
                      />
                      <span className="bar-index">{groupIndex * 8 + index}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div className="forecast-legend">
        <div className="legend-gradient" />
        <div className="legend-labels">
          <span className="tech-label">Low</span>
          <span className="tech-label">High</span>
        </div>
      </div>
    </div>
  );
};

export default ForecastVector; 