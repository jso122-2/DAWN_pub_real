import React from 'react';
import { TickState } from '../types/dawn';

interface RebloomGridProps {
  tickState: TickState | null;
}

const RebloomGrid: React.FC<RebloomGridProps> = ({ tickState }) => {
  if (!tickState || !tickState.memory_rebloom_flags) {
    return (
      <div className="rebloom-grid">
        <div className="no-rebloom-data">
          <div className="tech-label">⚠️ No Memory Data</div>
        </div>
      </div>
    );
  }

  const { memory_rebloom_flags } = tickState;
  const gridSize = 8; // 8x8 grid for 64 memory sectors
  
  // Calculate rebloom statistics
  const activeReblooms = memory_rebloom_flags.filter(Boolean).length;
  const rebloomPercentage = (activeReblooms / memory_rebloom_flags.length) * 100;

  return (
    <div className="rebloom-grid">
      <div className="rebloom-stats">
        <div className="stat">
          <span className="tech-label">Active</span>
          <span className="tech-value">{activeReblooms}/64</span>
        </div>
        <div className="stat">
          <span className="tech-label">Coverage</span>
          <span className="tech-value">{rebloomPercentage.toFixed(1)}%</span>
        </div>
      </div>

      <div 
        className="memory-sectors"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
          gap: '2px'
        }}
      >
        {memory_rebloom_flags.map((isActive, index) => {
          const row = Math.floor(index / gridSize);
          const col = index % gridSize;
          
          return (
            <div
              key={index}
              className={`memory-sector ${isActive ? 'active' : 'inactive'}`}
              style={{
                '--sector-row': row,
                '--sector-col': col
              } as React.CSSProperties}
              title={`Sector ${index}: ${isActive ? 'Reblooming' : 'Dormant'}`}
            >
              <div className="sector-inner">
                {isActive && (
                  <div className="rebloom-pulse" />
                )}
                <span className="sector-id">{index}</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="rebloom-legend">
        <div className="legend-item">
          <div className="legend-color active" />
          <span className="tech-label">Reblooming</span>
        </div>
        <div className="legend-item">
          <div className="legend-color inactive" />
          <span className="tech-label">Dormant</span>
        </div>
      </div>
    </div>
  );
};

export default RebloomGrid; 