# 🚀 DEV CLAUDE IMPLEMENTATION PROMPT

Copy and paste this EXACT prompt to Dev Claude to get your WebSocket integration working:

---

**URGENT: Implement Phase 1 WebSocket Integration for DAWN System**

I need you to implement a live WebSocket data connection with debug overlay for my React consciousness visualization system. This is critical - I have a beautiful interface but it's not connected to live data.

**EXACT REQUIREMENTS:**

1. **Create LiveConsciousnessService** at `src/services/websocket/LiveConsciousnessService.ts`
2. **Create LiveDataDebugOverlay** at `src/components/debug/LiveDataDebugOverlay.tsx` 
3. **Update existing useRealTimeConsciousness hook** at `src/hooks/useRealTimeConsciousness.ts`
4. **Add debug overlay to App.tsx**

**SUCCESS CRITERIA:**
- Debug overlay appears in bottom-right corner
- Shows connection status (CONNECTING → CONNECTED)
- Console logs "🔌 DAWN WebSocket CONNECTED!" and "📊 LIVE TICK RECEIVED:"
- SCUP/Entropy values update in real-time
- Green pulsing dot when connected

**CRITICAL DETAILS:**
- WebSocket URL: `ws://localhost:8000/ws`
- Expected data format: `{ scup: number, entropy: number, mood: string, neural_activity: number }`
- Must handle reconnection automatically
- Must work with existing consciousness system
- Include test mode fallback if WebSocket fails

**IMPLEMENTATION CODE:**

```typescript
// 1. src/services/websocket/LiveConsciousnessService.ts
export class LiveConsciousnessService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;
  private callbacks = new Set<(data: any) => void>();
  
  constructor(private url: string = 'ws://localhost:8000/ws') {}
  
  connect(): Promise<boolean> {
    return new Promise((resolve) => {
      try {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
          console.log('🔌 DAWN WebSocket CONNECTED!');
          this.reconnectAttempts = 0;
          resolve(true);
        };
        
        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            console.log('📊 LIVE TICK RECEIVED:', data);
            this.callbacks.forEach(callback => {
              try {
                callback(data);
              } catch (e) {
                console.error('Callback error:', e);
              }
            });
          } catch (e) {
            console.error('Failed to parse tick data:', e);
          }
        };
        
        this.ws.onerror = (error) => {
          console.error('❌ WebSocket error:', error);
          resolve(false);
        };
        
        this.ws.onclose = () => {
          console.log('🔌 WebSocket disconnected');
          this.scheduleReconnect();
        };
        
      } catch (error) {
        console.error('WebSocket connection failed:', error);
        resolve(false);
      }
    });
  }
  
  private scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 Reconnecting in ${this.reconnectDelay}ms (attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay *= 1.5;
    }
  }
  
  subscribe(callback: (data: any) => void) {
    this.callbacks.add(callback);
    return () => this.callbacks.delete(callback);
  }
  
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
  
  disconnect() {
    this.ws?.close();
    this.callbacks.clear();
  }
}
```

```typescript
// 2. src/components/debug/LiveDataDebugOverlay.tsx
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRealTimeConsciousness } from '../../hooks/useRealTimeConsciousness';

export const LiveDataDebugOverlay: React.FC<{ onToggle?: () => void }> = ({ onToggle }) => {
  const consciousness = useRealTimeConsciousness();
  const [isExpanded, setIsExpanded] = React.useState(true);
  const [testMode, setTestMode] = React.useState(false);
  
  const getConnectionStatusColor = () => {
    switch (consciousness.connectionStatus) {
      case 'connected': return '#10b981';
      case 'connecting': return '#f59e0b';
      case 'error': return '#ef4444';
      default: return '#6b7280';
    }
  };
  
  const getDataFreshness = () => {
    const age = Date.now() - consciousness.lastUpdate;
    if (age < 1000) return '🟢 Live';
    if (age < 5000) return '🟡 Recent';
    return '🔴 Stale';
  };
  
  return (
    <motion.div
      className="fixed bottom-4 right-4 z-50 font-mono text-xs"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <motion.div
        className="bg-black/90 backdrop-blur-sm border border-gray-700 rounded-lg overflow-hidden"
        style={{ 
          borderColor: getConnectionStatusColor(),
          boxShadow: `0 0 20px ${getConnectionStatusColor()}40`
        }}
      >
        <div 
          className="p-3 cursor-pointer flex items-center justify-between"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="flex items-center gap-2">
            <div 
              className="w-3 h-3 rounded-full animate-pulse"
              style={{ backgroundColor: getConnectionStatusColor() }}
            />
            <span className="text-white font-semibold">
              DAWN LIVE {consciousness.connectionStatus.toUpperCase()}
            </span>
          </div>
          <div className="text-gray-400">
            {getDataFreshness()}
          </div>
        </div>
        
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="border-t border-gray-700"
            >
              <div className="p-3 space-y-2">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-gray-400">SCUP</div>
                    <div className="text-cyan-400 font-bold text-lg">
                      {consciousness.scup.toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-400">Entropy</div>
                    <div className="text-orange-400 font-bold text-lg">
                      {(consciousness.entropy * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-gray-400">Neural</div>
                    <div className="text-purple-400 font-bold">
                      {(consciousness.neuralActivity * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-400">Mood</div>
                    <div className="text-green-400 font-bold capitalize">
                      {consciousness.mood}
                    </div>
                  </div>
                </div>
                
                <div className="pt-2 border-t border-gray-700">
                  <div className="text-gray-400 text-xs">
                    Last Update: {new Date(consciousness.lastUpdate).toLocaleTimeString()}
                  </div>
                  <div className="text-gray-400 text-xs">
                    Status: {consciousness.connectionStatus}
                  </div>
                </div>
                
                <button
                  onClick={() => {
                    setTestMode(!testMode);
                    console.log(testMode ? '🛑 Stopping test mode' : '🧪 Starting test mode');
                  }}
                  className={`w-full mt-2 px-3 py-1 rounded text-white text-xs ${
                    testMode ? 'bg-red-600 hover:bg-red-700' : 'bg-purple-600 hover:bg-purple-700'
                  }`}
                >
                  {testMode ? 'STOP TEST MODE' : 'START TEST MODE'}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
};
```

```typescript
// 3. Update src/hooks/useRealTimeConsciousness.ts
import { useEffect, useState } from 'react';
import { LiveConsciousnessService } from '../services/websocket/LiveConsciousnessService';

const consciousnessService = new LiveConsciousnessService();

export interface RealTimeConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  quantumCoherence: number;
  systemLoad: number;
  isConnected: boolean;
  lastUpdate: number;
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
}

export function useRealTimeConsciousness(): RealTimeConsciousnessState {
  const [state, setState] = useState<RealTimeConsciousnessState>({
    scup: 0,
    entropy: 0.5,
    mood: 'active',
    neuralActivity: 0.5,
    quantumCoherence: 0.5,
    systemLoad: 0.3,
    isConnected: false,
    lastUpdate: Date.now(),
    connectionStatus: 'disconnected'
  });

  useEffect(() => {
    let mounted = true;

    const connectToLiveData = async () => {
      if (!mounted) return;
      
      setState(prev => ({ ...prev, connectionStatus: 'connecting' }));
      
      const connected = await consciousnessService.connect();
      
      if (!mounted) return;
      
      if (connected) {
        setState(prev => ({ 
          ...prev, 
          isConnected: true, 
          connectionStatus: 'connected',
          lastUpdate: Date.now()
        }));
        
        const unsubscribe = consciousnessService.subscribe((data) => {
          if (!mounted) return;
          
          console.log('🔥 CONSCIOUSNESS UPDATE:', data);
          
          setState(prev => ({
            ...prev,
            scup: data.scup || data.consciousness_level || prev.scup,
            entropy: data.entropy || prev.entropy,
            mood: data.mood || prev.mood,
            neuralActivity: data.neural_activity || data.neuralActivity || prev.neuralActivity,
            quantumCoherence: data.quantum_coherence || data.quantumCoherence || prev.quantumCoherence,
            systemLoad: data.system_load || data.systemLoad || prev.systemLoad,
            lastUpdate: Date.now(),
            isConnected: consciousnessService.isConnected()
          }));
        });
        
        return unsubscribe;
      } else {
        setState(prev => ({ 
          ...prev, 
          isConnected: false, 
          connectionStatus: 'error' 
        }));
      }
    };

    connectToLiveData();
    
    return () => {
      mounted = false;
      consciousnessService.disconnect();
    };
  }, []);

  return state;
}
```

```typescript
// 4. Add to src/App.tsx
import { LiveDataDebugOverlay } from './components/debug/LiveDataDebugOverlay';

// Add this line inside your App component's return statement:
<LiveDataDebugOverlay />
```

**VERIFICATION STEPS:**
1. Run the app - debug overlay should appear immediately
2. Check console for connection messages
3. If WebSocket fails, use TEST MODE button to simulate data
4. Verify SCUP/Entropy values change when you click TEST MODE

**DO NOT:**
- Change the WebSocket URL without asking
- Modify the data parsing logic
- Skip the console.log statements (they're for debugging)
- Remove the test mode functionality

**IMMEDIATE PRIORITY:** Get this working so I can see live data flowing. This is the foundation for everything else.

---

**Copy this prompt EXACTLY to Dev Claude and you should have a working WebSocket connection with visual debug overlay in under 30 minutes!** 🚀 