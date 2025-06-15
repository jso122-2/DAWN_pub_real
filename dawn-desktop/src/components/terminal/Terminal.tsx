import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TerminalInput } from './TerminalInput';

interface TerminalProps {
  className?: string;
}

export const Terminal: React.FC<TerminalProps> = ({
  className = ''
}) => {
  const [history, setHistory] = useState<string[]>([
    'DAWN Terminal v1.0.0',
    'Type "help" for available commands',
    ''
  ]);
  const historyEndRef = useRef<HTMLDivElement>(null);

  const executeCommand = (cmd: string) => {
    // Add command to history
    setHistory(prev => [...prev, `> ${cmd}`]);

    // Simple command parsing
    const [command, ...args] = cmd.trim().split(' ');

    switch (command.toLowerCase()) {
      case 'help':
        setHistory(prev => [...prev, 
          'Available commands:',
          '  help     - Show this help message',
          '  clear    - Clear terminal history',
          '  status   - Show system status',
          '  modules  - List active modules',
          '  exit     - Exit terminal',
          ''
        ]);
        break;

      case 'clear':
        setHistory(['DAWN Terminal v1.0.0', 'Type "help" for available commands', '']);
        break;

      case 'status':
        setHistory(prev => [...prev,
          'System Status:',
          '  Neural Core: Active',
          '  SCUP: 75.5%',
          '  Entropy: 0.45',
          '  Memory: 2.4GB/4GB',
          ''
        ]);
        break;

      case 'modules':
        setHistory(prev => [...prev,
          'Active Modules:',
          '  [RUNNING] Neural Network',
          '  [RUNNING] Quantum Engine',
          '  [IDLE]    Consciousness Matrix',
          '  [ERROR]   Data Flow Visualizer',
          ''
        ]);
        break;

      case 'exit':
        setHistory(prev => [...prev, 'Terminal session ended', '']);
        break;

      default:
        setHistory(prev => [...prev, `Command not found: ${command}`, '']);
    }
  };

  // Auto-scroll to bottom
  useEffect(() => {
    historyEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  return (
    <motion.div
      className={`terminal-border p-4 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Terminal Output */}
      <div className="h-[500px] overflow-y-auto font-mono text-sm mb-4">
        {history.map((line, i) => (
          <div key={i} className="text-gray-300">
            {line}
          </div>
        ))}
        <div ref={historyEndRef} />
      </div>

      {/* Terminal Input */}
      <TerminalInput
        onCommand={executeCommand}
        prompt="DAWN://>"
        className="w-full"
      />
    </motion.div>
  );
}; 