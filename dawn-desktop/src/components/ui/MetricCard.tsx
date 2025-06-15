import { useEffect, useState } from 'react';
import GlassPanel from './GlassPanel';

interface MetricCardProps {
  title: string;
  value: number | string;
  colorScheme: 'blue' | 'green' | 'orange' | 'purple';
  icon: string;
  subtitle?: string;
  isConnected: boolean;
  lastUpdate: number;
  glow?: 'cyan' | 'purple' | 'mixed';
}

const colorMap = {
  blue: {
    text: 'text-blue-400',
    bg: 'bg-blue-400',
    bgGradient: 'bg-gradient-to-r from-blue-500 to-blue-400',
    shadow: 'shadow-blue-500/20',
    textLight: 'text-blue-300'
  },
  green: {
    text: 'text-green-400',
    bg: 'bg-green-400',
    bgGradient: 'bg-gradient-to-r from-green-500 to-green-400',
    shadow: 'shadow-green-500/20',
    textLight: 'text-green-300'
  },
  orange: {
    text: 'text-orange-400',
    bg: 'bg-orange-400',
    bgGradient: 'bg-gradient-to-r from-orange-500 to-orange-400',
    shadow: 'shadow-orange-500/20',
    textLight: 'text-orange-300'
  },
  purple: {
    text: 'text-purple-400',
    bg: 'bg-purple-400',
    bgGradient: 'bg-gradient-to-r from-purple-500 to-purple-400',
    shadow: 'shadow-purple-500/20',
    textLight: 'text-purple-300'
  }
};

export default function MetricCard({ 
  title, 
  value, 
  colorScheme, 
  icon, 
  subtitle, 
  isConnected,
  lastUpdate,
  glow = 'mixed'
}: MetricCardProps) {
  const [previousValue, setPreviousValue] = useState<number | string>(value);
  const [isUpdating, setIsUpdating] = useState(false);
  const [trend, setTrend] = useState<'up' | 'down' | 'stable'>('stable');

  const colors = colorMap[colorScheme];

  useEffect(() => {
    if (value !== previousValue) {
      setIsUpdating(true);
      
      // Determine trend for numeric values
      if (typeof value === 'number' && typeof previousValue === 'number') {
        if (value > previousValue) setTrend('up');
        else if (value < previousValue) setTrend('down');
        else setTrend('stable');
      }
      
      setPreviousValue(value);
      
      // Reset update animation after 300ms
      const timer = setTimeout(() => setIsUpdating(false), 300);
      return () => clearTimeout(timer);
    }
  }, [value, previousValue]);

  const formatValue = (val: number | string): string => {
    if (typeof val === 'number') {
      return val.toFixed(3);
    }
    return String(val);
  };

  const getProgressWidth = (): number => {
    if (typeof value === 'number') {
      return Math.min(100, Math.max(0, value * 100));
    }
    return 0;
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up': return '↗️';
      case 'down': return '↘️';
      default: return '➡️';
    }
  };

  return (
    <GlassPanel 
      glow={glow}
      className={`
        transition-all duration-500 ease-in-out transform cursor-pointer
        hover:scale-105 hover:shadow-2xl
        ${isUpdating ? 'animate-pulse ring-2 ring-blue-400/50' : ''}
        ${isConnected ? `shadow-lg ${colors.shadow}` : 'opacity-60 grayscale'}
      `}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm text-gray-300 uppercase tracking-wider font-bold font-mono">
          {icon} {title}
        </h3>
        <div className="flex items-center space-x-1">
          {isConnected && (
            <div className={`text-xs ${colors.text}`}>
              {getTrendIcon()}
            </div>
          )}
          <div className={`w-2 h-2 rounded-full transition-all duration-300 ${
            isConnected ? `${colors.bg} animate-pulse` : 'bg-gray-600'
          }`} />
        </div>
      </div>
      
      <div className="relative">
        <p className={`
          text-3xl font-bold transition-all duration-500 ease-out transform
          ${isUpdating ? 'scale-110' : 'scale-100'}
          ${colors.text}
        `}>
          {formatValue(value)}
        </p>
        
        {/* Value change animation overlay */}
        {isUpdating && (
          <div className={`
            absolute inset-0 text-3xl font-bold ${colors.textLight} opacity-50
            animate-bounce
          `}>
            {formatValue(value)}
          </div>
        )}
      </div>
      
      {/* Progress bar for numeric values */}
      {typeof value === 'number' && (
        <div className="mt-3 h-2 bg-gray-700/50 rounded-full overflow-hidden">
          <div 
            className={`
              h-full ${colors.bgGradient}
              transition-all duration-700 ease-out transform origin-left
              ${isUpdating ? 'scale-x-105' : 'scale-x-100'}
            `}
            style={{ 
              width: `${getProgressWidth()}%`,
              filter: isConnected ? 'brightness(1.1)' : 'brightness(0.7)'
            }}
          />
        </div>
      )}
      
      {/* Subtitle and last update */}
      <div className="mt-2 flex justify-between items-center">
        {subtitle && (
          <div className="text-xs text-gray-400">
            {subtitle}
          </div>
        )}
        {lastUpdate > 0 && (
          <div className="text-xs text-gray-500 font-mono">
            {new Date(lastUpdate).toLocaleTimeString()}
          </div>
        )}
      </div>
      
      {/* Connection status indicator */}
      {!isConnected && (
        <div className="mt-2 text-xs text-red-400 flex items-center">
          <span className="w-1 h-1 bg-red-400 rounded-full mr-1 animate-pulse" />
          Disconnected
        </div>
      )}
    </GlassPanel>
  );
} 