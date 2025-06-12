import { motion } from 'framer-motion';
import React from 'react';

interface CosmicSpinnerProps {
  label?: string;
}

const CosmicSpinner: React.FC<CosmicSpinnerProps> = ({ label = 'Loading...' }) => (
  <motion.div
    className="flex flex-col items-center justify-center w-full h-full"
    initial={{ opacity: 0, scale: 0.8 }}
    animate={{ opacity: 1, scale: 1 }}
    exit={{ opacity: 0, scale: 0.8 }}
    aria-label={label}
    role="status"
  >
    <div className="glass rounded-full p-6 shadow-glow-md mb-4">
      <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin" />
    </div>
    <span className="text-purple-300 text-sm mt-2">{label}</span>
  </motion.div>
);

export default CosmicSpinner; 