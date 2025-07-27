// src/components/MemoryMap.tsx
//! 64-sector memory activation visualization

import React from 'react';
import { useConsciousnessMonitor } from '../hooks/useConsciousnessMonitor';

export const MemoryMap: React.FC = () => {
  const { consciousness } = useConsciousnessMonitor();

  if (!consciousness) {
    return (
      <div className="blueprint-window">
        <div className="tech-label">MEMORY SECTORS</div>
        <div className="tech-value warning">NO MEMORY DATA</div>
      </div>
    );
  }

  const activeSectors = consciousness.memory_sectors.filter(Boolean).length;
  const activityLevel = activeSectors / 64;

  return (
    <div className="blueprint-window">
      <div className="tech-label">MEMORY ACTIVATION MAP</div>
      <div className="tech-value">{activeSectors}/64 SECTORS ACTIVE</div>
      
      {/* Memory sector grid */}
      <div className="memory-sector-grid">
        {consciousness.memory_sectors.map((active, index) => (
          <div
            key={index}
            className={`memory-sector ${active ? 'active' : ''}`}
            title={`Sector ${index}: ${active ? 'ACTIVE' : 'INACTIVE'}`}
          ></div>
        ))}
      </div>
      
      {/* Activity meter */}
      <div className="memory-activity-meter">
        <div className="tech-label">ACTIVITY LEVEL</div>
        <div className="activity-bar">
          <div 
            className="activity-fill"
            style={{ width: `${activityLevel * 100}%` }}
          ></div>
        </div>
        <div className="tech-value">{(activityLevel * 100).toFixed(1)}%</div>
      </div>
    </div>
  );
};