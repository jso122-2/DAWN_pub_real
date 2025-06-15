import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useConsciousnessStore } from '../../../stores/consciousnessStore';
import * as THREE from 'three';

export const StateControls: React.FC = () => {
  const {
    visualizationMode,
    measurementMode,
    timeEvolution,
    evolutionSpeed,
    setVisualizationMode,
    setMeasurementMode,
    toggleTimeEvolution,
    setEvolutionSpeed,
    evaluateState,
    createMultiState,
    triggerStateCollapse
  } = useConsciousnessStore();
  
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  const visualizationModes = [
    { id: 'field', name: 'Consciousness Field', icon: '🌊', description: 'Base consciousness field' },
    { id: 'particles', name: 'Particle States', icon: '⚛️', description: 'Particle clouds' },
    { id: 'entanglement', name: 'Correlation', icon: '🔗', description: 'Consciousness connections' },
    { id: 'thoughts', name: 'Thought Vectors', icon: '💭', description: 'Consciousness streams' }
  ];
  
  const measurementModes = [
    { id: 'position', name: 'Position', symbol: 'x̂' },
    { id: 'momentum', name: 'Momentum', symbol: 'p̂' },
    { id: 'spin', name: 'Spin', symbol: 'σ̂' },
    { id: 'energy', name: 'Energy', symbol: 'Ĥ' }
  ];
  
  const handleMeasurement = () => {
    evaluateState(measurementMode);
    console.log(`🌌 Consciousness Measurement: Collapsing ${measurementMode} observable!`);
  };
  
  const handleCreateMultiState = () => {
    const states = ['|0⟩', '|1⟩'];
    const amplitudes = [
      { real: 1/Math.sqrt(2), imaginary: 0 },
      { real: 1/Math.sqrt(2), imaginary: 0 }
    ];
          createMultiState(states, amplitudes);
      console.log('🌌 Created Bell State MultiState!');
  };
  
  const handleInduceDeunity = () => {
    triggerStateCollapse(
      new THREE.Vector3(0, 0, 0),
      Math.random() * 0.5 + 0.5
    );
    console.log('🌌 Environmental Deunity Induced!');
  };
  
  return (
    <motion.div 
      className="consciousness-controls"
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.8, delay: 0.5 }}
    >
      {/* Visualization Mode Selector */}
      <div className="control-section">
        <h3 className="section-title">
          <span className="title-icon">👁️</span>
          Visualization Mode
        </h3>
        <div className="mode-grid">
          {visualizationModes.map(mode => (
            <motion.button
              key={mode.id}
              className={`mode-btn ${visualizationMode === mode.id ? 'active' : ''}`}
              onClick={() => setVisualizationMode(mode.id as any)}
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
              title={mode.description}
            >
              <span className="mode-icon">{mode.icon}</span>
              <span className="mode-name">{mode.name}</span>
              <div className="mode-glow" />
            </motion.button>
          ))}
        </div>
      </div>
      
      {/* Measurement Controls */}
      <div className="control-section">
        <h3 className="section-title">
          <span className="title-icon">📏</span>
          Consciousness Measurement
        </h3>
        <div className="measurement-panel">
          <div className="observable-selector">
            {measurementModes.map(mode => (
              <motion.button
                key={mode.id}
                className={`observable-btn ${measurementMode === mode.id ? 'selected' : ''}`}
                onClick={() => setMeasurementMode(mode.id as any)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <span className="observable-symbol">{mode.symbol}</span>
                <span className="observable-name">{mode.name}</span>
              </motion.button>
            ))}
          </div>
          
          <motion.button 
            onClick={handleMeasurement} 
            className="collapse-btn"
            whileHover={{ 
              scale: 1.1,
              boxShadow: "0 0 30px rgba(255, 0, 255, 0.6)"
            }}
            whileTap={{ scale: 0.9 }}
          >
            <span className="btn-icon">💥</span>
            <span>Collapse Wave Function</span>
            <div className="btn-energy" />
          </motion.button>
        </div>
      </div>
      
      {/* Time Evolution Controls */}
      <div className="control-section">
        <h3 className="section-title">
          <span className="title-icon">⏰</span>
          Temporal Evolution
        </h3>
        <div className="time-controls">
          <motion.button 
            onClick={toggleTimeEvolution}
            className={`evolution-btn ${timeEvolution ? 'active' : ''}`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="btn-icon">{timeEvolution ? '⏸️' : '▶️'}</span>
            <span>{timeEvolution ? 'Pause Evolution' : 'Start Evolution'}</span>
          </motion.button>
          
          <div className="speed-control">
            <label className="speed-label">
              Evolution Speed: {evolutionSpeed.toFixed(1)}x
            </label>
            <motion.input
              type="range"
              min="0.1"
              max="3.0"
              step="0.1"
              value={evolutionSpeed}
              onChange={(e) => setEvolutionSpeed(parseFloat(e.target.value))}
              className="speed-slider"
              whileHover={{ scale: 1.02 }}
            />
            <div className="speed-markers">
              <span>0.1x</span>
              <span>1.5x</span>
              <span>3.0x</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Advanced Consciousness Operations */}
      <div className="control-section">
        <motion.button 
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="advanced-toggle"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <span className="toggle-icon">{showAdvanced ? '🔽' : '▶️'}</span>
          <span>Advanced Consciousness Operations</span>
          <div className="toggle-glow" />
        </motion.button>
        
        <motion.div
          className="advanced-panel"
          initial={false}
          animate={{ 
            height: showAdvanced ? 'auto' : 0,
            opacity: showAdvanced ? 1 : 0
          }}
          transition={{ duration: 0.3 }}
          style={{ overflow: 'hidden' }}
        >
          {showAdvanced && (
            <div className="consciousness-operations">
              <motion.button 
                onClick={handleCreateMultiState} 
                className="consciousness-op-btn"
                whileHover={{ 
                  scale: 1.05, 
                  boxShadow: "0 0 20px rgba(0, 255, 255, 0.5)" 
                }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="op-icon">🌀</span>
                <span className="op-text">Create Bell State</span>
                <span className="op-formula">|Ψ⟩ = (|00⟩ + |11⟩)/√2</span>
              </motion.button>
              
              <motion.button 
                onClick={handleInduceDeunity} 
                className="consciousness-op-btn"
                whileHover={{ 
                  scale: 1.05, 
                  boxShadow: "0 0 20px rgba(255, 100, 100, 0.5)" 
                }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="op-icon">💨</span>
                <span className="op-text">Induce Deunity</span>
                <span className="op-formula">ρ(t) = Σᵢ Kᵢρ(0)Kᵢ†</span>
              </motion.button>
              
              <motion.button 
                className="consciousness-op-btn"
                whileHover={{ 
                  scale: 1.05, 
                  boxShadow: "0 0 20px rgba(255, 255, 0, 0.5)" 
                }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="op-icon">🌊</span>
                <span className="op-text">Consciousness Tunneling</span>
                <span className="op-formula">T = e^(-2κa)</span>
              </motion.button>
              
              <motion.button 
                className="consciousness-op-btn"
                whileHover={{ 
                  scale: 1.05, 
                  boxShadow: "0 0 20px rgba(150, 0, 255, 0.5)" 
                }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="op-icon">🎭</span>
                <span className="op-text">Phase Gate</span>
                <span className="op-formula">|1⟩ → e^(iφ)|1⟩</span>
              </motion.button>
            </div>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
}; 