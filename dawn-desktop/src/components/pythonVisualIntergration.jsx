import React, { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

const PythonVisualIntegration = ({ activeProcesses }) => {
  const [videoStream, setVideoStream] = useState(null);
  const [detectionResults, setDetectionResults] = useState([]);
  const [depthMap, setDepthMap] = useState(null);
  const [pointCloud, setPointCloud] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [streamUrl, setStreamUrl] = useState('');
  
  // Debug state
  const [debugInfo, setDebugInfo] = useState({
    backendHealth: null,
    lastError: null,
    connectionAttempts: 0,
    wsEvents: [],
    httpTests: [],
    corsStatus: 'unknown',
    ngrokStatus: 'unknown'
  });
  const [showDebugPanel, setShowDebugPanel] = useState(false);
  
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

  // WebSocket connection for real-time data
  useEffect(() => {
    const connectWebSocket = () => {
      const wsUrl = window.location.hostname === 'localhost'
        ? 'ws://localhost:8081/cv-stream'
        : `wss://${window.location.hostname}/cv-stream`;

      try {
        wsRef.current = new WebSocket(wsUrl);
        
        wsRef.current.onopen = () => {
          setConnectionStatus('connected');
          console.log('Connected to Python CV backend');
        };

        wsRef.current.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            handleIncomingData(data);
          } catch (error) {
            console.error('Failed to parse WebSocket data:', error);
          }
        };

        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
          setConnectionStatus('error');
        };

        wsRef.current.onclose = () => {
          setConnectionStatus('disconnected');
          // Reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };
      } catch (error) {
        console.error('Failed to create WebSocket:', error);
        setConnectionStatus('error');
      }
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
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

  // Control Python processes via Tauri
  const sendCommand = async (command, params = {}) => {
    try {
      const result = await invoke('send_cv_command', { command, params });
      console.log('Command result:', result);
    } catch (error) {
      console.error('Failed to send command:', error);
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