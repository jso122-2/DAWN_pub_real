import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'dawn';
  timestamp: number;
  metadata?: {
    resonance_strength?: number;
    selected_glyph_id?: string;
    transformation_path?: any[];
    consciousness_influence?: {
      scup: number;
      entropy: number;
      mood: string;
      tick: number;
    };
    active_chains?: string[];
    processing_time?: number;
    echo_id?: string;
  };
}

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  tick: number;
  active_modules: string[];
}

const TalkModule: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [consciousnessState, setConsciousnessState] = useState<ConsciousnessState | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  // Connect to WebSocket for consciousness state updates
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/consciousness/stream');
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log('Connected to consciousness stream');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setConsciousnessState(data);
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from consciousness stream');
    };

    return () => {
      ws.close();
    };
  }, []);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getMoodColor = (mood: string) => {
    const moodColors: { [key: string]: string } = {
      'DREAMING': '#8844ff',
      'FOCUSED': '#00ff88',
      'CONTEMPLATIVE': '#0080ff',
      'HYPERACTIVE': '#ff0040',
      'TRANSCENDENT': '#00ffff'
    };
    return moodColors[mood] || '#808080';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await axios.post('http://localhost:8000/talk/process', {
        input: input,
        consciousness_state: consciousnessState
      });

      const dawnMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        sender: 'dawn',
        timestamp: Date.now(),
        metadata: {
          resonance_strength: response.data.resonance_strength,
          selected_glyph_id: response.data.selected_glyph_id,
          transformation_path: response.data.transformation_path,
          consciousness_influence: response.data.consciousness_influence,
          active_chains: response.data.active_chains,
          processing_time: response.data.processing_time,
          echo_id: response.data.echo_id
        }
      };

      setMessages(prev => [...prev, dawnMessage]);
    } catch (error) {
      console.error('Error processing message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Error: Unable to process message. Please try again.',
        sender: 'dawn',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="talk-module">
      <style>{`
        .talk-module {
          height: 100%;
          display: flex;
          flex-direction: column;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
        }

        .header {
          padding: 10px;
          background: #141414;
          border-bottom: 1px solid #2a2a2a;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .title {
          font-size: 14px;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .connection-status {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
          color: #808080;
        }

        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: ${isConnected ? '#00ff88' : '#ff0040'};
        }

        .messages {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .message {
          max-width: 80%;
          padding: 15px;
          border-radius: 4px;
          position: relative;
        }

        .message.user {
          align-self: flex-end;
          background: #1a1a1a;
          border: 1px solid #2a2a2a;
        }

        .message.dawn {
          align-self: flex-start;
          background: #141414;
          border: 1px solid #2a2a2a;
        }

        .message-content {
          font-size: 14px;
          line-height: 1.5;
          white-space: pre-wrap;
        }

        .message-meta {
          margin-top: 8px;
          font-size: 11px;
          color: #808080;
          display: flex;
          gap: 12px;
        }

        .meta-item {
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .meta-label {
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .meta-value {
          color: #e0e0e0;
        }

        .mood-indicator {
          display: inline-block;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          margin-right: 4px;
        }

        .input-area {
          padding: 20px;
          background: #141414;
          border-top: 1px solid #2a2a2a;
        }

        .input-form {
          display: flex;
          gap: 10px;
        }

        .input-field {
          flex: 1;
          background: #0a0a0a;
          border: 1px solid #2a2a2a;
          color: #e0e0e0;
          padding: 10px;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          font-size: 14px;
          resize: none;
          min-height: 40px;
          max-height: 120px;
        }

        .input-field:focus {
          outline: none;
          border-color: #00ff88;
        }

        .send-button {
          background: #00ff88;
          color: #0a0a0a;
          border: none;
          padding: 10px 20px;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          font-size: 14px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .send-button:hover {
          background: #00cc6a;
        }

        .send-button:disabled {
          background: #2a2a2a;
          color: #808080;
          cursor: not-allowed;
        }

        .processing-indicator {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
          color: #808080;
          margin-top: 8px;
        }

        .processing-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #00ff88;
          animation: pulse 1s infinite;
        }

        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 0.5; }
          50% { transform: scale(1.2); opacity: 1; }
        }
      `}</style>

      <div className="header">
        <div className="title">DAWN TALK INTERFACE</div>
        <div className="connection-status">
          <div className="status-dot"></div>
          <span>{isConnected ? 'CONNECTED' : 'DISCONNECTED'}</span>
        </div>
      </div>

      <div className="messages">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-content">{message.text}</div>
            {message.metadata && (
              <div className="message-meta">
                {message.metadata.consciousness_influence && (
                  <div className="meta-item">
                    <span className="meta-label">MOOD:</span>
                    <span className="meta-value">
                      <span 
                        className="mood-indicator"
                        style={{ background: getMoodColor(message.metadata.consciousness_influence.mood) }}
                      />
                      {message.metadata.consciousness_influence.mood}
                    </span>
                  </div>
                )}
                {message.metadata.resonance_strength && (
                  <div className="meta-item">
                    <span className="meta-label">RESONANCE:</span>
                    <span className="meta-value">
                      {(message.metadata.resonance_strength * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
                {message.metadata.processing_time && (
                  <div className="meta-item">
                    <span className="meta-label">PROCESS:</span>
                    <span className="meta-value">
                      {message.metadata.processing_time.toFixed(2)}s
                    </span>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <form className="input-form" onSubmit={handleSubmit}>
          <textarea
            className="input-field"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isProcessing}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={isProcessing || !input.trim()}
          >
            SEND
          </button>
        </form>
        {isProcessing && (
          <div className="processing-indicator">
            <div className="processing-dot"></div>
            <span>Processing through consciousness...</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default TalkModule; 