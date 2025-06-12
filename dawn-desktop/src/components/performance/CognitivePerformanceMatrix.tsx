import React, { useEffect, useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Props {
  intensity?: number;
  symbolicLoad?: number;
  entropyRate?: number;
  bufferDepth?: number;
  onDisturbance?: (disturbance: any) => void;
  loading?: boolean;
  theme: 'dark' | 'light';
}

const PARTICLE_COLORS_DARK = [
  'from-pink-400 to-purple-500',
  'from-cyan-400 to-blue-500',
  'from-yellow-400 to-pink-500',
  'from-green-400 to-cyan-400',
];
const PARTICLE_COLORS_LIGHT = [
  'from-pink-300 to-purple-300',
  'from-cyan-300 to-blue-300',
  'from-yellow-300 to-pink-300',
  'from-green-300 to-cyan-300',
];

interface ProgressBarProps {
  value: number;
  max?: number;
  color: string;
  label: string;
  critical?: boolean;
  theme: 'dark' | 'light';
}

const ProgressBar: React.FC<ProgressBarProps> = ({ value, max = 100, color, label, critical = false, theme }) => (
  <div className="mb-2">
    <div className="flex justify-between items-center mb-1">
      <span className="text-xs text-gray-400">{label}</span>
      <span className={`text-xs font-bold ${critical ? (theme === 'dark' ? 'text-pink-400' : 'text-pink-500 animate-pulse') : (theme === 'dark' ? 'text-cyan-300' : 'text-cyan-500')}`}>{value.toFixed(1)}%</span>
    </div>
    <div className={`relative h-4 rounded-full ${theme === 'dark' ? 'bg-black/40' : 'bg-white/40'} overflow-hidden border border-purple-500/20`}>
      <motion.div
        className={`absolute left-0 top-0 h-full rounded-full bg-gradient-to-r ${color} shadow-glow-sm`}
        initial={{ width: 0 }}
        animate={{ width: `${Math.min(100, value)}%` }}
        transition={{ duration: 0.7, type: 'spring' }}
      />
      {critical && (
        <motion.div
          className={`absolute right-0 top-0 h-full w-4 rounded-full ${theme === 'dark' ? 'bg-pink-400/80' : 'bg-pink-500/80'} animate-pulse`}
          initial={{ opacity: 0.7 }}
          animate={{ opacity: [0.7, 0.2, 0.7] }}
          transition={{ repeat: Infinity, duration: 1.2 }}
        />
      )}
    </div>
  </div>
);

interface NeonPulseProps {
  active: boolean;
  color?: string;
}

const NeonPulse: React.FC<NeonPulseProps> = ({ active, color = 'bg-pink-400' }) => (
  <motion.div
    className={`w-4 h-4 rounded-full ${color} shadow-glow-md`}
    animate={active ? { scale: [1, 1.3, 1], opacity: [1, 0.5, 1] } : { scale: 1, opacity: 0.7 }}
    transition={{ duration: 1.2, repeat: Infinity }}
  />
);

interface ParticleBurstProps {
  keyId: number;
  theme: 'dark' | 'light';
}

const ParticleBurst: React.FC<ParticleBurstProps> = ({ keyId, theme }) => (
  <AnimatePresence>
    <motion.div
      key={keyId}
      className="absolute inset-0 pointer-events-none"
      initial={{ opacity: 1 }}
      animate={{ opacity: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1.2 }}
    >
      {Array.from({ length: 18 }).map((_, i) => {
        const angle = (i / 18) * 2 * Math.PI;
        const dist = 60 + Math.random() * 30;
        const x = Math.cos(angle) * dist;
        const y = Math.sin(angle) * dist;
        const color = PARTICLE_COLORS_DARK[i % PARTICLE_COLORS_DARK.length];
        return (
          <motion.div
            key={i}
            className={`absolute w-3 h-3 rounded-full bg-gradient-to-br ${color} shadow-glow-sm`}
            style={{ left: '50%', top: '50%', x: -6, y: -6 }}
            initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
            animate={{ x, y, opacity: 0, scale: 0.7 + Math.random() * 0.5 }}
            transition={{ duration: 1.2, delay: i * 0.03 }}
          />
        );
      })}
    </motion.div>
  </AnimatePresence>
);

const CognitivePerformanceMatrix: React.FC<Props> = ({
  intensity = 0,
  symbolicLoad = 0,
  entropyRate = 0,
  bufferDepth = 0,
  onDisturbance,
  theme
}) => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [particleBursts, setParticleBursts] = useState<number[]>([]);

  // Animate metric transitions
  const [display, setDisplay] = useState({
    intensity,
    symbolicLoad,
    entropyRate,
    bufferDepth
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setDisplay(prev => ({
        intensity: prev.intensity + (intensity - prev.intensity) * 0.15,
        symbolicLoad: prev.symbolicLoad + (symbolicLoad - prev.symbolicLoad) * 0.15,
        entropyRate: prev.entropyRate + (entropyRate - prev.entropyRate) * 0.15,
        bufferDepth: prev.bufferDepth + (bufferDepth - prev.bufferDepth) * 0.15,
      }));
    }, 16);
    return () => clearInterval(interval);
  }, [intensity, symbolicLoad, entropyRate, bufferDepth]);

  // Particle burst for critical states
  useEffect(() => {
    if (display.intensity > 85 || display.entropyRate > 80) {
      setParticleBursts(bursts => [...bursts, Date.now()]);
      if (onDisturbance) {
        onDisturbance({
          type: display.intensity > 85 ? 'intensity' : 'entropy',
          message: 'Critical state detected',
          timestamp: new Date().toISOString()
        });
      }
    }
  }, [display.intensity, display.entropyRate, onDisturbance]);

  // Remove old particles
  useEffect(() => {
    if (particleBursts.length === 0) return;
    const timeout = setTimeout(() => {
      setParticleBursts(bursts => bursts.slice(1));
    }, 1200);
    return () => clearTimeout(timeout);
  }, [particleBursts]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-8 relative overflow-visible border border-purple-500/30 shadow-glow-md"
    >
      <h3 className="text-2xl font-bold text-purple-300 mb-6 flex items-center">
        <span className="w-4 h-4 rounded-full bg-gradient-to-r from-pink-400 to-purple-400 mr-2 animate-pulse" />
        Cognitive Performance Matrix
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Intensity */}
        <div className="relative">
          <ProgressBar
            value={display.intensity}
            color={theme === 'dark' ? 'from-pink-400 to-purple-500' : 'from-pink-300 to-purple-300'}
            label="Processing Intensity"
            critical={display.intensity > 85}
            theme={theme}
          />
          <div className="absolute top-2 right-2">
            <NeonPulse active={display.intensity > 85} color={theme === 'dark' ? 'bg-pink-400' : 'bg-pink-300'} />
          </div>
          {display.intensity > 85 && particleBursts.map((id) => <ParticleBurst key={id} keyId={id} theme={theme} />)}
        </div>
        {/* Symbolic Load */}
        <div className="relative">
          <ProgressBar
            value={display.symbolicLoad}
            color={theme === 'dark' ? 'from-cyan-400 to-blue-500' : 'from-cyan-300 to-blue-300'}
            label="Symbolic Load"
            critical={display.symbolicLoad > 85}
            theme={theme}
          />
          <div className="absolute top-2 right-2">
            <NeonPulse active={display.symbolicLoad > 85} color={theme === 'dark' ? 'bg-cyan-400' : 'bg-cyan-300'} />
          </div>
        </div>
        {/* Entropy Rate */}
        <div className="relative">
          <ProgressBar
            value={display.entropyRate}
            color={theme === 'dark' ? 'from-yellow-400 to-pink-500' : 'from-yellow-300 to-pink-300'}
            label="Entropy Rate"
            critical={display.entropyRate > 80}
            theme={theme}
          />
          <div className="absolute top-2 right-2">
            <NeonPulse active={display.entropyRate > 80} color={theme === 'dark' ? 'bg-yellow-400' : 'bg-yellow-300'} />
          </div>
          {display.entropyRate > 80 && particleBursts.map((id) => <ParticleBurst key={id} keyId={id} theme={theme} />)}
        </div>
        {/* Buffer Depth */}
        <div className="relative">
          <ProgressBar
            value={Math.min(100, (display.bufferDepth / 2000) * 100)}
            color={theme === 'dark' ? 'from-green-400 to-cyan-400' : 'from-green-300 to-cyan-300'}
            label="Buffer Depth"
            critical={display.bufferDepth > 1800}
            theme={theme}
          />
          <div className="absolute top-2 right-2">
            <NeonPulse active={display.bufferDepth > 1800} color={theme === 'dark' ? 'bg-green-400' : 'bg-green-300'} />
          </div>
        </div>
      </div>
      {/* Alerts */}
      <AnimatePresence>
        {alerts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="mt-6 p-4 rounded-lg bg-pink-900/30 border border-pink-400 text-pink-200 text-sm shadow-glow-md"
          >
            {alerts.map((alert, idx) => (
              <div key={idx}>{alert.message}</div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default CognitivePerformanceMatrix;
