import React, { useState, useEffect } from 'react';
import { useProcessFlowStore } from '../../store/processFlowStore';
import { PythonProcess } from './types';
import { ProcessUtils, processManager } from '../../services/processManager';

export const ProcessControls: React.FC = () => {
  const {
    processes,
    startAllProcesses,
    stopAllProcesses,
    autoArrangeProcesses,
    setViewMode,
    setFlowSpeed,
    toggleAutoArrange,
    toggleMetrics,
    viewMode,
    flowSpeed,
    autoArrange,
    showMetrics,
    addProcess
  } = useProcessFlowStore();
  
  const [showAddProcess, setShowAddProcess] = useState(false);
  const [availableScripts, setAvailableScripts] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // Load available scripts on mount
  useEffect(() => {
    const loadScripts = async () => {
      try {
        const scripts = await processManager.listAvailableScripts();
        setAvailableScripts(scripts);
      } catch (error) {
        console.error('Failed to load scripts:', error);
      }
    };
    
    loadScripts();
  }, []);
  
  const defaultScripts = [
    { name: 'Neural Processor', script: 'neural_process.py', category: 'neural' as const },
    { name: 'Consciousness Analyzer', script: 'consciousness_analysis.py', category: 'consciousness' as const },
    { name: 'Memory Consolidator', script: 'memory_consolidate.py', category: 'memory' as const },
    { name: 'Pattern Synthesizer', script: 'pattern_synthesis.py', category: 'synthesis' as const },
    { name: 'Entropy Monitor', script: 'entropy_monitor.py', category: 'analysis' as const },
    { name: 'Consciousness Probe', script: 'consciousness_probe.py', category: 'neural' as const },
    { name: 'Dream Analyzer', script: 'dream_analyzer.py', category: 'analysis' as const },
    { name: 'Reality Mapper', script: 'reality_mapper.py', category: 'synthesis' as const }
  ];
  
  const handleAddProcess = (scriptInfo: any) => {
    const newProcess: PythonProcess = {
      id: ProcessUtils.generateProcessId(),
      name: scriptInfo.name,
      script: scriptInfo.script,
      status: 'idle',
      category: scriptInfo.category,
      cpuUsage: 0,
      memoryUsage: 0,
      executionTime: 0,
      lastTick: 0,
      inputs: [{ 
        id: 'in1', 
        name: 'Input', 
        type: 'data', 
        dataType: 'json', 
        connected: false 
      }],
      outputs: [{ 
        id: 'out1', 
        name: 'Output', 
        type: 'data', 
        dataType: 'json', 
        connected: false 
      }],
      description: `Executes ${scriptInfo.script}`,
      author: 'DAWN',
      version: '1.0.0',
      dependencies: [],
      logs: [],
      errors: [],
      outputData: null,
      position: { 
        x: Math.random() * 400 - 200, 
        y: Math.random() * 400 - 200, 
        z: Math.random() * 200 - 100 
      },
      velocity: { x: 0, y: 0, z: 0 }
    };
    
    addProcess(newProcess);
    setShowAddProcess(false);
  };
  
  const handleStartAll = async () => {
    setIsLoading(true);
    try {
      await startAllProcesses();
    } catch (error) {
      console.error('Failed to start all processes:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleStopAll = async () => {
    setIsLoading(true);
    try {
      await stopAllProcesses();
    } catch (error) {
      console.error('Failed to stop all processes:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <>
      <div className="process-controls">
        <div className="control-group">
          <button 
            onClick={handleStartAll} 
            className="control-btn start"
            disabled={isLoading}
            title="Start all processes"
          >
            <span className="icon">▶</span> 
            {isLoading ? 'Starting...' : 'Start All'}
          </button>
          <button 
            onClick={handleStopAll} 
            className="control-btn stop"
            disabled={isLoading}
            title="Stop all processes"
          >
            <span className="icon">■</span> 
            {isLoading ? 'Stopping...' : 'Stop All'}
          </button>
          <button 
            onClick={() => setShowAddProcess(true)} 
            className="control-btn add"
            title="Add new process"
          >
            <span className="icon">+</span> Add Process
          </button>
        </div>
        
        <div className="control-group">
          <button 
            onClick={() => setViewMode(viewMode === '2d' ? '3d' : '2d')} 
            className={`control-btn view-mode ${viewMode}`}
            title={`Switch to ${viewMode === '2d' ? '3D' : '2D'} view`}
          >
            <span className="icon">{viewMode === '2d' ? '🎯' : '🌐'}</span>
            {viewMode.toUpperCase()} View
          </button>
          <button 
            onClick={toggleAutoArrange} 
            className={`control-btn ${autoArrange ? 'active' : ''}`}
            title="Toggle automatic arrangement"
          >
            <span className="icon">🔄</span>
            Auto Arrange
          </button>
          <button 
            onClick={toggleMetrics} 
            className={`control-btn ${showMetrics ? 'active' : ''}`}
            title="Toggle metrics display"
          >
            <span className="icon">📊</span>
            Show Metrics
          </button>
        </div>
        
        <div className="control-group">
          <label className="control-label">
            <span className="icon">⚡</span>
            Flow Speed
          </label>
          <input
            type="range"
            min="0.1"
            max="3"
            step="0.1"
            value={flowSpeed}
            onChange={(e) => setFlowSpeed(parseFloat(e.target.value))}
            className="flow-speed-slider"
            title={`Flow speed: ${flowSpeed.toFixed(1)}x`}
          />
          <span className="speed-value">{flowSpeed.toFixed(1)}x</span>
        </div>
        
        <div className="control-group">
          <button 
            onClick={autoArrangeProcesses}
            className="control-btn arrange"
            title="Manually arrange processes"
          >
            <span className="icon">🎨</span>
            Arrange
          </button>
        </div>
        
        <div className="process-stats">
          <div className="stat">
            <span className="stat-label">Total:</span>
            <span className="stat-value">{processes.size}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Running:</span>
            <span className="stat-value running">
              {Array.from(processes.values()).filter(p => p.status === 'running').length}
            </span>
          </div>
          <div className="stat">
            <span className="stat-label">Errors:</span>
            <span className="stat-value error">
              {Array.from(processes.values()).filter(p => p.status === 'error').length}
            </span>
          </div>
        </div>
      </div>
      
      {showAddProcess && (
        <div className="add-process-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>🚀 Add New Process</h3>
              <button 
                onClick={() => setShowAddProcess(false)} 
                className="close-btn"
                title="Close"
              >
                ✕
              </button>
            </div>
            
            <div className="script-list">
              {defaultScripts.map((script) => (
                <div
                  key={script.script}
                  className={`script-item ${script.category}`}
                  onClick={() => handleAddProcess(script)}
                  title={`Add ${script.name} process`}
                >
                  <div className="script-header">
                    <span className="script-name">{script.name}</span>
                    <span className={`script-category ${script.category}`}>
                      {script.category.toUpperCase()}
                    </span>
                  </div>
                  <span className="script-file">{script.script}</span>
                </div>
              ))}
            </div>
            
            <div className="modal-footer">
              <button 
                onClick={() => setShowAddProcess(false)} 
                className="cancel-btn"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}; 