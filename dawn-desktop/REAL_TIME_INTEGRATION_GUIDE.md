# 🧠 Real-time Consciousness Data Integration Guide

## Overview

The DAWN application now supports real-time WebSocket integration for consciousness data visualization. This allows the consciousness visualizer to display live tick data from your backend systems instead of simulated data.

## 🚀 Quick Start

### 1. Start the Test WebSocket Server

```bash
cd python
python websocket_consciousness_server.py
```

The server will start on `ws://localhost:8000` and begin broadcasting consciousness data at 60 FPS.

### 2. Start the Frontend

```bash
cd dawn-desktop
npm run dev
```

### 3. Test the Integration

1. Navigate to `/consciousness` in the DAWN app
2. Check the **Real-time Data Panel** (bottom-left in development mode)
3. Click **Connect WS** to establish connection
4. You should see the status change to "Connected" and real-time data flowing

## 🔧 Integration Components

### Frontend Components

#### `ConsciousnessDataService`
- **Location**: `src/services/ConsciousnessDataService.ts`
- **Purpose**: Manages WebSocket connection and data processing
- **Features**:
  - Automatic reconnection
  - Data smoothing and validation
  - SCUP calculation
  - Mood determination

#### `useRealTimeConsciousness`
- **Location**: `src/hooks/useRealTimeConsciousness.ts`
- **Purpose**: React hook providing real-time consciousness data
- **Features**:
  - Automatic fallback to simulated data
  - Connection status monitoring
  - Cosmic store integration

#### `RealTimeDataPanel`
- **Location**: `src/components/debug/RealTimeDataPanel.tsx`
- **Purpose**: Debug panel for monitoring and testing
- **Features**:
  - Connection status display
  - Manual test data injection
  - Preset consciousness states
  - WebSocket controls

### Backend Server

#### `websocket_consciousness_server.py`
- **Location**: `python/websocket_consciousness_server.py`
- **Purpose**: Test WebSocket server for consciousness data
- **Features**:
  - Realistic data generation patterns
  - 60 FPS tick rate
  - Multiple client support
  - Heartbeat monitoring

## 📡 WebSocket Protocol

### Message Types

#### From Frontend to Backend

```typescript
// Request initial data
{
  type: 'request_consciousness_data',
  subscribe: true,
  timestamp: 1234567890
}

// Heartbeat
{
  type: 'heartbeat',
  timestamp: 1234567890
}
```

#### From Backend to Frontend

```typescript
// Tick data (sent at 60 FPS)
{
  type: 'tick_data',
  data: {
    timestamp: 1234567890,
    entropy: 0.5,          // 0-1
    neuralActivity: 0.7,   // 0-1
    quantumCoherence: 0.6, // 0-1
    systemLoad: 0.3,       // 0-1
    scup: 60.0,           // 0-100 (calculated)
    mood: 'active',       // string
    performance: {
      fps: 60,
      latency: 15,
      memoryUsage: 0.4
    }
  },
  timestamp: 1234567890
}

// Direct consciousness update
{
  type: 'consciousness_update',
  data: { /* same as tick_data.data */ },
  timestamp: 1234567890
}

// Heartbeat response
{
  type: 'heartbeat_response',
  timestamp: 1234567890
}
```

## 🎛️ Configuration

### WebSocket Connection

Edit `src/services/websocket/WebSocketService.ts`:

```typescript
export const mainWebSocket = new WebSocketService({
  url: 'ws://your-backend:8000/ws',  // Change this URL
  reconnectInterval: 1000,
  maxReconnectAttempts: 5,
  heartbeatInterval: 30000,
});
```

### Data Processing

Edit `src/services/ConsciousnessDataService.ts`:

```typescript
private calculateConsciousnessMetrics(tickData: TickData): ConsciousnessMetrics {
  // Customize how raw tick data is converted to consciousness metrics
  // Add your own SCUP calculation logic here
  // Implement custom mood determination
}
```

## 🧪 Testing Features

### Test Data Panel

The Real-time Data Panel (development mode only) provides:

- **Connection Status**: Shows WebSocket connection state
- **Current Metrics**: Real-time display of consciousness values
- **Test Controls**: 
  - Start/Stop automated random data generation
  - Manual random data injection
  - Preset consciousness states (calm, active, critical, chaotic, euphoric)
- **WebSocket Controls**: Manual connect/disconnect

### Preset States

| Preset | Entropy | Neural | Quantum | Load | Mood |
|--------|---------|--------|---------|------|------|
| Calm | 0.2 | 0.3 | 0.8 | 0.1 | serene |
| Active | 0.6 | 0.8 | 0.7 | 0.4 | excited |
| Critical | 0.9 | 0.9 | 0.3 | 0.9 | critical |
| Chaotic | 0.95 | 0.6 | 0.2 | 0.7 | chaotic |
| Euphoric | 0.3 | 0.9 | 0.9 | 0.2 | euphoric |

## 🔌 Integration with Your System

### Connect to Existing Backend

1. **Update WebSocket URL**: Point to your existing WebSocket endpoint
2. **Implement Data Mapping**: Convert your system's data format to the expected schema
3. **Add Authentication**: Extend the WebSocket service for authentication if needed

### Custom Data Sources

Create a custom data service by extending `ConsciousnessDataService`:

```typescript
class CustomConsciousnessDataService extends ConsciousnessDataService {
  constructor() {
    super();
    // Connect to your custom data source
    this.connectToCustomSource();
  }
  
  private connectToCustomSource() {
    // Your custom connection logic
  }
}
```

### Backend Integration Example

```python
# In your existing Python backend
import asyncio
import websockets
import json

async def send_consciousness_data(websocket):
    while True:
        # Get data from your system
        data = get_system_consciousness_metrics()
        
        # Send in expected format
        message = {
            'type': 'tick_data',
            'data': {
                'timestamp': int(time.time() * 1000),
                'entropy': data.entropy,
                'neuralActivity': data.neural_activity,
                'quantumCoherence': data.quantum_coherence,
                'systemLoad': data.system_load,
                'mood': data.mood
            },
            'timestamp': int(time.time() * 1000)
        }
        
        await websocket.send(json.dumps(message))
        await asyncio.sleep(1/60)  # 60 FPS
```

## 🐛 Troubleshooting

### Connection Issues

1. **Check WebSocket URL**: Ensure the URL in `WebSocketService.ts` matches your server
2. **CORS Issues**: Make sure your WebSocket server allows connections from your frontend domain
3. **Firewall**: Verify port 8000 (or your custom port) is accessible

### Data Issues

1. **Invalid Data Format**: Check browser console for parsing errors
2. **Missing Properties**: Ensure all required fields are present in tick data
3. **Value Ranges**: Verify values are within expected ranges (0-1 for most metrics)

### Performance Issues

1. **Too High Frequency**: Reduce tick rate if causing performance issues
2. **Memory Leaks**: Check for proper cleanup of WebSocket connections
3. **Large Payloads**: Minimize data payload size for better performance

## 📊 Monitoring

### Connection Status

Monitor connection health using:

```typescript
const status = consciousnessDataService.getConnectionStatus();
console.log('Connected:', status.connected);
console.log('Last Update:', status.lastUpdate);
console.log('Buffer Size:', status.bufferSize);
```

### Data Quality

Check data quality in the Real-time Data Panel:
- **Update Frequency**: Should be ~60 updates per second
- **Value Ranges**: Metrics should be within 0-1 range
- **Mood Changes**: Mood should update based on metric values

## 🎯 Next Steps

1. **Production Setup**: Configure for production WebSocket endpoints
2. **Authentication**: Add user authentication for WebSocket connections
3. **Data Persistence**: Store historical consciousness data
4. **Alerts**: Set up alerts for critical consciousness states
5. **Analytics**: Add consciousness pattern analysis and reporting

## 🔗 Related Files

- `src/services/ConsciousnessDataService.ts` - Main data service
- `src/hooks/useRealTimeConsciousness.ts` - React hook
- `src/components/debug/RealTimeDataPanel.tsx` - Debug panel
- `python/websocket_consciousness_server.py` - Test server
- `src/services/websocket/WebSocketService.ts` - WebSocket client

---

**🧠 Your consciousness visualizer is now connected to the real world!** 