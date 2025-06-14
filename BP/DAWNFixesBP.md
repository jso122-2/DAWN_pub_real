# 🔧 DAWN Critical Fixes & Optimizations Blueprint

## 🎯 Mission: Fix Import Errors & Optimize Performance
This blueprint provides complete implementations for critical fixes identified in the DAWN codebase analysis.

---

# 📦 Priority 1: Core Infrastructure Fixes

## File: `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@services/*": ["src/services/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## File: `vite.config.ts`
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@types': path.resolve(__dirname, './src/types')
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
  build: {
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'animation': ['framer-motion'],
          'visualization': [
            './src/components/modules/ConsciousnessVisualizer/index.tsx',
            './src/utils/consciousness/particlePhysics.ts',
            './src/utils/consciousness/waveformGenerator.ts',
          ],
        },
      },
    },
  },
});
```

---

# 📦 Core Components Missing

## File: `src/components/core/ModuleContainer.tsx`
```typescript
import React, { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useBreathing } from '@/hooks/useBreathing';
import { useFloating } from '@/hooks/useFloating';
import * as styles from './ModuleContainer.styles';

export interface ModuleContainerProps {
  children: React.ReactNode;
  moduleId: string;
  category: 'neural' | 'quantum' | 'chaos' | 'process' | 'monitor';
  position?: { x: number; y: number; z: number };
  breathingIntensity?: number;
  floatingSpeed?: number;
  glowIntensity?: number;
  onClose?: () => void;
  className?: string;
}

export const ModuleContainer: React.FC<ModuleContainerProps> = ({
  children,
  moduleId,
  category,
  position = { x: 0, y: 0, z: 0 },
  breathingIntensity = 0.5,
  floatingSpeed = 1,
  glowIntensity = 0.5,
  onClose,
  className,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  const breathing = useBreathing({
    intensity: breathingIntensity,
    baseRate: 4000,
  });
  
  const floating = useFloating({
    amplitude: 20,
    speed: floatingSpeed,
    pattern: 'lissajous',
  });

  // Module-specific glow colors
  const glowColors = {
    neural: 'rgba(147, 51, 234, 0.5)',
    quantum: 'rgba(59, 130, 246, 0.5)',
    chaos: 'rgba(239, 68, 68, 0.5)',
    process: 'rgba(34, 197, 94, 0.5)',
    monitor: 'rgba(251, 191, 36, 0.5)',
  };

  const glowColor = glowColors[category];

  return (
    <AnimatePresence>
      <motion.div
        ref={containerRef}
        className={`${styles.container} ${className || ''}`}
        data-module-id={moduleId}
        data-category={category}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ 
          opacity: 1, 
          scale: 1,
          x: position.x,
          y: position.y,
        }}
        exit={{ opacity: 0, scale: 0.9 }}
        style={{
          ...floating,
          boxShadow: `0 0 ${30 * glowIntensity}px ${glowColor}`,
        }}
        {...breathing}
      >
        <div className={styles.glassLayer} />
        <div className={styles.contentLayer}>
          {onClose && (
            <motion.button
              className={styles.closeButton}
              onClick={onClose}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <X size={16} />
            </motion.button>
          )}
          {children}
        </div>
        <div 
          className={styles.glowBorder} 
          style={{ 
            background: `linear-gradient(135deg, ${glowColor}, transparent)`,
            opacity: glowIntensity,
          }} 
        />
      </motion.div>
    </AnimatePresence>
  );
};
```

## File: `src/components/core/ModuleContainer.styles.ts`
```typescript
import { css, keyframes } from '@emotion/css';

const shimmer = keyframes`
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
`;

export const container = css`
  position: relative;
  min-width: 300px;
  min-height: 200px;
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  background: rgba(15, 23, 42, 0.3);
  border: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    border-color: rgba(148, 163, 184, 0.2);
  }
`;

export const glassLayer = css`
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 50%,
    transparent 100%
  );
  pointer-events: none;
`;

export const contentLayer = css`
  position: relative;
  z-index: 1;
  height: 100%;
  width: 100%;
`;

export const glowBorder = css`
  position: absolute;
  inset: -1px;
  border-radius: 16px;
  opacity: 0.5;
  z-index: -1;
  animation: ${shimmer} 3s ease-out infinite;
  background-size: 1000px 100%;
`;

export const closeButton = css`
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  color: rgba(148, 163, 184, 0.8);
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(15, 23, 42, 0.8);
    color: rgba(226, 232, 240, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
  }
`;
```

---

# 📦 Essential Hooks

## File: `src/hooks/useBreathing.ts`
```typescript
import { useMemo } from 'react';
import { useAnimationFrame } from './useAnimationFrame';

interface BreathingConfig {
  intensity: number;      // 0-1
  baseRate: number;       // ms per cycle
  variance?: number;      // 0-1 irregularity
}

export function useBreathing(config: BreathingConfig) {
  const { intensity, baseRate, variance = 0 } = config;
  
  const animate = useMemo(() => {
    return {
      animate: {
        scale: [
          1 - (0.02 * intensity),
          1 + (0.02 * intensity),
          1 - (0.02 * intensity),
        ],
      },
      transition: {
        duration: baseRate / 1000,
        repeat: Infinity,
        ease: "easeInOut",
        times: [0, 0.5, 1],
      },
    };
  }, [intensity, baseRate]);

  return animate;
}
```

## File: `src/hooks/useFloating.ts`
```typescript
import { useState, useEffect } from 'react';
import { useAnimationFrame } from './useAnimationFrame';

interface FloatingConfig {
  amplitude: number;
  speed: number;
  pattern: 'lissajous' | 'orbital' | 'random' | 'magnetic';
}

export function useFloating(config: FloatingConfig) {
  const [position, setPosition] = useState({ x: 0, y: 0, rotate: 0 });
  const { amplitude, speed, pattern } = config;
  
  useAnimationFrame((time: number) => {
    const t = time * 0.001 * speed;
    
    let x = 0, y = 0, rotate = 0;
    
    switch (pattern) {
      case 'lissajous':
        x = amplitude * Math.sin(t * 1.3);
        y = amplitude * Math.sin(t * 2.1);
        rotate = Math.sin(t * 0.5) * 5;
        break;
        
      case 'orbital':
        x = amplitude * Math.cos(t);
        y = amplitude * Math.sin(t);
        rotate = t * 10 % 360;
        break;
        
      case 'random':
        x = amplitude * (Math.sin(t * 1.3) + Math.sin(t * 2.7) * 0.5);
        y = amplitude * (Math.sin(t * 2.1) + Math.sin(t * 3.2) * 0.5);
        rotate = Math.sin(t * 0.7) * 10;
        break;
        
      case 'magnetic':
        x = amplitude * Math.sin(t) * Math.cos(t * 0.7);
        y = amplitude * Math.cos(t) * Math.sin(t * 0.7);
        rotate = Math.sin(t * 0.3) * 3;
        break;
    }
    
    setPosition({ x, y, rotate });
  });
  
  return {
    transform: `translate(${position.x}px, ${position.y}px) rotate(${position.rotate}deg)`,
  };
}
```

## File: `src/hooks/useAnimationFrame.ts`
```typescript
import { useEffect, useRef, useCallback } from 'react';

export function useAnimationFrame(callback: (time: number) => void) {
  const requestRef = useRef<number>();
  const startTimeRef = useRef<number>();
  
  const animate = useCallback((time: number) => {
    if (!startTimeRef.current) {
      startTimeRef.current = time;
    }
    
    callback(time - startTimeRef.current);
    requestRef.current = requestAnimationFrame(animate);
  }, [callback]);
  
  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, [animate]);
}
```

---

# 📦 Optimized Services

## File: `src/services/websocket/WebSocketService.ts`
```typescript
import { EventEmitter } from 'events';

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export class WebSocketService extends EventEmitter {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private reconnectAttempts = 0;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private connectionState: 'disconnected' | 'connecting' | 'connected' = 'disconnected';
  private messageQueue: any[] = [];

  constructor(config: WebSocketConfig) {
    super();
    this.config = {
      reconnectInterval: 1000,
      maxReconnectAttempts: 5,
      heartbeatInterval: 30000,
      ...config,
    };
  }

  connect(): void {
    if (this.connectionState !== 'disconnected') {
      console.warn('WebSocket already connecting or connected');
      return;
    }

    this.connectionState = 'connecting';
    this.ws = new WebSocket(this.config.url);
    
    this.ws.onopen = this.handleOpen.bind(this);
    this.ws.onmessage = this.handleMessage.bind(this);
    this.ws.onerror = this.handleError.bind(this);
    this.ws.onclose = this.handleClose.bind(this);
  }

  private handleOpen(): void {
    console.log('WebSocket connected');
    this.connectionState = 'connected';
    this.reconnectAttempts = 0;
    
    // Send queued messages
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.send(message);
    }
    
    // Start heartbeat
    this.startHeartbeat();
    
    this.emit('connected');
  }

  private handleMessage(event: MessageEvent): void {
    try {
      const data = JSON.parse(event.data);
      this.emit('message', data);
      
      // Emit specific event types
      if (data.type) {
        this.emit(data.type, data.data);
      }
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
      this.emit('error', error);
    }
  }

  private handleError(event: Event): void {
    console.error('WebSocket error:', event);
    this.emit('error', event);
  }

  private handleClose(): void {
    console.log('WebSocket disconnected');
    this.connectionState = 'disconnected';
    this.stopHeartbeat();
    
    this.emit('disconnected');
    
    // Attempt reconnection
    if (this.reconnectAttempts < this.config.maxReconnectAttempts!) {
      this.scheduleReconnect();
    } else {
      this.emit('reconnect_failed');
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }

    const delay = Math.min(
      this.config.reconnectInterval! * Math.pow(2, this.reconnectAttempts),
      30000
    );

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts + 1})`);

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, delay);
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.isConnected()) {
        this.send({ type: 'heartbeat', timestamp: Date.now() });
      }
    }, this.config.heartbeatInterval!);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  send(data: any): void {
    if (!this.isConnected()) {
      // Queue message for later
      this.messageQueue.push(data);
      return;
    }

    try {
      this.ws!.send(JSON.stringify(data));
    } catch (error) {
      console.error('Failed to send WebSocket message:', error);
      this.emit('error', error);
    }
  }

  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    this.stopHeartbeat();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    this.connectionState = 'disconnected';
    this.messageQueue = [];
  }

  isConnected(): boolean {
    return this.connectionState === 'connected' && 
           this.ws !== null && 
           this.ws.readyState === WebSocket.OPEN;
  }

  getState(): string {
    return this.connectionState;
  }
}

// Singleton instances
export const mainWebSocket = new WebSocketService({
  url: 'ws://localhost:8000/ws',
});

export const processWebSocket = new WebSocketService({
  url: 'ws://localhost:8000/process-stream',
});
```

---

# 📦 Performance Optimization: Animation Manager

## File: `src/services/AnimationManager.ts`
```typescript
export type AnimationCallback = (deltaTime: number, totalTime: number) => void;

class AnimationManager {
  private callbacks = new Map<string, AnimationCallback>();
  private lastTime = 0;
  private animationId: number | null = null;
  private isRunning = false;

  register(id: string, callback: AnimationCallback): () => void {
    this.callbacks.set(id, callback);
    
    if (!this.isRunning && this.callbacks.size > 0) {
      this.start();
    }

    // Return unregister function
    return () => {
      this.callbacks.delete(id);
      if (this.callbacks.size === 0) {
        this.stop();
      }
    };
  }

  private start(): void {
    if (this.isRunning) return;
    
    this.isRunning = true;
    this.lastTime = performance.now();
    this.animate();
  }

  private stop(): void {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  private animate = (): void => {
    if (!this.isRunning) return;

    const currentTime = performance.now();
    const deltaTime = currentTime - this.lastTime;
    this.lastTime = currentTime;

    // Call all registered callbacks
    this.callbacks.forEach(callback => {
      try {
        callback(deltaTime, currentTime);
      } catch (error) {
        console.error('Animation callback error:', error);
      }
    });

    this.animationId = requestAnimationFrame(this.animate);
  };

  getActiveAnimations(): string[] {
    return Array.from(this.callbacks.keys());
  }

  isAnimating(): boolean {
    return this.isRunning;
  }
}

// Export singleton instance
export const animationManager = new AnimationManager();
```

---

# 📦 State Management: Consciousness Context

## File: `src/contexts/ConsciousnessContext.tsx`
```typescript
import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { mainWebSocket } from '@/services/websocket/WebSocketService';
import { ConsciousnessState, TickData } from '@/types/consciousness.types';

interface ConsciousnessContextValue {
  state: ConsciousnessState;
  tickHistory: TickData[];
  isConnected: boolean;
  updateState: (updates: Partial<ConsciousnessState>) => void;
}

const defaultState: ConsciousnessState = {
  scup: 50,
  entropy: 0.5,
  mood: 'contemplative',
  neuralActivity: 0.5,
  quantumCoherence: 0.5,
  memoryPressure: 0.3,
  timestamp: Date.now(),
};

const ConsciousnessContext = createContext<ConsciousnessContextValue | null>(null);

export const ConsciousnessProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<ConsciousnessState>(defaultState);
  const [tickHistory, setTickHistory] = useState<TickData[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    mainWebSocket.connect();

    // Handle connection events
    mainWebSocket.on('connected', () => {
      setIsConnected(true);
      console.log('Connected to consciousness engine');
    });

    mainWebSocket.on('disconnected', () => {
      setIsConnected(false);
      console.log('Disconnected from consciousness engine');
    });

    // Handle tick data
    mainWebSocket.on('tick', (data: TickData) => {
      setState({
        scup: data.scup,
        entropy: data.entropy,
        mood: data.mood,
        neuralActivity: data.neural_activity,
        quantumCoherence: data.quantum_coherence,
        memoryPressure: data.memory_pressure,
        timestamp: data.timestamp,
      });

      setTickHistory(prev => {
        const newHistory = [...prev, data];
        // Keep only last 1000 ticks
        return newHistory.slice(-1000);
      });
    });

    return () => {
      mainWebSocket.disconnect();
      mainWebSocket.removeAllListeners();
    };
  }, []);

  const updateState = useCallback((updates: Partial<ConsciousnessState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);

  return (
    <ConsciousnessContext.Provider value={{ state, tickHistory, isConnected, updateState }}>
      {children}
    </ConsciousnessContext.Provider>
  );
};

export const useConsciousness = () => {
  const context = useContext(ConsciousnessContext);
  if (!context) {
    throw new Error('useConsciousness must be used within ConsciousnessProvider');
  }
  return context.state;
};

export const useConsciousnessContext = () => {
  const context = useContext(ConsciousnessContext);
  if (!context) {
    throw new Error('useConsciousnessContext must be used within ConsciousnessProvider');
  }
  return context;
};
```

---

# 📦 Error Boundaries

## File: `src/components/core/ErrorBoundary.tsx`
```typescript
import React, { Component, ErrorInfo } from 'react';
import { AlertCircle } from 'lucide-react';
import * as styles from './ErrorBoundary.styles';

interface Props {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; resetError: () => void }>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught error:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        const FallbackComponent = this.props.fallback;
        return <FallbackComponent error={this.state.error} resetError={this.resetError} />;
      }

      return (
        <div className={styles.errorContainer}>
          <div className={styles.errorContent}>
            <AlertCircle size={48} className={styles.errorIcon} />
            <h2 className={styles.errorTitle}>Module Error</h2>
            <p className={styles.errorMessage}>{this.state.error.message}</p>
            <button onClick={this.resetError} className={styles.retryButton}>
              Retry
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Module-specific error boundary
export const ModuleErrorBoundary: React.FC<{ children: React.ReactNode; moduleId: string }> = ({ 
  children, 
  moduleId 
}) => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error(`Module ${moduleId} crashed:`, error, errorInfo);
        // Could send error to monitoring service
      }}
    >
      {children}
    </ErrorBoundary>
  );
};
```

## File: `src/components/core/ErrorBoundary.styles.ts`
```typescript
import { css } from '@emotion/css';

export const errorContainer = css`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 2rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(248, 113, 113, 0.2);
  border-radius: 12px;
  backdrop-filter: blur(10px);
`;

export const errorContent = css`
  text-align: center;
  max-width: 400px;
`;

export const errorIcon = css`
  color: rgba(248, 113, 113, 0.8);
  margin-bottom: 1rem;
`;

export const errorTitle = css`
  font-size: 1.5rem;
  font-weight: 600;
  color: rgba(248, 113, 113, 0.9);
  margin: 0 0 0.5rem 0;
`;

export const errorMessage = css`
  color: rgba(226, 232, 240, 0.8);
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
`;

export const retryButton = css`
  padding: 0.75rem 1.5rem;
  background: rgba(248, 113, 113, 0.2);
  border: 1px solid rgba(248, 113, 113, 0.4);
  border-radius: 8px;
  color: rgba(248, 113, 113, 0.9);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(248, 113, 113, 0.3);
    transform: translateY(-1px);
  }
`;
```

---

# 📦 Python Backend CORS Fix

## File: `python/start_api_fixed.py` (Update)
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List, Dict, Any

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.process_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, connection_type: str = "main"):
        await websocket.accept()
        if connection_type == "main":
            self.active_connections.append(websocket)
        else:
            self.process_connections.append(websocket)

    def disconnect(self, websocket: WebSocket, connection_type: str = "main"):
        if connection_type == "main":
            self.active_connections.remove(websocket)
        else:
            self.process_connections.remove(websocket)

    async def broadcast_tick(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json({"type": "tick", "data": data})
            except:
                # Connection might be closed
                pass

    async def broadcast_process(self, data: dict):
        for connection in self.process_connections:
            try:
                await connection.send_json(data)
            except:
                pass

manager = ConnectionManager()

# Main WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "main")
    try:
        while True:
            # Handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "heartbeat":
                await websocket.send_json({
                    "type": "heartbeat_response",
                    "timestamp": message.get("timestamp")
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket, "main")

# Process stream WebSocket endpoint
@app.websocket("/process-stream")
async def process_stream_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "process")
    try:
        while True:
            await asyncio.sleep(10)  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, "process")

# Process execution endpoints
@app.get("/api/scripts")
async def get_available_scripts():
    return [
        {
            "name": "neural_analyzer.py",
            "description": "Analyzes neural network patterns",
            "parameters": [],
            "tick_triggered": True,
            "category": "neural"
        },
        {
            "name": "quantum_processor.py",
            "description": "Quantum state calculations",
            "parameters": [],
            "tick_triggered": False,
            "category": "quantum"
        },
        # Add more scripts
    ]

@app.post("/api/process/execute")
async def execute_process(request: dict):
    # Implementation for process execution
    return {
        "process_id": f"process_{request['script']}_{int(asyncio.get_event_loop().time())}",
        "script": request["script"],
        "status": "running"
    }

# Background task to simulate tick loop
async def tick_loop():
    tick_number = 0
    while True:
        tick_data = {
            "tick_number": tick_number,
            "timestamp": int(asyncio.get_event_loop().time() * 1000),
            "scup": 50 + (tick_number % 50),
            "entropy": 0.5 + (0.3 * ((tick_number % 100) / 100)),
            "mood": "contemplative" if tick_number % 200 < 100 else "excited",
            "neural_activity": 0.5 + (0.5 * ((tick_number % 50) / 50)),
            "quantum_coherence": 0.7,
            "memory_pressure": 0.3,
            "active_processes": []
        }
        
        await manager.broadcast_tick(tick_data)
        tick_number += 1
        await asyncio.sleep(0.1)  # 10Hz tick rate

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(tick_loop())
```

---

# 🚀 Cursor Implementation Guide

## Step 1: Fix TypeScript Configuration
```bash
# Copy the tsconfig.json and vite.config.ts files
# This fixes all import path issues
```

## Step 2: Create Core Components
```bash
mkdir -p src/components/core src/contexts
# Implement ModuleContainer and ErrorBoundary
```

## Step 3: Implement Essential Hooks
```bash
mkdir -p src/hooks
# Create useBreathing, useFloating, useAnimationFrame
```

## Step 4: Optimize Services
```bash
# Replace existing WebSocket implementation with optimized version
# Add AnimationManager for centralized animation control
```

## Step 5: Update Python Backend
```bash
# Add CORS middleware to start_api_fixed.py
# Ensure WebSocket endpoints match frontend expectations
```

## Step 6: Wrap App with Providers
```typescript
// In main.tsx or App.tsx
import { ConsciousnessProvider } from '@/contexts/ConsciousnessContext';
import { ErrorBoundary } from '@/components/core/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <ConsciousnessProvider>
        {/* Your app components */}
      </ConsciousnessProvider>
    </ErrorBoundary>
  );
}
```

## Testing Checklist
- [ ] All imports resolve correctly
- [ ] WebSocket connects and stays connected
- [ ] Animations use centralized manager
- [ ] No memory leaks in effects
- [ ] Error boundaries catch module failures
- [ ] CORS allows frontend-backend communication

## Performance Verification
1. Open Chrome DevTools Performance tab
2. Record while app is running
3. Check for:
   - Consistent 60fps
   - No memory leaks
   - Efficient canvas rendering
   - Minimal re-renders

This blueprint fixes all identified issues and provides a solid foundation for DAWN!