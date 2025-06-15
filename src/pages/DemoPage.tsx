import React from 'react';
import { motion } from 'framer-motion';

const DemoPage: React.FC = () => {
  return (
    <div className="demo-page">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        style={{ 
          padding: '60px 40px',
          textAlign: 'center',
          minHeight: '100vh',
          background: '#000000',
          color: '#ffffff'
        }}
      >
        <h1 style={{
          fontSize: '48px',
          background: 'linear-gradient(135deg, #00ff88 0%, #00aaff 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '20px'
        }}>
          Demo Center
        </h1>
        <p style={{
          fontSize: '18px',
          color: 'rgba(255, 255, 255, 0.6)',
          marginBottom: '40px'
        }}>
          Interactive demonstrations and system showcases
        </p>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '20px',
          maxWidth: '1200px',
          margin: '0 auto'
        }}>
          {[
            { name: 'Consciousness Flow', desc: 'Interactive consciousness visualization' },
            { name: 'Neural Patterns', desc: 'Live neural network demonstrations' },
            { name: 'SCUP Dynamics', desc: 'Real-time SCUP measurement showcase' },
            { name: 'System Integration', desc: 'Full system operation examples' }
          ].map((demo, index) => (
            <motion.div
              key={demo.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              style={{
                background: 'rgba(0, 0, 0, 0.6)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(0, 255, 136, 0.2)',
                borderRadius: '15px',
                padding: '30px',
                cursor: 'pointer'
              }}
            >
              <h3 style={{ color: '#00ff88', marginBottom: '10px' }}>{demo.name}</h3>
              <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '14px' }}>
                {demo.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default DemoPage; 