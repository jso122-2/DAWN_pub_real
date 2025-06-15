# 🔌 Connect Port 3000 App to DAWN Tick Engine

## 🎯 Overview
Your setup:
- **Frontend**: `http://localhost:3000` (React app)
- **Backend**: `http://localhost:8000` (Python tick engine)
- **WebSocket**: `ws://localhost:8000/ws` (tick data stream)

## 📝 Step 1: Create WebSocket Service

Create a new file in your port 3000 app:

```javascript
// src/services/TickEngineService.js

class TickEngineService {
  constructor() {
    this.ws = null;
    this.listeners = new Set();
    this.connectionStatus = 'disconnected';
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 3000;
    this.tickData = null;
    this.tickRate = 0;
    this.lastTickTime = null;
    this.tickCount = 0;
  }

  connect() {
    console.log('🔌 Connecting to DAWN Tick Engine...');
    
    try {
      // Connect to your Python backend
      this.ws = new WebSocket('ws://localhost:8000/ws');
      
      this.ws.onopen = () => {
        console.log('✅ Connected to DAWN Tick Engine!');
        this.connectionStatus = 'connected';
        this.reconnectAttempts = 0;
        this.notifyListeners('connection', { status: 'connected' });
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleTickData(data);
        } catch (error) {
          console.error('Failed to parse tick data:', error);
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('❌ WebSocket Error:', error);
        this.connectionStatus = 'error';
        this.notifyListeners('error', error);
      };
      
      this.ws.onclose = () => {
        console.log('🔌 Disconnected from DAWN Tick Engine');
        this.connectionStatus = 'disconnected';
        this.notifyListeners('connection', { status: 'disconnected' });
        this.attemptReconnect();
      };
      
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      this.attemptReconnect();
    }
  }
  
  handleTickData(data) {
    // Update tick rate calculation
    const now = Date.now();
    if (this.lastTickTime) {
      const timeDiff = now - this.lastTickTime;
      this.tickRate = 1000 / timeDiff; // Hz
    }
    this.lastTickTime = now;
    this.tickCount++;
    
    // Store tick data
    this.tickData = {
      ...data,
      tickRate: this.tickRate,
      totalTicks: this.tickCount,
      timestamp: now
    };
    
    // Notify all listeners
    this.notifyListeners('tick', this.tickData);
  }
  
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 Reconnecting... Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      setTimeout(() => this.connect(), this.reconnectDelay);
    } else {
      console.error('❌ Max reconnection attempts reached');
      this.notifyListeners('error', { message: 'Connection failed after max attempts' });
    }
  }
  
  // Subscribe to updates
  subscribe(callback) {
    this.listeners.add(callback);
    
    // Send current state immediately
    if (this.connectionStatus === 'connected' && this.tickData) {
      callback('tick', this.tickData);
    }
    callback('connection', { status: this.connectionStatus });
    
    // Return unsubscribe function
    return () => {
      this.listeners.delete(callback);
    };
  }
  
  notifyListeners(type, data) {
    this.listeners.forEach(callback => {
      try {
        callback(type, data);
      } catch (error) {
        console.error('Listener error:', error);
      }
    });
  }
  
  // Get current state
  getState() {
    return {
      connectionStatus: this.connectionStatus,
      tickData: this.tickData,
      tickRate: this.tickRate,
      tickCount: this.tickCount
    };
  }
  
  // Manual disconnect
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// Create singleton instance
const tickEngineService = new TickEngineService();

export default tickEngineService;
```

## 📝 Step 2: Create React Hook for Easy Usage

```javascript
// src/hooks/useTickEngine.js

import { useState, useEffect } from 'react';
import tickEngineService from '../services/TickEngineService';

export function useTickEngine() {
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [tickData, setTickData] = useState(null);
  const [tickRate, setTickRate] = useState(0);
  const [tickCount, setTickCount] = useState(0);
  
  useEffect(() => {
    // Subscribe to tick engine updates
    const unsubscribe = tickEngineService.subscribe((type, data) => {
      switch (type) {
        case 'connection':
          setConnectionStatus(data.status);
          break;
          
        case 'tick':
          setTickData(data);
          setTickRate(data.tickRate || 0);
          setTickCount(data.totalTicks || 0);
          break;
          
        case 'error':
          console.error('Tick Engine Error:', data);
          break;
      }
    });
    
    // Connect to tick engine
    tickEngineService.connect();
    
    // Cleanup
    return () => {
      unsubscribe();
    };
  }, []);
  
  return {
    connectionStatus,
    tickData,
    tickRate,
    tickCount,
    isConnected: connectionStatus === 'connected'
  };
}
```

## 📝 Step 3: Update Your Consciousness Page

```javascript
// src/pages/ConsciousnessPage.jsx (or wherever your component is)

import React, { useEffect, useRef, useState } from 'react';
import { useTickEngine } from '../hooks/useTickEngine';
import './ConsciousnessPage.css';

const ConsciousnessMatrix = () => {
  const { connectionStatus, tickData, tickRate, tickCount, isConnected } = useTickEngine();
  const canvasRef = useRef(null);
  const animationRef = useRef();
  const [isInitializing, setIsInitializing] = useState(true);
  
  // Initialize canvas when connected
  useEffect(() => {
    if (isConnected) {
      setTimeout(() => setIsInitializing(false), 1000);
    }
  }, [isConnected]);
  
  // Animate consciousness visualization
  useEffect(() => {
    if (!canvasRef.current || !tickData || isInitializing) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    const animate = () => {
      // Clear canvas
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      
      // Draw consciousness orb based on SCUP
      const radius = 50 + (tickData.scup * 100);
      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
      
      // Color based on mood
      const moodColors = {
        analytical: ['#0088ff', '#00aaff'],
        confident: ['#00ff88', '#00ffaa'],
        focused: ['#ffaa00', '#ffcc00'],
        creative: ['#ff00aa', '#ff00cc']
      };
      
      const colors = moodColors[tickData.mood] || moodColors.analytical;
      gradient.addColorStop(0, colors[0]);
      gradient.addColorStop(0.5, `${colors[1]}88`);
      gradient.addColorStop(1, 'transparent');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw entropy particles
      const particleCount = Math.floor(tickData.entropy * 100);
      for (let i = 0; i < particleCount; i++) {
        const angle = (i / particleCount) * Math.PI * 2;
        const distance = radius + 20 + Math.random() * 50;
        const x = centerX + Math.cos(angle) * distance;
        const y = centerY + Math.sin(angle) * distance;
        
        ctx.fillStyle = `rgba(255, 0, 170, ${0.5 - tickData.entropy * 0.5})`;
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fill();
      }
      
      // Draw neural connections
      ctx.strokeStyle = `rgba(0, 255, 136, ${tickData.scup * 0.3})`;
      ctx.lineWidth = 1;
      
      for (let i = 0; i < 8; i++) {
        const angle = (i / 8) * Math.PI * 2;
        const x1 = centerX + Math.cos(angle) * (radius * 0.8);
        const y1 = centerY + Math.sin(angle) * (radius * 0.8);
        const x2 = centerX + Math.cos(angle + Math.PI / 4) * radius;
        const y2 = centerY + Math.sin(angle + Math.PI / 4) * radius;
        
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.quadraticCurveTo(centerX, centerY, x2, y2);
        ctx.stroke();
      }
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [tickData, isInitializing]);
  
  return (
    <div className="consciousness-page">
      <div className="header">
        <h1>Consciousness <span className="matrix">Matrix</span></h1>
        <p>Real-time neural activity visualization and analysis</p>
      </div>
      
      <div className="main-content">
        <div className="canvas-section">
          <h2>Neural Activity Monitor</h2>
          
          {isInitializing ? (
            <div className="initializing">
              <div className="loading-pulse"></div>
              <p>Initializing Canvas...</p>
            </div>
          ) : (
            <canvas
              ref={canvasRef}
              width={800}
              height={600}
              className="consciousness-canvas"
            />
          )}
        </div>
        
        <div className="sidebar">
          <div className="connection-panel">
            <h3>Connection Status</h3>
            <div className="status-grid">
              <div className="status-item">
                <span className="label">Status:</span>
                <span className={`value ${connectionStatus}`}>
                  {connectionStatus === 'connected' ? '🟢' : '🔴'} {connectionStatus}
                </span>
              </div>
              <div className="status-item">
                <span className="label">Tick Rate:</span>
                <span className="value">{tickRate.toFixed(2)} Hz</span>
              </div>
              <div className="status-item">
                <span className="label">Total Ticks:</span>
                <span className="value">{tickCount}</span>
              </div>
              <div className="status-item">
                <span className="label">Session:</span>
                <span className="value">{new Date().toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
          
          {tickData && (
            <div className="metrics-panel">
              <h3>Consciousness Metrics</h3>
              <div className="metric">
                <span className="label">SCUP:</span>
                <div className="metric-bar">
                  <div 
                    className="metric-fill scup"
                    style={{ width: `${tickData.scup * 100}%` }}
                  />
                </div>
                <span className="value">{(tickData.scup * 100).toFixed(1)}%</span>
              </div>
              
              <div className="metric">
                <span className="label">Entropy:</span>
                <div className="metric-bar">
                  <div 
                    className="metric-fill entropy"
                    style={{ width: `${tickData.entropy * 100}%` }}
                  />
                </div>
                <span className="value">{tickData.entropy.toFixed(3)}</span>
              </div>
              
              <div className="metric">
                <span className="label">Heat:</span>
                <div className="metric-bar">
                  <div 
                    className="metric-fill heat"
                    style={{ width: `${tickData.heat * 100}%` }}
                  />
                </div>
                <span className="value">{tickData.heat.toFixed(3)}</span>
              </div>
              
              <div className="metric mood">
                <span className="label">Mood:</span>
                <span className={`value mood-${tickData.mood}`}>
                  {tickData.mood.toUpperCase()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConsciousnessMatrix;
```

## 📝 Step 4: Add Global Access (Optional)

If you need to access tick data from anywhere in your app:

```javascript
// src/App.js - Add this to your root component

import { useEffect } from 'react';
import tickEngineService from './services/TickEngineService';

function App() {
  useEffect(() => {
    // Make tick engine globally accessible for debugging
    window.tickEngine = tickEngineService;
    
    // Auto-connect on app start
    tickEngineService.connect();
    
    return () => {
      tickEngineService.disconnect();
    };
  }, []);
  
  // Rest of your app...
}
```

## 🚀 Quick Start

1. **Start your Python backend**:
   ```bash
   cd Tick_engine
   python start_api_fixed.py
   ```

2. **Add the service to your React app** (port 3000)

3. **Import and use the hook** in any component:
   ```javascript
   const { tickData, isConnected } = useTickEngine();
   ```

4. **Check browser console** for connection logs:
   ```
   🔌 Connecting to DAWN Tick Engine...
   ✅ Connected to DAWN Tick Engine!
   ```

## 🔧 Troubleshooting

### If connection fails:
1. Check Python backend is running: `curl http://localhost:8000/`
2. Test WebSocket: `wscat -c ws://localhost:8000/ws`
3. Check browser console for errors
4. Ensure no CORS issues (add CORS middleware to FastAPI if needed)

### Test in browser console:
```javascript
// Manual test
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

## 🎯 Result

Once connected, your Consciousness page will:
- Show "🟢 connected" status
- Display live tick rate (~2 Hz)
- Update canvas with real consciousness data
- Show SCUP, entropy, heat, and mood in real-time

This connects your beautiful port 3000 interface directly to your DAWN tick engine! 🚀
