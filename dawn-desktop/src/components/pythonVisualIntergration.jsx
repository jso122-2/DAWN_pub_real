import React, { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

const isTauri = typeof window !== 'undefined' && typeof window.__TAURI_IPC__ === 'function';

function addDebugLog(channel, message, extra) {
  if (typeof setDebugInfo === 'function') {
    setDebugInfo(prev => ({
      ...prev,
      logs: [
        ...(prev.logs || []),
        { channel, message, extra, timestamp: new Date().toISOString() }
      ].slice(-100)
    }));
  } else {
    // fallback: log to console
    console.log(`[${channel}]`, message, extra || '');
  }
}

const PythonVisualIntegration = ({ activeProcesses }) => {
  const [showDebugPanel, setShowDebugPanel] = useState(false);
  const [videoStream, setVideoStream] = useState(null);
  const [detectionResults, setDetectionResults] = useState([]);
  const [depthMap, setDepthMap] = useState(null);
  const [pointCloud, setPointCloud] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [streamUrl, setStreamUrl] = useState('');
  const [debugInfo, setDebugInfo] = useState('');
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);

  // Configure stream URLs based on active processes
  useEffect(() => {
    const baseUrl = window.location.hostname === 'localhost' 
      ? 'http://localhost:8080'
      : `https://${window.location.hostname}`;
    
    // Check which Python processes are active
    const activeStreamUrl = activeProcesses.find(p => p.enabled && p.script)?.streamUrl;
    if (activeStreamUrl) {
      setStreamUrl(`${baseUrl}${activeStreamUrl}`);
    }
  }, [activeProcesses]);

  // Initial connection tests
  useEffect(() => {
    testBackendConnection();
  }, []);

  // WebSocket connection for real-time data with enhanced debugging
  useEffect(() => {
    const connectWebSocket = () => {
      const wsUrl = window.location.hostname === 'localhost'
        ? 'ws://localhost:8081/socketio/'  // Updated for SocketIO
        : `wss://${window.location.hostname}/socketio/`;

      addDebugLog('ws', `Attempting WebSocket connection to: ${wsUrl}`);
      setDebugInfo(prev => ({ 
        ...prev, 
        connectionAttempts: prev.connectionAttempts + 1 
      }));

      try {
        wsRef.current = new WebSocket(wsUrl);
        
        wsRef.current.onopen = () => {
          setConnectionStatus('connected');
          addDebugLog('ws', '✅ WebSocket connected successfully');
        };

        wsRef.current.onmessage = (event) => {
          addDebugLog('ws', '📨 WebSocket message received', { 
            size: event.data.length,
            preview: event.data.substring(0, 100) 
          });
          
          try {
            const data = JSON.parse(event.data);
            handleIncomingData(data);
          } catch (error) {
            addDebugLog('ws', '❌ Failed to parse WebSocket data', error.message);
          }
        };

        wsRef.current.onerror = (error) => {
          addDebugLog('ws', '❌ WebSocket error occurred', error);
          setConnectionStatus('error');
        };

        wsRef.current.onclose = (event) => {
          addDebugLog('ws', `🔌 WebSocket closed`, { 
            code: event.code, 
            reason: event.reason,
            wasClean: event.wasClean 
          });
          setConnectionStatus('disconnected');
          
          // Reconnect after 5 seconds with attempt limiting
          setTimeout(() => {
            if (debugInfo.connectionAttempts < 5) {
              addDebugLog('ws', '🔄 Attempting to reconnect...');
              connectWebSocket();
            } else {
              addDebugLog('ws', '❌ Max reconnection attempts reached');
            }
          }, 5000);
        };
      } catch (error) {
        addDebugLog('ws', '❌ Failed to create WebSocket', error.message);
        setConnectionStatus('error');
      }
    };

    // Delay initial connection to allow backend to start
    setTimeout(connectWebSocket, 1000);

    return () => {
      if (wsRef.current) {
        addDebugLog('ws', 'Closing WebSocket connection');
        wsRef.current.close();
      }
    };
  }, []);

  // Handle incoming data from Python processes
  const handleIncomingData = (data) => {
    switch (data.type) {
      case 'detection':
        setDetectionResults(data.detections || []);
        drawDetections(data.detections);
        break;
      
      case 'depth':
        setDepthMap(data.depthData);
        renderDepthMap(data.depthData);
        break;
      
      case 'pointcloud':
        setPointCloud(data.points);
        break;
      
      case 'frame':
        // Handle raw frame data if needed
        if (data.frame) {
          renderFrame(data.frame);
        }
        break;
      
      default:
        console.log('Unknown data type:', data.type);
    }
  };

  // Draw detection boxes on canvas
  const drawDetections = (detections) => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (!canvas || !video) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw each detection
    detections.forEach(detection => {
      const { x, y, width, height, class: className, confidence } = detection;
      
      // Draw bounding box
      ctx.strokeStyle = '#00ff00';
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y, width, height);
      
      // Draw label
      ctx.fillStyle = '#00ff00';
      ctx.font = '16px monospace';
      ctx.fillText(
        `${className} ${(confidence * 100).toFixed(1)}%`,
        x, y - 5
      );
    });
  };

  // Render depth map visualization
  const renderDepthMap = (depthData) => {
    // Implementation for depth map rendering
    console.log('Rendering depth map:', depthData);
  };

  // Render frame from base64 or array buffer
  const renderFrame = (frameData) => {
    if (videoRef.current && frameData) {
      // If frameData is base64
      if (typeof frameData === 'string') {
        const img = new Image();
        img.onload = () => {
          const canvas = canvasRef.current;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0);
        };
        img.src = `data:image/jpeg;base64,${frameData}`;
      }
    }
  };

  // Control Python processes via Tauri with debugging
  const sendCommand = async (command, params = {}) => {
    addDebugLog('http', `Sending command: ${command}`, params);
    
    if (isTauri) {
      try {
        const result = await invoke('send_cv_command', { command, params });
        addDebugLog('http', `✅ Command success: ${command}`, result);
        return result;
      } catch (error) {
        addDebugLog('http', `❌ Command failed: ${command}`, error.message);
        throw error;
      }
    } else {
      // fallback: log to console
      console.log(`[${command}]`, params);
      return null;
    }
  };

  // Debug panel helpers
  const runDiagnostics = async () => {
    addDebugLog('http', '🔍 Running full diagnostics...');
    await testBackendConnection();
    await testNgrokTunnels();
  };

  const clearDebugLogs = () => {
    setDebugInfo(prev => ({
      ...prev,
      wsEvents: [],
      httpTests: [],
      lastError: null
    }));
  };

  // Define testBackendConnection
  const testBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8081/health');
      const data = await response.json();
      console.log('Backend health:', data);
      setDebugInfo('Backend connected');
    } catch (error) {
      console.error('Backend connection error:', error);
      setDebugInfo('Backend disconnected');
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="w-3 h-3 bg-blue-500 rounded-full mr-2 animate-pulse"></span>
          Python CV Visual Output
        </h3>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${
              connectionStatus === 'connected' ? 'bg-green-500' : 
              connectionStatus === 'error' ? 'bg-red-500' : 'bg-yellow-500'
            } animate-pulse`}></div>
            <span className="text-sm text-gray-400">
              {connectionStatus === 'connected' ? 'Connected to Backend' : 
               connectionStatus === 'error' ? 'Connection Error' : 'Connecting...'}
            </span>
          </div>
          
          {/* Debug Toggle */}
          <button
            onClick={() => setShowDebugPanel(!showDebugPanel)}
            className={`px-3 py-1 rounded text-xs font-mono ${
              showDebugPanel ? 'bg-yellow-600 text-white' : 'bg-gray-700 text-gray-300'
            } hover:bg-yellow-500 transition-colors`}
          >
            DEBUG
          </button>
        </div>
      </div>

      {/* Video Display Area */}
      <div className="relative bg-black rounded-lg overflow-hidden mb-4">
        {streamUrl ? (
          <>
            <video
              ref={videoRef}
              className="w-full h-auto"
              autoPlay
              muted
              playsInline
              src={streamUrl}
              onError={(e) => console.error('Video error:', e)}
            />
            <canvas
              ref={canvasRef}
              className="absolute top-0 left-0 w-full h-full pointer-events-none"
            />
          </>
        ) : (
          <div className="flex items-center justify-center h-96 text-gray-500">
            <div className="text-center">
              <p className="text-lg mb-2">No active video stream</p>
              <p className="text-sm">Start a Python CV process to see output</p>
            </div>
          </div>
        )}
      </div>

      {/* Detection Results */}
      {detectionResults.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-4 mb-4">
          <h4 className="text-sm font-bold text-white mb-2">Detections</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {detectionResults.slice(0, 8).map((detection, idx) => (
              <div key={idx} className="bg-gray-700 rounded p-2 text-xs">
                <span className="text-green-400">{detection.class}</span>
                <span className="text-gray-400 ml-2">
                  {(detection.confidence * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Control Panel */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        <button
          onClick={() => sendCommand('toggle_detection')}
          className="px-3 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
        >
          Toggle Detection
        </button>
        <button
          onClick={() => sendCommand('toggle_tracking')}
          className="px-3 py-2 bg-purple-600 text-white rounded text-sm hover:bg-purple-700"
        >
          Toggle Tracking
        </button>
        <button
          onClick={() => sendCommand('toggle_depth')}
          className="px-3 py-2 bg-green-600 text-white rounded text-sm hover:bg-green-700"
        >
          Toggle Depth
        </button>
        <button
          onClick={() => sendCommand('capture_frame')}
          className="px-3 py-2 bg-yellow-600 text-white rounded text-sm hover:bg-yellow-700"
        >
          Capture Frame
        </button>
      </div>

      {/* Debug Panel */}
      {showDebugPanel && (
        <div className="mt-4 bg-gray-800 rounded-lg p-4 border border-yellow-500">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-sm font-bold text-yellow-400 font-mono">🔍 CV Debug Panel</h4>
            <div className="flex space-x-2">
              <button
                onClick={runDiagnostics}
                className="px-2 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700"
              >
                Run Diagnostics
              </button>
              <button
                onClick={clearDebugLogs}
                className="px-2 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700"
              >
                Clear Logs
              </button>
            </div>
          </div>

          {/* Connection Status */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-gray-900 rounded p-3">
              <h5 className="text-xs font-bold text-white mb-2">Backend Health</h5>
              <div className="text-xs text-gray-300">
                {debugInfo.backendHealth ? (
                  <div>
                    <div className="text-green-400">✅ Status: {debugInfo.backendHealth.status}</div>
                    <div>Camera: {debugInfo.backendHealth.camera_available ? '✅' : '❌'}</div>
                    <div>FPS: {debugInfo.backendHealth.fps || 'N/A'}</div>
                  </div>
                ) : (
                  <div className="text-red-400">❌ No health data</div>
                )}
              </div>
            </div>

            <div className="bg-gray-900 rounded p-3">
              <h5 className="text-xs font-bold text-white mb-2">Network Status</h5>
              <div className="text-xs text-gray-300">
                <div>CORS: <span className={`${
                  debugInfo.corsStatus === 'working' ? 'text-green-400' : 
                  debugInfo.corsStatus === 'blocked' ? 'text-red-400' : 'text-yellow-400'
                }`}>{debugInfo.corsStatus}</span></div>
                <div>ngrok: <span className={`${
                  debugInfo.ngrokStatus === 'active' ? 'text-green-400' : 'text-red-400'
                }`}>{debugInfo.ngrokStatus}</span></div>
                <div>WS Attempts: {debugInfo.connectionAttempts}</div>
              </div>
            </div>

            <div className="bg-gray-900 rounded p-3">
              <h5 className="text-xs font-bold text-white mb-2">URLs</h5>
              <div className="text-xs text-gray-300 font-mono">
                <div>Stream: <span className="text-blue-400">{streamUrl}</span></div>
                <div>Host: {window.location.hostname}</div>
                <div>Protocol: {window.location.protocol}</div>
              </div>
            </div>
          </div>

          {/* Error Display */}
          {debugInfo.lastError && (
            <div className="mb-4 p-3 bg-red-900 border border-red-500 rounded">
              <h5 className="text-xs font-bold text-red-400 mb-1">Last Error:</h5>
              <div className="text-xs text-red-300 font-mono">{debugInfo.lastError}</div>
            </div>
          )}

          {/* Debug Logs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* HTTP Tests */}
            <div className="bg-gray-900 rounded p-3">
              <h5 className="text-xs font-bold text-white mb-2">HTTP Tests ({debugInfo.httpTests.length})</h5>
              <div className="max-h-32 overflow-y-auto text-xs font-mono">
                {debugInfo.httpTests.slice(-5).map((log, idx) => (
                  <div key={idx} className="mb-1">
                    <span className="text-gray-500">{log.timestamp}</span>
                    <span className={`ml-2 ${
                      log.message.includes('✅') ? 'text-green-400' : 
                      log.message.includes('❌') ? 'text-red-400' : 'text-yellow-400'
                    }`}>{log.message}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* WebSocket Events */}
            <div className="bg-gray-900 rounded p-3">
              <h5 className="text-xs font-bold text-white mb-2">WebSocket Events ({debugInfo.wsEvents.length})</h5>
              <div className="max-h-32 overflow-y-auto text-xs font-mono">
                {debugInfo.wsEvents.slice(-5).map((log, idx) => (
                  <div key={idx} className="mb-1">
                    <span className="text-gray-500">{log.timestamp}</span>
                    <span className={`ml-2 ${
                      log.message.includes('✅') ? 'text-green-400' : 
                      log.message.includes('❌') ? 'text-red-400' : 'text-blue-400'
                    }`}>{log.message}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-4 flex flex-wrap gap-2">
            <button
              onClick={() => window.open('http://localhost:4040', '_blank')}
              className="px-2 py-1 bg-purple-600 text-white rounded text-xs hover:bg-purple-700"
            >
              Open ngrok Dashboard
            </button>
            <button
              onClick={() => window.open('http://localhost:8081/health', '_blank')}
              className="px-2 py-1 bg-green-600 text-white rounded text-xs hover:bg-green-700"
            >
              Test Backend Health
            </button>
            <button
              onClick={() => console.log('Debug Info:', debugInfo)}
              className="px-2 py-1 bg-gray-600 text-white rounded text-xs hover:bg-gray-700"
            >
              Log Debug to Console
            </button>
          </div>
        </div>
      )}

      {/* Status Information */}
      <div className="mt-4 grid grid-cols-3 gap-4 text-xs">
        <div className="bg-gray-800 rounded p-2">
          <span className="text-gray-400">FPS:</span>
          <span className="text-white ml-2">30</span>
        </div>
        <div className="bg-gray-800 rounded p-2">
          <span className="text-gray-400">Resolution:</span>
          <span className="text-white ml-2">1920x1080</span>
        </div>
        <div className="bg-gray-800 rounded p-2">
          <span className="text-gray-400">Latency:</span>
          <span className="text-white ml-2">12ms</span>
        </div>
      </div>
    </div>
  );
};

export default PythonVisualIntegration;