// Example integration of Process Flow Manager into DAWN system
import React, { useState, useEffect } from 'react';
import { ProcessFlowManager } from './ProcessFlowManager';
import { useProcessFlow } from '../../hooks/useProcessFlow';

// Example: DAWN Dashboard with Process Flow Manager
export const DAWNDashboardWithProcessFlow: React.FC = () => {
  const [activeTab, setActiveTab] = useState('process-flow');
  const {
    processes,
    flows,
    getSystemMetrics,
    initializeProcesses
  } = useProcessFlow();
  
  const metrics = getSystemMetrics();
  
  // Initialize processes on mount
  useEffect(() => {
    initializeProcesses();
  }, [initializeProcesses]);
  
  return (
    <div className="dawn-dashboard">
      {/* Dashboard Header */}
      <header className="dashboard-header">
        <h1>🌊 DAWN Consciousness Engine</h1>
        <div className="system-status">
          <div className="status-item">
            <span className="label">Processes:</span>
            <span className="value">{metrics.runningProcesses}/{metrics.totalProcesses}</span>
          </div>
          <div className="status-item">
            <span className="label">CPU:</span>
            <span className="value">{metrics.averageCpuUsage.toFixed(1)}%</span>
          </div>
          <div className="status-item">
            <span className="label">Flows:</span>
            <span className="value">{metrics.flowCount}</span>
          </div>
        </div>
      </header>
      
      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <button 
          className={`nav-tab ${activeTab === 'process-flow' ? 'active' : ''}`}
          onClick={() => setActiveTab('process-flow')}
        >
          🌊 Process Flow
        </button>
        <button 
          className={`nav-tab ${activeTab === 'memory-palace' ? 'active' : ''}`}
          onClick={() => setActiveTab('memory-palace')}
        >
          🏛️ Memory Palace
        </button>
        <button 
          className={`nav-tab ${activeTab === 'neural-network' ? 'active' : ''}`}
          onClick={() => setActiveTab('neural-network')}
        >
          🧠 Neural Network
        </button>
      </nav>
      
      {/* Main Content */}
      <main className="dashboard-content">
        {activeTab === 'process-flow' && (
          <div className="module-container">
            <ProcessFlowManager />
          </div>
        )}
        
        {activeTab === 'memory-palace' && (
          <div className="module-container">
            {/* Your Memory Palace component */}
            <div className="placeholder-module">
              <h2>🏛️ Memory Palace</h2>
              <p>Memory Palace module would go here</p>
            </div>
          </div>
        )}
        
        {activeTab === 'neural-network' && (
          <div className="module-container">
            {/* Your Neural Network component */}
            <div className="placeholder-module">
              <h2>🧠 Neural Network</h2>
              <p>Neural Network 3D module would go here</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

// Example: Process Flow Manager as a Widget
export const ProcessFlowWidget: React.FC = () => {
  const { getSystemMetrics } = useProcessFlow();
  const metrics = getSystemMetrics();
  
  return (
    <div className="process-flow-widget">
      <div className="widget-header">
        <h3>🌊 Process Flow</h3>
        <div className="widget-stats">
          {metrics.runningProcesses > 0 && (
            <span className="status-indicator running">
              {metrics.runningProcesses} Running
            </span>
          )}
          {metrics.errorCount > 0 && (
            <span className="status-indicator error">
              {metrics.errorCount} Errors
            </span>
          )}
        </div>
      </div>
      
      <div className="widget-content">
        <ProcessFlowManager />
      </div>
    </div>
  );
};

// Example: Integration with Existing WebSocket Context
export const ProcessFlowWithWebSocket: React.FC = () => {
  // Replace this with your actual WebSocket hook
  // const { lastTick, connectionStatus } = useWebSocket();
  
  return (
    <div className="process-flow-websocket">
      {/* Connection Status Indicator */}
      <div className="connection-status">
        <span className="status-dot connected"></span>
        WebSocket Connected
      </div>
      
      {/* Process Flow Manager */}
      <ProcessFlowManager />
    </div>
  );
};

// Example CSS for integration (add to your existing styles)
const integrationStyles = `
.dawn-dashboard {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
  color: white;
  font-family: 'Inter', sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 24px;
  background: linear-gradient(135deg, #00ff88 0%, #00aaff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.system-status {
  display: flex;
  gap: 20px;
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.status-item .label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
}

.status-item .value {
  font-size: 16px;
  font-weight: 600;
  color: #00ff88;
}

.dashboard-nav {
  display: flex;
  padding: 0 20px;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-tab {
  padding: 12px 20px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.nav-tab:hover {
  color: #00ff88;
}

.nav-tab.active {
  color: #00ff88;
  border-bottom-color: #00ff88;
}

.dashboard-content {
  flex: 1;
  overflow: hidden;
}

.module-container {
  width: 100%;
  height: 100%;
}

.placeholder-module {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.7);
}

.process-flow-widget {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 12px;
  overflow: hidden;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: rgba(0, 255, 136, 0.1);
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
}

.widget-header h3 {
  margin: 0;
  font-size: 16px;
}

.widget-stats {
  display: flex;
  gap: 10px;
}

.status-indicator {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.status-indicator.running {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

.status-indicator.error {
  background: rgba(255, 68, 68, 0.2);
  color: #ff4444;
}

.widget-content {
  height: 400px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(0, 255, 136, 0.1);
  font-size: 12px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.connected {
  background: #00ff88;
  box-shadow: 0 0 8px rgba(0, 255, 136, 0.5);
}
`;

export default DAWNDashboardWithProcessFlow;

/*
INTEGRATION INSTRUCTIONS:

1. Import and Use in Your Main App:
   import { DAWNDashboardWithProcessFlow } from './modules/ProcessFlowManager/example-integration';
   
   function App() {
     return <DAWNDashboardWithProcessFlow />;
   }

2. Or Use as a Widget:
   import { ProcessFlowWidget } from './modules/ProcessFlowManager/example-integration';
   
   <div className="dashboard-widgets">
     <ProcessFlowWidget />
   </div>

3. Replace Mock WebSocket with Real Context:
   // In ProcessFlowManager.tsx, line 17:
   import { useWebSocket } from '../../contexts/WebSocketContext';
   const { lastTick } = useWebSocket(); // Replace mockWebSocketContext

4. Connect to Your Backend:
   // Implement the API endpoints in your Python backend:
   - POST /api/processes/{id}/start
   - POST /api/processes/{id}/stop  
   - GET /api/processes/{id}/status
   - POST /api/execute
   - GET /api/processes/{id}/stream (Server-Sent Events)
   - GET /api/scripts
*/ 