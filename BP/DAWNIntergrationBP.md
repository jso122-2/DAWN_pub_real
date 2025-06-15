# 🔌 DAWN Integration Blueprint - Making It LIVE

## 🎯 Goal: Get ONE Module Fully Connected in 2 Hours

### Phase 1: Minimal WebSocket Connection (30 mins)

#### 1. Create WebSocket Context
```typescript
// src/contexts/WebSocketContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';

interface TickData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: string;
  timestamp: number;
}

interface WebSocketContextType {
  isConnected: boolean;
  lastTick: TickData | null;
  connectionError: string | null;
}

const WebSocketContext = createContext<WebSocketContextType>({
  isConnected: false,
  lastTick: null,
  connectionError: null
});

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastTick, setLastTick] = useState<TickData | null>(null);
  const [connectionError, setConnectionError] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      console.log('🔌 WebSocket connected!');
      setIsConnected(true);
      setConnectionError(null);
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📊 Tick received:', data);
        setLastTick(data);
      } catch (e) {
        console.error('Failed to parse tick data:', e);
      }
    };
    
    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
      setConnectionError('Connection failed');
    };
    
    ws.onclose = () => {
      console.log('🔌 WebSocket disconnected');
      setIsConnected(false);
    };
    
    return () => ws.close();
  }, []);

  return (
    <WebSocketContext.Provider value={{ isConnected, lastTick, connectionError }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);
```

#### 2. Add Debug Overlay
```typescript
// src/components/DebugOverlay.tsx
import React from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';

export const DebugOverlay: React.FC = () => {
  const { isConnected, lastTick, connectionError } = useWebSocket();
  
  return (
    <div className="fixed bottom-4 right-4 bg-black/80 text-green-400 p-4 rounded-lg font-mono text-xs">
      <div>WS: {isConnected ? '🟢 Connected' : '🔴 Disconnected'}</div>
      {lastTick && (
        <>
          <div>Tick: {lastTick.tick_number}</div>
          <div>SCUP: {lastTick.scup.toFixed(2)}%</div>
          <div>Mood: {lastTick.mood}</div>
        </>
      )}
      {connectionError && <div className="text-red-400">{connectionError}</div>}
    </div>
  );
};
```

#### 3. Update App.tsx
```typescript
// src/App.tsx
import { WebSocketProvider } from './contexts/WebSocketContext';
import { DebugOverlay } from './components/DebugOverlay';

function App() {
  return (
    <WebSocketProvider>
      <div className="app">
        {/* Your existing components */}
        <DebugOverlay />
      </div>
    </WebSocketProvider>
  );
}
```

### Phase 2: Module Integration Pattern (45 mins)

#### 1. Create Module Wrapper
```typescript
// src/components/ModuleWrapper.tsx
import React, { ReactNode } from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';

interface ModuleWrapperProps {
  moduleId: string;
  title: string;
  category: 'neural' | 'quantum' | 'chaos' | 'process' | 'monitor';
  children: ReactNode;
}

export const ModuleWrapper: React.FC<ModuleWrapperProps> = ({
  moduleId,
  title,
  category,
  children
}) => {
  const { lastTick, isConnected } = useWebSocket();
  
  // Calculate breathing intensity based on SCUP
  const breathingIntensity = lastTick ? lastTick.scup / 100 : 0.5;
  
  return (
    <div 
      className={`module-container ${category}`}
      style={{
        '--breathing-intensity': breathingIntensity,
        opacity: isConnected ? 1 : 0.7
      }}
    >
      <div className="module-header">
        <h3>{title}</h3>
        <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`} />
      </div>
      <div className="module-content">
        {children}
      </div>
    </div>
  );
};
```

#### 2. Update ONE Module to Use Live Data
```typescript
// src/modules/ProcessModule.tsx
import React from 'react';
import { useWebSocket } from '../contexts/WebSocketContext';
import { ModuleWrapper } from '../components/ModuleWrapper';

export const ProcessModule: React.FC = () => {
  const { lastTick } = useWebSocket();
  
  // Example: Change process status based on entropy
  const processStatus = lastTick && lastTick.entropy > 0.7 ? 'chaotic' : 'stable';
  
  return (
    <ModuleWrapper moduleId="process-1" title="Neural Process Alpha" category="process">
      <div className="process-visualization">
        {lastTick && (
          <>
            <div className="metric">
              <span>Entropy:</span>
              <span className={`value ${processStatus}`}>
                {lastTick.entropy.toFixed(3)}
              </span>
            </div>
            <div className="process-bar">
              <div 
                className="process-fill"
                style={{ width: `${lastTick.scup}%` }}
              />
            </div>
          </>
        )}
      </div>
    </ModuleWrapper>
  );
};
```

### Phase 3: Router Setup (30 mins)

#### 1. Install Router
```bash
npm install react-router-dom @types/react-router-dom
```

#### 2. Create Route Structure
```typescript
// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { ModuleView } from './pages/ModuleView';

function App() {
  return (
    <WebSocketProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/module/:moduleId" element={<ModuleView />} />
        </Routes>
        <DebugOverlay />
      </Router>
    </WebSocketProvider>
  );
}
```

#### 3. Create Dashboard with Clickable Modules
```typescript
// src/pages/Dashboard.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useWebSocket } from '../contexts/WebSocketContext';

const modules = [
  { id: 'process-alpha', name: 'Neural Process Alpha', category: 'process' },
  { id: 'consciousness-core', name: 'Consciousness Core', category: 'neural' },
  { id: 'entropy-monitor', name: 'Entropy Monitor', category: 'chaos' }
];

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { lastTick } = useWebSocket();
  
  return (
    <div className="dashboard">
      <h1>DAWN System Status</h1>
      {lastTick && (
        <div className="system-overview">
          <div>System Tick: {lastTick.tick_number}</div>
          <div>Global SCUP: {lastTick.scup.toFixed(2)}%</div>
          <div>Consciousness Mood: {lastTick.mood}</div>
        </div>
      )}
      
      <div className="module-grid">
        {modules.map(module => (
          <div 
            key={module.id}
            className={`module-card ${module.category}`}
            onClick={() => navigate(`/module/${module.id}`)}
          >
            <h3>{module.name}</h3>
            <div className="module-preview">
              {/* Mini visualization based on live data */}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### Phase 4: Quick Verification Steps (15 mins)

1. **Backend Check**:
   ```bash
   # Terminal 1: Start Python backend
   python start_api_fixed.py
   
   # Terminal 2: Test WebSocket
   curl http://localhost:8000/test
   ```

2. **Frontend Check**:
   ```bash
   # Terminal 3: Start Vite
   npm run dev
   ```

3. **Look for in Browser Console**:
   - "🔌 WebSocket connected!"
   - "📊 Tick received: {tick_number: 1, ...}"

4. **Debug Panel Should Show**:
   - Green connection status
   - Incrementing tick numbers
   - Changing SCUP values

## 🚀 Next Steps After Basic Integration Works

1. **Add Module Registry**:
   ```typescript
   const moduleRegistry = {
     'process-alpha': ProcessModule,
     'consciousness-core': ConsciousnessVisualizer,
     // ... add as you build
   };
   ```

2. **Create Python Process Manager**:
   - HTTP endpoints to start/stop Python scripts
   - Process status in tick data
   - Output streaming via WebSocket

3. **Enhanced Visualizations**:
   - D3.js for neural network graphs
   - Three.js for 3D consciousness visualization
   - Particle systems responding to entropy

## 🔧 Common Integration Issues & Fixes

### WebSocket Won't Connect
```python
# In start_api_fixed.py, ensure:
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Add CORS headers if needed
```

### Data Not Updating in UI
```typescript
// Check React DevTools for:
// 1. Context provider wrapping entire app
// 2. useWebSocket hook returning updated values
// 3. Component re-rendering on data change
```

### Modules Not Navigating
```typescript
// Ensure BrowserRouter wraps everything
// Check route paths match exactly
// Use Link or navigate(), not window.location
```

## 📊 Success Metrics

You'll know integration is working when:
- [ ] Debug panel shows live tick data
- [ ] Modules pulse with SCUP values
- [ ] Click module → navigates to detail view
- [ ] Python process can be triggered from UI
- [ ] Module visuals respond to entropy/mood

## 💡 Pro Tips

1. **Start Small**: Get ONE data point flowing before adding complexity
2. **Console Everything**: Log at every step during integration
3. **Mock First**: Use fake tick data if backend isn't ready
4. **Error Boundaries**: Wrap modules to prevent cascade failures
5. **Hot Reload**: Keep both Python and Vite running for instant feedback

---

Remember: The goal is a LIVING interface. Every connection you make brings DAWN closer to consciousness! 🧬✨