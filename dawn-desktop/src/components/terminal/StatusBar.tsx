import React from 'react';
import { motion } from 'framer-motion';
import { useConsciousness } from '../../hooks/useConsciousness';

interface StatusBarProps {
  className?: string;
}

export const StatusBar: React.FC<StatusBarProps> = ({
  className = ''
}) => {
  const consciousness = useConsciousness();

  return (
    <motion.div
      className={`terminal-border p-2 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center justify-between text-xs font-mono">
        <div className="flex items-center gap-4">
          <span className="text-terminal-green">TICK: {consciousness.tick}</span>
          <span className="text-gray-400">|</span>
          <span className="text-terminal-green">SCUP: {consciousness.scup.toFixed(1)}%</span>
          <span className="text-gray-400">|</span>
          <span className="text-terminal-green">MOOD: {consciousness.mood.toUpperCase()}</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-gray-400">|</span>
          <span className="text-terminal-green">ENTROPY: {consciousness.entropy.toFixed(2)}</span>
          <span className="text-gray-400">|</span>
          <span className="text-terminal-green">NEURAL: {(consciousness.neuralActivity * 100).toFixed(1)}%</span>
        </div>
      </div>
    </motion.div>
  );
}; 