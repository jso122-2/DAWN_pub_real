import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { SearchAddon } from 'xterm-addon-search';
import 'xterm/css/xterm.css';

// Types for Electron/Tauri IPC
interface ShellAPI {
  spawn: (shell?: string) => Promise<number>;
  write: (pid: number, data: string) => void;
  resize: (pid: number, cols: number, rows: number) => void;
  kill: (pid: number) => void;
  onData: (pid: number, callback: (data: string) => void) => void;
  onExit: (pid: number, callback: (code: number) => void) => void;
  logToFile: (message: string) => void;
}

interface ClaudeCommand {
  command: string;
  explanation?: string;
  risk_level?: 'safe' | 'moderate' | 'dangerous';
}

declare global {
  interface Window {
    shellAPI: ShellAPI;
  }
}

const NeuroShellOverlay: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  const [lastCommandStatus, setLastCommandStatus] = useState<'success' | 'error' | null>(null);
  const terminalRef = useRef<HTMLDivElement>(null);
  const xtermRef = useRef<Terminal | null>(null);
  const fitAddonRef = useRef<FitAddon | null>(null);
  const shellPidRef = useRef<number | null>(null);
  const commandHistoryRef = useRef<string[]>([]);
  const historyIndexRef = useRef<number>(-1);

  // Initialize terminal
  useEffect(() => {
    if (!terminalRef.current || xtermRef.current) return;

    const term = new Terminal({
      theme: {
        background: 'rgba(0, 0, 0, 0.85)',
        foreground: '#00ff00',
        cursor: '#00ff00',
        cursorAccent: '#000000',
        selection: 'rgba(0, 255, 0, 0.3)',
        black: '#000000',
        red: '#ff5555',
        green: '#50fa7b',
        yellow: '#f1fa8c',
        blue: '#6272a4',
        magenta: '#ff79c6',
        cyan: '#8be9fd',
        white: '#f8f8f2',
        brightBlack: '#44475a',
        brightRed: '#ff5555',
        brightGreen: '#50fa7b',
        brightYellow: '#f1fa8c',
        brightBlue: '#6272a4',
        brightMagenta: '#ff79c6',
        brightCyan: '#8be9fd',
        brightWhite: '#ffffff'
      },
      fontFamily: 'JetBrains Mono, Consolas, monospace',
      fontSize: 14,
      lineHeight: 1.2,
      cursorBlink: true,
      cursorStyle: 'block',
      allowTransparency: true,
      windowsMode: false,
      rendererType: 'canvas',
      scrollback: 10000,
    });

    // Add addons
    const fitAddon = new FitAddon();
    const webLinksAddon = new WebLinksAddon();
    const searchAddon = new SearchAddon();
    
    term.loadAddon(fitAddon);
    term.loadAddon(webLinksAddon);
    term.loadAddon(searchAddon);
    
    xtermRef.current = term;
    fitAddonRef.current = fitAddon;

    term.open(terminalRef.current);
    fitAddon.fit();

    // Custom prompt
    const setPrompt = () => {
      term.write('\r\n\x1b[32m[neuro@dawn]\x1b[0m $ ');
    };

    // Initialize shell
    const initShell = async () => {
      if (!window.shellAPI) {
        term.write('\r\n\x1b[31mError: Shell API not available\x1b[0m\r\n');
        return;
      }

      try {
        const pid = await window.shellAPI.spawn('/bin/bash');
        shellPidRef.current = pid;

        // Handle shell output
        window.shellAPI.onData(pid, (data) => {
          term.write(data);
          
          // Log to file
          window.shellAPI.logToFile(`[OUTPUT] ${new Date().toISOString()}: ${data}`);
        });

        // Handle shell exit
        window.shellAPI.onExit(pid, (code) => {
          term.write(`\r\n\x1b[31mShell exited with code ${code}\x1b[0m\r\n`);
          shellPidRef.current = null;
        });

        // Handle terminal input
        term.onData((data) => {
          if (shellPidRef.current) {
            window.shellAPI.write(shellPidRef.current, data);
          }
        });

        // Handle resize
        term.onResize(({ cols, rows }) => {
          if (shellPidRef.current) {
            window.shellAPI.resize(shellPidRef.current, cols, rows);
          }
        });

      } catch (error) {
        term.write(`\r\n\x1b[31mError spawning shell: ${error}\x1b[0m\r\n`);
      }
    };

    initShell();

    // Cleanup
    return () => {
      if (shellPidRef.current && window.shellAPI) {
        window.shellAPI.kill(shellPidRef.current);
      }
      term.dispose();
    };
  }, []);

  // Handle visibility and keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === '`') {
        e.preventDefault();
        setIsVisible(prev => !prev);
        
        // Focus terminal when shown
        if (!isVisible && xtermRef.current) {
          setTimeout(() => {
            xtermRef.current?.focus();
            fitAddonRef.current?.fit();
          }, 100);
        }
      }
      
      // Escape to hide
      if (e.key === 'Escape' && isVisible) {
        setIsVisible(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isVisible]);

  // Fetch and execute Claude command
  const executeClaudeCommand = useCallback(async () => {
    if (!xtermRef.current || !shellPidRef.current) return;

    setIsExecuting(true);
    const term = xtermRef.current;

    try {
      // Fetch command from Claude API
      const response = await fetch('/api/claude', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: 'Generate a useful system command for DAWN cognitive architecture monitoring',
          context: 'Linux bash environment'
        })
      });

      if (!response.ok) throw new Error('Failed to fetch Claude command');

      const data: ClaudeCommand = await response.json();
      
      // Show command info
      term.write(`\r\n\x1b[36m[Claude AI]\x1b[0m ${data.explanation || 'Executing generated command'}\r\n`);
      
      if (data.risk_level === 'dangerous') {
        term.write(`\x1b[31m⚠ Warning: High-risk command. Proceed with caution.\x1b[0m\r\n`);
      }

      // Execute command
      term.write(`\x1b[33m$ ${data.command}\x1b[0m\r\n`);
      window.shellAPI.write(shellPidRef.current, data.command + '\n');
      
      // Log Claude command
      window.shellAPI.logToFile(`[CLAUDE] ${new Date().toISOString()}: ${data.command}`);
      
      setLastCommandStatus('success');
    } catch (error) {
      term.write(`\r\n\x1b[31mError: ${error}\x1b[0m\r\n`);
      setLastCommandStatus('error');
    } finally {
      setIsExecuting(false);
      
      // Clear status after animation
      setTimeout(() => setLastCommandStatus(null), 2000);
    }
  }, []);

  // Window resize handler
  useEffect(() => {
    if (!isVisible) return;

    const handleResize = () => {
      if (fitAddonRef.current) {
        fitAddonRef.current.fit();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isVisible]);

  return (
    <div
      className={`fixed top-4 left-4 transition-all duration-300 ${
        isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'
      }`}
      style={{
        width: '600px',
        height: '400px',
        zIndex: 10000,
      }}
    >
      {/* Glass morphism container */}
      <div className="relative w-full h-full rounded-lg overflow-hidden shadow-2xl">
        {/* Blur background */}
        <div className="absolute inset-0 bg-black/60 backdrop-blur-xl" />
        
        {/* Glow effect based on command status */}
        <div
          className={`absolute inset-0 transition-all duration-1000 pointer-events-none ${
            lastCommandStatus === 'success' 
              ? 'shadow-[inset_0_0_50px_rgba(0,255,0,0.3)]' 
              : lastCommandStatus === 'error'
              ? 'shadow-[inset_0_0_50px_rgba(255,0,0,0.3)]'
              : ''
          }`}
        />
        
        {/* Header */}
        <div className="relative flex items-center justify-between px-4 py-2 bg-black/40 border-b border-green-500/20">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
            <h3 className="text-sm font-mono text-green-400">NeuroShell [PID: {shellPidRef.current || 'N/A'}]</h3>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={executeClaudeCommand}
              disabled={isExecuting}
              className={`px-3 py-1 text-xs font-mono rounded transition-all ${
                isExecuting 
                  ? 'bg-yellow-500/20 text-yellow-400 animate-pulse' 
                  : 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30'
              }`}
            >
              {isExecuting ? 'Executing...' : 'Claude CMD'}
            </button>
            
            <button
              onClick={() => setIsVisible(false)}
              className="text-green-400 hover:text-green-300 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        {/* Terminal */}
        <div 
          ref={terminalRef} 
          className="relative w-full h-[calc(100%-40px)]"
          style={{
            padding: '8px',
          }}
        />
        
        {/* Status line */}
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-green-500/50 to-transparent" />
      </div>
      
      {/* Help tooltip */}
      <div className="absolute -bottom-8 left-0 text-xs text-gray-500">
        Ctrl+~ to toggle • Esc to hide
      </div>
    </div>
  );
};

export default NeuroShellOverlay; 