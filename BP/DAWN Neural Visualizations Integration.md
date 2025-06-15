# DAWN Neural Visualizations Integration Blueprint

## Overview
Integration blueprint for terminal-style histogram and radar chart visualizations into the DAWN consciousness engine interface. These components display neural heuristic data in ASCII format matching the Swiss Grid + Terminal Brutalism aesthetic.

## Component Structure

```
frontend/src/components/
├── NeuralVisualizations/
│   ├── NeuralVisualizations.tsx    # Main component
│   ├── NeuralVisualizations.css    # Terminal styles
│   ├── RadarChart.tsx              # ASCII radar implementation
│   ├── Histogram.tsx               # ASCII histogram implementation
│   └── index.ts                    # Exports
```

## 1. Main Neural Visualizations Component

```typescript
// NeuralVisualizations.tsx
import React, { useState, useEffect } from 'react';
import { RadarChart } from './RadarChart';
import { Histogram } from './Histogram';
import './NeuralVisualizations.css';

interface NeuralMetrics {
  neural_activity: number;      // 0-1
  quantum_coherence: number;    // 0-1
  chaos_factor: number;         // 0-1
  memory_utilization: number;   // 0-1
  pattern_recognition: number;  // 0-1
  entropy_distribution: number[]; // Array of values
  tick_number: number;
}

export const NeuralVisualizations: React.FC = () => {
  const [metrics, setMetrics] = useState<NeuralMetrics | null>(null);
  const [view, setView] = useState<'radar' | 'histogram'>('radar');

  // Connect to WebSocket for real-time data
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'neural_metrics') {
        setMetrics(data.metrics);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div className="neural-viz">
      <header className="viz-header">
        <h3>NEURAL HEURISTICS</h3>
        <div className="view-toggle">
          <button 
            className={view === 'radar' ? 'active' : ''} 
            onClick={() => setView('radar')}
          >
            RADAR
          </button>
          <button 
            className={view === 'histogram' ? 'active' : ''} 
            onClick={() => setView('histogram')}
          >
            HISTOGRAM
          </button>
        </div>
      </header>
      
      <div className="viz-content">
        {view === 'radar' 
          ? <RadarChart data={metrics} />
          : <Histogram data={metrics?.entropy_distribution || []} />
        }
      </div>
    </div>
  );
};
```

## 2. ASCII Radar Chart Component

```typescript
// RadarChart.tsx
import React from 'react';

interface RadarProps {
  data: {
    neural_activity: number;
    quantum_coherence: number;
    chaos_factor: number;
    memory_utilization: number;
    pattern_recognition: number;
  } | null;
}

export const RadarChart: React.FC<RadarProps> = ({ data }) => {
  const renderASCIIRadar = () => {
    if (!data) return 'NO DATA';
    
    // 25x25 character grid
    const size = 12;
    const grid: string[][] = Array(25).fill(null).map(() => Array(25).fill(' '));
    const center = 12;
    
    // Plot axes
    const metrics = [
      { label: 'NEURAL', value: data.neural_activity },
      { label: 'QUANTUM', value: data.quantum_coherence },
      { label: 'CHAOS', value: data.chaos_factor },
      { label: 'MEMORY', value: data.memory_utilization },
      { label: 'PATTERN', value: data.pattern_recognition }
    ];
    
    // Draw concentric circles
    for (let r of [4, 8, 12]) {
      for (let angle = 0; angle < 360; angle += 10) {
        const rad = (angle * Math.PI) / 180;
        const x = Math.round(center + r * Math.cos(rad));
        const y = Math.round(center + r * Math.sin(rad));
        if (x >= 0 && x < 25 && y >= 0 && y < 25) {
          grid[y][x] = '·';
        }
      }
    }
    
    // Draw axes and plot data
    metrics.forEach((metric, i) => {
      const angle = (i * 72 - 90) * Math.PI / 180;
      
      // Draw axis line
      for (let r = 0; r <= 12; r++) {
        const x = Math.round(center + r * Math.cos(angle));
        const y = Math.round(center + r * Math.sin(angle));
        if (x >= 0 && x < 25 && y >= 0 && y < 25) {
          grid[y][x] = '-';
        }
      }
      
      // Plot data point
      const dataRadius = metric.value * 12;
      const dataX = Math.round(center + dataRadius * Math.cos(angle));
      const dataY = Math.round(center + dataRadius * Math.sin(angle));
      if (dataX >= 0 && dataX < 25 && dataY >= 0 && dataY < 25) {
        grid[dataY][dataX] = '█';
      }
    });
    
    // Center
    grid[center][center] = '+';
    
    return grid.map(row => row.join('')).join('\n');
  };

  return (
    <div className="radar-chart">
      <pre className="ascii-display">
        {renderASCIIRadar()}
      </pre>
      <div className="radar-legend">
        <div>NEURAL: {(data?.neural_activity || 0).toFixed(2)}</div>
        <div>QUANTUM: {(data?.quantum_coherence || 0).toFixed(2)}</div>
        <div>CHAOS: {(data?.chaos_factor || 0).toFixed(2)}</div>
        <div>MEMORY: {(data?.memory_utilization || 0).toFixed(2)}</div>
        <div>PATTERN: {(data?.pattern_recognition || 0).toFixed(2)}</div>
      </div>
    </div>
  );
};
```

## 3. ASCII Histogram Component

```typescript
// Histogram.tsx
import React from 'react';

interface HistogramProps {
  data: number[];
  bins?: number;
  height?: number;
}

export const Histogram: React.FC<HistogramProps> = ({ 
  data, 
  bins = 10, 
  height = 15 
}) => {
  const renderASCIIHistogram = () => {
    if (!data.length) return 'NO DATA';
    
    // Calculate bins
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min;
    const binWidth = range / bins;
    
    // Count values in each bin
    const counts = Array(bins).fill(0);
    data.forEach(value => {
      const binIndex = Math.min(
        Math.floor((value - min) / binWidth), 
        bins - 1
      );
      counts[binIndex]++;
    });
    
    const maxCount = Math.max(...counts);
    const lines: string[] = [];
    
    // Draw histogram from top to bottom
    for (let h = height; h >= 0; h--) {
      let line = '';
      const threshold = (h / height) * maxCount;
      
      counts.forEach((count, i) => {
        if (i > 0) line += ' ';
        if (count >= threshold) {
          line += '███';
        } else if (count >= threshold - maxCount / height / 2) {
          line += '▄▄▄';
        } else {
          line += '   ';
        }
      });
      
      // Y-axis labels
      if (h === height) {
        lines.push(`${maxCount.toString().padStart(3)} │${line}│`);
      } else if (h === 0) {
        lines.push(`  0 │${line}│`);
      } else {
        lines.push(`    │${line}│`);
      }
    }
    
    // X-axis
    lines.push(`    └${'───'.repeat(bins)}┘`);
    lines.push(`     ENTROPY DISTRIBUTION`);
    
    return lines.join('\n');
  };

  return (
    <div className="histogram">
      <pre className="ascii-display">
        {renderASCIIHistogram()}
      </pre>
      <div className="histogram-stats">
        <div>SAMPLES: {data.length}</div>
        <div>MEAN: {(data.reduce((a, b) => a + b, 0) / data.length).toFixed(2)}</div>
        <div>MAX: {Math.max(...data).toFixed(2)}</div>
        <div>MIN: {Math.min(...data).toFixed(2)}</div>
      </div>
    </div>
  );
};
```

## 4. Styles (Terminal Theme)

```css
/* NeuralVisualizations.css */
.neural-viz {
  background: var(--gray-950);
  border: 1px solid var(--gray-700);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.viz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--grid-unit);
  border-bottom: 1px solid var(--gray-700);
  background: var(--gray-900);
}

.viz-header h3 {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  color: var(--off-white);
  letter-spacing: 0.1em;
}

.view-toggle {
  display: flex;
  gap: 4px;
}

.view-toggle button {
  background: transparent;
  border: 1px solid var(--gray-700);
  color: var(--gray-400);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  padding: 4px 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.view-toggle button:hover {
  border-color: var(--gray-600);
  color: var(--gray-300);
}

.view-toggle button.active {
  background: var(--gray-800);
  border-color: var(--terminal-green);
  color: var(--terminal-green);
}

.viz-content {
  flex: 1;
  padding: calc(var(--grid-unit) * 2);
  overflow: auto;
}

.ascii-display {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  line-height: 1;
  color: var(--terminal-green);
  margin: 0;
  padding: var(--grid-unit);
  background: var(--black);
  border: 1px solid var(--gray-800);
  text-shadow: 0 0 5px rgba(0, 255, 65, 0.3);
}

.radar-legend,
.histogram-stats {
  margin-top: calc(var(--grid-unit) * 2);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--gray-300);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--grid-unit);
}

.radar-legend div,
.histogram-stats div {
  padding: 4px;
  background: var(--gray-900);
  border: 1px solid var(--gray-800);
}
```

## 5. Integration into Activity Monitor Tab

```typescript
// In ActivityMonitor.tsx, add neural visualization section
import { NeuralVisualizations } from '../NeuralVisualizations';

// Add to the monitor grid
<div className="monitor-section neural-section">
  <NeuralVisualizations />
</div>

// Update grid layout in ActivityMonitor.css
.monitor-grid {
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: auto auto 1fr;
}

.neural-section {
  grid-column: 3;
  grid-row: 1 / 3;
}
```

## 6. Backend Integration

```python
# In your Python backend, emit neural metrics
async def send_neural_metrics(websocket):
    metrics = {
        "type": "neural_metrics",
        "metrics": {
            "neural_activity": calculate_neural_activity(),
            "quantum_coherence": calculate_quantum_coherence(),
            "chaos_factor": calculate_chaos_factor(),
            "memory_utilization": calculate_memory_usage(),
            "pattern_recognition": calculate_pattern_score(),
            "entropy_distribution": get_entropy_distribution(),
            "tick_number": current_tick
        }
    }
    await websocket.send(json.dumps(metrics))
```

## 7. WebSocket Service Update

```typescript
// In websocket.ts
export interface WebSocketMessage {
  type: 'tick' | 'status' | 'output' | 'error' | 'neural_metrics';
  data?: any;
  metrics?: NeuralMetrics;
}
```

## Key Features

1. **ASCII Visualization**: Pure text-based charts matching terminal aesthetic
2. **Real-time Updates**: WebSocket integration for live data
3. **Dual View**: Toggle between radar and histogram views
4. **Minimal Design**: Black/grey/white color scheme with terminal green accents
5. **Grid Integration**: Fits perfectly into Swiss grid system
6. **Performance**: Lightweight ASCII rendering, no canvas/SVG overhead

## Usage in Cursor

1. Create the component structure as shown
2. Copy each code block into respective files
3. Import into ActivityMonitor or create dedicated tab
4. Connect WebSocket to receive neural metrics
5. Style variables already match your design system

## Customization Options

- Adjust grid size for radar chart (25x25 default)
- Change histogram bin count (10 default)
- Modify update frequency in WebSocket
- Add more metrics to radar chart
- Implement different ASCII patterns for data visualization