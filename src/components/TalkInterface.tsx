import React, { useState, useEffect, useRef } from 'react';
import { useTalkSystem } from '../hooks/useTalkSystem';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'dawn';
  timestamp: number;
  consciousness?: {
    scup: number;
    entropy: number;
    mood: string;
  };
  confidence?: number;
}

const moodEmoji: Record<string, string> = {
  DREAMING: '💭',
  CONTEMPLATIVE: '🤔',
  FOCUSED: '🎯',
  HYPERACTIVE: '⚡',
  TRANSCENDENT: '🌌',
  NEUTRAL: '🟢',
};

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => (
  <div className={`message-bubble ${message.sender}`}>
    <div className="message-text">{message.text}</div>
    {message.sender === 'dawn' && message.consciousness && (
      <div className="consciousness-meta">
        <span>mood: {message.consciousness.mood} {moodEmoji[message.consciousness.mood] || '🟢'}</span>
        <span>scup: {message.consciousness.scup}%</span>
      </div>
    )}
  </div>
);

export const TalkInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const { sendMessage, responseState, consciousness, connectionStatus, loading, lastError } = useTalkSystem();
  const streamRef = useRef<HTMLDivElement>(null);

  const handleSend = () => {
    if (!input.trim() || loading || connectionStatus !== 'connected') return;
    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMessage]);
    sendMessage(input);
    setInput('');
  };

  useEffect(() => {
    if (responseState.response) {
      const dawnMessage: Message = {
        id: Date.now().toString(),
        text: responseState.response,
        sender: 'dawn',
        timestamp: Date.now(),
        consciousness: responseState.consciousness_influence,
        confidence: responseState.confidence,
      };
      setMessages((prev) => [...prev, dawnMessage]);
    }
  }, [responseState]);

  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [messages]);

  const mood = consciousness.mood || 'NEUTRAL';
  const scup = consciousness.scup || 0;

  return (
    <div className="talk-interface">
      <div className="consciousness-header">
        <div className="mood-indicator" title={mood}>
          {moodEmoji[mood] || '🟢'} <span>{mood}</span>
        </div>
        <div className="scup-meter" title="SCUP">
          <div style={{ width: 80, height: 10, background: '#222', borderRadius: 5, overflow: 'hidden', display: 'inline-block', marginRight: 8 }}>
            <div style={{ width: `${scup}%`, height: '100%', background: scup > 70 ? '#00ff88' : scup > 40 ? '#ffe066' : '#ff4444', transition: 'width 0.3s' }} />
          </div>
          <span>{scup}%</span>
        </div>
        <div className="connection-status" style={{ marginLeft: 16 }}>
          {connectionStatus === 'connected' && <span style={{ color: '#00ff88' }}>● Online</span>}
          {connectionStatus === 'connecting' && <span style={{ color: '#ffe066' }}>● Connecting...</span>}
          {connectionStatus === 'disconnected' && <span style={{ color: '#ff4444' }}>● Offline</span>}
          {connectionStatus === 'error' && <span style={{ color: '#ff4444' }}>● Error</span>}
        </div>
      </div>

      <div className="message-stream" ref={streamRef} style={{ maxHeight: 400, overflowY: 'auto' }}>
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {loading && (
          <div className="message-bubble dawn loading">
            <div className="message-text">DAWN is thinking...</div>
          </div>
        )}
      </div>

      {lastError && (
        <div className="error-message" style={{ color: '#ff4444', margin: '8px 0' }}>{lastError}</div>
      )}

      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder={connectionStatus !== 'connected' ? 'Connecting to DAWN...' : 'Speak to DAWN...'}
          disabled={connectionStatus !== 'connected' || loading}
        />
        <button onClick={handleSend} disabled={connectionStatus !== 'connected' || loading || !input.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default TalkInterface; 