import React, { useState, useEffect, useRef } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import 'xterm/css/xterm.css';
import { wsService } from '../../utils/websocketCompatibility';
import { TerminalProps } from './types';
import './Terminal.css';

interface TerminalMessage {
  message: string;
  type?: string;
  timestamp?: number;
}

// Debug function to test backend connectivity
const testBackend = async () => {
  try {
    // Test HTTP endpoint
    const response = await fetch('http://localhost:8000/health');
    console.log('Backend HTTP status:', response.status);
    
    // Test direct WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onopen = () => {
      console.log('✅ Backend WebSocket is running!');
      ws.close();
    };
    ws.onerror = (e) => {
      console.error('❌ Backend WebSocket error:', e);
      console.log('Make sure your Python backend is running on port 8000');
    };
  } catch (error) {
    console.error('Backend test failed:', error);
  }
};

export const Terminal: React.FC<TerminalProps> = () => {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);
  const terminal = useRef<XTerm | null>(null);
  const connectionPromiseRef = useRef<Promise<void> | null>(null);

  // Initialize terminal
  useEffect(() => {
    if (terminalRef.current && !terminal.current) {
      // Initialize terminal
      terminal.current = new XTerm({
        cursorBlink: true,
        fontSize: 14,
        fontFamily: 'JetBrains Mono, monospace',
        theme: {
          background: '#000000',
          foreground: '#cacaca',
          cursor: '#cacaca',
          black: '#000000',
          red: '#ff5555',
          green: '#50fa7b',
          yellow: '#f1fa8c',
          blue: '#bd93f9',
          magenta: '#ff79c6',
          cyan: '#8be9fd',
          white: '#f8f8f2',
          brightBlack: '#6272a4',
          brightRed: '#ff6e67',
          brightGreen: '#5af78e',
          brightYellow: '#f4f99d',
          brightBlue: '#caa9fa',
          brightMagenta: '#ff92d0',
          brightCyan: '#9aedfe',
          brightWhite: '#f8f8f2',
        },
      });

      // Add addons
      const fitAddon = new FitAddon();
      const webLinksAddon = new WebLinksAddon();
      terminal.current.loadAddon(fitAddon);
      terminal.current.loadAddon(webLinksAddon);

      // Open terminal
      terminal.current.open(terminalRef.current);
      fitAddon.fit();

      // Welcome message
      terminal.current.writeln('\x1b[1;36mDAWN - Consciousness Engine Interface\x1b[0m');
      terminal.current.writeln('\x1b[90mWebSocket status will appear below.\x1b[0m\n');

      // Handle window resize
      const handleResize = () => {
        fitAddon.fit();
      };
      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        terminal.current?.dispose();
      };
    }
  }, []);

  // Connect to WebSocket on mount
  useEffect(() => {
    let mounted = true;

    const initConnection = async () => {
      if (!mounted) return;
      
      console.log('Terminal: Initializing connection');
      try {
        // Only connect if not already connected
        if (!wsService.isConnected && !connectionPromiseRef.current) {
          connectionPromiseRef.current = wsService.connect();
          await connectionPromiseRef.current;
          connectionPromiseRef.current = null;
        }
      } catch (error) {
        console.error('Terminal: Connection failed:', error);
        connectionPromiseRef.current = null;
      }
    };

    initConnection();

    return () => {
      mounted = false;
      console.log('Terminal: Cleanup');
      // Don't disconnect on unmount in development
      if (!import.meta.env.DEV) {
        wsService.disconnect();
      }
    };
  }, []);

  // Test backend connectivity on mount
  useEffect(() => {
    testBackend();
  }, []);

  // Handle backend messages
  useEffect(() => {
    if (!terminal.current) return;

    const handleBackendMessage = (payload: any) => {
      terminal.current?.writeln(`\x1b[32m[Backend]\x1b[0m ${typeof payload === 'string' ? payload : JSON.stringify(payload)}`);
    };

    const handleTerminalOutput = (data: TerminalMessage) => {
      setOutput(prev => [...prev, data.message]);
      terminal.current?.writeln(`\x1b[33m[Output]\x1b[0m ${data.message}`);
    };

    const handleError = (error: any) => {
      terminal.current?.writeln(`\x1b[31m[Error]\x1b[0m ${error.message || 'An error occurred'}`);
    };

    // Add message handlers
    wsService.on(handleBackendMessage);
    wsService.on(handleTerminalOutput);
    wsService.on(handleError);

    // Cleanup
    return () => {
      wsService.removeMessageHandler(handleBackendMessage);
      wsService.removeMessageHandler(handleTerminalOutput);
      wsService.removeMessageHandler(handleError);
    };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      const command = input.trim();
      setOutput(prev => [...prev, `> ${command}`]);
      terminal.current?.writeln(`\x1b[36m[Command]\x1b[0m ${command}`);
      wsService.send({ type: 'command', data: command });
      setInput('');
    }
  };

  return (
    <div className="terminal-wrapper">
      <div ref={terminalRef} className="terminal-container">
        <div className="terminal-output">
          {output.map((line, i) => (
            <div key={i} className="terminal-line">{line}</div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="terminal-input">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={wsService.isConnected ? "Enter command..." : "Connecting..."}
            disabled={!wsService.isConnected}
          />
        </form>
      </div>
      <div className="terminal-status">
        {wsService.isConnected ? (
          <span className="status-connected">Connected</span>
        ) : (
          <span className="status-disconnected">Disconnected</span>
        )}
      </div>
    </div>
  );
}; 