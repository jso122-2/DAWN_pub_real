// CONSCIOUSNESS ENGINE VISUALIZATION BLUEPRINT FOR CURSOR SCAFFOLDING
// File: src/components/ConsciousnessVisualizer.tsx

import React, { useState, useEffect, useRef } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface ConsciousnessData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: string;
  timestamp: string;
  memory_usage: number;
  neural_activity: number;
  quantum_coherence: number;
  subsystems: {
    [key: string]: {
      active: boolean;
      health: number;
    };
  };
}

interface HistoricalData {
  ticks: number[];
  scup: number[];
  entropy: number[];
  neural_activity: number[];
  quantum_coherence: number[];
}

const ConsciousnessVisualizer: React.FC = () => {
  const [currentData, setCurrentData] = useState<ConsciousnessData | null>(null);
  const [historicalData, setHistoricalData] = useState<HistoricalData>({
    ticks: [],
    scup: [],
    entropy: [],
    neural_activity: [],
    quantum_coherence: []
  });
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:8000/consciousness/stream');
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log('Connected to consciousness stream');
    };

    ws.onmessage = (event) => {
      const data: ConsciousnessData = JSON.parse(event.data);
      setCurrentData(data);
      
      // Update historical data (keep last 50 points)
      setHistoricalData(prev => ({
        ticks: [...prev.ticks.slice(-49), data.tick_number],
        scup: [...prev.scup.slice(-49), data.scup],
        entropy: [...prev.entropy.slice(-49), data.entropy],
        neural_activity: [...prev.neural_activity.slice(-49), data.neural_activity],
        quantum_coherence: [...prev.quantum_coherence.slice(-49), data.quantum_coherence]
      }));
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from consciousness stream');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      ws.close();
    };
  }, []);

  // Chart configurations
  const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: '#1a1a1a',
        titleColor: '#e0e0e0',
        bodyColor: '#808080',
        borderColor: '#2a2a2a',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        grid: {
          color: '#1a1a1a',
          drawBorder: false
        },
        ticks: {
          color: '#808080',
          font: {
            size: 10
          }
        }
      },
      y: {
        grid: {
          color: '#1a1a1a',
          drawBorder: false
        },
        ticks: {
          color: '#808080',
          font: {
            size: 10
          }
        },
        min: 0,
        max: 1
      }
    }
  };

  const getMoodColor = (mood: string) => {
    const moodColors: { [key: string]: string } = {
      'contemplative': '#0080ff',
      'energetic': '#00ff88',
      'chaotic': '#ff0040',
      'harmonious': '#00ffff',
      'introspective': '#8844ff',
      'analytical': '#ffaa00'
    };
    return moodColors[mood] || '#808080';
  };

  return (
    <div className="consciousness-visualizer">
      <style>{`
        .consciousness-visualizer {
          height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          padding: 20px;
          display: grid;
          grid-template-columns: 1fr 1fr 1fr;
          grid-template-rows: auto 1fr 1fr;
          gap: 20px;
        }

        .header {
          grid-column: 1 / -1;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px;
          background: #141414;
          border: 1px solid #2a2a2a;
        }

        .title {
          font-size: 16px;
          text-transform: uppercase;
          letter-spacing: 2px;
        }

        .connection-status {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
          color: #808080;
        }

        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: ${props => props.isConnected ? '#00ff88' : '#ff0040'};
        }

        .metric-card {
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
          display: flex;
          flex-direction: column;
        }

        .metric-label {
          font-size: 11px;
          color: #808080;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 10px;
        }

        .metric-value {
          font-size: 32px;
          font-weight: 300;
          color: #e0e0e0;
          margin-bottom: 10px;
        }

        .metric-bar {
          height: 4px;
          background: #1a1a1a;
          margin-top: auto;
          position: relative;
          overflow: hidden;
        }

        .metric-bar-fill {
          height: 100%;
          background: #00ff88;
          transition: width 0.3s ease;
        }

        .mood-card {
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }

        .mood-value {
          font-size: 24px;
          margin-bottom: 10px;
          text-transform: uppercase;
          letter-spacing: 2px;
        }

        .mood-indicator {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          opacity: 0.3;
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 0.3; }
          50% { transform: scale(1.1); opacity: 0.8; }
        }

        .chart-container {
          grid-column: 1 / -1;
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
          position: relative;
        }

        .chart-title {
          font-size: 12px;
          color: #808080;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 15px;
        }

        .subsystems-grid {
          grid-column: 1 / -1;
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
        }

        .subsystems-title {
          font-size: 12px;
          color: #808080;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 20px;
        }

        .subsystem-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
          gap: 10px;
        }

        .subsystem-item {
          padding: 10px;
          background: #0f0f0f;
          border: 1px solid #1a1a1a;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 12px;
        }

        .subsystem-name {
          color: #e0e0e0;
        }

        .subsystem-health {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .health-bar {
          width: 50px;
          height: 4px;
          background: #1a1a1a;
          position: relative;
        }

        .health-fill {
          height: 100%;
          background: #00ff88;
          transition: width 0.3s ease;
        }

        .tick-counter {
          font-size: 14px;
          color: #808080;
        }

        .tick-number {
          color: #00ff88;
          font-weight: bold;
        }
      `}</style>

      <div className="header">
        <div className="title">CONSCIOUSNESS ENGINE MONITOR</div>
        <div className="connection-status">
          <div className="status-dot" style={{ background: isConnected ? '#00ff88' : '#ff0040' }}></div>
          <span>{isConnected ? 'CONNECTED' : 'DISCONNECTED'}</span>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="metric-card">
        <div className="metric-label">SCUP (System Consciousness Unity %)</div>
        <div className="metric-value">{currentData ? (currentData.scup * 100).toFixed(1) : '0.0'}%</div>
        <div className="metric-bar">
          <div 
            className="metric-bar-fill" 
            style={{ 
              width: `${currentData ? currentData.scup * 100 : 0}%`,
              background: '#00ff88'
            }}
          />
        </div>
      </div>

      <div className="metric-card">
        <div className="metric-label">Entropy</div>
        <div className="metric-value">{currentData ? currentData.entropy.toFixed(3) : '0.000'}</div>
        <div className="metric-bar">
          <div 
            className="metric-bar-fill" 
            style={{ 
              width: `${currentData ? currentData.entropy * 100 : 0}%`,
              background: '#ff0040'
            }}
          />
        </div>
      </div>

      <div className="mood-card">
        <div className="metric-label">Current Mood</div>
        <div 
          className="mood-value"
          style={{ color: currentData ? getMoodColor(currentData.mood) : '#808080' }}
        >
          {currentData ? currentData.mood : 'UNKNOWN'}
        </div>
        <div 
          className="mood-indicator"
          style={{ background: currentData ? getMoodColor(currentData.mood) : '#808080' }}
        />
        <div className="tick-counter">
          TICK: <span className="tick-number">{currentData ? currentData.tick_number : 0}</span>
        </div>
      </div>

      {/* Main Chart */}
      <div className="chart-container">
        <div className="chart-title">Consciousness Metrics Timeline</div>
        <div style={{ height: '300px' }}>
          <Line
            data={{
              labels: historicalData.ticks.map(t => t.toString()),
              datasets: [
                {
                  label: 'SCUP',
                  data: historicalData.scup,
                  borderColor: '#00ff88',
                  backgroundColor: 'rgba(0, 255, 136, 0.1)',
                  tension: 0.4,
                  borderWidth: 2
                },
                {
                  label: 'Entropy',
                  data: historicalData.entropy,
                  borderColor: '#ff0040',
                  backgroundColor: 'rgba(255, 0, 64, 0.1)',
                  tension: 0.4,
                  borderWidth: 2
                },
                {
                  label: 'Neural Activity',
                  data: historicalData.neural_activity,
                  borderColor: '#0080ff',
                  backgroundColor: 'rgba(0, 128, 255, 0.1)',
                  tension: 0.4,
                  borderWidth: 2
                }
              ]
            }}
            options={chartOptions}
          />
        </div>
      </div>

      {/* Subsystems Grid */}
      <div className="subsystems-grid">
        <div className="subsystems-title">Subsystem Health Monitor</div>
        <div className="subsystem-list">
          {currentData && currentData.subsystems && Object.entries(currentData.subsystems).map(([name, data]) => (
            <div key={name} className="subsystem-item">
              <span className="subsystem-name">{name}</span>
              <div className="subsystem-health">
                <span style={{ color: data.active ? '#00ff88' : '#ff0040' }}>
                  {data.active ? 'ON' : 'OFF'}
                </span>
                <div className="health-bar">
                  <div 
                    className="health-fill" 
                    style={{ 
                      width: `${data.health * 100}%`,
                      background: data.health > 0.7 ? '#00ff88' : data.health > 0.3 ? '#ffaa00' : '#ff0040'
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ConsciousnessVisualizer;