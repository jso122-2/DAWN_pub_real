import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useConsciousness } from '../contexts/ConsciousnessContext';
import './HomePage.css';

const moduleCards = [
  { id: 1, name: 'Consciousness Core', path: '/consciousness', status: 'online', progress: 85, color: '#00ff88' },
  { id: 2, name: 'Neural Network', path: '/neural', status: 'processing', progress: 72, color: '#00aaff' },
  { id: 3, name: 'Memory Archive', path: '/modules', status: 'online', progress: 96, color: '#ff00aa' },
  { id: 4, name: 'Pattern Engine', path: '/demo', status: 'online', progress: 68, color: '#ffaa00' },
  { id: 5, name: 'Quantum Bridge', path: '/modules', status: 'offline', progress: 0, color: '#ff4444' },
  { id: 6, name: 'Reality Parser', path: '/demo', status: 'processing', progress: 45, color: '#aa00ff' },
];

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { data } = useConsciousness();

  const handleModuleClick = (path: string) => {
    navigate(path);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return '#00ff88';
      case 'processing': return '#ffaa00';
      case 'offline': return '#ff4444';
      default: return '#666666';
    }
  };

  return (
    <div className="homepage">
      {/* Animated Background */}
      <div className="background-grid">
        {Array.from({ length: 50 }).map((_, i) => (
          <motion.div
            key={i}
            className="grid-particle"
            animate={{
              y: [0, -100, 0],
              opacity: [0.1, 0.5, 0.1],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="homepage-content">
        {/* Epic Title */}
        <motion.div
          className="title-section"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.2 }}
        >
          <h1 className="epic-title">DAWN</h1>
          <p className="title-subtitle">Digital Autonomous Waking Network</p>
          <div className="title-glow" />
        </motion.div>

        {/* Live Metrics Bar */}
        <motion.div
          className="metrics-bar"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <div className="metric-item">
            <span className="metric-label">SCUP</span>
            <span className="metric-value scup">{data.scup.toFixed(0)}%</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Entropy</span>
            <span className="metric-value entropy">{data.entropy.toFixed(2)}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Heat</span>
            <span className="metric-value heat">{data.heat.toFixed(2)}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Mood</span>
            <span className={`metric-value mood ${data.mood}`}>{data.mood}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Tick Rate</span>
            <span className="metric-value tick">{data.tickRate}/s</span>
          </div>
        </motion.div>

        {/* Central Consciousness Orb */}
        <motion.div
          className="consciousness-orb-container"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.2, delay: 0.8 }}
        >
          <div className="consciousness-orb">
            <motion.div
              className="orb-core"
              animate={{
                scale: [1, 1.1, 1],
                boxShadow: [
                  `0 0 50px rgba(0, 255, 136, ${data.scup / 100})`,
                  `0 0 80px rgba(0, 255, 136, ${data.scup / 80})`,
                  `0 0 50px rgba(0, 255, 136, ${data.scup / 100})`,
                ],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
            <div className="orb-value">
              <span className="orb-scup">{data.scup.toFixed(0)}</span>
              <span className="orb-label">SCUP</span>
            </div>
            <div className="orb-rings">
              {[1, 2, 3].map((ring) => (
                <motion.div
                  key={ring}
                  className="orb-ring"
                  animate={{ rotate: 360 }}
                  transition={{
                    duration: 10 + ring * 5,
                    repeat: Infinity,
                    ease: "linear",
                  }}
                  style={{
                    animationDelay: `${ring * 0.5}s`,
                  }}
                />
              ))}
            </div>
          </div>
        </motion.div>

        {/* Module Cards Grid */}
        <motion.div
          className="modules-grid"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 1 }}
        >
          {moduleCards.map((module, index) => (
            <motion.div
              key={module.id}
              className="module-card"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.2 + index * 0.1 }}
              whileHover={{
                scale: 1.05,
                boxShadow: `0 20px 40px rgba(${parseInt(module.color.slice(1, 3), 16)}, ${parseInt(module.color.slice(3, 5), 16)}, ${parseInt(module.color.slice(5, 7), 16)}, 0.3)`,
              }}
              onClick={() => handleModuleClick(module.path)}
            >
              <div className="card-header">
                <h3>{module.name}</h3>
                <div 
                  className="status-indicator"
                  style={{ backgroundColor: getStatusColor(module.status) }}
                />
              </div>
              
              <div className="progress-container">
                <svg className="progress-ring" viewBox="0 0 100 100">
                  <circle
                    className="progress-ring-bg"
                    cx="50"
                    cy="50"
                    r="45"
                  />
                  <motion.circle
                    className="progress-ring-fill"
                    cx="50"
                    cy="50"
                    r="45"
                    style={{
                      stroke: module.color,
                      strokeDasharray: `${2 * Math.PI * 45}`,
                    }}
                    initial={{ strokeDashoffset: 2 * Math.PI * 45 }}
                    animate={{
                      strokeDashoffset: 2 * Math.PI * 45 * (1 - module.progress / 100),
                    }}
                    transition={{ duration: 1.5, delay: 1.5 + index * 0.1 }}
                  />
                </svg>
                <div className="progress-text">
                  <span className="progress-value">{module.progress}%</span>
                  <span className="progress-status">{module.status}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Quick Actions & System Health */}
        <motion.div
          className="bottom-section"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 2 }}
        >
          <div className="quick-actions">
            <motion.button
              className="action-btn primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              🚀 Initialize Sequence
            </motion.button>
            <motion.button
              className="action-btn secondary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ⚡ Boost Performance
            </motion.button>
            <motion.button
              className="action-btn tertiary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              🔧 System Diagnostics
            </motion.button>
          </div>

          <div className="system-health">
            <h4>System Health</h4>
            <div className="health-bar">
              <motion.div
                className="health-fill"
                initial={{ width: 0 }}
                animate={{ width: `${data.networkHealth}%` }}
                transition={{ duration: 2, delay: 2.5 }}
              />
            </div>
            <span className="health-value">{data.networkHealth}%</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default HomePage; 