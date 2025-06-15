import React from 'react';
import { useConsciousnessStore } from '../stores/consciousnessStore';

const DebugConsciousness = () => {
  const { 
    tickData, 
    isConnected, 
    connectionState, 
    tickRate, 
    totalTicks 
  } = useConsciousnessStore();
  
  return (
    <div style={{
      position: 'fixed',
      top: '10px',
      right: '10px',
      background: 'rgba(0, 0, 0, 0.8)',
      color: 'white',
      padding: '10px',
      borderRadius: '5px',
      fontSize: '12px',
      fontFamily: 'monospace',
      zIndex: 9999,
      border: '1px solid #333'
    }}>
      <div><strong>🧠 Consciousness Debug</strong></div>
      <div>Connection: <span style={{color: isConnected ? '#00ff88' : '#ff4444'}}>
        {connectionState} {isConnected ? '✅' : '❌'}
      </span></div>
      <div>Tick Rate: {tickRate.toFixed(2)} Hz</div>
      <div>Total Ticks: {totalTicks}</div>
      
      {tickData ? (
        <div style={{marginTop: '10px'}}>
          <div><strong>Latest Data:</strong></div>
          <div>SCUP: {(tickData.scup * 100).toFixed(1)}%</div>
          <div>Entropy: {tickData.entropy.toFixed(3)}</div>
          <div>Heat: {tickData.heat.toFixed(3)}</div>
          <div>Mood: {tickData.mood}</div>
          <div>Timestamp: {new Date(tickData.timestamp).toLocaleTimeString()}</div>
        </div>
      ) : (
        <div style={{marginTop: '10px', color: '#888'}}>
          No tick data received yet...
        </div>
      )}
    </div>
  );
};

export default DebugConsciousness; 