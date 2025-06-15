import React from 'react';
import { RadarChartProps } from '../../types/neural';

export const RadarChart: React.FC<RadarChartProps> = ({ data }) => {
  const renderASCIIRadar = () => {
    if (!data) return 'NO DATA';
    
    // 25x25 character grid
    const size = 12;
    const grid: string[][] = Array(25).fill(null).map(() => Array(25).fill(' '));
    const center = 12;
    
    // Plot axes
    const metrics = [
      { label: 'NEURAL', value: data.neural_activity },
      { label: 'QUANTUM', value: data.quantum_coherence },
      { label: 'CHAOS', value: data.chaos_factor },
      { label: 'MEMORY', value: data.memory_utilization },
      { label: 'PATTERN', value: data.pattern_recognition }
    ];
    
    // Draw concentric circles
    for (let r of [4, 8, 12]) {
      for (let angle = 0; angle < 360; angle += 10) {
        const rad = (angle * Math.PI) / 180;
        const x = Math.round(center + r * Math.cos(rad));
        const y = Math.round(center + r * Math.sin(rad));
        if (x >= 0 && x < 25 && y >= 0 && y < 25) {
          grid[y][x] = '·';
        }
      }
    }
    
    // Draw axes and plot data
    metrics.forEach((metric, i) => {
      const angle = (i * 72 - 90) * Math.PI / 180;
      
      // Draw axis line
      for (let r = 0; r <= 12; r++) {
        const x = Math.round(center + r * Math.cos(angle));
        const y = Math.round(center + r * Math.sin(angle));
        if (x >= 0 && x < 25 && y >= 0 && y < 25) {
          grid[y][x] = '-';
        }
      }
      
      // Plot data point
      const dataRadius = metric.value * 12;
      const dataX = Math.round(center + dataRadius * Math.cos(angle));
      const dataY = Math.round(center + dataRadius * Math.sin(angle));
      if (dataX >= 0 && dataX < 25 && dataY >= 0 && dataY < 25) {
        grid[dataY][dataX] = '█';
      }
    });
    
    // Center
    grid[center][center] = '+';
    
    return grid.map(row => row.join('')).join('\n');
  };

  return (
    <div className="radar-chart">
      <pre className="ascii-display">
        {renderASCIIRadar()}
      </pre>
      <div className="radar-legend">
        <div>NEURAL: {(data?.neural_activity || 0).toFixed(2)}</div>
        <div>QUANTUM: {(data?.quantum_coherence || 0).toFixed(2)}</div>
        <div>CHAOS: {(data?.chaos_factor || 0).toFixed(2)}</div>
        <div>MEMORY: {(data?.memory_utilization || 0).toFixed(2)}</div>
        <div>PATTERN: {(data?.pattern_recognition || 0).toFixed(2)}</div>
      </div>
    </div>
  );
}; 