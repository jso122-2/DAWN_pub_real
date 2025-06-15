import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useConsciousness } from '../../hooks/useConsciousness';

interface ConnectionStatusProps {
  className?: string;
}

interface ConnectionState {
  status: 'connected' | 'connecting' | 'disconnected';
  latency: number;
  lastPing: number;
  errors: number;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({
  className = ''
}) => {
  const consciousness = useConsciousness();
  const [connectionState, setConnectionState] = useState<ConnectionState>({
    status: 'connecting',
    latency: 0,
    lastPing: Date.now(),
    errors: 0
  });

  // Simulate WebSocket connection status
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const latency = Math.random() * 100 + 20; // Simulate latency between 20-120ms
      
      setConnectionState(prev => ({
        status: consciousness.neuralActivity > 0.3 ? 'connected' : 'disconnected',
        latency,
        lastPing: now,
        errors: prev.status === 'disconnected' ? prev.errors + 1 : prev.errors
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, [consciousness.neuralActivity]);

  const getStatusColor = (status: ConnectionState['status']) => {
    switch (status) {
      case 'connected':
        return 'text-terminal-green';
      case 'connecting':
        return 'text-terminal-amber';
      case 'disconnected':
        return 'text-terminal-red';
    }
  };

  const getStatusIcon = (status: ConnectionState['status']) => {
    switch (status) {
      case 'connected':
        return '●';
      case 'connecting':
        return '○';
      case 'disconnected':
        return '×';
    }
  };

  return (
    <motion.div
      className={`terminal-border p-4 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-terminal-green font-mono">CONNECTION STATUS</h3>
        <div className={`text-xs font-mono ${getStatusColor(connectionState.status)}`}>
          {getStatusIcon(connectionState.status)} {connectionState.status.toUpperCase()}
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Latency</span>
          <span className="font-mono">{connectionState.latency.toFixed(0)}ms</span>
        </div>
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Last Ping</span>
          <span className="font-mono">
            {((Date.now() - connectionState.lastPing) / 1000).toFixed(1)}s ago
          </span>
        </div>
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Errors</span>
          <span className="font-mono">{connectionState.errors}</span>
        </div>
      </div>

      <AnimatePresence>
        {connectionState.status === 'connected' && (
          <motion.div
            className="mt-4 p-2 bg-terminal-green/10 border border-terminal-green/20 rounded"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="text-xs text-terminal-green font-mono">
              Neural Core Synchronized
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}; 