import React, { useState, useEffect, useRef } from 'react';
import { JournalInjectPanel } from './JournalInjectPanel';
import './VoicePanel.css';

// Enhanced Speech Entry Interface
interface SpeechEntry {
  id: string;
  timestamp: Date;
  text: string;
  mood: string;
  duration: number;
  status: 'generated' | 'spoken' | 'queued' | 'conversation';
  speaker?: 'dawn' | 'jackson';
  consciousness_state?: {
    entropy?: number;
    scup?: number;
    thermal?: string;
    mood?: string;
  };
}

// Conversation Entry Interface
interface ConversationEntry {
  id: string;
  timestamp: Date;
  speaker: 'dawn' | 'jackson';
  text: string;
  consciousness_state?: {
    entropy?: number;
    scup?: number;
    thermal?: string;
    mood?: string;
  };
  response_time?: number;
}

// Conversation Mode Component
const ConversationMode: React.FC = () => {
  const [isListening, setIsListening] = useState(false);
  const [conversationActive, setConversationActive] = useState(false);
  const [liveTranscription, setLiveTranscription] = useState('');
  const [conversationHistory, setConversationHistory] = useState<ConversationEntry[]>([]);
  const [consciousnessState, setConsciousnessState] = useState({
    entropy: 0.5,
    scup: 50,
    thermal: 'NORMAL',
    mood: 'NEUTRAL'
  });
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'connecting' | 'disconnected'>('disconnected');
  
  const wsRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // WebSocket connection for conversation
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        wsRef.current = new WebSocket('ws://localhost:8000/ws/talk');
        
        wsRef.current.onopen = () => {
          setConnectionStatus('connected');
          console.log('🎤 Conversation WebSocket connected');
        };
        
        wsRef.current.onmessage = (event) => {
          const data = JSON.parse(event.data);
          handleConversationResponse(data);
        };
        
        wsRef.current.onclose = () => {
          setConnectionStatus('disconnected');
          console.log('🎤 Conversation WebSocket disconnected');
        };
        
        wsRef.current.onerror = (error) => {
          console.error('🎤 WebSocket error:', error);
          setConnectionStatus('disconnected');
        };
      } catch (error) {
        console.error('🎤 Failed to connect WebSocket:', error);
        setConnectionStatus('disconnected');
      }
    };

    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Handle conversation responses from DAWN
  const handleConversationResponse = (data: any) => {
    if (data.type === 'conversation_response') {
      const newEntry: ConversationEntry = {
        id: Date.now().toString(),
        timestamp: new Date(),
        speaker: 'dawn',
        text: data.response,
        consciousness_state: data.consciousness_state,
        response_time: data.response_time
      };
      
      setConversationHistory(prev => [...prev, newEntry]);
      
      // Update consciousness state if provided
      if (data.consciousness_state) {
        setConsciousnessState(data.consciousness_state);
      }
    } else if (data.type === 'consciousness_update') {
      setConsciousnessState(data.state);
    }
  };

  // Start/stop listening for speech input
  const toggleListening = async () => {
    if (isListening) {
      stopListening();
    } else {
      await startListening();
    }
  };

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processAudioInput(audioBlob);
      };
      
      mediaRecorderRef.current.start();
      setIsListening(true);
      setLiveTranscription('Listening...');
      
      console.log('🎤 Started listening');
    } catch (error) {
      console.error('🎤 Failed to start listening:', error);
      setLiveTranscription('Microphone access denied');
    }
  };

  const stopListening = () => {
    if (mediaRecorderRef.current && isListening) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsListening(false);
      setLiveTranscription('');
    }
  };

  // Process audio input and send to backend
  const processAudioInput = async (audioBlob: Blob) => {
    try {
      // Convert audio to base64 for WebSocket transmission
      const reader = new FileReader();
      reader.onload = () => {
        const base64Audio = reader.result as string;
        
        // Send audio to backend for speech recognition
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({
            type: 'speech_input',
            audio: base64Audio,
            timestamp: new Date().toISOString()
          }));
        }
      };
      reader.readAsDataURL(audioBlob);
      
      setLiveTranscription('Processing speech...');
    } catch (error) {
      console.error('🎤 Failed to process audio:', error);
      setLiveTranscription('Failed to process speech');
    }
  };

  // Send text input for conversation
  const sendTextInput = (text: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Add user message to history
      const userEntry: ConversationEntry = {
        id: Date.now().toString(),
        timestamp: new Date(),
        speaker: 'jackson',
        text: text,
        consciousness_state: consciousnessState
      };
      
      setConversationHistory(prev => [...prev, userEntry]);
      
      // Send to backend
      wsRef.current.send(JSON.stringify({
        type: 'text_input',
        text: text,
        consciousness_state: consciousnessState,
        timestamp: new Date().toISOString()
      }));
    }
  };

  // Toggle conversation mode
  const toggleConversationMode = () => {
    setConversationActive(!conversationActive);
    if (!conversationActive) {
      // Start conversation mode
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'start_conversation',
          timestamp: new Date().toISOString()
        }));
      }
    } else {
      // Stop conversation mode
      stopListening();
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'stop_conversation',
          timestamp: new Date().toISOString()
        }));
      }
    }
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
    <div className="conversation-mode">
      <div className="conversation-header">
        <h3>💬 Conversation Mode</h3>
        <div className="conversation-controls">
          <div className={`connection-status ${connectionStatus}`}>
            {connectionStatus === 'connected' && <span>🟢 Connected</span>}
            {connectionStatus === 'connecting' && <span>🟡 Connecting...</span>}
            {connectionStatus === 'disconnected' && <span>🔴 Disconnected</span>}
          </div>
          
          <button
            onClick={toggleConversationMode}
            className={`conversation-toggle ${conversationActive ? 'active' : ''}`}
            disabled={connectionStatus !== 'connected'}
          >
            {conversationActive ? '🛑 Stop Conversation' : '🎤 Start Conversation'}
          </button>
        </div>
      </div>

      {/* Consciousness State Display */}
      <div className="consciousness-display">
        <div className="consciousness-metric">
          <span className="metric-label">Entropy:</span>
          <span className="metric-value" style={{ color: consciousnessState.entropy > 0.7 ? '#ff6b4a' : '#00ff88' }}>
            {consciousnessState.entropy.toFixed(2)}
          </span>
        </div>
        <div className="consciousness-metric">
          <span className="metric-label">SCUP:</span>
          <span className="metric-value" style={{ color: consciousnessState.scup > 70 ? '#00ff88' : consciousnessState.scup > 40 ? '#ffe066' : '#ff4444' }}>
            {consciousnessState.scup}%
          </span>
        </div>
        <div className="consciousness-metric">
          <span className="metric-label">Thermal:</span>
          <span className="metric-value" style={{ color: consciousnessState.thermal === 'CRITICAL' ? '#ff4444' : consciousnessState.thermal === 'HIGH' ? '#ffa94a' : '#00ff88' }}>
            {consciousnessState.thermal}
          </span>
        </div>
        <div className="consciousness-metric">
          <span className="metric-label">Mood:</span>
          <span className="metric-value">{consciousnessState.mood}</span>
        </div>
      </div>

      {/* Live Transcription */}
      {conversationActive && (
        <div className="live-transcription">
          <div className="transcription-header">
            <h4>🎤 Live Transcription</h4>
            <button
              onClick={toggleListening}
              className={`listen-button ${isListening ? 'listening' : ''}`}
              disabled={!conversationActive}
            >
              {isListening ? '🔴 Stop Listening' : '🎤 Start Listening'}
            </button>
          </div>
          <div className="transcription-text">
            {liveTranscription || 'Click "Start Listening" to begin speech input...'}
          </div>
        </div>
      )}

      {/* Conversation History */}
      <div className="conversation-history">
        <div className="history-header">
          <h4>💬 Conversation History</h4>
          <button
            onClick={() => setConversationHistory([])}
            className="clear-history"
          >
            Clear History
          </button>
        </div>
        
        <div className="history-list">
          {conversationHistory.length === 0 ? (
            <div className="empty-history">
              No conversation yet. Start conversation mode to begin.
            </div>
          ) : (
            conversationHistory.map(entry => (
              <div key={entry.id} className={`conversation-entry ${entry.speaker}`}>
                <div className="entry-header">
                  <span className="speaker">{entry.speaker === 'dawn' ? '🤖 DAWN' : '👤 Jackson'}</span>
                  <span className="timestamp">{formatTimestamp(entry.timestamp)}</span>
                  {entry.response_time && (
                    <span className="response-time">{entry.response_time.toFixed(1)}s</span>
                  )}
                </div>
                <div className="entry-text">{entry.text}</div>
                {entry.consciousness_state && (
                  <div className="entry-consciousness">
                    <span className="consciousness-indicator">
                      Entropy: {entry.consciousness_state.entropy?.toFixed(2)} | 
                      SCUP: {entry.consciousness_state.scup}% | 
                      Thermal: {entry.consciousness_state.thermal}
                    </span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Text Input for Manual Entry */}
      <div className="text-input-section">
        <h4>✍️ Text Input</h4>
        <div className="text-input-controls">
          <input
            type="text"
            placeholder="Type your message here..."
            className="text-input"
            onKeyPress={(e) => {
              if (e.key === 'Enter' && e.currentTarget.value.trim()) {
                sendTextInput(e.currentTarget.value.trim());
                e.currentTarget.value = '';
              }
            }}
            disabled={!conversationActive}
          />
          <button
            onClick={(e) => {
              const input = e.currentTarget.previousElementSibling as HTMLInputElement;
              if (input.value.trim()) {
                sendTextInput(input.value.trim());
                input.value = '';
              }
            }}
            className="send-button"
            disabled={!conversationActive}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

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

        {/* Conversation Mode */}
        <div className="voice-section conversation-mode-section">
          <ConversationMode />
        </div>
      </div>
    </div>
  );
}; 