import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ConsciousnessMatrix from '../components/ConsciousnessMatrix';
import DebugConsciousness from '../components/DebugConsciousness';
import { useConsciousnessStore } from '../stores/consciousnessStore';
import GlassPanel from '../components/ui/GlassPanel';
import MetricCard from '../components/ui/MetricCard';

const ConsciousnessPage: React.FC = () => {
  const { 
    tickData, 
    isConnected, 
    averageScup, 
    currentTrend, 
    totalTicks, 
    tickRate,
    getScupTrend,
    getEntropyTrend,
    clearHistory
  } = useConsciousnessStore();
  
  const [viewMode, setViewMode] = useState<'overview' | 'detailed' | 'analysis'>('overview');
  const [autoRotate, setAutoRotate] = useState(true);
  
  const scupTrend = getScupTrend();
  const entropyTrend = getEntropyTrend();
  
  const connectionTime = new Date().toLocaleTimeString();
  
  return (
    <div className="consciousness-page" style={{ 
      minHeight: '100vh', 
      background: 'radial-gradient(ellipse at center, #0a0a1a 0%, #000000 100%)',
      overflow: 'hidden'
    }}>
      <DebugConsciousness />
      
      {/* Use our enhanced ConsciousnessMatrix component */}
      <ConsciousnessMatrix />
    </div>
  );
};

export default ConsciousnessPage; 