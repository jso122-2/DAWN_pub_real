import React from 'react';
import { TickState } from '../types/dawn';

interface MoodZoneIndicatorProps {
  tickState: TickState | null;
}

const MoodZoneIndicator: React.FC<MoodZoneIndicatorProps> = ({ tickState }) => {
  if (!tickState) {
    return (
      <div className="mood-zone-indicator">
        <div className="no-mood-data">
          <div className="tech-label">⚠️ No Mood Data</div>
        </div>
      </div>
    );
  }

  const { mood_zone } = tickState;
  
  // Determine overall mood classification
  const getMoodClass = () => {
    if (mood_zone.valence > 0.3) return 'positive';
    if (mood_zone.valence < -0.3) return 'negative';
    return 'neutral';
  };

  const getMoodEmoji = () => {
    const moodClass = getMoodClass();
    if (moodClass === 'positive') return '😊';
    if (moodClass === 'negative') return '😔';
    return '😐';
  };

  return (
    <div className="mood-zone-indicator">
      <div className="mood-overview">
        <div className={`mood-state ${getMoodClass()}`}>
          <span className="mood-emoji">{getMoodEmoji()}</span>
          <span className="mood-label">{getMoodClass().toUpperCase()}</span>
        </div>
      </div>

      <div className="mood-metrics">
        <div className="mood-dimension">
          <div className="tech-label">Valence</div>
          <div className="mood-bar-container">
            <div 
              className={`mood-bar ${mood_zone.valence >= 0 ? 'positive' : 'negative'}`}
              style={{'--mood-level': `${Math.abs(mood_zone.valence) * 50 + 50}%`} as React.CSSProperties}
            />
            <span className="tech-value">{mood_zone.valence.toFixed(2)}</span>
          </div>
        </div>

        <div className="mood-dimension">
          <div className="tech-label">Arousal</div>
          <div className="mood-bar-container">
            <div 
              className="mood-bar arousal"
              style={{'--mood-level': `${mood_zone.arousal * 100}%`} as React.CSSProperties}
            />
            <span className="tech-value">{mood_zone.arousal.toFixed(2)}</span>
          </div>
        </div>

        <div className="mood-dimension">
          <div className="tech-label">Dominance</div>
          <div className="mood-bar-container">
            <div 
              className="mood-bar dominance"
              style={{'--mood-level': `${mood_zone.dominance * 100}%`} as React.CSSProperties}
            />
            <span className="tech-value">{mood_zone.dominance.toFixed(2)}</span>
          </div>
        </div>

        <div className="mood-dimension">
          <div className="tech-label">Coherence</div>
          <div className="mood-bar-container">
            <div 
              className="mood-bar coherence"
              style={{'--mood-level': `${mood_zone.coherence * 100}%`} as React.CSSProperties}
            />
            <span className="tech-value">{mood_zone.coherence.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MoodZoneIndicator; 