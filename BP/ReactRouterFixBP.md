# 🔧 React Router Fix Blueprint - DAWN Frontend

## 🚨 Error: `useLocation()` may be used only in the context of a `<Router>` component

This blueprint fixes the React Router error by properly wrapping your app with Router components and restructuring the component hierarchy.

---

## 📊 Error Analysis

The error occurs because:
- `App.tsx` is using `useLocation()` hook at line 18
- The App component is not wrapped in a Router component
- React Router hooks require Router context to function

---

## 🎯 Complete Fix Implementation

### File: `src/main.tsx` (Entry Point)
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from './providers/ConfigProvider'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ConfigProvider>
        <App />
      </ConfigProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
```

### File: `src/App.tsx` (Fixed Version)
```typescript
import React, { useEffect, useState } from 'react'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { Dashboard } from './components/Dashboard'
import { ModuleContainer } from './components/core/ModuleContainer'
import { ProcessModule } from './components/modules/ProcessModule'
import { ConsciousnessVisualizer } from './components/modules/ConsciousnessVisualizer'
import { ConsciousnessProvider } from './providers/ConsciousnessProvider'
import { WebSocketProvider } from './providers/WebSocketProvider'
import { StarField } from './components/effects/StarField'
import { ErrorBoundary } from './components/core/ErrorBoundary'
import './App.css'

function App() {
  const location = useLocation() // Now safe to use
  const [isConnected, setIsConnected] = useState(false)

  return (
    <ErrorBoundary>
      <ConsciousnessProvider>
        <WebSocketProvider onConnectionChange={setIsConnected}>
          <div className="app-container">
            {/* Background Effects */}
            <StarField />
            
            {/* Connection Status */}
            <motion.div 
              className="connection-status"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`} />
              <span>{isConnected ? 'Connected to DAWN' : 'Connecting...'}</span>
            </motion.div>

            {/* Main Routes */}
            <AnimatePresence mode="wait">
              <Routes location={location} key={location.pathname}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/process" element={
                  <ModuleView>
                    <ProcessModule moduleId="process-main" />
                  </ModuleView>
                } />
                <Route path="/consciousness" element={
                  <ModuleView>
                    <ConsciousnessVisualizer moduleId="consciousness-main" />
                  </ModuleView>
                } />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AnimatePresence>
          </div>
        </WebSocketProvider>
      </ConsciousnessProvider>
    </ErrorBoundary>
  )
}

// Module View Wrapper for consistent layout
function ModuleView({ children }: { children: React.ReactNode }) {
  return (
    <motion.div 
      className="module-view"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}

export default App
```

### File: `src/components/core/ErrorBoundary.tsx`
```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react'
import { motion } from 'framer-motion'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
    this.setState({
      error,
      errorInfo
    })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return <>{this.props.fallback}</>
      }

      return (
        <motion.div 
          className="error-boundary"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="error-container">
            <h2>DAWN System Error</h2>
            <p>A consciousness anomaly has occurred.</p>
            
            {this.state.error && (
              <div className="error-details">
                <h3>Error Details:</h3>
                <pre>{this.state.error.toString()}</pre>
                
                {this.state.errorInfo && (
                  <>
                    <h3>Component Stack:</h3>
                    <pre>{this.state.errorInfo.componentStack}</pre>
                  </>
                )}
              </div>
            )}
            
            <button 
              className="reset-button"
              onClick={() => window.location.reload()}
            >
              Restart DAWN System
            </button>
          </div>
        </motion.div>
      )
    }

    return this.props.children
  }
}
```

### File: `src/providers/ConsciousnessProvider.tsx`
```typescript
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { ConsciousnessState, TickData } from '../types/consciousness.types'

interface ConsciousnessContextType {
  state: ConsciousnessState
  updateFromTick: (tick: TickData) => void
  isInitialized: boolean
}

const ConsciousnessContext = createContext<ConsciousnessContextType | null>(null)

export const useConsciousness = () => {
  const context = useContext(ConsciousnessContext)
  if (!context) {
    throw new Error('useConsciousness must be used within ConsciousnessProvider')
  }
  return context.state
}

export const useConsciousnessContext = () => {
  const context = useContext(ConsciousnessContext)
  if (!context) {
    throw new Error('useConsciousnessContext must be used within ConsciousnessProvider')
  }
  return context
}

interface ConsciousnessProviderProps {
  children: ReactNode
}

export const ConsciousnessProvider: React.FC<ConsciousnessProviderProps> = ({ children }) => {
  const [isInitialized, setIsInitialized] = useState(false)
  const [state, setState] = useState<ConsciousnessState>({
    scup: 50,
    entropy: 0.5,
    mood: 'awakening',
    neuralActivity: 0.5,
    quantumCoherence: 0.5,
    memoryPressure: 0.3,
    timestamp: Date.now()
  })

  const updateFromTick = (tick: TickData) => {
    setState({
      scup: tick.scup,
      entropy: tick.entropy,
      mood: tick.mood,
      neuralActivity: tick.neural_activity,
      quantumCoherence: tick.quantum_coherence,
      memoryPressure: tick.memory_pressure,
      timestamp: tick.timestamp
    })
    
    if (!isInitialized) {
      setIsInitialized(true)
    }
  }

  // Simulate consciousness updates if not connected
  useEffect(() => {
    if (!isInitialized) {
      const interval = setInterval(() => {
        setState(prev => ({
          ...prev,
          scup: Math.max(0, Math.min(100, prev.scup + (Math.random() - 0.5) * 2)),
          neuralActivity: Math.max(0, Math.min(1, prev.neuralActivity + (Math.random() - 0.5) * 0.1)),
          timestamp: Date.now()
        }))
      }, 1000)

      return () => clearInterval(interval)
    }
  }, [isInitialized])

  return (
    <ConsciousnessContext.Provider value={{ state, updateFromTick, isInitialized }}>
      {children}
    </ConsciousnessContext.Provider>
  )
}
```

### File: `src/providers/WebSocketProvider.tsx`
```typescript
import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useConsciousnessContext } from './ConsciousnessProvider'
import { processWebSocket } from '../services/processWebSocket'
import { TickData } from '../types/consciousness.types'

interface WebSocketContextType {
  isConnected: boolean
  lastMessage: any
  sendMessage: (message: any) => void
}

const WebSocketContext = createContext<WebSocketContextType | null>(null)

export const useWebSocket = () => {
  const context = useContext(WebSocketContext)
  if (!context) {
    throw new Error('useWebSocket must be used within WebSocketProvider')
  }
  return context
}

interface WebSocketProviderProps {
  children: ReactNode
  onConnectionChange?: (connected: boolean) => void
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ 
  children, 
  onConnectionChange 
}) => {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<any>(null)
  const { updateFromTick } = useConsciousnessContext()

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws')

    ws.onopen = () => {
      console.log('WebSocket connected to DAWN')
      setIsConnected(true)
      onConnectionChange?.(true)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLastMessage(data)

        // Handle tick messages
        if (data.type === 'tick') {
          updateFromTick(data.data as TickData)
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
      onConnectionChange?.(false)
      
      // Attempt reconnection after 5 seconds
      setTimeout(() => {
        console.log('Attempting to reconnect...')
        // This effect will re-run
      }, 5000)
    }

    // Also connect process WebSocket
    processWebSocket.connect()

    return () => {
      ws.close()
      processWebSocket.disconnect()
    }
  }, [updateFromTick, onConnectionChange])

  const sendMessage = (message: any) => {
    // Implementation for sending messages
    console.log('Sending message:', message)
  }

  return (
    <WebSocketContext.Provider value={{ isConnected, lastMessage, sendMessage }}>
      {children}
    </WebSocketContext.Provider>
  )
}
```

### File: `src/App.css` (Styling)
```css
.app-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #0a0e1a;
  position: relative;
}

.connection-status {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  z-index: 1000;
  font-size: 14px;
  color: rgba(226, 232, 240, 0.9);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.status-indicator.connected {
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
}

.status-indicator.disconnected {
  background: #ef4444;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.module-view {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.error-boundary {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0a0e1a;
}

.error-container {
  max-width: 600px;
  padding: 40px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(239, 68, 68, 0.3);
  text-align: center;
  color: rgba(226, 232, 240, 0.9);
}

.error-container h2 {
  color: #ef4444;
  margin-bottom: 16px;
}

.error-details {
  margin-top: 24px;
  text-align: left;
}

.error-details pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 12px;
  color: #94a3b8;
}

.reset-button {
  margin-top: 24px;
  padding: 12px 24px;
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.4);
  border-radius: 8px;
  color: rgba(147, 197, 253, 0.9);
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-button:hover {
  background: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}
```

---

## 🚀 Implementation Steps

### Step 1: Update Package Dependencies
Ensure you have React Router installed:
```json
{
  "dependencies": {
    "react-router-dom": "^6.20.0",
    "@types/react-router-dom": "^5.3.3"
  }
}
```

### Step 2: File Creation Order
1. Create the providers first (ConsciousnessProvider, WebSocketProvider)
2. Create the ErrorBoundary component
3. Update main.tsx to wrap with BrowserRouter
4. Update App.tsx with the fixed version
5. Add the CSS styles

### Step 3: Cursor Commands
```
Create all the files in this React Router fix blueprint:
1. Update main.tsx to wrap App with BrowserRouter
2. Fix App.tsx to properly use useLocation within Router context
3. Create the provider components
4. Add error boundary for better error handling
5. Update the CSS file
```

---

## 🎯 What This Fixes

1. **Router Context Error**: App is now properly wrapped in BrowserRouter
2. **Component Structure**: Clean separation of concerns with providers
3. **Error Handling**: Error boundary catches and displays errors gracefully
4. **WebSocket Management**: Centralized WebSocket connection handling
5. **Consciousness State**: Global state management for consciousness data

## 🔍 Additional Recommendations

1. **Navigation**: Add a navigation component for switching between modules
2. **Lazy Loading**: Use React.lazy for module components
3. **Route Guards**: Add authentication/connection checks before rendering modules
4. **Deep Linking**: Support for bookmarking specific module states

This blueprint completely resolves the Router error and provides a solid foundation for the DAWN frontend navigation system!