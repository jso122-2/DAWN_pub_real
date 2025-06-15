import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TerminalInput } from '../terminal/TerminalInput';
import { DataModule } from '../terminal/DataModule';

interface TerminalModuleProps {
  moduleId: string;
  position?: { x: number; y: number };
  className?: string;
}

interface TerminalLine {
  type: 'input' | 'output' | 'error' | 'system';
  content: string;
  timestamp: number;
}

export function TerminalModule({ moduleId, position, className = '' }: TerminalModuleProps) {
  const [lines, setLines] = useState<TerminalLine[]>([
    { type: 'system', content: 'DAWN Terminal v1.0.0', timestamp: Date.now() },
    { type: 'system', content: 'Type "help" for available commands', timestamp: Date.now() },
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const terminalRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new lines are added
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [lines]);

  const handleCommand = async (command: string) => {
    // Add command to history
    setLines(prev => [...prev, { type: 'input', content: command, timestamp: Date.now() }]);
    setIsProcessing(true);

    try {
      // Simulate command processing
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Add response
      setLines(prev => [...prev, { 
        type: 'output', 
        content: `Command executed: ${command}`, 
        timestamp: Date.now() 
      }]);
    } catch (error: any) {
      setLines(prev => [...prev, { 
        type: 'error', 
        content: `Error: ${error?.message || 'Unknown error'}`, 
        timestamp: Date.now() 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <motion.div
      className={`terminal-border crt-effect ${className}`}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      style={position ? {
        position: 'absolute',
        left: position.x,
        top: position.y,
      } : undefined}
    >
      {/* Terminal Header */}
      <div className="module-header">
        <span className="ascii-corner">╔═</span>
        <h3>DAWN Terminal</h3>
        <span className="ascii-corner">═╗</span>
      </div>

      {/* Terminal Output */}
      <div 
        ref={terminalRef}
        className="module-content overflow-y-auto"
        style={{ maxHeight: '400px' }}
      >
        {lines.map((line, i) => (
          <div 
            key={i}
            className={`mono text-sm mb-1 ${
              line.type === 'input' ? 'text-terminal-green' :
              line.type === 'error' ? 'text-terminal-red' :
              line.type === 'system' ? 'text-terminal-amber' :
              'text-off-white'
            }`}
          >
            {line.type === 'input' && '> '}
            {line.content}
          </div>
        ))}
      </div>

      {/* Terminal Input */}
      <div className="module-footer">
        <TerminalInput
          onCommand={handleCommand}
          disabled={isProcessing}
          prompt="DAWN://>"
        />
      </div>

      {/* Status Bar */}
      <div className="module-footer">
        <span className="ascii-corner">╚═</span>
        <span className="status">
          {isProcessing ? 'PROCESSING' : 'READY'}
        </span>
        <span className="ascii-corner">═╝</span>
      </div>
    </motion.div>
  );
} 