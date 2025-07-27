# 🔧 Fix Consciousness Page Connection Issues

## 🔴 The Problem
Your Consciousness page is:
1. **Stuck on "Initializing Canvas..."**
2. **Connection Status: Disconnected**
3. **Tick Rate: 0.00 Hz**

## ✅ Quick Fixes

### 1. **Check if Backend is Running**
```bash
# Terminal 1: Make sure your Python backend is running
cd Tick_engine
python start_api_fixed.py

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     WebSocket endpoint ready at ws://localhost:8000/ws
```

### 2. **Fix WebSocket Connection in Frontend**

Find your WebSocket connection code and update it:

```javascript
// src/services/WebSocketService.js or similar

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
  }

  connect() {
    try {
      // Make sure this matches your backend!
      this.ws = new WebSocket('ws://localhost:8000/ws');
      
      this.ws.onopen = () => {
        console.log('✅ WebSocket Connected!');
        this.reconnectAttempts = 0;
        // Update UI to show connected status
        this.updateConnectionStatus('Connected');
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📊 Received tick data:', data);
          this.handleTickData(data);
        } catch (error) {
          console.error('Failed to parse message:', error);
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('❌ WebSocket Error:', error);
        this.updateConnectionStatus('Error');
      };
      
      this.ws.onclose = () => {
        console.log('🔌 WebSocket Disconnected');
        this.updateConnectionStatus('Disconnected');
        this.attemptReconnect();
      };
      
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      this.attemptReconnect();
    }
  }
  
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 Reconnecting... Attempt ${this.reconnectAttempts}`);
      setTimeout(() => this.connect(), this.reconnectDelay);
    }
  }
  
  updateConnectionStatus(status) {
    // Update your UI component
    // This depends on your state management
    if (window.updateConnectionStatus) {
      window.updateConnectionStatus(status);
    }
  }
  
  handleTickData(data) {
    // Update your consciousness visualization
    if (window.updateConsciousnessData) {
      window.updateConsciousnessData(data);
    }
  }
}

// Create and export singleton
export const webSocketService = new WebSocketService();
```

### 3. **Fix the Consciousness Component**

Update your Consciousness component to properly handle connection:

```javascript
// ConsciousnessPage.jsx or similar

import React, { useEffect, useState, useRef } from 'react';
import { webSocketService } from '../services/WebSocketService';

const ConsciousnessMatrix = () => {
  const [connectionStatus, setConnectionStatus] = useState('Disconnected');
  const [tickRate, setTickRate] = useState(0);
  const [totalTicks, setTotalTicks] = useState(0);
  const [isCanvasReady, setIsCanvasReady] = useState(false);
  const canvasRef = useRef(null);
  
  useEffect(() => {
    // Set up global functions for WebSocket to call
    window.updateConnectionStatus = (status) => {
      setConnectionStatus(status);
      if (status === 'Connected') {
        setIsCanvasReady(true);
      }
    };
    
    window.updateConsciousnessData = (data) => {
      // Update your visualization with tick data
      console.log('Updating consciousness viz with:', data);
      setTotalTicks(data.tick_count || 0);
      
      // Calculate tick rate
      // ... your tick rate calculation
      
      // Update canvas visualization
      if (canvasRef.current && isCanvasReady) {
        updateCanvasVisualization(data);
      }
    };
    
    // Connect to WebSocket
    webSocketService.connect();
    
    // Cleanup
    return () => {
      window.updateConnectionStatus = null;
      window.updateConsciousnessData = null;
    };
  }, []);
  
  const updateCanvasVisualization = (data) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw based on consciousness data
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    // Draw consciousness orb
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 100);
    gradient.addColorStop(0, `rgba(0, 255, 136, ${data.scup || 0.5})`);
    gradient.addColorStop(0.5, `rgba(0, 255, 136, ${(data.scup || 0.5) * 0.5})`);
    gradient.addColorStop(1, 'rgba(0, 255, 136, 0)');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 100, 0, Math.PI * 2);
    ctx.fill();
    
    // Add more visualization based on your data
  };
  
  return (
    <div className="consciousness-matrix">
      <h1>Consciousness Matrix</h1>
      <p>Real-time neural activity visualization and analysis</p>
      
      <div className="canvas-container">
        {!isCanvasReady ? (
          <div className="initializing">
            <div className="loading-orb"></div>
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
      
      <div className="connection-status">
        <h3>Connection Status</h3>
        <p>Status: <span className={connectionStatus.toLowerCase()}>{connectionStatus}</span></p>
        <p>Tick Rate: {tickRate.toFixed(2)} Hz</p>
        <p>Total Ticks: {totalTicks}</p>
        <p>Session: {new Date().toLocaleTimeString()}</p>
      </div>
    </div>
  );
};
```

### 4. **Debug in Browser Console**

Open browser DevTools (F12) and check:

```javascript
// Check if WebSocket is connecting
// You should see logs like:
// ✅ WebSocket Connected!
// 📊 Received tick data: {scup: 0.75, entropy: 0.3, ...}

// If you see errors, check:
// 1. Is backend running?
// 2. Is the WebSocket URL correct?
// 3. Any CORS issues?
```

### 5. **Common Issues & Solutions**

#### **Issue: "WebSocket connection to 'ws://localhost:8000/ws' failed"**
```bash
# Solution 1: Check if backend is running
curl http://localhost:8000/
# Should return something, not "connection refused"

# Solution 2: Test WebSocket directly
wscat -c ws://localhost:8000/ws
# Should connect and show tick data
```

#### **Issue: CORS Errors**
```python
# In your start_api_fixed.py, add CORS middleware:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Issue: Canvas Stuck Initializing**
```javascript
// Add timeout to show error if connection fails
useEffect(() => {
  const timeout = setTimeout(() => {
    if (connectionStatus === 'Disconnected') {
      setIsCanvasReady(true); // Show canvas anyway
      console.error('Connection timeout - showing offline mode');
    }
  }, 5000);
  
  return () => clearTimeout(timeout);
}, [connectionStatus]);
```

## 🚀 Quick Test

1. **Start Backend**:
   ```bash
   cd Tick_engine
   python start_api_fixed.py
   ```

2. **Check Connection**:
   ```bash
   # In another terminal
   curl http://localhost:8000/
   wscat -c ws://localhost:8000/ws
   ```

3. **Refresh Frontend**:
   - Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
   - Check console for connection logs

## 🎯 Expected Result

Once connected, you should see:
- ✅ **Status: Connected** (green)
- ✅ **Tick Rate: ~2.00 Hz**
- ✅ **Total Ticks: increasing number**
- ✅ **Canvas showing animated consciousness visualization**

## 💡 Alternative: Mock Data for Testing

If backend connection is still problematic, add mock data:

```javascript
// Add this to test visualization without backend
const mockTickData = () => {
  const mockData = {
    scup: Math.random(),
    entropy: Math.random(),
    heat: Math.random(),
    mood: ['analytical', 'confident', 'focused', 'creative'][Math.floor(Math.random() * 4)],
    tick_count: totalTicks + 1,
    timestamp: Date.now()
  };
  
  window.updateConsciousnessData(mockData);
};

// Use mock data if not connected
useEffect(() => {
  if (connectionStatus === 'Disconnected') {
    const interval = setInterval(mockTickData, 500);
    return () => clearInterval(interval);
  }
}, [connectionStatus, totalTicks]);
```

This will at least show the visualization working while you debug the connection!