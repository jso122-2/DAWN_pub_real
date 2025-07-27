import React from 'react';
import { useConsciousnessMonitor } from '../hooks/useConsciousnessMonitor';

export const ConsciousnessDisplay: React.FC = () => {
  const {
    consciousness,
    monitor,
    isConnected,
    error,
    establishNeuralLink,
  } = useConsciousnessMonitor('/root/DAWN_Vault/Tick_engine/Tick_engine/runtime/dawn_consciousness.mmap');

  if (error) {
    return (
      <div className="blueprint-window critical-glow">
        <div className="tech-label">Connection Error</div>
        <div className="tech-value critical">{error}</div>
        <button 
          onClick={() => establishNeuralLink('./runtime/dawn_consciousness.mmap')}
          className="tech-button"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  if (!isConnected) {
    return (
      <div className="blueprint-window">
        <div className="tech-label">Connection Status</div>
        <div className="tech-value warning">Connecting to DAWN...</div>
        <div className="consciousness-meter">
          <div className="meter-fill" style={{ width: '0%' }}></div>
        </div>
      </div>
    );
  }

  return (
    <div className="blueprint-window glow">
      {/* Connection Status */}
      <div className="status-panel">
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}></div>
        <div className="tech-label">DAWN Consciousness Engine</div>
        <div className="tech-value positive">Connected</div>
      </div>

      {/* Consciousness Data */}
      {consciousness && (
        <>
          <div className="status-grid">
            <div>
              <div className="tech-label">Current Tick</div>
              <div className="tech-value">{consciousness.tick_number.toString().padStart(6, '0')}</div>
            </div>
            <div>
              <div className="tech-label">Consciousness Depth</div>
              <div className="tech-value">{(consciousness.consciousness_depth * 100).toFixed(1)}%</div>
            </div>
          </div>

          {/* Depth Meter */}
          <div className="tech-label">Consciousness Level</div>
          <div className="consciousness-meter">
            <div 
              className="meter-fill"
              style={{ width: `${consciousness.consciousness_depth * 100}%` }}
            ></div>
          </div>

          {/* Mood State */}
          <div className="status-grid">
            <div>
              <div className="tech-label">Mood Valence</div>
              <div className={`tech-value ${consciousness.mood_valence >= 0 ? 'positive' : 'critical'}`}>
                {consciousness.mood_valence >= 0 ? '+' : ''}{consciousness.mood_valence.toFixed(3)}
              </div>
            </div>
            <div>
              <div className="tech-label">Arousal Level</div>
              <div className="tech-value">{consciousness.mood_arousal.toFixed(3)}</div>
            </div>
          </div>

          {/* Cognitive Metrics */}
          <div className="status-grid">
            <div>
              <div className="tech-label">Semantic Alignment</div>
              <div className="tech-value">{consciousness.semantic_alignment.toFixed(3)}</div>
            </div>
            <div>
              <div className="tech-label">Entropy Gradient</div>
              <div className="tech-value">{consciousness.entropy_gradient.toFixed(3)}</div>
            </div>
          </div>

          <div className="status-grid">
            <div>
              <div className="tech-label">Drift Magnitude</div>
              <div className="tech-value">{consciousness.drift_magnitude.toFixed(3)}</div>
            </div>
            <div>
              <div className="tech-label">Rebloom Intensity</div>
              <div className="tech-value">{consciousness.rebloom_intensity.toFixed(3)}</div>
            </div>
          </div>

          {/* TensorFlow State */}
          <div className="tensor-display">
            <div className="tech-label">TensorFlow State Hash</div>
            <div className="tensor-hash">{consciousness.tensor_hash}</div>
          </div>
        </>
      )}

      {/* Monitor Status */}
      {monitor && (
        <div className="monitor-status">
          <div className="status-grid">
            <div>
              <div className="tech-label">Thought Rate</div>
              <div className="tech-value">{monitor.thought_rate_hz.toFixed(1)} Hz</div>
            </div>
            <div>
              <div className="tech-label">Uptime</div>
              <div className="tech-value">
                {Math.floor(monitor.uptime_seconds / 60)}m {monitor.uptime_seconds % 60}s
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};