import React from 'react';
import { LastSpokenPanel } from './LastSpokenPanel';

/**
 * Demo component showing LastSpokenPanel integration
 * This demonstrates how to integrate the voice reflection panel
 * into DAWN's consciousness dashboard
 */
export const LastSpokenPanelDemo: React.FC = () => {
  return (
    <div className="dawn-dashboard-demo">
      {/* Dashboard Header */}
      <div className="demo-header">
        <h2>🗣️ DAWN Voice Reflection Monitor</h2>
        <p>Real-time display of DAWN's spoken thoughts and reflections</p>
      </div>

      {/* Main Dashboard Grid */}
      <div className="demo-grid">
        {/* Left Column - Last Spoken Panel */}
        <div className="demo-column">
          <LastSpokenPanel 
            maxEntries={5}
            updateInterval={2000}
            className="demo-voice-panel"
          />
        </div>

        {/* Right Column - Integration Notes */}
        <div className="demo-column">
          <div className="integration-notes">
            <h3>🔧 Integration Status</h3>
            <div className="status-grid">
              <div className="status-item">
                <span className="status-label">Log File:</span>
                <span className="status-value">runtime/logs/spoken_trace.log</span>
              </div>
              <div className="status-item">
                <span className="status-label">Update Rate:</span>
                <span className="status-value">2 seconds</span>
              </div>
              <div className="status-item">
                <span className="status-label">Max Entries:</span>
                <span className="status-value">5 reflections</span>
              </div>
              <div className="status-item">
                <span className="status-label">Risk Detection:</span>
                <span className="status-value">Enabled</span>
              </div>
            </div>

            <h3>📝 Features Demonstrated</h3>
            <ul className="feature-list">
              <li>✅ Real-time voice reflection display</li>
              <li>✅ Risk word highlighting (drift, uncertainty, cascade)</li>
              <li>✅ Entropy and confidence metrics</li>
              <li>✅ Color-coded risk levels</li>
              <li>✅ Blueprint panel styling</li>
              <li>✅ Live/pause controls</li>
              <li>✅ Fade-in animations</li>
              <li>✅ Responsive design</li>
            </ul>

            <h3>🔮 Next Steps</h3>
            <div className="next-steps">
              <div className="step-item">
                <span className="step-number">1</span>
                <span className="step-text">Connect to real spoken_trace.log</span>
              </div>
              <div className="step-item">
                <span className="step-number">2</span>
                <span className="step-text">Implement ReflectionToVoiceMap.ts</span>
              </div>
              <div className="step-item">
                <span className="step-number">3</span>
                <span className="step-text">Build SigilFromSpeechBridge.ts</span>
              </div>
              <div className="step-item">
                <span className="step-number">4</span>
                <span className="step-text">Create spoken_trace_explorer.py</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="demo-footer">
        <p>🧠 <strong>DAWN Voice Echo System</strong> — Making thought audible, introspection visible</p>
      </div>
    </div>
  );
};

export default LastSpokenPanelDemo; 