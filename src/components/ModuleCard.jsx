import React from 'react';
import { motion } from 'framer-motion';
import { useConsciousnessStore } from '../stores/consciousnessStore';
import './ModuleCard.css';

const ModuleCard = ({ module }) => {
  const { tickData } = useConsciousnessStore();
  
  const getModuleMetric = () => {
    if (!tickData) return module.defaultMetric || 0;
    
    switch (module.id) {
      case 'neural-network':
        return Math.floor((tickData.scup / 100) * 100);
      case 'chaos-engine':
        return Math.floor(tickData.entropy * 100);
      case 'neural-state':
        return Math.floor((1 - (tickData.heat || 0)) * 100);
      case 'consciousness-matrix':
        return Math.floor((tickData.scup / 100) * 100);
      case 'memory-core':
        return Math.floor(((tickData.scup / 100) + (1 - tickData.entropy)) / 2 * 100);
      default:
        return module.defaultMetric || Math.floor(Math.random() * 100);
    }
  };
  
  const metric = getModuleMetric();
  const isActive = metric > 50;
  const isHighActivity = metric > 75;
  
  // Determine color based on module type and activity
  const getModuleColor = () => {
    if (!isActive) return '#64748b'; // Gray for inactive
    
    switch (module.id) {
      case 'neural-network':
        return '#0088ff';
      case 'chaos-engine':
        return '#ff6b35';
      case 'neural-state':
        return '#00ff88';
      case 'consciousness-matrix':
        return '#8b5cf6';
      case 'memory-core':
        return '#f59e0b';
      default:
        return module.color || '#0088ff';
    }
  };
  
  const moduleColor = getModuleColor();
  
  return (
    <motion.div
      className={`module-card ${isActive ? 'active' : ''} ${isHighActivity ? 'high-activity' : ''}`}
      whileHover={{ 
        scale: 1.02,
        y: -2
      }}
      whileTap={{ scale: 0.98 }}
      animate={{
        borderColor: isActive ? moduleColor + '40' : '#374151',
        boxShadow: isActive 
          ? `0 4px 20px ${moduleColor}20` 
          : '0 2px 8px rgba(0, 0, 0, 0.1)'
      }}
      transition={{ duration: 0.3 }}
    >
      <div className="module-header">
        <div 
          className="module-icon"
          style={{ color: moduleColor }}
        >
          {module.icon}
        </div>
        <div className="module-status">
          {isActive && (
            <motion.div
              className="status-pulse"
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.7, 1, 0.7]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              style={{ backgroundColor: moduleColor }}
            />
          )}
        </div>
      </div>
      
      <div className="module-content">
        <h3 className="module-name">{module.name}</h3>
        <p className="module-description">{module.description}</p>
        
        <div className="module-metrics">
          <div className="metric-display">
            <div className="metric-bar">
              <motion.div 
                className="metric-fill"
                style={{ backgroundColor: moduleColor }}
                initial={{ width: 0 }}
                animate={{ width: `${metric}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
              <div className="metric-glow" style={{ 
                background: `linear-gradient(90deg, transparent, ${moduleColor}40, transparent)`,
                animation: isActive ? 'slideGlow 2s infinite' : 'none'
              }} />
            </div>
            <div className="metric-details">
              <span className="metric-value" style={{ color: moduleColor }}>
                {metric}%
              </span>
              <span className="metric-label">
                {module.metricLabel || 'Activity'}
              </span>
            </div>
          </div>
          
          {/* Additional metrics for consciousness data */}
          {tickData && module.showExtraMetrics && (
            <div className="extra-metrics">
              <div className="extra-metric">
                <span className="extra-metric-label">SCUP</span>
                <span className="extra-metric-value">{(tickData.scup / 100 * 100).toFixed(1)}%</span>
              </div>
              <div className="extra-metric">
                <span className="extra-metric-label">Entropy</span>
                <span className="extra-metric-value">{(tickData.entropy * 100).toFixed(1)}%</span>
              </div>
              <div className="extra-metric">
                <span className="extra-metric-label">Mood</span>
                <span className="extra-metric-value mood-indicator">{tickData.mood}</span>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {isActive && (
        <motion.div
          className="active-indicator"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <motion.span
            className="pulse-ring"
            animate={{
              scale: [1, 2],
              opacity: [0.8, 0]
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeOut"
            }}
            style={{ borderColor: moduleColor }}
          />
          <span 
            className="pulse-dot"
            style={{ backgroundColor: moduleColor }}
          />
        </motion.div>
      )}
      
      {/* Activity waves for high activity modules */}
      {isHighActivity && (
        <div className="activity-waves">
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              className="wave"
              animate={{
                scaleX: [0, 1],
                opacity: [0.6, 0]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.6,
                ease: "easeOut"
              }}
              style={{ 
                background: `linear-gradient(90deg, transparent, ${moduleColor}30, transparent)`
              }}
            />
          ))}
        </div>
      )}
    </motion.div>
  );
};

export default ModuleCard; 