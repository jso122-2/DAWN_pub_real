import React, { useState, useEffect, useRef } from 'react';
import eventBus from '../../lib/eventBus';
import { motion } from 'framer-motion';

// TypeScript interfaces
interface Process {
  id: string;
  name: string;
  enabled: boolean;
  script?: string;
  streamUrl?: string;
}

interface DetectionResult {
  x: number;
  y: number;
  width: number;
  height: number;
  class: string;
  confidence: number;
}

interface PythonVisualIntegrationProps {
  activeProcesses: Process[];
}

const PythonVisualIntegration: React.FC<PythonVisualIntegrationProps> = ({ activeProcesses }) => {
  const [showDebugPanel, setShowDebugPanel] = useState(false);
  const [videoStream, setVideoStream] = useState<string | null>(null);
  const [detectionResults, setDetectionResults] = useState<DetectionResult[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'error' | 'connecting'>('disconnected');
  const [streamUrl, setStreamUrl] = useState('');
  const [debugLogs, setDebugLogs] = useState<string[]>([]);

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Set stream URL based on active processes
  useEffect(() => {
    const baseUrl = window.location.hostname === 'localhost' 
      ? 'http://localhost:8001'
      : `https://${window.location.hostname}`;
    const activeStreamUrl = activeProcesses.find(p => p.enabled && p.script)?.streamUrl;
    if (activeStreamUrl) {
      setStreamUrl(`${baseUrl}${activeStreamUrl}`);
    }
  }, [activeProcesses]);

  // WebSocket eventBus integration
  useEffect(() => {
    setConnectionStatus('connecting');
    const handleDetection = (event: CustomEvent) => {
      setDetectionResults(event.detail.detections || []);
      setConnectionStatus('connected');
      setDebugLogs(logs => [...logs, `[ws] Detection event received (${event.detail.detections?.length || 0})`].slice(-100));
    };
    const handleError = (event: CustomEvent) => {
      setConnectionStatus('error');
      setDebugLogs(logs => [...logs, `[ws] Error: ${event.detail?.error || 'Unknown error'}`].slice(-100));
    };
    eventBus.addEventListener('detection', handleDetection as EventListener);
    eventBus.addEventListener('error', handleError as EventListener);
    return () => {
      eventBus.removeEventListener('detection', handleDetection as EventListener);
      eventBus.removeEventListener('error', handleError as EventListener);
    };
  }, []);

  // Draw detection boxes on canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    detectionResults.forEach(detection => {
      const { x, y, width, height, class: className, confidence } = detection;
      ctx.strokeStyle = '#a78bfa';
      ctx.lineWidth = 2;
      ctx.shadowColor = '#a78bfa';
      ctx.shadowBlur = 10;
      ctx.strokeRect(x, y, width, height);
      ctx.shadowBlur = 0;
      ctx.fillStyle = '#a78bfa';
      ctx.font = '16px monospace';
      ctx.fillText(
        `${className} ${(confidence * 100).toFixed(1)}%`,
        x, y - 5
      );
    });
  }, [detectionResults]);

  // Modern control button style
  const controlButton = 'px-3 py-2 bg-gradient-to-r from-purple-600 to-pink-500 text-white rounded-lg shadow-glow-md hover:from-pink-500 hover:to-purple-600 transition-colors font-semibold';

  return (
    <div className="glass rounded-xl p-6 shadow-glow-md border border-purple-500/20 backdrop-blur-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-purple-300 flex items-center">
          <span className="w-3 h-3 bg-gradient-to-r from-cyan-400 via-pink-400 to-purple-400 rounded-full mr-2 animate-pulse" />
          Python CV Visual Output
        </h3>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full animate-pulse ${
              connectionStatus === 'connected' ? 'bg-gradient-to-r from-cyan-400 to-purple-400' : 
              connectionStatus === 'error' ? 'bg-pink-500' : 'bg-yellow-400'
            }`} />
            <span className="text-sm text-gray-400">
              {connectionStatus === 'connected' ? 'Connected' : 
               connectionStatus === 'error' ? 'Error' : 'Connecting...'}
            </span>
          </div>
          <button
            onClick={() => setShowDebugPanel(!showDebugPanel)}
            className="px-3 py-1 rounded-lg text-xs font-mono bg-gradient-to-r from-yellow-500 to-pink-500 text-white hover:from-pink-500 hover:to-yellow-500 transition-colors"
          >
            DEBUG
          </button>
        </div>
      </div>

      {/* Video Display Area */}
      <div className="relative glass rounded-xl overflow-hidden mb-4 shadow-glow-md border-2 border-purple-500/40">
        {streamUrl ? (
          <>
            <video
              ref={videoRef}
              className="w-full h-auto"
              autoPlay
              muted
              playsInline
              src={streamUrl}
              onError={(e) => setConnectionStatus('error')}
            />
            <canvas
              ref={canvasRef}
              className="absolute top-0 left-0 w-full h-full pointer-events-none"
            />
          </>
        ) : (
          <div className="flex items-center justify-center h-96 text-purple-300">
            <div className="text-center">
              <p className="text-lg mb-2">No active video stream</p>
              <p className="text-sm">Start a Python CV process to see output</p>
            </div>
          </div>
        )}
      </div>

      {/* Detection Results */}
      {detectionResults.length > 0 && (
        <div className="glass rounded-lg p-4 mb-4 border border-purple-500/20">
          <h4 className="text-sm font-bold text-purple-300 mb-2">Detections</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {detectionResults.slice(0, 8).map((detection, idx) => (
              <div key={idx} className="glass rounded p-2 text-xs border border-purple-500/20">
                <span className="text-cyan-400">{detection.class}</span>
                <span className="text-gray-400 ml-2">
                  {(detection.confidence * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Control Panel */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-4">
        <button className={controlButton} onClick={() => eventBus.dispatchEvent(new CustomEvent('toggle-detection'))}>
          Toggle Detection
        </button>
        <button className={controlButton} onClick={() => eventBus.dispatchEvent(new CustomEvent('toggle-tracking'))}>
          Toggle Tracking
        </button>
        <button className={controlButton} onClick={() => eventBus.dispatchEvent(new CustomEvent('toggle-depth'))}>
          Toggle Depth
        </button>
        <button className={controlButton} onClick={() => eventBus.dispatchEvent(new CustomEvent('capture-frame'))}>
          Capture Frame
        </button>
      </div>

      {/* Debug Panel */}
      {showDebugPanel && (
        <div className="mt-4 glass rounded-lg p-4 border border-yellow-500">
          <h4 className="text-sm font-bold text-yellow-400 font-mono mb-2">🔍 CV Debug Panel</h4>
          <div className="max-h-40 overflow-y-auto text-xs font-mono text-gray-300">
            {debugLogs.slice(-20).map((log, idx) => (
              <div key={idx} className="mb-1">
                {log}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PythonVisualIntegration;