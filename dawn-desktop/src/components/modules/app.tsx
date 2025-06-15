import React from 'react';
import { Terminal } from '../terminal/Terminal';
import { StatusBar } from '../terminal/StatusBar';
import { Module } from '../terminal/Module';
import { NeuralTerminal } from '../terminal/NeuralTerminal';
import { BrainwaveVisualizer } from '../terminal/BrainwaveVisualizer';
import { ConnectionStatus } from '../terminal/ConnectionStatus';
import ConsciousnessVisualizer from '../ConsciousnessVisualizer';

const App: React.FC = () => {
  return (
    <div className="app">
      <style>{`
        .app {
          min-height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .main-terminal {
          height: 300px;
        }

        .status-bar {
          height: 40px;
        }

        .content-grid {
          display: grid;
          grid-template-columns: 1fr 2fr 1fr;
          gap: 20px;
          flex: 1;
        }

        .status-modules {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .neural-interface {
          height: 500px;
        }

        .brainwave-patterns {
          height: 300px;
        }

        .consciousness-visualizer {
          height: 600px;
        }
      `}</style>

      <div className="main-terminal">
        <Terminal />
      </div>

      <div className="status-bar">
        <StatusBar />
      </div>

      <div className="content-grid">
        <div className="status-modules">
          <Module title="CONNECTION">
            <ConnectionStatus />
          </Module>
          <Module title="SYSTEM">
            <div>CPU: 42%</div>
            <div>MEM: 1.2GB</div>
            <div>UPTIME: 2d 4h</div>
          </Module>
        </div>

        <div className="neural-interface">
          <Module title="NEURAL INTERFACE">
            <NeuralTerminal moduleId="neural-interface" />
          </Module>
        </div>

        <div className="status-modules">
          <Module title="ACTIVITY">
            <div>NEURAL: 78%</div>
            <div>QUANTUM: 92%</div>
            <div>COHERENCE: 85%</div>
          </Module>
          <Module title="MEMORY">
            <div>SHORT: 45%</div>
            <div>LONG: 62%</div>
            <div>WORKING: 38%</div>
          </Module>
        </div>
      </div>

      <div className="brainwave-patterns">
        <Module title="BRAINWAVE PATTERNS">
          <BrainwaveVisualizer />
        </Module>
      </div>

      <div className="consciousness-visualizer">
        <ConsciousnessVisualizer />
      </div>
    </div>
  );
};

export default App;