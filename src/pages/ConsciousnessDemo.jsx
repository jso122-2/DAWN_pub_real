import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import ConsciousnessMatrix from '../components/ConsciousnessMatrix';
import ModuleCard from '../components/ModuleCard';
import { NeuralNetworkViewer } from '../modules/neuralNetwork3D/components/NeuralNetworkViewer';
import { useConsciousnessStore } from '../stores/consciousnessStore';
import { useMetricsHistory } from '../hooks/useMetricsHistory';
import { webSocketService } from '../services/WebSocketService';
import './ConsciousnessDemo.css';

const ConsciousnessDemo = () => {
  const { tickData, isConnected, connectionState } = useConsciousnessStore();
  const metricsHistory = useMetricsHistory(tickData);
  
  // Connect to WebSocket on component mount
  useEffect(() => {
    console.log('🔌 Initializing DAWN Consciousness Demo...');
    webSocketService.connect();
    
    return () => {
      console.log('🔌 Disconnecting from DAWN...');
      webSocketService.disconnect();
    };
  }, []);
  
  // Demo modules for dashboard
  const demoModules = [
    {
      id: 'consciousness-matrix',
      name: 'Consciousness Matrix',
      description: 'Core consciousness visualization and analysis',
      icon: '🧠',
      color: '#8b5cf6',
      showExtraMetrics: true,
      metricLabel: 'Coherence'
    },
    {
      id: 'neural-network',
      name: 'Neural Network',
      description: 'Real-time neural activity mapping',
      icon: '🕸️',
      color: '#0088ff',
      showExtraMetrics: false,
      metricLabel: 'Activity'
    },
    {
      id: 'chaos-engine',
      name: 'Chaos Engine',
      description: 'Entropy and chaos dynamics monitoring',
      icon: '🌪️',
      color: '#ff6b35',
      showExtraMetrics: false,
      metricLabel: 'Entropy'
    },
    {
      id: 'memory-core',
      name: 'Memory Core',
      description: 'Memory formation and recall patterns',
      icon: '💾',
      color: '#f59e0b',
      showExtraMetrics: false,
      metricLabel: 'Retention'
    }
  ];
  
  return (
    <div className="consciousness-demo">
      {/* Header */}
      <motion.div 
        className="demo-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="demo-title">
          DAWN Consciousness
          <span className="highlight"> Visualization</span>
        </h1>
        <p className="demo-subtitle">
          Real-time consciousness monitoring and analysis system
        </p>
        
        {/* Connection Status */}
        <div className={`connection-indicator ${connectionState}`}>
          <div className="connection-dot" />
          <span className="connection-text">
            {isConnected ? 'Connected to DAWN Engine' : `Status: ${connectionState}`}
          </span>
          {tickData && (
            <span className="tick-info">
              Tick #{tickData.tick_count} • Rate: {webSocketService.getTickRate().toFixed(1)} Hz
            </span>
          )}
        </div>
      </motion.div>
      
      {/* Main Consciousness Matrix */}
      <motion.section 
        className="matrix-section"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <ConsciousnessMatrix />
      </motion.section>
      
      {/* Dashboard Modules */}
      <motion.section 
        className="modules-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <h2 className="section-title">System Modules</h2>
        <div className="modules-grid">
          {demoModules.map((module, index) => (
            <motion.div
              key={module.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ 
                duration: 0.5, 
                delay: 0.6 + index * 0.1 
              }}
            >
              <ModuleCard module={module} />
            </motion.div>
          ))}
        </div>
      </motion.section>
      
      {/* Neural Network 3D */}
      <motion.section 
        className="neural-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.8 }}
      >
        <h2 className="section-title">Neural Network Visualization</h2>
        <div className="neural-container">
          <NeuralNetworkViewer 
            moduleId="neural-demo"
            showActivity={true}
            showBrainwaves={true}
            onNeuronSelect={(neuron) => {
              console.log('Selected neuron:', neuron);
            }}
          />
        </div>
      </motion.section>
      
      {/* Metrics Overview */}
      {metricsHistory.history.length > 0 && (
        <motion.section 
          className="metrics-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
        >
          <h2 className="section-title">Metrics Analysis</h2>
          <div className="metrics-overview">
            <div className="metric-card">
              <h3>Performance Score</h3>
              <div className="metric-value large">
                {metricsHistory.performanceScore}%
              </div>
              <div className="metric-trend">
                Trend: {metricsHistory.trends.scup}
              </div>
            </div>
            
            <div className="metric-card">
              <h3>SCUP Volatility</h3>
              <div className="metric-value">
                {(metricsHistory.volatility.scup * 100).toFixed(1)}%
              </div>
            </div>
            
            <div className="metric-card">
              <h3>Entropy Correlation</h3>
              <div className="metric-value">
                {metricsHistory.correlations.scupEntropy.toFixed(3)}
              </div>
            </div>
            
            <div className="metric-card">
              <h3>Data Points</h3>
              <div className="metric-value">
                {metricsHistory.history.length}
              </div>
            </div>
          </div>
          
          {/* Mood Distribution */}
          <div className="mood-distribution">
            <h3>Mood Distribution</h3>
            <div className="mood-chart">
              {Object.entries(metricsHistory.getMoodDistribution()).map(([mood, data]) => (
                <div key={mood} className="mood-bar">
                  <span className="mood-label">{mood}</span>
                  <div className="mood-progress">
                    <div 
                      className="mood-fill"
                      style={{ 
                        width: `${data.percentage}%`,
                        backgroundColor: `hsl(${mood.length * 30}, 70%, 50%)`
                      }}
                    />
                  </div>
                  <span className="mood-percentage">{data.percentage.toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        </motion.section>
      )}
      
      {/* Debug Info (only in development) */}
      {process.env.NODE_ENV === 'development' && tickData && (
        <motion.section 
          className="debug-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 1.2 }}
        >
          <h3>Debug Information</h3>
          <pre className="debug-data">
            {JSON.stringify(tickData, null, 2)}
          </pre>
        </motion.section>
      )}
    </div>
  );
};

export default ConsciousnessDemo;