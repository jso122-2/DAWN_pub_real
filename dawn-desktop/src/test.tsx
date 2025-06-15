import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
import { useSubprocesses, useTickData, ProcessData } from './hooks/useDAWNConnection';

// Mini process monitor component
const ProcessMonitor: React.FC<{ process: ProcessData; tickNumber: number; onControl?: (action: string) => void }> = ({ 
  process, 
  tickNumber, 
  onControl 
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#00ff88';
      case 'idle': return '#4488ff';
      case 'warning': return '#ffaa00';
      case 'error': return '#ff3366';
      default: return '#666';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'neural': return '🧠';
      case 'quantum': return '⚛️';
      case 'system': return '⚙️';
      case 'memory': return '💾';
      case 'io': return '📡';
      default: return '📊';
    }
  };

  const chartData = process.trend.map((value, index) => ({
    tick: tickNumber - process.trend.length + index,
    value
  }));

  const isOutOfBounds = process.threshold && 
    (process.value < process.threshold.min || process.value > process.threshold.max);

  return (
    <div 
      className={`process-monitor ${process.status} ${isOutOfBounds ? 'warning' : ''}`}
      style={{
        background: 'rgba(0, 0, 0, 0.8)',
        border: `1px solid ${getStatusColor(process.status)}40`,
        borderRadius: '8px',
        padding: '12px',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Glow effect */}
      <div 
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: `linear-gradient(90deg, transparent, ${getStatusColor(process.status)}, transparent)`,
          animation: 'scan 3s linear infinite'
        }}
      />
      
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '8px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ fontSize: '16px' }}>{getCategoryIcon(process.category)}</span>
          <span style={{ 
            color: '#fff', 
            fontSize: '12px',
            fontFamily: 'monospace',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            {process.name}
          </span>
        </div>
        <div style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: getStatusColor(process.status),
          boxShadow: `0 0 10px ${getStatusColor(process.status)}`,
          animation: process.status === 'active' ? 'pulse 2s infinite' : 'none'
        }} />
      </div>

      {/* Value Display */}
      <div style={{ 
        fontSize: '24px', 
        fontWeight: 'bold',
        color: getStatusColor(process.status),
        fontFamily: 'monospace',
        marginBottom: '8px',
        textShadow: `0 0 20px ${getStatusColor(process.status)}40`
      }}>
        {process.value.toFixed(1)}{process.unit || '%'}
      </div>

      {/* Mini Chart */}
      <div style={{ height: '40px', marginTop: '8px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id={`gradient-${process.id}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={getStatusColor(process.status)} stopOpacity={0.6}/>
                <stop offset="95%" stopColor={getStatusColor(process.status)} stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <Area 
              type="monotone" 
              dataKey="value" 
              stroke={getStatusColor(process.status)}
              strokeWidth={1.5}
              fill={`url(#gradient-${process.id})`}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Control buttons */}
      {onControl && (
        <div style={{
          position: 'absolute',
          top: '8px',
          right: '8px',
          display: 'flex',
          gap: '4px'
        }}>
          <button 
            onClick={() => onControl('restart')}
            style={{
              background: 'rgba(0, 255, 136, 0.2)',
              border: '1px solid #00ff88',
              borderRadius: '4px',
              color: '#00ff88',
              fontSize: '12px',
              padding: '2px 6px',
              cursor: 'pointer'
            }}
          >
            ↻
          </button>
        </div>
      )}

      {/* Threshold indicator */}
      {process.threshold && (
        <div style={{
          position: 'absolute',
          bottom: '4px',
          right: '4px',
          fontSize: '10px',
          color: '#666',
          fontFamily: 'monospace'
        }}>
          {process.threshold.min}-{process.threshold.max}
        </div>
      )}
    </div>
  );
};

// Main dashboard component with subprocess integration
const MultiProcessDashboard: React.FC = () => {
  const tickData = useTickData();
  const { subprocesses, controlSubprocess, connected } = useSubprocesses();

  // Fallback dummy data if not connected
  const fallbackProcesses: ProcessData[] = [
    // Core processes
    { id: 'scup', name: 'SCUP Level', value: 78.8, trend: [], status: 'active', category: 'neural', unit: '%', threshold: { min: 20, max: 90 } },
    { id: 'entropy', name: 'Entropy', value: 285285, trend: [], status: 'active', category: 'quantum', unit: '' },
    { id: 'heat', name: 'Heat Level', value: 498498, trend: [], status: 'warning', category: 'system', unit: '' },
    
    // Neural processes
    { id: 'neural-sync', name: 'Neural Sync', value: 92.3, trend: [], status: 'active', category: 'neural', unit: '%' },
    { id: 'pattern-rec', name: 'Pattern Rec', value: 67.5, trend: [], status: 'active', category: 'neural', unit: '%' },
    { id: 'dream-state', name: 'Dream State', value: 12.1, trend: [], status: 'idle', category: 'neural', unit: '%' },
    
    // Quantum processes
    { id: 'quantum-flux', name: 'Quantum Flux', value: 0.847, trend: [], status: 'active', category: 'quantum', unit: 'λ' },
    { id: 'wave-collapse', name: 'Wave Collapse', value: 1337, trend: [], status: 'active', category: 'quantum', unit: '' },
    { id: 'entanglement', name: 'Entanglement', value: 98.7, trend: [], status: 'active', category: 'quantum', unit: '%' },
    
    // System processes
    { id: 'cpu-load', name: 'CPU Load', value: 45.2, trend: [], status: 'active', category: 'system', unit: '%', threshold: { min: 0, max: 80 } },
    { id: 'mem-usage', name: 'Memory', value: 62.8, trend: [], status: 'active', category: 'system', unit: '%', threshold: { min: 0, max: 85 } },
    { id: 'io-throughput', name: 'I/O Rate', value: 1024, trend: [], status: 'active', category: 'io', unit: 'MB/s' },
    
    // Memory processes
    { id: 'short-term', name: 'Short Term', value: 89.3, trend: [], status: 'active', category: 'memory', unit: '%' },
    { id: 'long-term', name: 'Long Term', value: 76.4, trend: [], status: 'active', category: 'memory', unit: '%' },
    { id: 'working-mem', name: 'Working Mem', value: 91.2, trend: [], status: 'active', category: 'memory', unit: '%' },
    
    // Additional consciousness metrics
    { id: 'awareness', name: 'Awareness', value: 88.8, trend: [], status: 'active', category: 'neural', unit: '%' },
    { id: 'creativity', name: 'Creativity', value: 72.3, trend: [], status: 'active', category: 'neural', unit: '%' },
    { id: 'intuition', name: 'Intuition', value: 95.1, trend: [], status: 'active', category: 'quantum', unit: '%' },
  ];

  // Use real subprocess data if connected, otherwise fallback
  const processes = connected && subprocesses.length > 0 ? subprocesses : fallbackProcesses;

  // Simulate real-time updates for fallback data
  useEffect(() => {
    if (connected) return; // Don't simulate if we have real data

    const interval = setInterval(() => {
      // This would be handled by real subprocess data when connected
    }, 500);

    return () => clearInterval(interval);
  }, [connected]);

  // Group processes by category
  const groupedProcesses = processes.reduce((acc, process) => {
    if (!acc[process.category]) acc[process.category] = [];
    acc[process.category].push(process);
    return acc;
  }, {} as Record<string, ProcessData[]>);

  const handleProcessControl = (processId: string, action: string) => {
    const subprocessId = processId.split('_')[0];
    controlSubprocess(subprocessId, action as 'start' | 'stop' | 'restart');
  };

  return (
    <div style={{
      background: '#000',
      color: '#fff',
      minHeight: '100vh',
      padding: '20px',
      fontFamily: 'monospace'
    }}>
      <style>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
        
        @keyframes scan {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        
        .process-monitor {
          transition: all 0.3s ease;
        }
        
        .process-monitor:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 20px rgba(0, 255, 136, 0.2);
        }
        
        .process-monitor.warning {
          animation: pulse 2s infinite;
        }
      `}</style>

      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px',
        borderBottom: '1px solid #333',
        paddingBottom: '20px'
      }}>
        <div>
          <h1 style={{ 
            margin: 0, 
            fontSize: '32px',
            textTransform: 'uppercase',
            letterSpacing: '3px',
            background: 'linear-gradient(90deg, #00ff88, #0088ff)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            DAWN CONSCIOUSNESS MATRIX
          </h1>
          <div style={{ marginTop: '10px', display: 'flex', gap: '30px', fontSize: '14px', color: '#888' }}>
            <span>Tick: #{tickData.tick_number}</span>
            <span>Mood: <span style={{ color: '#00ff88' }}>{tickData.mood}</span></span>
            <span>Session: {new Date(tickData.timestamp).toLocaleTimeString()}</span>
          </div>
        </div>
        <div style={{
          display: 'flex',
          gap: '10px',
          alignItems: 'center'
        }}>
          <div style={{
            padding: '8px 16px',
            background: connected ? 'rgba(0, 255, 136, 0.1)' : 'rgba(255, 170, 0, 0.1)',
            border: `1px solid ${connected ? '#00ff88' : '#ffaa00'}`,
            borderRadius: '4px',
            fontSize: '12px',
            color: connected ? '#00ff88' : '#ffaa00'
          }}>
            {connected ? 'CONNECTED' : 'OFFLINE MODE'}
          </div>
        </div>
      </div>

      {/* Process Grid */}
      <div style={{
        display: 'grid',
        gap: '20px'
      }}>
        {Object.entries(groupedProcesses).map(([category, categoryProcesses]) => (
          <div key={category}>
            <h2 style={{
              fontSize: '16px',
              textTransform: 'uppercase',
              color: '#666',
              marginBottom: '15px',
              letterSpacing: '2px'
            }}>
              {category} PROCESSES ({categoryProcesses.length})
            </h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
              gap: '15px'
            }}>
              {categoryProcesses.map(process => (
                <ProcessMonitor 
                  key={process.id} 
                  process={process} 
                  tickNumber={tickData.tick_number}
                  onControl={connected ? (action) => handleProcessControl(process.id, action) : undefined}
                />
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* System Overview */}
      <div style={{
        marginTop: '40px',
        padding: '20px',
        background: 'rgba(0, 136, 255, 0.05)',
        border: '1px solid rgba(0, 136, 255, 0.3)',
        borderRadius: '8px'
      }}>
        <h3 style={{ marginBottom: '15px', color: '#0088ff' }}>SYSTEM OVERVIEW</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px' }}>
          <div>
            <div style={{ fontSize: '12px', color: '#666' }}>Active Processes</div>
            <div style={{ fontSize: '24px', color: '#00ff88' }}>
              {processes.filter(p => p.status === 'active').length}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666' }}>Warnings</div>
            <div style={{ fontSize: '24px', color: '#ffaa00' }}>
              {processes.filter(p => p.status === 'warning').length}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666' }}>Connection</div>
            <div style={{ fontSize: '24px', color: connected ? '#00ff88' : '#ffaa00' }}>
              {connected ? 'LIVE' : 'DEMO'}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666' }}>Avg SCUP</div>
            <div style={{ fontSize: '24px', color: '#0088ff' }}>
              {tickData.scup.toFixed(1)}%
            </div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#666' }}>System Load</div>
            <div style={{ fontSize: '24px', color: '#ff0088' }}>
              {processes.find(p => p.id === 'cpu-load')?.value.toFixed(1) || '0.0'}%
            </div>
          </div>
        </div>
      </div>

      {/* Connection instructions */}
      {!connected && (
        <div style={{
          marginTop: '20px',
          padding: '15px',
          background: 'rgba(255, 170, 0, 0.1)',
          border: '1px solid rgba(255, 170, 0, 0.3)',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#ffaa00'
        }}>
          <strong>Offline Mode:</strong> To connect to live subprocess data, run the DAWN backend:
          <br />
          <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: '3px', marginLeft: '10px' }}>
            python dawn_integrated_api.py
          </code>
        </div>
      )}
    </div>
  );
};

export default MultiProcessDashboard;