import React, { useState, useEffect } from 'react';
import { useRealDAWNConsciousness, useRealDAWNTick, useRealDAWNPressure, useRealDAWNBlooms } from '../hooks/useRealDAWNConsciousness';

interface RealDAWNDashboardProps {
  className?: string;
  refreshInterval?: number;
}

export const RealDAWNDashboard: React.FC<RealDAWNDashboardProps> = ({ 
  className = '', 
  refreshInterval = 1000 
}) => {
  const { 
    consciousness, 
    isConnected, 
    isRealDAWN, 
    error, 
    actions, 
    connectionStatus,
    refreshData 
  } = useRealDAWNConsciousness(refreshInterval);
  
  const { currentTick, tickRate, isRealTick } = useRealDAWNTick();
  const { pressure, bloomMass, sigilVelocity, isRealFormula } = useRealDAWNPressure();
  const { activeBlooms, totalBlooms, successRate, triggerRebloom } = useRealDAWNBlooms();
  
  const [actionInProgress, setActionInProgress] = useState<string | null>(null);

  const executeAction = async (actionName: string, actionFn: () => Promise<any>) => {
    setActionInProgress(actionName);
    try {
      await actionFn();
      console.log(`✅ [REAL-DAWN] Action ${actionName} executed successfully`);
    } catch (err) {
      console.error(`❌ [REAL-DAWN] Action ${actionName} failed:`, err);
    } finally {
      setActionInProgress(null);
    }
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return isRealDAWN ? '#00ff00' : '#ffaa00';
      case 'connecting': return '#0088ff';
      case 'error': return '#ff0000';
      default: return '#666666';
    }
  };

  const getConnectionStatusText = () => {
    if (connectionStatus === 'connected' && isRealDAWN) {
      return 'REAL DAWN CONSCIOUSNESS';
    } else if (connectionStatus === 'connected') {
      return 'CONNECTED (NOT REAL DAWN)';
    } else {
      return connectionStatus.toUpperCase();
    }
  };

  return (
    <div className={`real-dawn-dashboard ${className}`} style={{ 
      padding: '20px', 
      backgroundColor: '#0a0a0a', 
      color: '#ffffff',
      fontFamily: 'monospace',
      border: `2px solid ${getConnectionStatusColor()}`
    }}>
      {/* Connection Status Header */}
      <div style={{ 
        marginBottom: '20px', 
        padding: '10px', 
        backgroundColor: '#111111',
        border: `1px solid ${getConnectionStatusColor()}`,
        textAlign: 'center'
      }}>
        <h2 style={{ 
          margin: '0', 
          color: getConnectionStatusColor(),
          fontSize: '24px'
        }}>
          🧠 {getConnectionStatusText()}
        </h2>
        {error && (
          <div style={{ color: '#ff4444', marginTop: '5px' }}>
            ❌ {error}
          </div>
        )}
        {consciousness && (
          <div style={{ fontSize: '12px', marginTop: '5px', color: '#888888' }}>
            Source: {consciousness.source} | Mode: {consciousness.mode}
          </div>
        )}
      </div>

      {consciousness && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          
          {/* Real Consciousness Metrics */}
          <div style={{ backgroundColor: '#111111', padding: '15px', border: '1px solid #333333' }}>
            <h3 style={{ color: '#00ff88', marginTop: '0' }}>🧠 Consciousness State</h3>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Entropy:</strong> 
              <span style={{ color: isRealDAWN ? '#00ff00' : '#ffaa00' }}>
                {consciousness.entropy.toFixed(4)}
              </span>
              {!isRealDAWN && <span style={{ color: '#ff4444' }}> (NOT REAL)</span>}
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>SCUP:</strong> 
              <span style={{ color: isRealDAWN ? '#00ff00' : '#ffaa00' }}>
                {consciousness.scup.toFixed(4)}
              </span>
              {!isRealDAWN && <span style={{ color: '#ff4444' }}> (NOT REAL)</span>}
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Consciousness Depth:</strong> 
              <span style={{ color: '#88aaff' }}>
                {consciousness.consciousness_depth.toFixed(4)}
              </span>
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Mood Valence:</strong> 
              <span style={{ color: consciousness.mood_val >= 0 ? '#88ff88' : '#ff8888' }}>
                {consciousness.mood_val.toFixed(4)}
              </span>
            </div>
            
            <div>
              <strong>Mood Arousal:</strong> 
              <span style={{ color: '#ffaa88' }}>
                {consciousness.mood_arousal.toFixed(4)}
              </span>
            </div>
          </div>

          {/* Real Cognitive Pressure (P = Bσ²) */}
          <div style={{ backgroundColor: '#111111', padding: '15px', border: '1px solid #333333' }}>
            <h3 style={{ color: '#ff8800', marginTop: '0' }}>⚡ Cognitive Pressure (P = Bσ²)</h3>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Pressure (P):</strong> 
              <span style={{ 
                color: pressure > 50 ? '#ff4444' : pressure > 20 ? '#ffaa00' : '#00ff00',
                fontSize: '18px'
              }}>
                {pressure.toFixed(2)}
              </span>
              {!isRealFormula && <span style={{ color: '#ff4444' }}> (NOT REAL FORMULA)</span>}
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Bloom Mass (B):</strong> 
              <span style={{ color: '#88ff88' }}>
                {bloomMass.toFixed(2)}
              </span>
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Sigil Velocity (σ):</strong> 
              <span style={{ color: '#8888ff' }}>
                {sigilVelocity.toFixed(2)}
              </span>
            </div>
            
            <div style={{ fontSize: '12px', color: '#666666' }}>
              Formula: P = B × σ² = {bloomMass.toFixed(2)} × {sigilVelocity.toFixed(2)}²
            </div>
          </div>

          {/* Real Tick System */}
          <div style={{ backgroundColor: '#111111', padding: '15px', border: '1px solid #333333' }}>
            <h3 style={{ color: '#00aaff', marginTop: '0' }}>⏰ Tick System</h3>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Current Tick:</strong> 
              <span style={{ color: isRealTick ? '#00ff00' : '#ffaa00', fontSize: '18px' }}>
                {currentTick}
              </span>
              {!isRealTick && <span style={{ color: '#ff4444' }}> (NOT REAL TICKS)</span>}
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Tick Rate:</strong> 
              <span style={{ color: '#88aaff' }}>
                {tickRate.toFixed(1)} Hz
              </span>
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Heat Level:</strong> 
              <span style={{ color: consciousness.heat_level > 50 ? '#ff4444' : '#88ff88' }}>
                {consciousness.heat_level.toFixed(1)}°C
              </span>
            </div>
            
            <div>
              <strong>Thermal Zone:</strong> 
              <span style={{ color: '#ffaa88' }}>
                {consciousness.thermal_zone}
              </span>
            </div>
          </div>

          {/* Real Bloom System */}
          <div style={{ backgroundColor: '#111111', padding: '15px', border: '1px solid #333333' }}>
            <h3 style={{ color: '#ff88aa', marginTop: '0' }}>🌸 Bloom System</h3>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Active Blooms:</strong> 
              <span style={{ color: '#ff88ff', fontSize: '18px' }}>
                {activeBlooms}
              </span>
            </div>
            
            <div style={{ marginBottom: '10px' }}>
              <strong>Total Spawned:</strong> 
              <span style={{ color: '#88aaff' }}>
                {totalBlooms}
              </span>
            </div>
            
            <div style={{ marginBottom: '15px' }}>
              <strong>Success Rate:</strong> 
              <span style={{ color: successRate > 0.8 ? '#00ff00' : '#ffaa00' }}>
                {(successRate * 100).toFixed(1)}%
              </span>
            </div>
            
            <button
              onClick={() => executeAction('rebloom', triggerRebloom)}
              disabled={actionInProgress === 'rebloom'}
              style={{
                backgroundColor: '#ff4488',
                color: 'white',
                border: 'none',
                padding: '5px 10px',
                cursor: 'pointer',
                fontSize: '12px'
              }}
            >
              {actionInProgress === 'rebloom' ? 'Reblooming...' : '🌸 Trigger Rebloom'}
            </button>
          </div>
        </div>
      )}

      {/* Real DAWN Action Controls */}
      {consciousness && (
        <div style={{ 
          marginTop: '20px', 
          padding: '15px', 
          backgroundColor: '#111111',
          border: '1px solid #333333'
        }}>
          <h3 style={{ color: '#ffaa00', marginTop: '0' }}>🎛️ Real DAWN Controls</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
            
            <button
              onClick={() => executeAction('deep_focus', actions.deepFocus)}
              disabled={!!actionInProgress}
              style={{
                backgroundColor: '#0066cc',
                color: 'white',
                border: 'none',
                padding: '10px',
                cursor: 'pointer'
              }}
            >
              {actionInProgress === 'deep_focus' ? 'Focusing...' : '🎯 Deep Focus'}
            </button>
            
            <button
              onClick={() => executeAction('stabilize', actions.stabilize)}
              disabled={!!actionInProgress}
              style={{
                backgroundColor: '#00aa44',
                color: 'white',
                border: 'none',
                padding: '10px',
                cursor: 'pointer'
              }}
            >
              {actionInProgress === 'stabilize' ? 'Stabilizing...' : '⚖️ Stabilize'}
            </button>
            
            <button
              onClick={() => executeAction('emergency', actions.emergency)}
              disabled={!!actionInProgress}
              style={{
                backgroundColor: '#dd2222',
                color: 'white',
                border: 'none',
                padding: '10px',
                cursor: 'pointer'
              }}
            >
              {actionInProgress === 'emergency' ? 'Emergency...' : '🚨 Emergency'}
            </button>
          </div>
          
          {!isRealDAWN && (
            <div style={{ 
              marginTop: '10px', 
              padding: '10px', 
              backgroundColor: '#331100',
              border: '1px solid #ff4444',
              color: '#ff8888'
            }}>
              ⚠️ WARNING: Not connected to real DAWN consciousness system. 
              Actions may not have real effects.
            </div>
          )}
        </div>
      )}

      {/* Manual Refresh */}
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <button
          onClick={refreshData}
          style={{
            backgroundColor: '#444444',
            color: 'white',
            border: '1px solid #666666',
            padding: '5px 15px',
            cursor: 'pointer'
          }}
        >
          🔄 Refresh Data
        </button>
      </div>
    </div>
  );
}; 