import React from 'react';
import { motion } from 'framer-motion';

interface DataModuleProps {
  title: string;
  value: string | number;
  status?: 'active' | 'inactive' | 'error' | 'warning';
  className?: string;
  onClick?: () => void;
}

export const DataModule: React.FC<DataModuleProps> = ({
  title,
  value,
  status = 'active',
  className = '',
  onClick,
}) => {
  const getStatusColor = () => {
    switch (status) {
      case 'active':
        return 'var(--terminal-green-dim)';
      case 'inactive':
        return 'var(--gray-400)';
      case 'error':
        return 'var(--terminal-red)';
      case 'warning':
        return 'var(--terminal-amber)';
      default:
        return 'var(--terminal-green-dim)';
    }
  };

  return (
    <motion.div
      className={`data-module ${className}`}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      <div className="module-header">
        <span className="ascii-corner">╔═</span>
        <h3>{title}</h3>
        <span className="ascii-corner">═╗</span>
      </div>
      <div className="module-content">
        <div className="data-value crt-glow">{value}</div>
      </div>
      <div className="module-footer">
        <span className="ascii-corner">╚═</span>
        <span className="status" style={{ color: getStatusColor() }}>
          {status.toUpperCase()}
        </span>
        <span className="ascii-corner">═╝</span>
      </div>
    </motion.div>
  );
}; 