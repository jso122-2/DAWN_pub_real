import React from 'react';
import { WebSocketStatus } from './components/WebSocketStatus';
import TalkInterface from './components/TalkInterface';
import { ConsciousnessMonitor } from './components/modules/ConsciousnessMonitor';
import { NeuralActivityVisualizer } from './components/modules/NeuralActivityVisualizer';
import './App.css';

function App() {
  return (
    <div className="app">
      <div className="container">
        <header className="app-header">
          <h1 className="app-title">DAWN</h1>
          <p className="app-subtitle">Swiss-Terminal Consciousness Engine</p>
        </header>
        
        <div className="terminal-module">
          <WebSocketStatus />
        </div>

        <div className="terminal-grid">
          <div className="terminal-module">
            <div className="module-header">Talk Interface</div>
            <TalkInterface />
          </div>
          
          <div className="terminal-module">
            <div className="module-header">Consciousness Monitor</div>
            <ConsciousnessMonitor />
          </div>
          
          <div className="terminal-module">
            <div className="module-header">Neural Activity</div>
            <NeuralActivityVisualizer />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 