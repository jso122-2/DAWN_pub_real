import React from 'react';
import { motion } from 'framer-motion';
import { useConsciousness } from '../contexts/ConsciousnessContext';

const SimpleConsciousnessPage: React.FC = () => {
  const { data } = useConsciousness();

  return (
    <div style={{ 
      minHeight: '100vh', 
      padding: '40px', 
      background: '#000000', 
      color: '#ffffff' 
    }}>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}
      >
        <h1 style={{
          fontSize: '48px',
          background: 'linear-gradient(135deg, #00ff88 0%, #00aaff 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '20px'
        }}>
          Consciousness Monitor
        </h1>
        
        <p style={{
          fontSize: '18px',
          color: 'rgba(255, 255, 255, 0.6)',
          marginBottom: '40px'
        }}>
          Real-time consciousness flow analysis and SCUP metrics
        </p>

        {/* Connection Status */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '10px',
          marginBottom: '40px',
          padding: '15px 25px',
          background: 'rgba(0, 0, 0, 0.6)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 255, 136, 0.3)',
          borderRadius: '30px',
          width: 'fit-content',
          margin: '0 auto 40px auto'
        }}>
          <div style={{
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            background: data.isConnected ? '#00ff88' : '#ff4444',
            boxShadow: data.isConnected ? '0 0 10px #00ff88' : 'none'
          }} />
          <span>{data.isConnected ? 'Connected to consciousness stream' : 'Disconnected'}</span>
        </div>

        {/* Simple Metrics */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '20px',
          marginBottom: '40px'
        }}>
          <div style={{
            background: 'rgba(0, 255, 136, 0.1)',
            border: '1px solid rgba(0, 255, 136, 0.3)',
            borderRadius: '15px',
            padding: '20px',
            textAlign: 'center'
          }}>
            <h3 style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '10px' }}>SCUP Level</h3>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#00ff88' }}>
              {data.scup.toFixed(0)}%
            </div>
          </div>

          <div style={{
            background: 'rgba(255, 0, 170, 0.1)',
            border: '1px solid rgba(255, 0, 170, 0.3)',
            borderRadius: '15px',
            padding: '20px',
            textAlign: 'center'
          }}>
            <h3 style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '10px' }}>Entropy</h3>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#ff00aa' }}>
              {data.entropy.toFixed(3)}
            </div>
          </div>

          <div style={{
            background: 'rgba(255, 170, 0, 0.1)',
            border: '1px solid rgba(255, 170, 0, 0.3)',
            borderRadius: '15px',
            padding: '20px',
            textAlign: 'center'
          }}>
            <h3 style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '10px' }}>Heat</h3>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#ffaa00' }}>
              {data.heat.toFixed(3)}
            </div>
          </div>

          <div style={{
            background: 'rgba(0, 170, 255, 0.1)',
            border: '1px solid rgba(0, 170, 255, 0.3)',
            borderRadius: '15px',
            padding: '20px',
            textAlign: 'center'
          }}>
            <h3 style={{ color: 'rgba(255, 255, 255, 0.6)', marginBottom: '10px' }}>Tick Rate</h3>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#00aaff' }}>
              {data.tickRate}/s
            </div>
          </div>
        </div>

        <div style={{
          background: 'rgba(0, 0, 0, 0.6)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 255, 136, 0.2)',
          borderRadius: '15px',
          padding: '30px',
          textAlign: 'center'
        }}>
          <h3 style={{ color: '#00ff88', marginBottom: '20px' }}>Current Mood</h3>
          <div style={{ 
            fontSize: '24px', 
            fontWeight: 'bold',
            color: data.mood === 'confident' ? '#00ff88' : 
                   data.mood === 'analytical' ? '#0088ff' :
                   data.mood === 'focused' ? '#ffaa00' : '#ff00aa',
            textTransform: 'capitalize'
          }}>
            {data.mood}
          </div>
        </div>

        <p style={{
          marginTop: '40px',
          color: 'rgba(255, 255, 255, 0.5)',
          fontSize: '14px'
        }}>
          ✅ Simple consciousness page loaded successfully!
        </p>
      </motion.div>
    </div>
  );
};

export default SimpleConsciousnessPage; 