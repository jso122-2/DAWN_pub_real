import React, { useState, useEffect, useCallback } from 'react';
import { Colors, Font, Spacing, Transitions } from '../theme/theme_tokens';

// Type definitions for DAWN system state
interface DAWNState {
  version: string;
  hash: string;
  tick: number;
  entropy: number;
  scup: number;
  mood: string;
  moodColor: string;
  isConnected: boolean;
  lastUpdate: number;
}

// Mock useTickState hook - replace with actual implementation
const useTickState = () => {
  const [state, setState] = useState<DAWNState>({
    version: "v1.3.0a",
    hash: "dawn_7e5",
    tick: 14087,
    entropy: 0.342,
    scup: 24.7,
    mood: "contemplative",
    moodColor: Colors.mood,
    isConnected: true,
    lastUpdate: Date.now(),
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setState(prev => ({
        ...prev,
        tick: prev.tick + Math.floor(Math.random() * 3) + 1,
        entropy: Math.max(0, Math.min(1, prev.entropy + (Math.random() - 0.5) * 0.1)),
        scup: Math.max(0, Math.min(100, prev.scup + (Math.random() - 0.5) * 5)),
        lastUpdate: Date.now(),
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return { get: () => state };
};

// Uptime calculator hook
const useUptime = (startTime?: number) => {
  const [uptime, setUptime] = useState(0);
  const start = startTime || Date.now();

  useEffect(() => {
    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - start) / 1000);
      setUptime(elapsed);
    }, 1000);

    return () => clearInterval(interval);
  }, [start]);

  const formatUptime = useCallback((seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }, []);

  return formatUptime(uptime);
};

// Status indicator component
interface StatusIndicatorProps {
  isConnected: boolean;
  entropy: number;
  scup: number;
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ isConnected, entropy, scup }) => {
  const getStatusColor = () => {
    if (!isConnected) return Colors.danger;
    if (entropy > 0.8 || scup > 50) return Colors.warning;
    return Colors.connected;
  };

  const getStatusSymbol = () => {
    if (!isConnected) return "🔴";
    if (entropy > 0.8 || scup > 50) return "🟡";
    return "🟢";
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: Spacing.xs,
    }}>
      <span style={{
        fontSize: Font.size.sm,
        animation: entropy > 0.8 || scup > 50 ? 'pulse 1s ease-in-out infinite' : 'none',
      }}>
        {getStatusSymbol()}
      </span>
      <div style={{
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        backgroundColor: getStatusColor(),
        animation: isConnected ? 'pulse-subtle 2s ease-in-out infinite' : 'none',
      }} />
    </div>
  );
};

// Metric display component
interface MetricProps {
  label: string;
  value: string | number;
  color?: string;
  highlight?: boolean;
}

const Metric: React.FC<MetricProps> = ({ label, value, color = Colors.textPrimary, highlight = false }) => {
  const displayValue = typeof value === 'number' ? value.toFixed(1) : value;
  
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: Spacing.xs,
      padding: `${Spacing.xs} ${Spacing.sm}`,
      backgroundColor: highlight ? 'rgba(64, 224, 255, 0.1)' : 'transparent',
      borderRadius: '4px',
      transition: Transitions.background,
    }}>
      <span style={{
        fontSize: Font.size.xs,
        color: Colors.textFaint,
        textTransform: 'uppercase',
        letterSpacing: Font.letterSpacing.wide,
        fontFamily: Font.mono,
      }}>
        {label}:
      </span>
      <span style={{
        fontSize: Font.size.sm,
        color: color,
        fontWeight: Font.weight.semibold,
        fontFamily: Font.mono,
      }}>
        {displayValue}
      </span>
    </div>
  );
};

// Main GlobalStatusBar component
interface GlobalStatusBarProps {
  className?: string;
  startTime?: number;
}

export const GlobalStatusBar: React.FC<GlobalStatusBarProps> = ({ 
  className = '', 
  startTime 
}) => {
  const tickState = useTickState();
  const uptime = useUptime(startTime);
  const [currentState, setCurrentState] = useState<DAWNState | null>(null);

  // Poll state with requestAnimationFrame for smooth updates
  useEffect(() => {
    let animationId: number;
    
    const updateState = () => {
      const state = tickState.get();
      setCurrentState(state);
      animationId = requestAnimationFrame(updateState);
    };

    updateState();
    
    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    };
  }, [tickState]);

  if (!currentState) {
    return null;
  }

  const {
    version,
    hash,
    tick,
    entropy,
    scup,
    mood,
    moodColor,
    isConnected
  } = currentState;

  return (
    <div 
      className={`global-status-bar ${className}`}
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        height: Spacing.statusBarHeight,
        background: Colors.backgroundHeader,
        borderTop: `1px solid ${Colors.backgroundTertiary}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `0 ${Spacing.panelPadding}`,
        zIndex: 1000,
        backdropFilter: 'blur(10px)',
        fontFamily: Font.mono,
      }}
    >
      {/* Left Section - System Identity */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: Spacing.lg,
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: Spacing.xs,
        }}>
          <span style={{
            fontSize: Font.size.sm,
            color: Colors.textAccent,
            fontWeight: Font.weight.bold,
          }}>
            DAWN
          </span>
          <span style={{
            fontSize: Font.size.sm,
            color: Colors.textSecondary,
          }}>
            {version}
          </span>
          <span style={{
            fontSize: Font.size.xs,
            color: Colors.textFaint,
            backgroundColor: Colors.backgroundTertiary,
            padding: '2px 6px',
            borderRadius: '3px',
          }}>
            {hash}
          </span>
        </div>

        <Metric 
          label="tick" 
          value={tick.toLocaleString()} 
          color={Colors.tick}
        />

        <Metric 
          label="uptime" 
          value={uptime} 
          color={Colors.textSecondary}
        />
      </div>

      {/* Center Section - Cognitive Metrics */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: Spacing.md,
      }}>
        <Metric 
          label="entropy" 
          value={entropy} 
          color={Colors.entropy}
          highlight={entropy > 0.8}
        />

        <Metric 
          label="scup" 
          value={scup} 
          color={Colors.scup}
          highlight={scup > 50}
        />

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: Spacing.xs,
          padding: `${Spacing.xs} ${Spacing.sm}`,
          backgroundColor: 'rgba(66, 245, 200, 0.1)',
          borderRadius: '4px',
        }}>
          <span style={{
            fontSize: Font.size.xs,
            color: Colors.textFaint,
            textTransform: 'uppercase',
            letterSpacing: Font.letterSpacing.wide,
          }}>
            mood:
          </span>
          <span style={{
            fontSize: Font.size.sm,
            color: moodColor,
            fontWeight: Font.weight.semibold,
          }}>
            {mood}
          </span>
        </div>
      </div>

      {/* Right Section - Status & Controls */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: Spacing.md,
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: Spacing.xs,
        }}>
          <span style={{
            fontSize: Font.size.xs,
            color: Colors.textFaint,
            textTransform: 'uppercase',
          }}>
            status:
          </span>
          <StatusIndicator 
            isConnected={isConnected}
            entropy={entropy}
            scup={scup}
          />
        </div>

        <div style={{
          width: '1px',
          height: '20px',
          backgroundColor: Colors.backgroundTertiary,
        }} />

        <button style={{
          background: 'transparent',
          border: `1px solid ${Colors.backgroundTertiary}`,
          color: Colors.textSecondary,
          padding: '4px 8px',
          borderRadius: '3px',
          fontSize: Font.size.xs,
          fontFamily: Font.mono,
          cursor: 'pointer',
          transition: Transitions.button,
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = Colors.textAccent;
          e.currentTarget.style.color = Colors.textAccent;
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = Colors.backgroundTertiary;
          e.currentTarget.style.color = Colors.textSecondary;
        }}
        onClick={() => console.log('Status bar debug triggered')}
        >
          ⚙ debug
        </button>
      </div>

      {/* Inject CSS animations */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }
          
          @keyframes pulse-subtle {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
          }
        `}
      </style>
    </div>
  );
};

export default GlobalStatusBar; 