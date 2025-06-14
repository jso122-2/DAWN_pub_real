import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ModuleContainer } from '../../core/ModuleContainer';
import { WaveformDisplay } from './WaveformDisplay';
import { ParticleField } from './ParticleField';
import { NeuralMap } from './NeuralMap';
import { useRealTimeConsciousness } from '../../../hooks/useRealTimeConsciousness';
import * as styles from './ConsciousnessVisualizer.styles';

export interface ConsciousnessVisualizerProps {
  moduleId: string;
  position?: { x: number; y: number; z: number };
  onClose?: () => void;
}

type VisualizationMode = 'waveform' | 'particles' | 'neural' | 'combined';

export const ConsciousnessVisualizer: React.FC<ConsciousnessVisualizerProps> = ({
  moduleId,
  position,
  onClose,
}) => {
  const [mode, setMode] = useState<VisualizationMode>('combined');
  const consciousness = useRealTimeConsciousness();
  const { scup, entropy, mood, neuralActivity } = consciousness;

  const breathingIntensity = scup / 100;
  const glowIntensity = neuralActivity;

  const renderVisualization = () => {
    switch (mode) {
      case 'waveform':
        return <WaveformDisplay fullscreen />;
      case 'particles':
        return <ParticleField fullscreen />;
      case 'neural':
        return <NeuralMap fullscreen />;
      case 'combined':
        return (
          <div className={styles.combinedView}>
            <div className={styles.quadrant}>
              <WaveformDisplay />
            </div>
            <div className={styles.quadrant}>
              <ParticleField />
            </div>
            <div className={styles.quadrant}>
              <NeuralMap />
            </div>
            <div className={styles.quadrant}>
              <div className={styles.metrics}>
                <h4>Consciousness Metrics</h4>
                <div className={styles.metricItem}>
                  <span>SCUP</span>
                  <div className={styles.metricBar}>
                    <motion.div
                      className={styles.metricFill}
                      animate={{ width: `${scup}%` }}
                      style={{ background: `hsl(${180 + scup * 1.8}, 70%, 50%)` }}
                    />
                  </div>
                  <span>{scup.toFixed(1)}%</span>
                </div>
                <div className={styles.metricItem}>
                  <span>Entropy</span>
                  <div className={styles.metricBar}>
                    <motion.div
                      className={styles.metricFill}
                      animate={{ width: `${entropy * 100}%` }}
                      style={{ background: `hsl(${30 + entropy * 60}, 70%, 50%)` }}
                    />
                  </div>
                  <span>{(entropy * 100).toFixed(1)}%</span>
                </div>
                <div className={styles.metricItem}>
                  <span>Neural Activity</span>
                  <div className={styles.metricBar}>
                    <motion.div
                      className={styles.metricFill}
                      animate={{ width: `${neuralActivity * 100}%` }}
                      style={{ background: `hsl(${260 + neuralActivity * 60}, 70%, 50%)` }}
                    />
                  </div>
                  <span>{(neuralActivity * 100).toFixed(1)}%</span>
                </div>
                <div className={styles.moodIndicator}>
                  <span>Mood</span>
                  <motion.div
                    className={styles.moodDisplay}
                    animate={{
                      background: getMoodGradient(mood),
                      boxShadow: `0 0 20px ${getMoodColor(mood)}`
                    }}
                  >
                    {mood}
                  </motion.div>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <ModuleContainer
      category="monitor"
      moduleId={moduleId}
      position={position}
      breathingIntensity={breathingIntensity}
      glowIntensity={glowIntensity}
      onClose={onClose}
      className={styles.container}
    >
      <div className={styles.header}>
        <div className="flex items-center gap-3">
          <h3 className={styles.title}>Consciousness Visualizer</h3>
          <div className={`flex items-center gap-1 text-xs ${consciousness.isConnected ? 'text-green-400' : 'text-red-400'}`}>
            <div className={`w-2 h-2 rounded-full ${consciousness.isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
            <span>{consciousness.isConnected ? 'Real-time' : 'Simulated'}</span>
          </div>
        </div>
        <div className={styles.modeSelector}>
          {(['combined', 'waveform', 'particles', 'neural'] as VisualizationMode[]).map(m => (
            <motion.button
              key={m}
              className={styles.modeButton(mode === m)}
              onClick={() => setMode(m)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {m}
            </motion.button>
          ))}
        </div>
      </div>
      
      <div className={styles.visualizationContainer}>
        {renderVisualization()}
      </div>
    </ModuleContainer>
  );
};

function getMoodColor(mood: string): string {
  const colors: Record<string, string> = {
    'contemplative': 'rgba(148, 163, 184, 0.5)',
    'excited': 'rgba(251, 191, 36, 0.5)',
    'serene': 'rgba(134, 239, 172, 0.5)',
    'anxious': 'rgba(248, 113, 113, 0.5)',
    'euphoric': 'rgba(196, 181, 253, 0.5)',
    'chaotic': 'rgba(239, 68, 68, 0.5)',
    'active': 'rgba(59, 130, 246, 0.5)'
  };
  return colors[mood] || 'rgba(148, 163, 184, 0.5)';
}

function getMoodGradient(mood: string): string {
  const gradients: Record<string, string> = {
    'contemplative': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'excited': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'serene': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'anxious': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'euphoric': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    'chaotic': 'linear-gradient(135deg, #ff0844 0%, #ffb199 100%)',
    'active': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)'
  };
  return gradients[mood] || gradients['contemplative'];
} 