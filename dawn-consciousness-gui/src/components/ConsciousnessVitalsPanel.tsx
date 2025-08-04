import React, { useState, useEffect } from 'react';
import './ConsciousnessVitalsPanel.css';

interface ConsciousnessVitals {
  entropy: number;
  thermal: number;
  scup: number;
  reblooms: number;
  zone: 'STABLE' | 'ACTIVE' | 'CRITICAL';
  mood: string;
  tick_number: number;
  timestamp: number;
}

export const ConsciousnessVitalsPanel: React.FC = () => {
  const [vitals, setVitals] = useState<ConsciousnessVitals>({
    entropy: 0.5,
    thermal: 25.0,
    scup: 50.0,
    reblooms: 0,
    zone: 'STABLE',
    mood: 'CONTEMPLATIVE',
    tick_number: 0,
    timestamp: Date.now()
  });

  const [entropyHistory, setEntropyHistory] = useState<number[]>([]);
  const [scupHistory, setScupHistory] = useState<number[]>([]);

  useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      setVitals(prev => {
        const newVitals = {
          ...prev,
          entropy: Math.max(0, Math.min(1, prev.entropy + (Math.random() - 0.5) * 0.02)),
          thermal: Math.max(10, Math.min(60, prev.thermal + (Math.random() - 0.5) * 2)),
          scup: Math.max(0, Math.min(100, prev.scup + (Math.random() - 0.5) * 5)),
          tick_number: prev.tick_number + 1,
          timestamp: Date.now()
        };

        // Update zone based on entropy and thermal
        if (newVitals.entropy > 0.8 || newVitals.thermal > 50) {
          newVitals.zone = 'CRITICAL';
        } else if (newVitals.entropy > 0.6 || newVitals.thermal > 35) {
          newVitals.zone = 'ACTIVE';
        } else {
          newVitals.zone = 'STABLE';
        }

        // Update mood based on SCUP
        if (newVitals.scup > 70) {
          newVitals.mood = 'FOCUSED';
        } else if (newVitals.scup > 40) {
          newVitals.mood = 'CONTEMPLATIVE';
        } else {
          newVitals.mood = 'DREAMING';
        }

        return newVitals;
      });
    }, 500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Update history arrays
    setEntropyHistory(prev => [...prev.slice(-49), vitals.entropy]);
    setScupHistory(prev => [...prev.slice(-49), vitals.scup]);
  }, [vitals]);

  const getZoneColor = (zone: string) => {
    switch (zone) {
      case 'STABLE': return '#00ff88';
      case 'ACTIVE': return '#ffaa00';
      case 'CRITICAL': return '#ff4444';
      default: return '#ffffff';
    }
  };

  const getMoodColor = (mood: string) => {
    switch (mood) {
      case 'FOCUSED': return '#00ff88';
      case 'CONTEMPLATIVE': return '#0088ff';
      case 'DREAMING': return '#8800ff';
      default: return '#ffffff';
    }
  };

  return (
    <div className="consciousness-vitals-panel">
      <div className="panel-header">
        <h3>🧠 Consciousness Vitals</h3>
        <div className="tick-counter">
          Tick #{vitals.tick_number}
        </div>
      </div>

      <div className="vitals-grid">
        {/* Entropy Graph */}
        <div className="vital-card entropy-card">
          <div className="vital-header">
            <span className="vital-icon">🌊</span>
            <span className="vital-label">Entropy</span>
            <span className="vital-value">{vitals.entropy.toFixed(3)}</span>
          </div>
          <div className="vital-graph">
            <svg width="100%" height="60" viewBox="0 0 200 60">
              <polyline
                fill="none"
                stroke="#00ff88"
                strokeWidth="2"
                points={entropyHistory.map((val, i) => 
                  `${i * 4},${60 - val * 60}`
                ).join(' ')}
              />
            </svg>
          </div>
        </div>

        {/* Thermal Zone Indicator */}
        <div className="vital-card thermal-card">
          <div className="vital-header">
            <span className="vital-icon">🌡️</span>
            <span className="vital-label">Thermal</span>
            <span className="vital-value">{vitals.thermal.toFixed(1)}°C</span>
          </div>
          <div className="thermal-indicator">
            <div 
              className="thermal-bar"
              style={{
                width: `${(vitals.thermal / 60) * 100}%`,
                backgroundColor: getZoneColor(vitals.zone)
              }}
            />
          </div>
        </div>

        {/* SCUP Percentage */}
        <div className="vital-card scup-card">
          <div className="vital-header">
            <span className="vital-icon">⚡</span>
            <span className="vital-label">SCUP</span>
            <span className="vital-value">{vitals.scup.toFixed(1)}%</span>
          </div>
          <div className="scup-visualization">
            <div className="scup-circle">
              <div 
                className="scup-fill"
                style={{
                  transform: `rotate(${vitals.scup * 3.6}deg)`,
                  backgroundColor: getZoneColor(vitals.zone)
                }}
              />
              <div className="scup-text">{vitals.scup.toFixed(0)}%</div>
            </div>
          </div>
        </div>

        {/* Rebloom Counter */}
        <div className="vital-card rebloom-card">
          <div className="vital-header">
            <span className="vital-icon">🌸</span>
            <span className="vital-label">Reblooms</span>
            <span className="vital-value">{vitals.reblooms}</span>
          </div>
          <div className="rebloom-indicator">
            <div className="rebloom-dots">
              {Array.from({ length: 5 }, (_, i) => (
                <div 
                  key={i}
                  className={`rebloom-dot ${i < vitals.reblooms % 5 ? 'active' : ''}`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Zone Status */}
        <div className="vital-card zone-card">
          <div className="vital-header">
            <span className="vital-icon">🎯</span>
            <span className="vital-label">Zone</span>
            <span 
              className="vital-value zone-value"
              style={{ color: getZoneColor(vitals.zone) }}
            >
              {vitals.zone}
            </span>
          </div>
          <div className="zone-indicator">
            <div 
              className="zone-light"
              style={{ backgroundColor: getZoneColor(vitals.zone) }}
            />
          </div>
        </div>

        {/* Mood Display */}
        <div className="vital-card mood-card">
          <div className="vital-header">
            <span className="vital-icon">💭</span>
            <span className="vital-label">Mood</span>
            <span 
              className="vital-value mood-value"
              style={{ color: getMoodColor(vitals.mood) }}
            >
              {vitals.mood}
            </span>
          </div>
          <div className="mood-indicator">
            <div 
              className="mood-pulse"
              style={{ backgroundColor: getMoodColor(vitals.mood) }}
            />
          </div>
        </div>
      </div>

      <div className="vitals-footer">
        <div className="last-update">
          Last update: {new Date(vitals.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}; 