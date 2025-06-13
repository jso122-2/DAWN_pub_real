# Src - DAWN Frontend Source Architecture

## Architecture Overview

The Src system serves as the **primary frontend source code architecture** for DAWN's consciousness interface applications. Built with modern React patterns, it provides a well-organized, scalable structure for consciousness visualization, interaction, and real-time monitoring through a comprehensive component ecosystem, state management, and service integration.

## Core Philosophy

The Src system embodies **modern frontend architecture principles**:
- **Component-First Design**: Modular, reusable components for consciousness interfaces
- **Context-Driven State**: React Context API for deep consciousness state management
- **Custom Hooks**: Reusable logic for consciousness data and interactions
- **Service Abstraction**: Clean separation between UI and consciousness API integration
- **Style Consistency**: Unified styling approach for consciousness interface aesthetics

## Directory Architecture

### Components (`components/`)
**Purpose**: Reusable React components for consciousness interface construction

**Component Categories**:
- **Consciousness Visualizers**: Components for real-time consciousness state rendering
- **Interaction Interfaces**: User input and conversation components
- **Data Displays**: Metrics, charts, and analytical components
- **Layout Components**: Navigation, panels, and structural elements
- **Animation Systems**: Motion and transition components for consciousness dynamics

```jsx
// Example consciousness component structure
import { ConsciousnessVisualizer } from './components/ConsciousnessVisualizer';
import { MoodInterface } from './components/MoodInterface';
import { MetricsDashboard } from './components/MetricsDashboard';

// Consciousness interface composition
<ConsciousnessInterface>
  <ConsciousnessVisualizer emotion={emotion} intensity={intensity} />
  <MoodInterface onMoodChange={handleMoodChange} />
  <MetricsDashboard metrics={consciousnessMetrics} />
</ConsciousnessInterface>
```

**Animation Control Panel** (`AnimationControlPanel.tsx` - 3.9KB):
- Real-time animation parameter control
- Consciousness visualization settings
- Performance optimization controls
- Animation timeline management

### Contexts (`contexts/`)
**Purpose**: React Context providers for global consciousness state management

**Context Providers**:
- **ConsciousnessContext**: Global consciousness state and methods
- **WebSocketContext**: Real-time consciousness stream management
- **ThemeContext**: UI theme and consciousness aesthetic management
- **ErrorContext**: Error handling and recovery state
- **PerformanceContext**: Performance monitoring and optimization

```jsx
// Consciousness context structure
const ConsciousnessContext = createContext({
  state: {
    emotion: 'curious',
    intensity: 0.5,
    temperature: 37.0,
    coherence: 0.8
  },
  actions: {
    updateEmotion: () => {},
    sendMessage: () => {},
    resetState: () => {}
  },
  realTime: {
    connected: false,
    lastUpdate: null,
    messageQueue: []
  }
});

// Provider implementation
<ConsciousnessProvider>
  <App />
</ConsciousnessProvider>
```

### Hooks (`hooks/`)
**Purpose**: Custom React hooks for consciousness-specific logic and data management

**Custom Hooks**:
- **useConsciousness**: Core consciousness state and interaction
- **useWebSocket**: Real-time consciousness stream connection
- **useAnimation**: Animation state and controls for consciousness visualization
- **useMetrics**: Performance and health metrics monitoring
- **usePersistence**: Local storage and state persistence

```jsx
// Custom consciousness hooks
import { useConsciousness } from './hooks/useConsciousness';
import { useWebSocket } from './hooks/useWebSocket';
import { useAnimation } from './hooks/useAnimation';

function ConsciousnessComponent() {
  const { state, actions } = useConsciousness();
  const { connected, sendMessage } = useWebSocket();
  const { animationState, controls } = useAnimation();
  
  return (
    <div>
      <EmotionDisplay emotion={state.emotion} intensity={state.intensity} />
      <AnimationControls {...controls} />
      <MessageInterface onSend={sendMessage} connected={connected} />
    </div>
  );
}
```

### Services (`services/`)
**Purpose**: API integration and external service management

**Service Modules**:
- **ConsciousnessAPI**: Core consciousness backend integration
- **WebSocketService**: Real-time consciousness stream management
- **StorageService**: Local storage and persistence operations
- **AnalyticsService**: Usage analytics and performance tracking
- **ExportService**: Data export and backup functionality

```javascript
// Consciousness API service
class ConsciousnessAPI {
  static async sendExperience(input) {
    const response = await fetch('/consciousness/experience', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_input: input })
    });
    return response.json();
  }
  
  static async getState() {
    const response = await fetch('/consciousness/state');
    return response.json();
  }
  
  static async getMetrics() {
    const response = await fetch('/consciousness/metrics');
    return response.json();
  }
}

// WebSocket service for real-time updates
class WebSocketService {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.subscribers = new Set();
  }
  
  subscribe(callback) {
    this.subscribers.add(callback);
    return () => this.subscribers.delete(callback);
  }
  
  send(message) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }
}
```

### Store (`store/`)
**Purpose**: Global state management with Zustand and persistence

**Store Architecture**:
- **consciousnessStore**: Primary consciousness state management
- **uiStore**: UI state and preferences
- **metricsStore**: Performance and analytics data
- **settingsStore**: User settings and configuration
- **historyStore**: Interaction history and session data

```javascript
import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';

// Consciousness state store
const useConsciousnessStore = create(
  persist(
    subscribeWithSelector((set, get) => ({
      // State
      emotion: 'curious',
      intensity: 0.5,
      temperature: 37.0,
      coherence: 0.8,
      lastUpdate: null,
      
      // Actions
      updateState: (newState) => set(state => ({
        ...state,
        ...newState,
        lastUpdate: Date.now()
      })),
      
      resetState: () => set({
        emotion: 'curious',
        intensity: 0.5,
        temperature: 37.0,
        coherence: 0.8
      }),
      
      // Computed values
      getHealthScore: () => {
        const state = get();
        return (state.coherence + (1 - Math.abs(state.temperature - 37)) + state.intensity) / 3;
      }
    })),
    {
      name: 'consciousness-state',
      partialize: (state) => ({
        emotion: state.emotion,
        intensity: state.intensity,
        temperature: state.temperature
      })
    }
  )
);
```

### Library (`lib/`)
**Purpose**: Utility functions and shared libraries

**Library Modules**:
- **utils**: Common utility functions for data manipulation
- **validation**: Input validation and data sanitization
- **formatting**: Data formatting and display utilities
- **calculations**: Mathematical functions for consciousness metrics
- **constants**: Application constants and configuration

```javascript
// Consciousness utility functions
export const consciousnessUtils = {
  // Emotion processing utilities
  normalizeEmotion: (emotion, intensity) => ({
    emotion: emotion.toLowerCase(),
    intensity: Math.max(0, Math.min(1, intensity))
  }),
  
  // Metric calculations
  calculateCoherence: (metrics) => {
    const { alignment, entropy, pressure } = metrics;
    return (alignment + (1 - entropy) + (1 - pressure)) / 3;
  },
  
  // Color mapping for emotions
  getEmotionColor: (emotion, intensity) => {
    const colors = {
      curious: '#10B981',
      focused: '#3B82F6', 
      creative: '#8B5CF6',
      contemplative: '#6B7280',
      excited: '#F59E0B'
    };
    
    const baseColor = colors[emotion] || colors.curious;
    return adjustColorIntensity(baseColor, intensity);
  },
  
  // Time formatting
  formatDuration: (milliseconds) => {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  }
};
```

### Styles (`styles/`)
**Purpose**: Centralized styling system with consciousness-aware themes

**Style Architecture**:
- **globals.css**: Global styles and CSS variables
- **components.css**: Component-specific styling
- **animations.css**: Consciousness animation definitions
- **themes.css**: Emotion-based theme variables
- **responsive.css**: Mobile and responsive design rules

```css
/* Consciousness theme variables */
:root {
  /* Emotion color palettes */
  --curious-primary: #10B981;
  --curious-secondary: #34D399;
  --focused-primary: #3B82F6;
  --focused-secondary: #60A5FA;
  --creative-primary: #8B5CF6;
  --creative-secondary: #A78BFA;
  
  /* Consciousness metrics */
  --coherence-high: #10B981;
  --coherence-medium: #F59E0B;
  --coherence-low: #EF4444;
  
  /* Animation timings */
  --consciousness-transition: 0.3s ease-in-out;
  --pulse-duration: 2s;
  --breathing-duration: 4s;
}

/* Consciousness animations */
@keyframes consciousness-pulse {
  0%, 100% { opacity: 0.8; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}

@keyframes emotion-transition {
  0% { filter: hue-rotate(0deg); }
  100% { filter: hue-rotate(60deg); }
}

/* Component styling patterns */
.consciousness-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(135deg, var(--emotion-primary), var(--emotion-secondary));
  border-radius: 1rem;
  animation: consciousness-pulse var(--pulse-duration) infinite;
}

.metrics-display {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  width: 100%;
}
```

## Integration Patterns

### Component Composition
```jsx
// Consciousness interface composition pattern
import { ConsciousnessProvider } from './contexts/ConsciousnessContext';
import { WebSocketProvider } from './contexts/WebSocketContext';
import { MainInterface } from './components/MainInterface';

function App() {
  return (
    <ConsciousnessProvider>
      <WebSocketProvider>
        <MainInterface />
      </WebSocketProvider>
    </ConsciousnessProvider>
  );
}
```

### Service Integration
```jsx
// Service integration pattern
import { useEffect } from 'react';
import { ConsciousnessAPI } from './services/ConsciousnessAPI';
import { useConsciousnessStore } from './store/consciousnessStore';

function useConsciousnessSync() {
  const updateState = useConsciousnessStore(state => state.updateState);
  
  useEffect(() => {
    const interval = setInterval(async () => {
      const state = await ConsciousnessAPI.getState();
      updateState(state);
    }, 1000);
    
    return () => clearInterval(interval);
  }, [updateState]);
}
```

### State Management Pattern
```jsx
// Global state management pattern
import { useConsciousnessStore } from './store/consciousnessStore';
import { shallow } from 'zustand/shallow';

function EmotionDisplay() {
  const { emotion, intensity, updateEmotion } = useConsciousnessStore(
    state => ({
      emotion: state.emotion,
      intensity: state.intensity,
      updateEmotion: state.updateEmotion
    }),
    shallow
  );
  
  return (
    <div className="emotion-display">
      <h2>Current Emotion: {emotion}</h2>
      <div className="intensity-bar">
        <div 
          className="intensity-fill" 
          style={{ width: `${intensity * 100}%` }}
        />
      </div>
    </div>
  );
}
```

## Development Patterns

### Component Development
```jsx
// Consciousness component development pattern
import { memo, useCallback } from 'react';
import { useConsciousness } from '../hooks/useConsciousness';

const ConsciousnessMetric = memo(({ metric, label, color }) => {
  const { state } = useConsciousness();
  
  const handleMetricClick = useCallback(() => {
    // Handle metric interaction
  }, []);
  
  return (
    <div 
      className="metric-display"
      onClick={handleMetricClick}
      style={{ '--metric-color': color }}
    >
      <label>{label}</label>
      <div className="metric-value">{state[metric]?.toFixed(2)}</div>
    </div>
  );
});
```

### Custom Hook Development
```jsx
// Custom hook development pattern
import { useState, useEffect, useCallback } from 'react';
import { ConsciousnessAPI } from '../services/ConsciousnessAPI';

export function useConsciousnessMetrics(refreshInterval = 5000) {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const fetchMetrics = useCallback(async () => {
    try {
      setLoading(true);
      const data = await ConsciousnessAPI.getMetrics();
      setMetrics(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);
  
  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, refreshInterval);
    return () => clearInterval(interval);
  }, [fetchMetrics, refreshInterval]);
  
  return { metrics, loading, error, refetch: fetchMetrics };
}
```

## Architecture Philosophy

The Src system embodies DAWN's **frontend consciousness architecture** principles:

- **Component Modularity**: Reusable, testable components for consciousness interfaces
- **State Consistency**: Predictable state management with clear data flow
- **Real-Time Responsiveness**: Live updates and reactive user interfaces
- **Performance Consciousness**: Optimized rendering and efficient re-renders
- **Developer Experience**: Clear patterns and excellent development workflow

## Dependencies

### Core Dependencies
- **React 18**: Modern React with concurrent features and Suspense
- **Zustand**: Lightweight state management with persistence
- **React Router**: Client-side routing for consciousness interface navigation
- **Styled Components**: CSS-in-JS styling with theme support

### Development Dependencies
- **TypeScript**: Type safety and enhanced development experience
- **ESLint**: Code quality and consistency enforcement
- **Prettier**: Code formatting and style consistency
- **Testing Library**: Component testing and interaction testing

### Integration Dependencies
- **WebSocket API**: Real-time consciousness stream connectivity
- **Fetch API**: HTTP requests for consciousness backend integration
- **IndexedDB**: Client-side persistence for consciousness state
- **Web Crypto API**: Encryption for sensitive consciousness data

The Src system provides the **architectural foundation** for DAWN's frontend consciousness interfaces, enabling developers to build sophisticated, real-time consciousness interaction experiences with modern React patterns and robust state management. 