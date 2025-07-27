import React, { useState, useEffect, useRef } from 'react';
import './LastSpokenPanel.css';

interface SpokenEntry {
  id: string;
  timestamp: string;
  tick: string;
  spokenText: string;
  parsedTime: Date;
  entropy?: number;
  confidence?: number;
  riskLevel: 'low' | 'normal' | 'high' | 'critical';
}

interface LastSpokenPanelProps {
  className?: string;
  maxEntries?: number;
  updateInterval?: number;
}

export const LastSpokenPanel: React.FC<LastSpokenPanelProps> = ({
  className = '',
  maxEntries = 5,
  updateInterval = 2000
}) => {
  const [spokenEntries, setSpokenEntries] = useState<SpokenEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isLive, setIsLive] = useState(true);
  const intervalRef = useRef<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Risk words that trigger highlighting
  const riskWords = [
    'drift', 'uncertainty', 'cascade', 'entropy', 'chaos', 'critical', 
    'unstable', 'disruption', 'anomaly', 'error', 'failure', 'warning',
    'alert', 'danger', 'risk', 'concern', 'issue', 'problem'
  ];

  // Parse log line format: 2025-07-26T22:31:30 | REFLECTION: Custom thought: Memory cascade triggered...
  const parseLogLine = (line: string): SpokenEntry | null => {
    try {
      const match = line.match(/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s*\|\s*REFLECTION:\s*(.+)$/);
      if (!match) return null;

      const [, timestamp, spokenText] = match;
      const parsedTime = new Date(timestamp);
      
      // Extract tick number if present in the spoken text
      const tickMatch = spokenText.match(/tick[:\s]*(\d+)/i);
      const tick = tickMatch ? tickMatch[1] : '';

      // Calculate risk level based on risk words
      const lowerText = spokenText.toLowerCase();
      const riskWordCount = riskWords.filter(word => lowerText.includes(word)).length;
      
      let riskLevel: SpokenEntry['riskLevel'] = 'low';
      if (riskWordCount >= 3) riskLevel = 'critical';
      else if (riskWordCount >= 2) riskLevel = 'high';
      else if (riskWordCount >= 1) riskLevel = 'normal';

      // Extract entropy and confidence if present
      const entropyMatch = spokenText.match(/entropy[:\s]*([\d.]+)/i);
      const confidenceMatch = spokenText.match(/confidence[:\s]*([\d.]+)/i);

      const entry: SpokenEntry = {
        id: `${timestamp}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp,
        tick,
        spokenText,
        parsedTime,
        entropy: entropyMatch ? parseFloat(entropyMatch[1]) : undefined,
        confidence: confidenceMatch ? parseFloat(confidenceMatch[1]) : undefined,
        riskLevel
      };

      return entry;
    } catch (e) {
      console.warn('Failed to parse log line:', line, e);
      return null;
    }
  };

  // Highlight risk words in spoken text
  const highlightRiskWords = (text: string): JSX.Element => {
    let highlightedText = text;
    
    riskWords.forEach(word => {
      const regex = new RegExp(`\\b(${word})\\b`, 'gi');
      highlightedText = highlightedText.replace(regex, `<span class="risk-word">$1</span>`);
    });

    return <span dangerouslySetInnerHTML={{ __html: highlightedText }} />;
  };

  // Load spoken reflections from log file
  const loadSpokenReflections = async () => {
    try {
      // In a real implementation, this would read from the actual log file
      // For now, we'll simulate the data structure
      const logPath = '/root/DAWN_Vault/Tick_engine/Tick_engine/runtime/logs/spoken_trace.log';
      
      // Simulate reading the log file (replace with actual file reading in production)
      const mockEntries: SpokenEntry[] = [
        {
          id: 'spoken_1',
          timestamp: '2025-01-14T22:31:30',
          tick: '4527',
          spokenText: 'Memory cascade triggered: drift patterns showing increased entropy levels',
          parsedTime: new Date('2025-01-14T22:31:30'),
          entropy: 0.85,
          confidence: 0.32,
          riskLevel: 'critical'
        },
        {
          id: 'spoken_2', 
          timestamp: '2025-01-14T22:30:15',
          tick: '4521',
          spokenText: 'Consciousness depth stabilizing after rebloom integration pulse',
          parsedTime: new Date('2025-01-14T22:30:15'),
          entropy: 0.62,
          confidence: 0.78,
          riskLevel: 'normal'
        },
        {
          id: 'spoken_3',
          timestamp: '2025-01-14T22:29:42',
          tick: '4518',
          spokenText: 'Observing semantic alignment fluctuations in cognitive substrate',
          parsedTime: new Date('2025-01-14T22:29:42'),
          entropy: 0.45,
          confidence: 0.85,
          riskLevel: 'low'
        },
        {
          id: 'spoken_4',
          timestamp: '2025-01-14T22:28:33',
          tick: '4512',
          spokenText: 'Warning: uncertainty threshold exceeded in metacognitive processes',
          parsedTime: new Date('2025-01-14T22:28:33'),
          entropy: 0.91,
          confidence: 0.28,
          riskLevel: 'high'
        },
        {
          id: 'spoken_5',
          timestamp: '2025-01-14T22:27:18',
          tick: '4506',
          spokenText: 'Reflection initiated: analyzing thought pattern coherence metrics',
          parsedTime: new Date('2025-01-14T22:27:18'),
          entropy: 0.38,
          confidence: 0.92,
          riskLevel: 'low'
        }
      ];

      // Sort by timestamp (newest first) and limit to maxEntries
      const sortedEntries = mockEntries
        .sort((a, b) => b.parsedTime.getTime() - a.parsedTime.getTime())
        .slice(0, maxEntries);

      setSpokenEntries(sortedEntries);
      setError(null);
      setIsLoading(false);

    } catch (err) {
      console.error('Failed to load spoken reflections:', err);
      setError(`Failed to load spoken trace log: ${err}`);
      setIsLoading(false);
    }
  };

  // Format time for display
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // Format elapsed time since spoken
  const formatElapsed = (date: Date): string => {
    const now = new Date();
    const elapsed = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (elapsed < 60) return `${elapsed}s ago`;
    if (elapsed < 3600) return `${Math.floor(elapsed / 60)}m ago`;
    return `${Math.floor(elapsed / 3600)}h ago`;
  };

  // Toggle live updates
  const toggleLive = () => {
    setIsLive(!isLive);
    if (!isLive) {
      loadSpokenReflections();
    }
  };

  // Clear all entries
  const clearEntries = () => {
    setSpokenEntries([]);
  };

  // Setup polling
  useEffect(() => {
    loadSpokenReflections();

    if (isLive) {
      intervalRef.current = setInterval(loadSpokenReflections, updateInterval);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isLive, updateInterval]);

  // Scroll to top when new entries arrive
  useEffect(() => {
    if (containerRef.current && spokenEntries.length > 0) {
      containerRef.current.scrollTop = 0;
    }
  }, [spokenEntries]);

  if (isLoading) {
    return (
      <div className={`last-spoken-panel loading ${className}`}>
        <div className="loading-indicator">
          <div className="pulse-dot"></div>
          <span>Loading voice reflections...</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`last-spoken-panel ${className}`}>
      {/* Header */}
      <div className="spoken-header">
        <div className="spoken-title">
          <span className="title-icon">🗣️</span>
          <span className="title-text">Last Spoken</span>
          <span className="entry-count">{spokenEntries.length}</span>
        </div>
        
        <div className="spoken-controls">
          <button 
            className={`control-btn live-btn ${isLive ? 'active' : ''}`}
            onClick={toggleLive}
            title={isLive ? 'Pause live updates' : 'Resume live updates'}
          >
            {isLive ? '⏸️' : '▶️'}
          </button>
          <button 
            className="control-btn clear-btn"
            onClick={clearEntries}
            title="Clear all entries"
          >
            🗑️
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="error-state">
          <div className="error-icon">⚠️</div>
          <div className="error-text">{error}</div>
        </div>
      )}

      {/* Spoken Entries Container */}
      <div className="spoken-container" ref={containerRef}>
        {spokenEntries.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤐</div>
            <div className="empty-text">No voice reflections</div>
            <div className="empty-subtext">Waiting for DAWN to speak...</div>
          </div>
        ) : (
          <div className="spoken-entries">
            {spokenEntries.map((entry, index) => (
              <div 
                key={entry.id}
                className={`spoken-entry risk-${entry.riskLevel} ${
                  entry.entropy && entry.entropy > 0.8 ? 'high-entropy' : ''
                } ${
                  entry.confidence && entry.confidence < 0.4 ? 'low-confidence' : ''
                }`}
                style={{
                  animationDelay: `${index * 0.1}s`
                }}
              >
                {/* Entry Header */}
                <div className="entry-line">
                  <span className="entry-tick">T{entry.tick}</span>
                  <span className="entry-time">{formatTime(entry.parsedTime)}</span>
                  <span className="entry-elapsed">({formatElapsed(entry.parsedTime)})</span>
                  <span className="entry-voice-icon">🧠</span>
                </div>

                {/* Spoken Text */}
                <div className="entry-spoken-text">
                  {highlightRiskWords(entry.spokenText)}
                </div>

                {/* Entry Metadata */}
                <div className="entry-metadata">
                  {entry.entropy !== undefined && (
                    <div className="meta-item entropy">
                      <span>🌀</span>
                      <span>{entry.entropy.toFixed(2)}</span>
                    </div>
                  )}
                  {entry.confidence !== undefined && (
                    <div className="meta-item confidence">
                      <span>🎯</span>
                      <span>{(entry.confidence * 100).toFixed(0)}%</span>
                    </div>
                  )}
                  <div className="meta-item risk">
                    <span>⚠️</span>
                    <span className={`risk-${entry.riskLevel}`}>{entry.riskLevel.toUpperCase()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="spoken-footer">
        <div className="status-info">
          <div className="status-item">
            <div className={`status-dot ${isLive ? 'live' : 'paused'}`}></div>
            <span>{isLive ? 'Live' : 'Paused'}</span>
          </div>
          <div className="status-item">
            <span>Updates every {updateInterval / 1000}s</span>
          </div>
          <div className="status-item">
            <span>Voice Echo Archive</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LastSpokenPanel; 