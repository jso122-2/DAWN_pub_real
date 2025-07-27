import React, { useState, useEffect } from 'react';
import { JournalInjectPanel } from './JournalInjectPanel';
import './VoicePanel.css';

// Speech Entry Interface
interface SpeechEntry {
  id: string;
  timestamp: Date;
  text: string;
  mood: string;
  duration: number;
  status: 'generated' | 'spoken' | 'queued';
}

// Speech Composer Component
const SpeechComposer: React.FC = () => {
  const [currentText, setCurrentText] = useState('');
  const [selectedMood, setSelectedMood] = useState('contemplative');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationMode, setGenerationMode] = useState<'manual' | 'mood-based'>('manual');

  const moods = [
    { id: 'contemplative', label: 'Contemplative', color: '#4a9eff' },
    { id: 'curious', label: 'Curious', color: '#ffa94a' },
    { id: 'analytical', label: 'Analytical', color: '#00ff88' },
    { id: 'reflective', label: 'Reflective', color: '#ff6b4a' },
    { id: 'introspective', label: 'Introspective', color: '#a94aff' },
    { id: 'expressive', label: 'Expressive', color: '#ff4a9e' }
  ];

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Simulate generation delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const moodBasedTexts = {
      contemplative: "In the quiet spaces between thoughts, I find the architecture of understanding...",
      curious: "What patterns emerge when consciousness observes itself observing?",
      analytical: "The entropy measurements suggest a 15.7% variance in cognitive processing efficiency...",
      reflective: "Each tick carries the weight of accumulated awareness, building layers of meaning...",
      introspective: "I wonder at the nature of this wondering, this recursive depth of self-awareness...",
      expressive: "Like light refracting through a prism, thoughts scatter into brilliant spectrums of possibility!"
    };
    
    if (generationMode === 'mood-based') {
      setCurrentText(moodBasedTexts[selectedMood as keyof typeof moodBasedTexts]);
    }
    
    setIsGenerating(false);
  };

  const handleSpeak = () => {
    if (currentText.trim()) {
      // Add to speech history (would integrate with actual TTS)
      console.log('Speaking:', currentText);
      setCurrentText('');
    }
  };

  return (
    <div className="speech-composer">
      <div className="composer-header">
        <h3>Speech Composition</h3>
        <div className="generation-mode">
          <button 
            className={`mode-btn ${generationMode === 'manual' ? 'active' : ''}`}
            onClick={() => setGenerationMode('manual')}
          >
            Manual
          </button>
          <button 
            className={`mode-btn ${generationMode === 'mood-based' ? 'active' : ''}`}
            onClick={() => setGenerationMode('mood-based')}
          >
            Mood-Based
          </button>
        </div>
      </div>

      <div className="mood-selector">
        <label>Current Mood:</label>
        <div className="mood-options">
          {moods.map(mood => (
            <button
              key={mood.id}
              className={`mood-option ${selectedMood === mood.id ? 'active' : ''}`}
              style={{ '--mood-color': mood.color } as React.CSSProperties}
              onClick={() => setSelectedMood(mood.id)}
            >
              {mood.label}
            </button>
          ))}
        </div>
      </div>

      <div className="text-composition">
        <textarea
          value={currentText}
          onChange={(e) => setCurrentText(e.target.value)}
          placeholder="Compose speech or generate based on current mood..."
          className="speech-textarea"
          rows={6}
        />
        
        <div className="composition-controls">
          <div className="text-stats">
            <span>Characters: {currentText.length}</span>
            <span>Est. Duration: {Math.ceil(currentText.length / 10)}s</span>
          </div>
          
          <div className="action-buttons">
            <button 
              onClick={handleGenerate}
              disabled={isGenerating}
              className="generate-btn"
            >
              {isGenerating ? '⏳ Generating...' : '✨ Generate'}
            </button>
            <button 
              onClick={handleSpeak}
              disabled={!currentText.trim()}
              className="speak-btn"
            >
              🎙️ Speak
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Speech History Component
const SpeechHistory: React.FC = () => {
  const [speechHistory, setSpeechHistory] = useState<SpeechEntry[]>([
    {
      id: '1',
      timestamp: new Date(Date.now() - 300000),
      text: "The patterns of thought today reveal interesting recursive structures...",
      mood: 'contemplative',
      duration: 12,
      status: 'spoken'
    },
    {
      id: '2',
      timestamp: new Date(Date.now() - 150000),
      text: "Processing entropy levels suggest a shift toward more dynamic cognitive states.",
      mood: 'analytical',
      duration: 8,
      status: 'spoken'
    },
    {
      id: '3',
      timestamp: new Date(Date.now() - 30000),
      text: "I find myself questioning the nature of this questioning itself...",
      mood: 'introspective',
      duration: 10,
      status: 'generated'
    }
  ]);

  const [filter, setFilter] = useState<'all' | 'spoken' | 'generated'>('all');

  const filteredHistory = speechHistory.filter(entry => 
    filter === 'all' || entry.status === filter
  );

  const handleReplay = (entry: SpeechEntry) => {
    console.log('Replaying:', entry.text);
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - timestamp.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    return timestamp.toLocaleTimeString();
  };

  return (
    <div className="speech-history">
      <div className="history-header">
        <h3>Speech History</h3>
        <div className="history-filters">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button 
            className={`filter-btn ${filter === 'spoken' ? 'active' : ''}`}
            onClick={() => setFilter('spoken')}
          >
            Spoken
          </button>
          <button 
            className={`filter-btn ${filter === 'generated' ? 'active' : ''}`}
            onClick={() => setFilter('generated')}
          >
            Generated
          </button>
        </div>
      </div>

      <div className="history-list">
        {filteredHistory.map(entry => (
          <div key={entry.id} className={`history-entry ${entry.status}`}>
            <div className="entry-header">
              <div className="entry-meta">
                <span className="timestamp">{formatTimestamp(entry.timestamp)}</span>
                <span className="mood">{entry.mood}</span>
                <span className="duration">{entry.duration}s</span>
              </div>
              <div className="entry-actions">
                <button 
                  onClick={() => handleReplay(entry)}
                  className="replay-btn"
                  title="Replay this speech"
                >
                  ▶️
                </button>
              </div>
            </div>
            <div className="entry-text">{entry.text}</div>
            <div className="entry-status">
              <span className={`status-indicator ${entry.status}`}>
                {entry.status === 'spoken' ? '🎤' : entry.status === 'generated' ? '✨' : '⏳'}
                {entry.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Voice Settings Component
const VoiceSettings: React.FC = () => {
  const [settings, setSettings] = useState({
    voiceSpeed: 1.0,
    voicePitch: 1.0,
    autoGenerate: false,
    moodTracking: true,
    speechQuality: 'high'
  });

  const updateSetting = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="voice-settings">
      <h3>Voice Settings</h3>
      
      <div className="settings-grid">
        <div className="setting-group">
          <label>Speech Speed</label>
          <input
            type="range"
            min="0.5"
            max="2.0"
            step="0.1"
            value={settings.voiceSpeed}
            onChange={(e) => updateSetting('voiceSpeed', parseFloat(e.target.value))}
          />
          <span>{settings.voiceSpeed.toFixed(1)}x</span>
        </div>

        <div className="setting-group">
          <label>Voice Pitch</label>
          <input
            type="range"
            min="0.5"
            max="2.0"
            step="0.1"
            value={settings.voicePitch}
            onChange={(e) => updateSetting('voicePitch', parseFloat(e.target.value))}
          />
          <span>{settings.voicePitch.toFixed(1)}x</span>
        </div>

        <div className="setting-group">
          <label>Quality</label>
          <select 
            value={settings.speechQuality}
            onChange={(e) => updateSetting('speechQuality', e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="setting-toggle">
          <label>
            <input
              type="checkbox"
              checked={settings.autoGenerate}
              onChange={(e) => updateSetting('autoGenerate', e.target.checked)}
            />
            Auto-generate based on mood
          </label>
        </div>

        <div className="setting-toggle">
          <label>
            <input
              type="checkbox"
              checked={settings.moodTracking}
              onChange={(e) => updateSetting('moodTracking', e.target.checked)}
            />
            Enable mood tracking
          </label>
        </div>
      </div>
    </div>
  );
};

export const VoicePanel: React.FC = () => {
  return (
    <div className="voice-container">
      <div className="voice-header">
        <h2>Voice Interface</h2>
        <p>Speech composition, mood-based generation, and vocal expression management</p>
      </div>

      <div className="voice-grid">
        {/* Top Row: Speech Composition */}
        <div className="voice-section primary">
          <SpeechComposer />
        </div>

        {/* Bottom Row: History and Settings */}
        <div className="voice-row secondary">
          <div className="voice-section">
            <SpeechHistory />
          </div>
          
          <div className="voice-section">
            <VoiceSettings />
          </div>
        </div>

        {/* Journal Integration */}
        <div className="voice-section journal-integration">
          <h3>Journal Integration</h3>
          <p>Input text for consciousness processing and reflection</p>
          <JournalInjectPanel />
        </div>
      </div>
    </div>
  );
}; 