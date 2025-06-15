import React, { useState, useEffect } from 'react';
import { WebSocketManager } from '../services/websocket';

const WebSocketDebugger: React.FC = () => {
  const [wsManager, setWsManager] = useState<WebSocketManager | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<string>('Disconnected');
  const [logs, setLogs] = useState<string[]>([]);
  
  const addLog = (message: string) => {
    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${message}`]);
  };

  const testEndpoints = [
    'ws://localhost:8000/ws/talk',
    'ws://localhost:8000/ws',
    'ws://localhost:8000/websocket',
    'ws://localhost:8000/consciousness/stream',
    'ws://127.0.0.1:8000/ws/talk'
  ];

  const testConnection = async (url: string) => {
    addLog(`Testing: ${url}`);
    
    const testWs = new WebSocketManager({ 
      url, 
      debug: true,
      maxReconnectAttempts: 0 // Don't retry for testing
    });

    try {
      await testWs.connect();
      addLog(`✓ SUCCESS: ${url} is accessible`);
      setConnectionStatus('Connected');
      setWsManager(testWs);
      return true;
    } catch (error) {
      addLog(`✗ FAILED: ${url}`);
      return false;
    }
  };

  const runDiagnostics = async () => {
    setLogs([]);
    addLog('Starting WebSocket diagnostics...');
    
    // Test if backend is running
    try {
      const response = await fetch('http://localhost:8000/');
      addLog(`Backend HTTP check: ${response.ok ? 'OK' : 'Failed'} (Status: ${response.status})`);
    } catch (error) {
      addLog('Backend HTTP check: Failed - Is your backend running?');
      return;
    }

    // Test each endpoint
    for (const endpoint of testEndpoints) {
      const success = await testConnection(endpoint);
      if (success) break;
    }
  };

  return (
    <div style={{
      padding: '20px',
      backgroundColor: '#0a0a0a',
      color: '#e0e0e0',
      fontFamily: 'monospace',
      minHeight: '100vh'
    }}>
      <h2>WebSocket Debugger</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={runDiagnostics}
          style={{
            padding: '10px 20px',
            backgroundColor: '#00ff88',
            color: '#0a0a0a',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Run Diagnostics
        </button>
        
        <span style={{ marginLeft: '20px' }}>
          Status: <strong style={{ color: connectionStatus === 'Connected' ? '#00ff88' : '#ff0040' }}>
            {connectionStatus}
          </strong>
        </span>
      </div>

      <div style={{
        backgroundColor: '#141414',
        border: '1px solid #2a2a2a',
        padding: '15px',
        height: '400px',
        overflow: 'auto'
      }}>
        <h3>Diagnostic Logs:</h3>
        {logs.map((log, i) => (
          <div key={i} style={{ 
            color: log.includes('SUCCESS') ? '#00ff88' : 
                   log.includes('FAILED') ? '#ff0040' : '#808080' 
          }}>
            {log}
          </div>
        ))}
      </div>

      <div style={{ marginTop: '20px' }}>
        <h3>Common Issues & Solutions:</h3>
        <ul style={{ lineHeight: '1.8' }}>
          <li><strong>Backend not running:</strong> Make sure your FastAPI server is running on port 8000</li>
          <li><strong>Wrong endpoint:</strong> Check your backend WebSocket route configuration</li>
          <li><strong>CORS issues:</strong> Ensure your backend allows WebSocket connections from your frontend origin</li>
          <li><strong>Firewall/Antivirus:</strong> Some security software blocks local WebSocket connections</li>
        </ul>
      </div>
    </div>
  );
};

export default WebSocketDebugger; 