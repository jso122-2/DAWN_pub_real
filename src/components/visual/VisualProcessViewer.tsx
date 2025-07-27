import React, { useEffect, useRef, useState } from 'react';
import { useWebSocket } from '../../hooks/useWebSocket';

interface ProcessMetadata {
  name: string;
  is_active: boolean;
  fps: number;
  frame_count: number;
  last_update: number;
  [key: string]: any;
}

interface VisualProcessViewerProps {
  processName: string;
  width?: number;
  height?: number;
  className?: string;
}

export const VisualProcessViewer: React.FC<VisualProcessViewerProps> = ({
  processName,
  width = 800,
  height = 600,
  className = ''
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [metadata, setMetadata] = useState<ProcessMetadata | null>(null);
  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // WebSocket connection for real-time updates
  const { send, lastMessage, isConnected } = useWebSocket();

  // Request frame updates
  useEffect(() => {
    if (isConnected && isActive) {
      const interval = setInterval(() => {
        send({
          type: 'capture_frame',
          process: processName
        });
      }, 1000 / 30); // 30 FPS

      return () => clearInterval(interval);
    }
  }, [isConnected, isActive, processName, send]);

  // Handle incoming frames
  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage);
        if (data.type === 'frame' && data.process === processName) {
          // Update canvas with new frame
          const canvas = canvasRef.current;
          if (canvas) {
            const ctx = canvas.getContext('2d');
            if (ctx) {
              const img = new Image();
              img.onload = () => {
                ctx.drawImage(img, 0, 0, width, height);
              };
              img.src = `data:image/png;base64,${data.frame}`;
            }
          }
        } else if (data.type === 'error') {
          setError(data.message);
        }
      } catch (e) {
        console.error('Error processing WebSocket message:', e);
      }
    }
  }, [lastMessage, processName, width, height]);

  // Fetch process metadata
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const response = await fetch(`/api/processes/${processName}`);
        if (response.ok) {
          const data = await response.json();
          setMetadata(data.data);
          setIsActive(data.data.is_active);
        } else {
          setError('Failed to fetch process metadata');
        }
      } catch (e) {
        setError('Error fetching process metadata');
      }
    };

    fetchMetadata();
    const interval = setInterval(fetchMetadata, 1000);
    return () => clearInterval(interval);
  }, [processName]);

  // Toggle process state
  const toggleProcess = async () => {
    try {
      const response = await fetch(`/api/processes/${processName}/${isActive ? 'stop' : 'start'}`, {
        method: 'POST'
      });
      if (response.ok) {
        setIsActive(!isActive);
      } else {
        setError(`Failed to ${isActive ? 'stop' : 'start'} process`);
      }
    } catch (e) {
      setError(`Error ${isActive ? 'stopping' : 'starting'} process`);
    }
  };

  return (
    <div className={`terminal-module ${className}`}>
      <div className="module-header">
        <div className="flex justify-between items-center">
          <h3 className="text-white/80 text-sm font-mono">{processName}</h3>
          <div className="flex items-center space-x-2">
            <div className={`status-indicator ${isActive ? 'online' : 'offline'}`} />
            <span className="text-xs text-white/60">
              {isActive ? 'ACTIVE' : 'INACTIVE'}
            </span>
          </div>
        </div>
      </div>

      <div className="relative">
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          className="w-full h-auto bg-black rounded"
        />
        
        {error && (
          <div className="terminal-alert error mt-2">
            {error}
          </div>
        )}

        {metadata && (
          <div className="mt-2 space-y-1">
            <div className="metric">
              <span className="metric-label">FPS</span>
              <span className="metric-value">{metadata.fps.toFixed(1)}</span>
            </div>
            <div className="metric">
              <span className="metric-label">Frames</span>
              <span className="metric-value">{metadata.frame_count}</span>
            </div>
            {Object.entries(metadata)
              .filter(([key]) => !['name', 'is_active', 'fps', 'frame_count', 'last_update'].includes(key))
              .map(([key, value]) => (
                <div key={key} className="metric">
                  <span className="metric-label">{key}</span>
                  <span className="metric-value">
                    {typeof value === 'number' ? value.toFixed(2) : String(value)}
                  </span>
                </div>
              ))}
          </div>
        )}

        <div className="mt-4 flex justify-end">
          <button
            onClick={toggleProcess}
            className={`px-4 py-2 rounded text-sm font-mono transition-colors ${
              isActive
                ? 'bg-red-500/20 text-red-300 hover:bg-red-500/30'
                : 'bg-green-500/20 text-green-300 hover:bg-green-500/30'
            }`}
          >
            {isActive ? 'STOP' : 'START'}
          </button>
        </div>
      </div>
    </div>
  );
}; 