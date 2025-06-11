import { useEffect, useState } from 'react';

interface ConnectionStatusProps {
  backend: 'connected' | 'connecting' | 'disconnected' | 'error';
  websocket: boolean;
  lastUpdate: number;
}

export default function ConnectionStatus({ backend, websocket, lastUpdate }: ConnectionStatusProps) {
  const [pulseClass, setPulseClass] = useState('');
  
  useEffect(() => {
    if (backend === 'connecting') {
      setPulseClass('animate-pulse');
    } else {
      setPulseClass('');
    }
  }, [backend]);

  const getStatusIcon = () => {
    switch (backend) {
      case 'connected': return '🟢';
      case 'connecting': return '🟡';
      case 'error': return '🔴';
      default: return '⚪';
    }
  };

  const getStatusText = () => {
    const wsIcon = websocket ? '🔗' : '📡';
    switch (backend) {
      case 'connected': return `${wsIcon} Connected`;
      case 'connecting': return '🔄 Connecting...';
      case 'error': return '❌ Error';
      default: return '⚪ Disconnected';
    }
  };

  const getStatusColor = () => {
    switch (backend) {
      case 'connected': return 'text-green-400';
      case 'connecting': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getBorderColor = () => {
    switch (backend) {
      case 'connected': return 'border-green-500/30';
      case 'connecting': return 'border-yellow-500/30';
      case 'error': return 'border-red-500/30';
      default: return 'border-gray-500/30';
    }
  };

  return (
    <div className={`
      flex items-center space-x-4 px-4 py-2 rounded-lg border backdrop-blur-sm
      transition-all duration-300 ${getBorderColor()}
      ${backend === 'connected' ? 'bg-green-900/10' : ''}
      ${backend === 'connecting' ? 'bg-yellow-900/10' : ''}
      ${backend === 'error' ? 'bg-red-900/10' : ''}
    `}>
      <div className={`flex items-center space-x-2 ${pulseClass}`}>
        <span className="text-lg">{getStatusIcon()}</span>
        <span className={`text-sm font-medium ${getStatusColor()}`}>
          {getStatusText()}
        </span>
      </div>
      
      {/* WebSocket indicator */}
      <div className="flex items-center space-x-1">
        <div className={`w-2 h-2 rounded-full transition-all duration-300 ${
          websocket ? 'bg-blue-400 animate-pulse' : 'bg-gray-500'
        }`} />
        <span className="text-xs text-gray-500">
          WS
        </span>
      </div>
      
      {/* Last update timestamp */}
      {lastUpdate > 0 && (
        <div className="text-xs text-gray-500 border-l border-gray-600 pl-2">
          {new Date(lastUpdate).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
} 