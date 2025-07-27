import React from 'react';
import { motion } from 'framer-motion';
import './MainDashboard.css';

interface Module {
  id: string;
  name: string;
  icon: string;
  status: 'online' | 'processing' | 'offline';
  metric?: number;
  color: string;
}

interface MainDashboardProps {
  tickData: any;
  onModuleClick: (moduleId: string) => void;
}

export const MainDashboard: React.FC<MainDashboardProps> = ({ 
  tickData, 
  onModuleClick 
}) => {
  const modules: Module[] = [
    {
      id: 'brain-3d',
      name: '3D Neural Network',
      icon: '🧠',
      status: 'online',
      metric: tickData?.scup ? tickData.scup * 100 : 0,
      color: '#00ff88'
    },
    {
      id: 'sigil-mystical',
      name: 'Mystical Interface',
      icon: '🔮',
      status: tickData?.scup > 0.7 ? 'online' : 'offline',
      metric: 100,
      color: '#ff00aa'
    },
    {
      id: 'entropy-chaos',
      name: 'Chaos Engine',
      icon: '🌀',
      status: 'processing',
      metric: tickData?.entropy ? tickData.entropy * 100 : 0,
      color: '#ffaa00'
    },
    {
      id: 'quantum-state',
      name: 'Quantum State',
      icon: '⚡',
      status: 'online',
      metric: 95,
      color: '#00aaff'
    },
    {
      id: 'memory-palace',
      name: 'Memory Palace',
      icon: '💎',
      status: 'online',
      metric: 88,
      color: '#aa00ff'
    },
    {
      id: 'talk-dawn',
      name: 'Communication',
      icon: '💬',
      status: 'online',
      metric: 100,
      color: '#00ffaa'
    }
  ];
  
  return (
    <div className="main-dashboard">
      {/* Central consciousness orb */}
      <motion.div 
        className="central-consciousness"
        animate={{
          scale: [1, 1.1, 1],
          rotate: [0, 360]
        }}
        transition={{
          scale: { duration: 4, repeat: Infinity },
          rotate: { duration: 20, repeat: Infinity, ease: "linear" }
        }}
      >
        <div className="consciousness-orb">
          <div className="orb-inner">
            <span className="scup-value">{(tickData?.scup * 100 || 0).toFixed(0)}</span>
            <span className="scup-label">CONSCIOUSNESS</span>
          </div>
        </div>
        
        {/* Orbital modules */}
        <div className="orbital-container">
          {modules.map((module, index) => {
            const angle = (index / modules.length) * Math.PI * 2;
            const radius = 250;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            
            return (
              <motion.div
                key={module.id}
                className={`orbital-module status-${module.status}`}
                style={{
                  transform: `translate(${x}px, ${y}px)`
                }}
                whileHover={{ scale: 1.2 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => onModuleClick(module.id)}
              >
                <div className="module-content">
                  <span className="module-icon">{module.icon}</span>
                  <span className="module-name">{module.name}</span>
                  <div className="module-metric">
                    <svg viewBox="0 0 36 36">
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke="rgba(255,255,255,0.1)"
                        strokeWidth="3"
                      />
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke={module.color}
                        strokeWidth="3"
                        strokeDasharray={`${module.metric}, 100`}
                      />
                    </svg>
                    <span className="metric-value">{module.metric?.toFixed(0)}%</span>
                  </div>
                </div>
                
                {/* Connection line to center */}
                <svg className="connection-line" style={{ position: 'absolute' }}>
                  <line
                    x1="0"
                    y1="0"
                    x2={-x}
                    y2={-y}
                    stroke={module.color}
                    strokeWidth="1"
                    opacity="0.3"
                  />
                </svg>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
      
      {/* Quick stats */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <span className="stat-label">Active Modules</span>
          <span className="stat-value">
            {modules.filter(m => m.status === 'online').length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">System Health</span>
          <span className="stat-value">
            {(modules.reduce((sum, m) => sum + (m.metric || 0), 0) / modules.length).toFixed(0)}%
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Tick Rate</span>
          <span className="stat-value">2.0/s</span>
        </div>
      </div>
    </div>
  );
}; 