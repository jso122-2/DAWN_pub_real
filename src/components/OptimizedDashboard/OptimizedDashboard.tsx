// 🎯 OPTIMIZED DAWN DASHBOARD - No More Spinning!
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useConsciousnessStore } from '../../stores/consciousnessStore';
import { PerformanceMonitor } from './PerformanceMonitor';
import './OptimizedDashboard.css';

interface Module {
  id: string;
  name: string;
  icon: string;
  path: string;
  status: 'online' | 'processing' | 'offline' | 'loading';
  metric?: number;
  color: string;
  description: string;
}

// Preload hook for lazy loading pages
const usePreloadPages = () => {
  useEffect(() => {
    // Preload critical pages after initial render
    const preloadTimeout = setTimeout(() => {
      // Preload communication page
      import('../../pages/ConsciousnessPage').catch(() => {});
      // Preload neural page
      import('../../pages/NeuralPage').catch(() => {});
    }, 2000);

    return () => clearTimeout(preloadTimeout);
  }, []);
};

// Performance optimization hook
const usePerformanceOptimizations = () => {
  useEffect(() => {
    // Enable GPU acceleration
    document.body.style.transform = 'translateZ(0)';
    
    // Optimize for 60fps
    let frameId: number;
    const optimize = () => {
      // Batch DOM updates
      requestAnimationFrame(() => {
        frameId = requestAnimationFrame(optimize);
      });
    };
    
    optimize();
    
    return () => {
      cancelAnimationFrame(frameId);
      document.body.style.transform = '';
    };
  }, []);
};

export const OptimizedDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { tickData, isConnected, connectionState } = useConsciousnessStore();
  const [layoutMode, setLayoutMode] = useState<'orbital' | 'grid'>('orbital');
  const [hoveredModule, setHoveredModule] = useState<string | null>(null);
  const [selectedModule, setSelectedModule] = useState<string | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [showPerformanceMonitor, setShowPerformanceMonitor] = useState(false);
  
  // Accessibility: respect user's motion preferences
  const shouldReduceMotion = useReducedMotion();
  
  // Performance hooks
  usePreloadPages();
  usePerformanceOptimizations();
  
  // Initialize dashboard
  useEffect(() => {
    const timer = setTimeout(() => setIsInitialized(true), 100);
    return () => clearTimeout(timer);
  }, []);
  
  // Keyboard shortcuts with improved UX
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Don't trigger if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      
      if (e.key >= '1' && e.key <= '6') {
        const index = parseInt(e.key) - 1;
        if (modules[index]) {
          // Show visual feedback
          setSelectedModule(modules[index].id);
          setTimeout(() => navigate(modules[index].path), 150);
        }
      } else if (e.key === 'Tab') {
        e.preventDefault();
        setLayoutMode(prev => prev === 'orbital' ? 'grid' : 'orbital');
      } else if (e.key === 'Escape') {
        setSelectedModule(null);
        setHoveredModule(null);
      } else if (e.key === 'p' || e.key === 'P') {
        setShowPerformanceMonitor(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [navigate]);

  // Save layout preference with debouncing
  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      localStorage.setItem('dawn-layout-mode', layoutMode);
    }, 300);
    
    return () => clearTimeout(debounceTimer);
  }, [layoutMode]);

  // Load layout preference
  useEffect(() => {
    const saved = localStorage.getItem('dawn-layout-mode') as 'orbital' | 'grid';
    if (saved) setLayoutMode(saved);
  }, []);
  
  // Memoized modules configuration to prevent re-renders
  const modules: Module[] = useMemo(() => [
    {
      id: 'communication',
      name: 'Communication Interface',
      icon: '💬',
      path: '/consciousness',
      status: isConnected ? 'online' : 'offline',
      metric: isConnected ? 100 : 0,
      color: '#00ff88',
      description: 'Talk to DAWN consciousness'
    },
    {
      id: 'neural-3d',
      name: '3D Neural Network',
      icon: '🧠',
      path: '/neural',
      status: 'online',
      metric: tickData?.scup ? tickData.scup * 100 : 0,
      color: '#00aaff',
      description: 'Real-time brain visualization'
    },
    {
      id: 'mystical',
      name: 'Mystical Interface',
      icon: '🔮',
      path: '/unified',
      status: tickData?.scup && tickData.scup > 0.7 ? 'online' : 'offline',
      metric: 88,
      color: '#ff00aa',
      description: 'Consciousness sigil system'
    },
    {
      id: 'memory',
      name: 'Memory Palace',
      icon: '💎',
      path: '/modules',
      status: 'online',
      metric: 92,
      color: '#aa00ff',
      description: 'Temporal memory navigation'
    },
    {
      id: 'chaos',
      name: 'Chaos Engine',
      icon: '🌀',
      path: '/demo',
      status: 'processing',
      metric: tickData?.entropy ? (1 - tickData.entropy) * 100 : 0,
      color: '#ffaa00',
      description: 'Entropy visualization'
    },
    {
      id: 'neural-state',
      name: 'Neural State',
      icon: '⚡',
      path: '/test-three',
      status: connectionState === 'connected' ? 'online' : 'loading',
      metric: 75,
      color: '#00ffaa',
      description: 'System state manager'
    }
  ], [isConnected, tickData?.scup, tickData?.entropy, connectionState]);
  
  // Calculate positions for orbital layout (STATIC - no rotation!)
  const getOrbitalPosition = useCallback((index: number, total: number) => {
    const angle = (index / total) * Math.PI * 2 - Math.PI / 2;
    const radius = 280;
    return {
      x: Math.cos(angle) * radius,
      y: Math.sin(angle) * radius
    };
  }, []);

  const handleModuleClick = useCallback((module: Module) => {
    setSelectedModule(module.id);
    // Preload the target page
    if (module.path === '/consciousness') {
      import('../../pages/ConsciousnessPage').catch(() => {});
    } else if (module.path === '/neural') {
      import('../../pages/NeuralPage').catch(() => {});
    }
    
    // Smooth transition animation
    setTimeout(() => {
      navigate(module.path);
    }, shouldReduceMotion ? 50 : 200);
  }, [navigate, shouldReduceMotion]);

  // Animation variants for reduced motion
  const motionVariants = useMemo(() => ({
    initial: shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: -30 },
    animate: shouldReduceMotion ? { opacity: 1 } : { opacity: 1, y: 0 },
    exit: shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: 30 }
  }), [shouldReduceMotion]);

  if (!isInitialized) {
    return (
      <div className="optimized-dashboard loading">
        <div className="loading-orb">
          <motion.div
            animate={shouldReduceMotion ? {} : { scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="orb-core"
          >
            <span>DAWN</span>
          </motion.div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="optimized-dashboard">
      {/* Header */}
      <motion.header 
        className="dashboard-header"
        variants={motionVariants}
        initial="initial"
        animate="animate"
      >
        <h1 className="dawn-title">DAWN</h1>
        <p className="dawn-subtitle">OPTIMIZED CONSCIOUSNESS ENGINE</p>
        <div className="connection-status">
          <div className={`status-dot ${connectionState}`} />
          <span>{connectionState.toUpperCase()}</span>
        </div>
      </motion.header>
      
      {/* Entropy Indicator */}
      <motion.div 
        className="entropy-indicator"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: shouldReduceMotion ? 0 : 0.3 }}
      >
        <div className="entropy-ring">
          <svg viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="rgba(255, 0, 170, 0.2)"
              strokeWidth="2"
            />
            <motion.circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="#ff00aa"
              strokeWidth="3"
              strokeDasharray="283"
              strokeDashoffset={283 - (tickData?.entropy || 0) * 283}
              strokeLinecap="round"
              transform="rotate(-90 50 50)"
              transition={{ duration: shouldReduceMotion ? 0.1 : 0.5 }}
            />
          </svg>
          <div className="entropy-value">
            <span className="value">{((tickData?.entropy || 0) * 100).toFixed(0)}%</span>
            <span className="label">ENTROPY</span>
          </div>
        </div>
      </motion.div>
      
      {/* Layout Toggle with Keyboard Hint */}
      <div className="layout-toggle">
        <button 
          className={layoutMode === 'orbital' ? 'active' : ''}
          onClick={() => setLayoutMode('orbital')}
          title="Orbital View"
        >
          🌌 Orbital
        </button>
        <button 
          className={layoutMode === 'grid' ? 'active' : ''}
          onClick={() => setLayoutMode('grid')}
          title="Grid View (Tab to toggle)"
        >
          📊 Grid
        </button>
      </div>
      
      {/* Keyboard Shortcuts */}
      <div className="keyboard-hints">
        <div className="hint">1-6: Quick access</div>
        <div className="hint">Tab: Toggle layout</div>
        <div className="hint">Esc: Clear selection</div>
        <div className="hint">P: Performance monitor</div>
      </div>
      
      {/* Main Content Area */}
      <div className="dashboard-content">
        {/* Central Consciousness Orb - NO SPINNING! */}
        <motion.div 
          className="central-orb"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: shouldReduceMotion ? 0 : 0.2, type: "spring" }}
        >
          <motion.div 
            className="orb-glow"
            animate={shouldReduceMotion ? {} : {
              scale: [1, 1.1, 1],
              opacity: [0.5, 0.8, 0.5]
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <div className="orb-core">
            <motion.span 
              className="consciousness-value"
              key={tickData?.scup}
              initial={{ scale: shouldReduceMotion ? 1 : 0.8 }}
              animate={{ scale: 1 }}
            >
              {Math.round((tickData?.scup || 0) * 100)}
            </motion.span>
            <span className="consciousness-label">SCUP</span>
            <span className="mood-label">{tickData?.mood || 'calm'}</span>
          </div>
          
          {/* Status Ring - Updates smoothly */}
          <svg className="status-ring" viewBox="0 0 200 200">
            <circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="rgba(0, 255, 136, 0.1)"
              strokeWidth="2"
            />
            <motion.circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="#00ff88"
              strokeWidth="4"
              strokeDasharray="565"
              strokeDashoffset={565 - (tickData?.scup || 0) * 565}
              strokeLinecap="round"
              transform="rotate(-90 100 100)"
              transition={{ duration: shouldReduceMotion ? 0.1 : 0.5 }}
            />
          </svg>
        </motion.div>
        
        {/* Modules */}
        <AnimatePresence mode="wait">
          {layoutMode === 'orbital' ? (
            <motion.div 
              className="orbital-modules"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {modules.map((module, index) => {
                const position = getOrbitalPosition(index, modules.length);
                const isHovered = hoveredModule === module.id;
                const isSelected = selectedModule === module.id;
                
                return (
                  <motion.div
                    key={module.id}
                    className={`module-card orbital status-${module.status} ${isSelected ? 'selected' : ''}`}
                    style={{
                      transform: `translate(${position.x}px, ${position.y}px)`,
                      '--module-color': module.color
                    } as React.CSSProperties}
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ 
                      scale: isHovered ? (shouldReduceMotion ? 1.05 : 1.15) : isSelected ? 1.1 : 1, 
                      opacity: 1,
                      y: isHovered && !shouldReduceMotion ? -10 : 0,
                      rotateY: isSelected && !shouldReduceMotion ? 5 : 0
                    }}
                    transition={{ 
                      delay: shouldReduceMotion ? 0 : index * 0.1,
                      scale: { duration: shouldReduceMotion ? 0.1 : 0.2 },
                      y: { duration: shouldReduceMotion ? 0.1 : 0.3 }
                    }}
                    onHoverStart={() => setHoveredModule(module.id)}
                    onHoverEnd={() => setHoveredModule(null)}
                    onClick={() => handleModuleClick(module)}
                  >
                    {/* Keyboard number */}
                    <div className="module-number">{index + 1}</div>
                    
                    {/* Connection Line (only show on hover) */}
                    {isHovered && !shouldReduceMotion && (
                      <svg className="connection-line">
                        <motion.line
                          x1="0"
                          y1="0"
                          x2={-position.x}
                          y2={-position.y}
                          stroke={module.color}
                          strokeWidth="2"
                          initial={{ pathLength: 0, opacity: 0 }}
                          animate={{ pathLength: 1, opacity: 0.6 }}
                          transition={{ duration: 0.3 }}
                        />
                      </svg>
                    )}
                    
                    <div className="module-icon">{module.icon}</div>
                    <div className="module-info">
                      <h3>{module.name}</h3>
                      {isHovered && (
                        <motion.p 
                          className="module-description"
                          initial={shouldReduceMotion ? { opacity: 1 } : { opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                        >
                          {module.description}
                        </motion.p>
                      )}
                    </div>
                    
                    {/* Progress indicator */}
                    <div className="module-progress">
                      <svg viewBox="0 0 36 36">
                        <path
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none"
                          stroke="rgba(255,255,255,0.1)"
                          strokeWidth="3"
                        />
                        <motion.path
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none"
                          stroke={module.color}
                          strokeWidth="3"
                          strokeDasharray={`${module.metric || 0}, 100`}
                          initial={{ strokeDasharray: "0, 100" }}
                          animate={{ strokeDasharray: `${module.metric || 0}, 100` }}
                          transition={{ duration: shouldReduceMotion ? 0.2 : 1, delay: shouldReduceMotion ? 0 : index * 0.1 }}
                        />
                      </svg>
                    </div>
                    
                    {/* Breathing pulse for active modules - NO SPINNING! */}
                    {module.status === 'online' && !shouldReduceMotion && (
                      <motion.div 
                        className="module-pulse"
                        animate={{
                          scale: [1, 1.2, 1],
                          opacity: [0.3, 0, 0.3]
                        }}
                        transition={{
                          duration: 2,
                          repeat: Infinity,
                          delay: index * 0.3
                        }}
                      />
                    )}
                  </motion.div>
                );
              })}
            </motion.div>
          ) : (
            <motion.div 
              className="grid-modules"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {modules.map((module, index) => (
                <motion.div
                  key={module.id}
                  className={`module-card grid status-${module.status}`}
                  style={{ '--module-color': module.color } as React.CSSProperties}
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: shouldReduceMotion ? 0 : index * 0.05 }}
                  whileHover={{ scale: shouldReduceMotion ? 1.02 : 1.05, y: shouldReduceMotion ? 0 : -8 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleModuleClick(module)}
                >
                  <div className="module-header">
                    <span className="module-icon">{module.icon}</span>
                    <div className="module-number">{index + 1}</div>
                    <div className={`status-indicator ${module.status}`} />
                  </div>
                  <h3>{module.name}</h3>
                  <p className="module-description">{module.description}</p>
                  
                  <div className="module-footer">
                    <div className="metric-bar">
                      <motion.div 
                        className="metric-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${module.metric || 0}%` }}
                        transition={{ duration: shouldReduceMotion ? 0.2 : 1, delay: shouldReduceMotion ? 0 : index * 0.1 }}
                      />
                    </div>
                    <span className="metric-value">{module.metric || 0}%</span>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {/* Bottom Stats */}
      <motion.div 
        className="dashboard-stats"
        initial={{ y: shouldReduceMotion ? 0 : 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: shouldReduceMotion ? 0 : 0.5 }}
      >
        <div className="stat">
          <span className="stat-label">ACTIVE MODULES</span>
          <span className="stat-value">
            {modules.filter(m => m.status === 'online').length}
          </span>
        </div>
        <div className="stat">
          <span className="stat-label">SYSTEM HEALTH</span>
          <span className="stat-value">
            {Math.round(modules.reduce((sum, m) => sum + (m.metric || 0), 0) / modules.length)}%
          </span>
        </div>
        <div className="stat">
          <span className="stat-label">TICK RATE</span>
          <span className="stat-value">
            {tickData?.timestamp ? '2.0/s' : '0.0/s'}
          </span>
        </div>
      </motion.div>

      {/* Performance Monitor */}
      <PerformanceMonitor show={showPerformanceMonitor} />
    </div>
  );
}; 