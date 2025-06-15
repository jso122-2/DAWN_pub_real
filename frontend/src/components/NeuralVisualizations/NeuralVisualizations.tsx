import React, { useState } from 'react';
import { RadarChart } from './RadarChart';
import { Histogram } from './Histogram';
import { useNeuralMetrics } from '../../hooks/useNeuralMetrics';
import './NeuralVisualizations.css';

export const NeuralVisualizations: React.FC = () => {
  const [view, setView] = useState<'radar' | 'histogram'>('radar');
  const { connected, metrics } = useNeuralMetrics();

  return (
    <div className="neural-viz">
      <header className="viz-header">
        <h3>NEURAL HEURISTICS</h3>
        <div className="view-toggle">
          <button 
            className={view === 'radar' ? 'active' : ''} 
            onClick={() => setView('radar')}
          >
            RADAR
          </button>
          <button 
            className={view === 'histogram' ? 'active' : ''} 
            onClick={() => setView('histogram')}
          >
            HISTOGRAM
          </button>
        </div>
      </header>
      
      <div className="viz-content">
        {!connected ? (
          <div className="connection-status">Connecting to neural metrics...</div>
        ) : view === 'radar' ? (
          <RadarChart data={metrics} />
        ) : (
          <Histogram data={metrics?.entropy_distribution || []} />
        )}
      </div>
    </div>
  );
}; 