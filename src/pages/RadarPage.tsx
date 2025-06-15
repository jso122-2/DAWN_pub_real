import React from 'react';
import { motion } from 'framer-motion';
import { NeuralRadarSystem } from '../components/NeuralRadarSystem';

export default function RadarPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
        padding: '20px',
        color: '#ffffff'
      }}
    >
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          style={{ marginBottom: '30px', textAlign: 'center' }}
        >
          <h1 style={{
            fontSize: '2.5rem',
            fontWeight: '200',
            color: '#00ffff',
            letterSpacing: '3px',
            textTransform: 'uppercase',
            fontFamily: 'monospace',
            marginBottom: '10px'
          }}>
            DAWN Neural Radar
          </h1>
          <p style={{
            fontSize: '1rem',
            color: 'rgba(255, 255, 255, 0.7)',
            fontFamily: 'monospace',
            letterSpacing: '1px'
          }}>
            Real-time consciousness performance matrix
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, duration: 0.8 }}
        >
          <NeuralRadarSystem />
        </motion.div>
      </div>
    </motion.div>
  );
} 