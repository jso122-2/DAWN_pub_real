// 🎮 UNIFIED DASHBOARD - The Ultimate DAWN Control Center
import React, { useState, useEffect, useCallback, useRef, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ErrorBoundary } from './core/ErrorBoundary';
import { DashboardModule, ModuleConnection, Position } from '../types/dashboard.types';
import { dashboardCore } from '../core/DashboardCore';
import { moduleRegistry } from '../core/ModuleRegistry';
import { CosmicBackground } from './CosmicBackground';
import { LoadingOrb } from './cosmic/LoadingOrb';

export interface UnifiedDashboardProps {
  initialLayout?: string;
  showPerformanceOverlay?: boolean;
  enableKeyboardShortcuts?: boolean;
  className?: string;
}

export const UnifiedDashboard: React.FC<UnifiedDashboardProps> = ({
  initialLayout,
  showPerformanceOverlay = true,
  enableKeyboardShortcuts = true,
  className = ''
}) => {
  // Dashboard state
  const [modules, setModules] = useState<DashboardModule[]>([]);
  const [connections, setConnections] = useState<ModuleConnection[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);
  const [selectedModules, setSelectedModules] = useState<Set<string>>(new Set());
  const [showModulePalette, setShowModulePalette] = useState(false);
  const [showGlobalControls, setShowGlobalControls] = useState(false);
  const [connectionMode, setConnectionMode] = useState(false);

  // Viewport state
  const [viewport, setViewport] = useState({
    zoom: 1,
    pan: { x: 0, y: 0 }
  });

  // Refs
  const dashboardRef = useRef<HTMLDivElement>(null);

  // ========================================
  // INITIALIZATION
  // ========================================

  useEffect(() => {
    const initializeDashboard = async () => {
      try {
        await dashboardCore.initialize();
        await moduleRegistry.initialize();
        
        // Listen for dashboard events
        const unsubscribe = dashboardCore.on('MODULE_ADDED', (payload: any) => {
          setModules(prev => [...prev, payload.module]);
        });

        dashboardCore.on('MODULE_REMOVED', (payload: any) => {
          setModules(prev => prev.filter(m => m.id !== payload.moduleId));
        });

        dashboardCore.on('MODULE_CONNECTED', (payload: any) => {
          setConnections(prev => [...prev, payload.connection]);
        });

        dashboardCore.on('MODULE_DISCONNECTED', (payload: any) => {
          setConnections(prev => prev.filter(c => c.id !== payload.connectionId));
        });

        setIsInitialized(true);

        return () => {
          unsubscribe();
        };
      } catch (error) {
        console.error('Failed to initialize dashboard:', error);
      }
    };

    initializeDashboard();
  }, []);

  // ========================================
  // MODULE MANAGEMENT
  // ========================================

  const handleAddModule = useCallback(async (type: string, position?: Position) => {
    try {
      const finalPosition = position || {
        x: Math.random() * 400 + 100,
        y: Math.random() * 300 + 100
      };

      await dashboardCore.addModule(type, finalPosition);
    } catch (error) {
      console.error('Failed to add module:', error);
    }
  }, []);

  const handleRemoveModule = useCallback(async (moduleId: string) => {
    try {
      await dashboardCore.removeModule(moduleId);
      setSelectedModules(prev => {
        const next = new Set(prev);
        next.delete(moduleId);
        return next;
      });
    } catch (error) {
      console.error('Failed to remove module:', error);
    }
  }, []);

  // ========================================
  // KEYBOARD SHORTCUTS
  // ========================================

  useEffect(() => {
    if (!enableKeyboardShortcuts) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case 'n':
            e.preventDefault();
            setShowModulePalette(true);
            break;
          case 'g':
            e.preventDefault();
            setShowGlobalControls(true);
            break;
          case 'c':
            e.preventDefault();
            setConnectionMode(!connectionMode);
            break;
        }
      }

      if (e.key === 'Escape') {
        setSelectedModules(new Set());
        setConnectionMode(false);
        setShowModulePalette(false);
        setShowGlobalControls(false);
      }

      if (e.key === 'Delete' && selectedModules.size > 0) {
        selectedModules.forEach(moduleId => {
          handleRemoveModule(moduleId);
        });
        setSelectedModules(new Set());
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [enableKeyboardShortcuts, connectionMode, selectedModules, handleRemoveModule]);

  // ========================================
  // RENDER MODULE
  // ========================================

  const renderModule = useCallback((module: DashboardModule) => {
    return (
      <motion.div
        key={module.id}
        className="absolute"
        style={{
          left: module.position.x,
          top: module.position.y,
          width: module.size.width,
          height: module.size.height,
          zIndex: module.zIndex
        }}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.8 }}
        transition={{ duration: 0.3 }}
        whileHover={{ scale: 1.02 }}
        drag
        dragMomentum={false}
        onDragEnd={(_, info) => {
          const newPosition = {
            x: module.position.x + info.offset.x,
            y: module.position.y + info.offset.y
          };
          dashboardCore.updateModule(module.id, { position: newPosition });
        }}
      >
        <ErrorBoundary moduleId={module.id}>
          <div className="dashboard-module glass-neural p-4 rounded-lg border border-white/10 bg-slate-900/40 backdrop-blur-md">
            {/* Module Header */}
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-white/90">{module.title}</h3>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${
                  module.state.status === 'active' ? 'bg-green-400' :
                  module.state.status === 'error' ? 'bg-red-400' :
                  module.state.status === 'loading' ? 'bg-yellow-400' :
                  'bg-gray-400'
                }`} />
                <button
                  onClick={() => handleRemoveModule(module.id)}
                  className="w-6 h-6 flex items-center justify-center rounded text-white/60 hover:text-white hover:bg-red-500/20 transition-colors"
                >
                  ×
                </button>
              </div>
            </div>

            {/* Module Content */}
            <div className="module-content min-h-[200px] bg-black/20 rounded border border-white/5">
              <Suspense fallback={<LoadingOrb />}>
                {module.component && React.createElement(module.component, {
                  moduleId: module.id,
                  config: module.config,
                  consciousness: module.state.consciousness
                })}
              </Suspense>
            </div>

            {/* Module Ports */}
            <div className="module-ports absolute inset-0 pointer-events-none">
              {module.inputPorts.map(port => (
                <div
                  key={port.id}
                  className={`absolute w-3 h-3 rounded-full pointer-events-auto cursor-pointer transition-all ${
                    connectionMode 
                      ? 'bg-blue-400 hover:bg-blue-300 scale-125' 
                      : 'bg-blue-500/50 hover:bg-blue-400/80'
                  }`}
                  style={{
                    left: port.position.x + '%',
                    top: port.position.y + '%',
                    transform: 'translate(-50%, -50%)'
                  }}
                  title={port.description}
                />
              ))}
              {module.outputPorts.map(port => (
                <div
                  key={port.id}
                  className={`absolute w-3 h-3 rounded-full pointer-events-auto cursor-pointer transition-all ${
                    connectionMode 
                      ? 'bg-green-400 hover:bg-green-300 scale-125' 
                      : 'bg-green-500/50 hover:bg-green-400/80'
                  }`}
                  style={{
                    left: port.position.x + '%',
                    top: port.position.y + '%',
                    transform: 'translate(-50%, -50%)'
                  }}
                  title={port.description}
                />
              ))}
            </div>
          </div>
        </ErrorBoundary>
      </motion.div>
    );
  }, [connectionMode, handleRemoveModule]);

  // Don't render until dashboard is initialized
  if (!isInitialized) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <LoadingOrb />
          <p className="mt-4 text-white/70">Initializing DAWN Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`unified-dashboard fixed inset-0 bg-slate-900 overflow-hidden ${className}`} ref={dashboardRef}>
      {/* Cosmic Background */}
      <CosmicBackground />

      {/* Main Viewport */}
      <div 
        className="dashboard-viewport absolute inset-0"
        style={{
          transform: `translate(${viewport.pan.x}px, ${viewport.pan.y}px) scale(${viewport.zoom})`,
          transformOrigin: '0 0'
        }}
      >
        {/* Grid Background */}
        <div className="grid-background absolute inset-0 opacity-20">
          <svg width="100%" height="100%" className="absolute inset-0">
            <defs>
              <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
          </svg>
        </div>

        {/* Connection Lines */}
        <svg className="connections-layer absolute inset-0 pointer-events-none" style={{ zIndex: 1 }}>
          {connections.map(connection => {
            const sourceModule = modules.find(m => m.id === connection.sourceModuleId);
            const targetModule = modules.find(m => m.id === connection.targetModuleId);
            
            if (!sourceModule || !targetModule) return null;

            const startX = sourceModule.position.x + sourceModule.size.width;
            const startY = sourceModule.position.y + sourceModule.size.height / 2;
            const endX = targetModule.position.x;
            const endY = targetModule.position.y + targetModule.size.height / 2;

            const midX = (startX + endX) / 2;

            return (
              <motion.path
                key={connection.id}
                d={`M ${startX} ${startY} Q ${midX} ${startY} ${midX} ${(startY + endY) / 2} Q ${midX} ${endY} ${endX} ${endY}`}
                stroke="rgba(59, 130, 246, 0.6)"
                strokeWidth="2"
                fill="none"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 0.5 }}
              />
            );
          })}
        </svg>

        {/* Modules */}
        <AnimatePresence>
          {modules.map(renderModule)}
        </AnimatePresence>
      </div>

      {/* Toolbar */}
      <div className="dashboard-toolbar absolute top-4 left-4 right-4 flex items-center justify-between z-50">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-bold text-white">DAWN Unified Dashboard</h1>
          <div className="flex items-center gap-2 text-sm text-white/60">
            <span>{modules.length} modules</span>
            <span>•</span>
            <span>{connections.length} connections</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowModulePalette(true)}
            className="px-3 py-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/30 rounded text-blue-200 text-sm transition-colors"
          >
            + Add Module
          </button>
          
          <button
            onClick={() => setConnectionMode(!connectionMode)}
            className={`px-3 py-2 border rounded text-sm transition-colors ${
              connectionMode 
                ? 'bg-green-500/20 border-green-400/30 text-green-200' 
                : 'bg-gray-500/20 border-gray-400/30 text-gray-200'
            }`}
          >
            {connectionMode ? 'Connecting...' : 'Connect'}
          </button>

          <button
            onClick={() => setShowGlobalControls(true)}
            className="px-3 py-2 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-400/30 rounded text-purple-200 text-sm transition-colors"
          >
            Controls
          </button>
        </div>
      </div>

      {/* Module Palette */}
      <AnimatePresence>
        {showModulePalette && (
          <motion.div
            className="module-palette fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowModulePalette(false)}
          >
            <motion.div
              className="bg-slate-800 rounded-lg p-6 m-4 max-w-4xl w-full max-h-[80vh] overflow-y-auto"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-xl font-bold text-white mb-4">Add Module</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {moduleRegistry.getAllModuleDefinitions().map(definition => (
                  <button
                    key={definition.type}
                    onClick={() => {
                      handleAddModule(definition.type);
                      setShowModulePalette(false);
                    }}
                    className="module-card p-4 bg-slate-700 hover:bg-slate-600 rounded-lg border border-slate-600 transition-colors text-left"
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-2xl">{definition.icon}</span>
                      <h3 className="font-medium text-white">{definition.title}</h3>
                    </div>
                    <p className="text-sm text-gray-300">{definition.description}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-xs px-2 py-1 bg-slate-600 rounded text-gray-300">
                        {definition.category}
                      </span>
                      {definition.version && (
                        <span className="text-xs text-gray-400">v{definition.version}</span>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Global Controls */}
      <AnimatePresence>
        {showGlobalControls && (
          <motion.div
            className="global-controls fixed top-16 right-4 z-50"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
          >
            <div className="bg-slate-800/90 backdrop-blur-md rounded-lg p-4 w-80 border border-white/10">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-medium text-white">Global Controls</h3>
                <button
                  onClick={() => setShowGlobalControls(false)}
                  className="text-white/60 hover:text-white"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-sm text-gray-300 block mb-2">Consciousness Level</label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    defaultValue="50"
                    className="w-full"
                    onChange={(e) => {
                      dashboardCore.updateConsciousness({
                        globalSCUP: parseInt(e.target.value)
                      } as any);
                    }}
                  />
                </div>
                
                <div>
                  <label className="text-sm text-gray-300 block mb-2">Entropy Level</label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    defaultValue="0.5"
                    className="w-full"
                    onChange={(e) => {
                      dashboardCore.updateConsciousness({
                        globalEntropy: parseFloat(e.target.value)
                      } as any);
                    }}
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => dashboardCore.pauseConsciousness()}
                    className="flex-1 px-3 py-2 bg-yellow-500/20 border border-yellow-400/30 rounded text-yellow-200 text-sm hover:bg-yellow-500/30 transition-colors"
                  >
                    Pause
                  </button>
                  <button
                    onClick={() => dashboardCore.resumeConsciousness()}
                    className="flex-1 px-3 py-2 bg-green-500/20 border border-green-400/30 rounded text-green-200 text-sm hover:bg-green-500/30 transition-colors"
                  >
                    Resume
                  </button>
                  <button
                    onClick={() => dashboardCore.resetConsciousness()}
                    className="flex-1 px-3 py-2 bg-red-500/20 border border-red-400/30 rounded text-red-200 text-sm hover:bg-red-500/30 transition-colors"
                  >
                    Reset
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Status Bar */}
      <div className="status-bar absolute bottom-4 left-4 right-4 flex items-center justify-between text-sm text-white/60 z-50">
        <div className="flex items-center gap-4">
          <span>Zoom: {(viewport.zoom * 100).toFixed(0)}%</span>
          <span>Modules: {modules.length}</span>
          <span>Connections: {connections.length}</span>
        </div>
        
        <div className="flex items-center gap-4">
          <span>Ctrl+N: Add Module</span>
          <span>Ctrl+C: Connect</span>
          <span>Del: Delete</span>
        </div>
      </div>
    </div>
  );
};
