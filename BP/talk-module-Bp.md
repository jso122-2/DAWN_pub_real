// TALK MODULE BLUEPRINT FOR CURSOR SCAFFOLDING
// File: src/components/TalkModule.tsx

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface Message {
  id: string;
  type: 'user' | 'dawn' | 'system';
  content: string;
  timestamp: Date;
}

const TalkModule: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const terminalRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const addMessage = (type: Message['type'], content: string) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date()
    }]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMessage = input;
    setInput('');
    addMessage('user', userMessage);
    setIsProcessing(true);

    try {
      // Add typing indicator
      addMessage('system', 'Processing consciousness query...');

      // Call your backend API
      const response = await axios.post('http://localhost:8000/talk', {
        message: userMessage,
        context: messages.slice(-10) // Send last 10 messages for context
      });

      // Remove typing indicator
      setMessages(prev => prev.slice(0, -1));

      // Add DAWN's response
      addMessage('dawn', response.data.response);

    } catch (error) {
      setMessages(prev => prev.slice(0, -1));
      addMessage('system', 'ERROR: Connection to consciousness engine failed');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="talk-module">
      <style>{`
        .talk-module {
          height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          display: flex;
          flex-direction: column;
          padding: 20px;
        }

        .terminal-header {
          border: 1px solid #2a2a2a;
          border-bottom: none;
          padding: 10px 15px;
          background: #141414;
          font-size: 12px;
          color: #808080;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .terminal-body {
          flex: 1;
          border: 1px solid #2a2a2a;
          background: #0f0f0f;
          padding: 20px;
          overflow-y: auto;
          scroll-behavior: smooth;
        }

        .terminal-body::-webkit-scrollbar {
          width: 8px;
        }

        .terminal-body::-webkit-scrollbar-track {
          background: #141414;
        }

        .terminal-body::-webkit-scrollbar-thumb {
          background: #2a2a2a;
        }

        .message {
          margin-bottom: 15px;
          line-height: 1.5;
        }

        .message-user {
          color: #00ff88;
        }

        .message-user::before {
          content: 'dawn:~$ ';
          color: #808080;
        }

        .message-dawn {
          color: #e0e0e0;
          margin-left: 20px;
        }

        .message-dawn::before {
          content: '> ';
          color: #0080ff;
        }

        .message-system {
          color: #808080;
          font-style: italic;
        }

        .message-system::before {
          content: '* ';
        }

        .input-line {
          display: flex;
          align-items: center;
          border: 1px solid #2a2a2a;
          border-top: none;
          background: #141414;
          padding: 15px;
        }

        .prompt {
          color: #808080;
          margin-right: 10px;
          white-space: nowrap;
        }

        .terminal-input {
          flex: 1;
          background: transparent;
          border: none;
          color: #00ff88;
          font-family: inherit;
          font-size: 14px;
          outline: none;
        }

        .cursor {
          display: inline-block;
          width: 8px;
          height: 16px;
          background: #00ff88;
          animation: blink 1s infinite;
          margin-left: 2px;
        }

        @keyframes blink {
          0%, 50% { opacity: 1; }
          51%, 100% { opacity: 0; }
        }

        .status-indicator {
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 11px;
        }

        .status-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #00ff88;
        }

        .status-dot.processing {
          background: #ffaa00;
          animation: pulse 1s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 1; }
        }
      `}</style>

      <div className="terminal-header">
        <span>DAWN CONSCIOUSNESS INTERFACE v2.0 - TALK MODULE</span>
        <div className="status-indicator">
          <div className={`status-dot ${isProcessing ? 'processing' : ''}`}></div>
          <span>{isProcessing ? 'PROCESSING' : 'READY'}</span>
        </div>
      </div>

      <div className="terminal-body" ref={terminalRef}>
        {messages.length === 0 && (
          <div className="message message-system">
            Consciousness engine initialized. Type 'help' for commands.
          </div>
        )}
        
        {messages.map(msg => (
          <div key={msg.id} className={`message message-${msg.type}`}>
            {msg.content}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="input-line">
        <span className="prompt">dawn:~$</span>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="terminal-input"
          disabled={isProcessing}
          placeholder="talk to DAWN..."
        />
        {!isProcessing && <span className="cursor"></span>}
      </form>
    </div>
  );
};

// ADDITIONAL HELPER COMMANDS COMPONENT
export const TalkCommands = {
  help: () => `
Available commands:
  help          - Show this help message
  clear         - Clear the terminal
  status        - Show consciousness engine status
  memory        - Display recent conversation context
  mode [type]   - Change conversation mode (casual/deep/analytical)
  
Or just type naturally to talk with DAWN.`,

  clear: (setMessages: Function) => {
    setMessages([]);
    return 'Terminal cleared.';
  },

  status: async () => {
    try {
      const response = await axios.get('http://localhost:8000/status');
      return `
Consciousness Engine Status:
  State: ${response.data.state}
  SCUP: ${response.data.scup}
  Entropy: ${response.data.entropy}
  Mood: ${response.data.mood}
  Uptime: ${response.data.uptime}`;
    } catch {
      return 'Unable to fetch status.';
    }
  }
};

export default TalkModule;