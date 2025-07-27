// src/components/MoodZoneDisplay.tsx
//! Emotional state quadrant visualization

import React from 'react';
import { useConsciousnessMonitor } from '../hooks/useConsciousnessMonitor';

export const MoodZoneDisplay: React.FC = () => {
  const { consciousness } = useConsciousnessMonitor();

  if (!consciousness) {
    return (
      <div className="blueprint-window">
        <div className="tech-label">EMOTIONAL STATE</div>
        <div className="tech-value warning">NO MOOD DATA</div>
      </div>
    );
  }

  // Calculate 2D mood position
  const moodX = ((consciousness.mood_valence + 1) / 2) * 100; // Convert -1,1 to 0,100
  const moodY = (1 - consciousness.mood_arousal) * 100; // Flip Y axis

  return (
    <div className="blueprint-window">
      <div className="tech-label">EMOTIONAL QUADRANT</div>
      
      {/* 2D Mood Space */}
      <div className="mood-space">
        <div className="mood-grid-lines">
          {/* Vertical center line */}
          <div className="mood-axis vertical"></div>
          {/* Horizontal center line */}
          <div className="mood-axis horizontal"></div>
        </div>
        
        {/* Mood indicator */}
        <div 
          className="mood-indicator"
          style={{
            left: `${moodX}%`,
            top: `${moodY}%`,
            backgroundColor: consciousness.mood_valence >= 0 ? 'var(--emotion-positive)' : 'var(--emotion-negative)',
            transform: `scale(${0.5 + consciousness.mood_dominance * 0.5})`,
            opacity: consciousness.mood_coherence
          }}
        ></div>
        
        {/* Quadrant labels */}
        <div className="mood-labels">
          <span className="mood-label top-left">ANXIOUS</span>
          <span className="mood-label top-right">EXCITED</span>
          <span className="mood-label bottom-left">DEPRESSED</span>
          <span className="mood-label bottom-right">CONTENT</span>
        </div>
      </div>
      
      {/* Mood metrics */}
      <div className="mood-metrics">
        <div className="mood-metric">
          <span className="tech-label">VALENCE</span>
          <span className={`tech-value ${consciousness.mood_valence >= 0 ? 'positive' : 'critical'}`}>
            {consciousness.mood_valence >= 0 ? '+' : ''}{consciousness.mood_valence.toFixed(2)}
          </span>
        </div>
        <div className="mood-metric">
          <span className="tech-label">AROUSAL</span>
          <span className="tech-value">{consciousness.mood_arousal.toFixed(2)}</span>
        </div>
        <div className="mood-metric">
          <span className="tech-label">DOMINANCE</span>
          <span className="tech-value">{consciousness.mood_dominance.toFixed(2)}</span>
        </div>
        <div className="mood-metric">
          <span className="tech-label">COHERENCE</span>
          <span className="tech-value">{consciousness.mood_coherence.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
};