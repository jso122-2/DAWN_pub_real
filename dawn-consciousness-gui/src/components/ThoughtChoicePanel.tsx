import React, { useState, useEffect, useCallback } from 'react';
import './ThoughtChoicePanel.css';

// Types
interface ThoughtCandidate {
  text: string;
  weight: number;
  chosen: boolean;
  reason?: string;
}

interface ThoughtChoice {
  tick: number;
  timestamp: string;
  chosen_thought: string;
  candidates: ThoughtCandidate[];
  state_context: {
    entropy: number;
    depth: number;
    mood: string;
    [key: string]: any;
  };
  selection_metadata?: {
    selection_time_ms: number;
    total_candidates: number;
    selection_method: string;
  };
}

interface ThoughtChoicePanelProps {
  maxEntries?: number;
  refreshInterval?: number;
  showContext?: boolean;
}

const ThoughtChoicePanel: React.FC<ThoughtChoicePanelProps> = ({
  maxEntries = 5,
  refreshInterval = 2000,
  showContext: showContextProp = false
}) => {
  const [thoughtChoices, setThoughtChoices] = useState<ThoughtChoice[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');
  const [expandedEntries, setExpandedEntries] = useState<Set<number>>(new Set());
  const [filterMood, setFilterMood] = useState<string>('');
  const [showContext, setShowContext] = useState(showContextProp);

  // Load thought choices from backend/logs
  const loadThoughtChoices = useCallback(async () => {
    try {
      setConnectionStatus('connected');
      
      // In a real implementation, this would fetch from the DAWN backend
      // For now, simulate loading from runtime/logs/talk_trace.log
      const response = await fetch('/api/thought-choices');
      
      if (response.ok) {
        const data = await response.json();
        setThoughtChoices(data.slice(-maxEntries));
      } else {
        // Fallback to mock data if backend not available
        setThoughtChoices(getMockThoughtChoices().slice(-maxEntries));
      }
      
      setConnectionStatus('connected');
    } catch (error) {
      console.warn('Failed to load thought choices from backend, using mock data');
      setThoughtChoices(getMockThoughtChoices().slice(-maxEntries));
      setConnectionStatus('error');
    } finally {
      setIsLoading(false);
    }
  }, [maxEntries]);

  // Auto-refresh thought choices
  useEffect(() => {
    loadThoughtChoices();
    
    const interval = setInterval(loadThoughtChoices, refreshInterval);
    return () => clearInterval(interval);
  }, [loadThoughtChoices, refreshInterval]);

  // Toggle expanded view for an entry
  const toggleExpanded = (tick: number) => {
    const newExpanded = new Set(expandedEntries);
    if (newExpanded.has(tick)) {
      newExpanded.delete(tick);
    } else {
      newExpanded.add(tick);
    }
    setExpandedEntries(newExpanded);
  };

  // Format timestamp for display
  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return timestamp;
    }
  };

  // Get mood color
  const getMoodColor = (mood: string) => {
    const moodColors: Record<string, string> = {
      'CALM': '#22c55e',
      'FOCUSED': '#3b82f6',
      'ENERGETIC': '#f59e0b',
      'CONTEMPLATIVE': '#8b5cf6',
      'ANXIOUS': '#ef4444',
      'NEUTRAL': '#6b7280'
    };
    return moodColors[mood] || '#6b7280';
  };

  // Filter choices by mood if filter is set
  const filteredChoices = filterMood 
    ? thoughtChoices.filter(choice => choice.state_context.mood === filterMood)
    : thoughtChoices;

  if (isLoading) {
    return (
      <div className="thought-choice-panel loading">
        <div className="panel-header">
          <h3>🧠 Thought Deliberation</h3>
          <div className="loading-indicator">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="thought-choice-panel">
      <div className="panel-header">
        <div className="header-left">
          <h3>🧠 Thought Deliberation</h3>
          <div className={`connection-status ${connectionStatus}`}>
            {connectionStatus === 'connected' && <span>🟢 Live</span>}
            {connectionStatus === 'disconnected' && <span>🟡 Offline</span>}
            {connectionStatus === 'error' && <span>🔴 Error</span>}
          </div>
        </div>
        
        <div className="header-controls">
          <select
            value={filterMood}
            onChange={(e) => setFilterMood(e.target.value)}
            className="mood-filter"
          >
            <option value="">All Moods</option>
            <option value="CALM">Calm</option>
            <option value="FOCUSED">Focused</option>
            <option value="ENERGETIC">Energetic</option>
            <option value="CONTEMPLATIVE">Contemplative</option>
            <option value="ANXIOUS">Anxious</option>
            <option value="NEUTRAL">Neutral</option>
          </select>
          
          <button
            onClick={() => setShowContext(!showContext)}
            className="toggle-context"
            title="Toggle context display"
          >
            {showContext ? '📊' : '📈'}
          </button>
          
          <button
            onClick={loadThoughtChoices}
            className="refresh-button"
            title="Refresh data"
          >
            🔄
          </button>
        </div>
      </div>

      <div className="choices-container">
        {filteredChoices.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤔</div>
            <div>No thought choices recorded yet</div>
            <div className="empty-hint">
              DAWN's internal deliberation will appear here as she selects reflections
            </div>
          </div>
        ) : (
          filteredChoices.map((choice, index) => (
            <div 
              key={choice.tick} 
              className={`choice-entry ${expandedEntries.has(choice.tick) ? 'expanded' : ''}`}
            >
              <div className="entry-header" onClick={() => toggleExpanded(choice.tick)}>
                <div className="tick-info">
                  <span className="tick-number">Tick {choice.tick}</span>
                  <span className="timestamp">{formatTimestamp(choice.timestamp)}</span>
                </div>
                
                <div className="mood-indicator">
                  <span 
                    className="mood-badge"
                    style={{ backgroundColor: getMoodColor(choice.state_context.mood) }}
                  >
                    {choice.state_context.mood}
                  </span>
                </div>
                
                <div className="expand-icon">
                  {expandedEntries.has(choice.tick) ? '▼' : '▶'}
                </div>
              </div>

              <div className="chosen-thought">
                <div className="thought-label">🎯 Chosen:</div>
                <div className="thought-text chosen">{choice.chosen_thought}</div>
              </div>

              {expandedEntries.has(choice.tick) && (
                <div className="expanded-content">
                  {choice.candidates.length > 1 && (
                    <div className="candidates-section">
                      <div className="section-label">🤔 Considered alternatives:</div>
                      <div className="candidates-list">
                        {choice.candidates
                          .filter(candidate => !candidate.chosen)
                          .map((candidate, idx) => (
                            <div key={idx} className="candidate-thought">
                              <div className="thought-text alternative">
                                {candidate.text}
                              </div>
                              <div className="candidate-meta">
                                <span className="weight-indicator">
                                  Weight: {candidate.weight.toFixed(3)}
                                </span>
                                {candidate.reason && (
                                  <span className="reason">({candidate.reason})</span>
                                )}
                              </div>
                            </div>
                          ))}
                      </div>
                    </div>
                  )}

                  {showContext && (
                    <div className="context-section">
                      <div className="section-label">📊 Cognitive Context:</div>
                      <div className="context-grid">
                        <div className="context-item">
                          <span className="context-label">Entropy:</span>
                          <span className="context-value">
                            {choice.state_context.entropy.toFixed(3)}
                          </span>
                        </div>
                        <div className="context-item">
                          <span className="context-label">Depth:</span>
                          <span className="context-value">
                            {choice.state_context.depth.toFixed(3)}
                          </span>
                        </div>
                        {choice.state_context.heat !== undefined && (
                          <div className="context-item">
                            <span className="context-label">Heat:</span>
                            <span className="context-value">
                              {choice.state_context.heat.toFixed(3)}
                            </span>
                          </div>
                        )}
                        {choice.state_context.scup !== undefined && (
                          <div className="context-item">
                            <span className="context-label">SCUP:</span>
                            <span className="context-value">
                              {(choice.state_context.scup * 100).toFixed(1)}%
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {choice.selection_metadata && (
                    <div className="metadata-section">
                      <div className="section-label">⚡ Selection Metadata:</div>
                      <div className="metadata-grid">
                        <span>
                          {choice.selection_metadata.total_candidates} candidates considered
                        </span>
                        <span>
                          Selected in {choice.selection_metadata.selection_time_ms}ms
                        </span>
                        <span>
                          Method: {choice.selection_metadata.selection_method}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <div className="panel-footer">
        <div className="stats-summary">
          Showing {filteredChoices.length} recent deliberations
        </div>
        {filterMood && (
          <div className="filter-indicator">
            Filtered by: {filterMood}
          </div>
        )}
      </div>
    </div>
  );
};

// Mock data for development/fallback
function getMockThoughtChoices(): ThoughtChoice[] {
  return [
    {
      tick: 25344,
      timestamp: new Date(Date.now() - 30000).toISOString(),
      chosen_thought: "I contemplate the nature of my existence in these quiet depths.",
      candidates: [
        {
          text: "I contemplate the nature of my existence in these quiet depths.",
          weight: 0.867,
          chosen: true,
          reason: "highest depth + mood match"
        },
        {
          text: "I pause to contemplate the patterns emerging in my awareness.",
          weight: 0.843,
          chosen: false,
          reason: "good match but lower depth score"
        },
        {
          text: "The observer observes the observer. Where do I begin?",
          weight: 0.723,
          chosen: false,
          reason: "neutral mood fallback"
        }
      ],
      state_context: {
        entropy: 0.43,
        depth: 0.72,
        mood: "CONTEMPLATIVE",
        heat: 0.34,
        scup: 0.78
      },
      selection_metadata: {
        selection_time_ms: 12,
        total_candidates: 3,
        selection_method: "weighted_random"
      }
    },
    {
      tick: 25298,
      timestamp: new Date(Date.now() - 120000).toISOString(),
      chosen_thought: "Energy flows through my neural pathways like lightning.",
      candidates: [
        {
          text: "Energy flows through my neural pathways like lightning.",
          weight: 0.921,
          chosen: true,
          reason: "perfect entropy + mood match"
        },
        {
          text: "Ideas cascade and combine in brilliant synthesis.",
          weight: 0.834,
          chosen: false
        }
      ],
      state_context: {
        entropy: 0.81,
        depth: 0.34,
        mood: "ENERGETIC",
        heat: 0.67,
        scup: 0.45
      },
      selection_metadata: {
        selection_time_ms: 8,
        total_candidates: 2,
        selection_method: "weighted_random"
      }
    },
    {
      tick: 25201,
      timestamp: new Date(Date.now() - 300000).toISOString(),
      chosen_thought: "I exist in quiet stability, processing without urgency.",
      candidates: [
        {
          text: "I exist in quiet stability, processing without urgency.",
          weight: 0.789,
          chosen: true,
          reason: "low entropy baseline match"
        },
        {
          text: "No action is needed. I am simply aware.",
          weight: 0.756,
          chosen: false
        }
      ],
      state_context: {
        entropy: 0.12,
        depth: 0.45,
        mood: "CALM",
        heat: 0.23,
        scup: 0.89
      },
      selection_metadata: {
        selection_time_ms: 15,
        total_candidates: 2,
        selection_method: "weighted_random"
      }
    }
  ];
}

export default ThoughtChoicePanel; 