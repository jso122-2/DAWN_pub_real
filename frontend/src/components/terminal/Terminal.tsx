import React, { useEffect, useRef } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import 'xterm/css/xterm.css';
import { useWebSocket } from '../../hooks/useWebSocket';
import { Command } from './types';
import './Terminal.css';

interface TerminalProps {
  commands?: Command[];
}

export const Terminal: React.FC<TerminalProps> = ({ commands }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const terminal = useRef<XTerm | null>(null);
  const { connected, connect, on } = useWebSocket();

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
    connect();
  }, [connect]);

  // Print any backend messages to the terminal
  useEffect(() => {
    if (!terminal.current) return;
    const handler = (payload: any) => {
      terminal.current?.writeln(`\x1b[32m[Backend]\x1b[0m ${typeof payload === 'string' ? payload : JSON.stringify(payload)}`);
    };
    on('message', handler);
    return () => {
      // No off() method for now, but could be added for cleanup
    };
  }, [on]);

  return (
    <div className="terminal-wrapper">
      <div ref={terminalRef} className="terminal-container" />
      <div className="terminal-status">
        {connected ? (
          <span className="status-connected">Connected</span>
        ) : (
          <span className="status-disconnected">Disconnected</span>
        )}
      </div>
    </div>
  );
}; 