import React from 'react';
import { motion } from 'framer-motion';

interface ModuleProps {
  title: string;
  className?: string;
  children: React.ReactNode;
}

export const Module: React.FC<ModuleProps> = ({
  title,
  className = '',
  children
}) => {
  return (
    <motion.div
      className={`terminal-border p-4 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center gap-2 mb-4">
        <span className="text-terminal-green font-mono">[</span>
        <h2 className="text-terminal-green font-mono">{title}</h2>
        <span className="text-terminal-green font-mono">]</span>
      </div>
      <div className="font-mono">
        {children}
      </div>
    </motion.div>
  );
}; 