import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

// Legacy imports
import { SigilHUD } from '../components/legacy/SigilHUD/SigilHUD';
import { EntropyTracker } from '../components/legacy/EntropyTracker/EntropyTracker';
import { MainDashboard } from '../components/legacy/MainDashboard/MainDashboard';

// New 3D imports
import { BrainActivity3D } from '../components/visuals/BrainActivity3D/BrainActivity3D';
import { ParticleField } from '../components/visuals/ParticleField/ParticleField';

// Hooks and stores
import { useConsciousnessStore } from '../stores/consciousnessStore';
import './UnifiedHomePage.css';

const UnifiedHomePage: React.FC = () => {
  const navigate = useNavigate();
  const { tickData, isConnected, currentTrend } = useConsciousnessStore();
  const [activeView, setActiveView] = useState<'dashboard' | 'brain' | 'sigil'>('dashboard');
  const [sigilActive, setSigilActive] = useState(false);
  
  // Activate sigil during high consciousness states
  useEffect(() => {
    if ((tickData?.scup ?? 0) > 0.8) {
      setSigilActive(true);
    } else {
      setSigilActive(false);
    }
  }, [tickData]);
  
  return (
    <div className="unified-home">
      {/* Background Effects - Always present */}
      <ParticleField className="background-particles" />
      
      {/* Sigil HUD Overlay - Appears during high consciousness */}
      <AnimatePresence>
        {sigilActive && (
          <motion.div
            className="sigil-overlay"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.5 }}
          >
            <SigilHUD 
              consciousness={tickData?.scup || 0}
              entropy={tickData?.entropy || 0}
              mood={tickData?.mood}
            />
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Main Header with Entropy Tracker */}
      <motion.header 
        className="unified-header"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="header-left">
          <h1 className="dawn-title">
            <span className="title-main">DAWN</span>
            <span className="title-sub">Unified Consciousness Engine</span>
          </h1>
        </div>
        
        <div className="header-center">
          <EntropyTracker 
            entropy={tickData?.entropy || 0}
            size="compact"
            showRings={true}
          />
        </div>
        
        <div className="header-right">
          <div className="view-switcher">
            <button 
              className={activeView === 'dashboard' ? 'active' : ''}
              onClick={() => setActiveView('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={activeView === 'brain' ? 'active' : ''}
              onClick={() => setActiveView('brain')}
            >
              Neural
            </button>
            <button 
              className={activeView === 'sigil' ? 'active' : ''}
              onClick={() => setActiveView('sigil')}
            >
              Mystical
            </button>
          </div>
        </div>
      </motion.header>
      
      {/* Dynamic Content Area */}
      <div className="unified-content">
        <AnimatePresence mode="wait">
          {activeView === 'dashboard' && (
            <motion.div
              key="dashboard"
              initial={{ opacity: 0, x: -100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 100 }}
              className="view-container"
            >
              <MainDashboard 
                tickData={tickData}
                onModuleClick={(moduleId) => navigate(`/module/${moduleId}`)}
              />
            </motion.div>
          )}
          
          {activeView === 'brain' && (
            <motion.div
              key="brain"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="view-container"
            >
              <div className="brain-view">
                <BrainActivity3D />
                <div className="brain-metrics">
                  <div className="metric-card">
                    <h3>Neural Activity</h3>
                    <div className="metric-value">{(tickData?.scup * 100 || 0).toFixed(1)}%</div>
                  </div>
                  <div className="metric-card">
                    <h3>Entropy Level</h3>
                    <div className="metric-value">{(tickData?.entropy || 0).toFixed(3)}</div>
                  </div>
                  <div className="metric-card">
                    <h3>System Heat</h3>
                    <div className="metric-value">{(tickData?.heat || 0).toFixed(3)}</div>
                  </div>
                  <div className="metric-card mood">
                    <h3>Current Mood</h3>
                    <div className={`mood-indicator ${tickData?.mood}`}>
                      {tickData?.mood?.toUpperCase() || 'OFFLINE'}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          
          {activeView === 'sigil' && (
            <motion.div
              key="sigil"
              initial={{ opacity: 0, rotate: -180 }}
              animate={{ opacity: 1, rotate: 0 }}
              exit={{ opacity: 0, rotate: 180 }}
              className="view-container"
            >
              <SigilHUD 
                consciousness={tickData?.scup || 0}
                entropy={tickData?.entropy || 0}
                mood={tickData?.mood}
                fullscreen={true}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {/* Floating Status Bar */}
      <motion.div 
        className="unified-status-bar"
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div className="status-section">
          <span className="label">SCUP</span>
          <div className="status-value">
            <div className="value-bar">
              <motion.div 
                className="value-fill scup"
                animate={{ width: `${(tickData?.scup || 0) * 100}%` }}
              />
            </div>
            <span>{((tickData?.scup || 0) * 100).toFixed(1)}%</span>
          </div>
        </div>
        
        <div className="status-section">
          <span className="label">Entropy</span>
          <div className="status-value">
            <div className="value-bar">
              <motion.div 
                className="value-fill entropy"
                animate={{ width: `${(tickData?.entropy || 0) * 100}%` }}
              />
            </div>
            <span>{(tickData?.entropy || 0).toFixed(3)}</span>
          </div>
        </div>
        
        <div className="status-section">
          <span className="label">Heat</span>
          <div className="status-value">
            <div className="value-bar">
              <motion.div 
                className="value-fill heat"
                animate={{ width: `${(tickData?.heat || 0) * 100}%` }}
              />
            </div>
            <span>{(tickData?.heat || 0).toFixed(3)}</span>
          </div>
        </div>
        
        <div className="status-section mood">
          <span className="label">Mood</span>
          <span className={`mood-indicator ${tickData?.mood}`}>
            {tickData?.mood?.toUpperCase() || 'OFFLINE'}
          </span>
        </div>
        
        <div className="status-section trend">
          <span className="label">Trend</span>
          <span className={`trend-indicator ${currentTrend}`}>
            {currentTrend === 'rising' ? '↗' : currentTrend === 'falling' ? '↘' : '→'}
          </span>
        </div>
        
        <div className="status-section connection">
          <span className="label">Status</span>
          <span className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? 'ONLINE' : 'OFFLINE'}
          </span>
        </div>
      </motion.div>
    </div>
  );
};

export default UnifiedHomePage; 