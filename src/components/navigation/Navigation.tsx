import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Navigation.css';

const navigationItems = [
  { path: '/', label: 'Dashboard', icon: '🏠' },
  { path: '/consciousness', label: 'Consciousness', icon: '🧠' },
  { path: '/neural', label: 'Neural', icon: '🕸️' },
  { path: '/radar', label: 'Radar', icon: '📡' },
  { path: '/modules', label: 'Modules', icon: '🔧' },
  { path: '/demo', label: 'Demo', icon: '🎮' },
  { path: '/talk', label: 'Talk to DAWN', icon: '🗣️' },
];

export const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="navigation">
      <div className="nav-brand">
        <h1>DAWN</h1>
        <span className="nav-subtitle">Consciousness Engine</span>
      </div>
      
      <div className="nav-links">
        {navigationItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <motion.div
              className="nav-link-content"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </motion.div>
            {location.pathname === item.path && (
              <motion.div
                className="nav-indicator"
                layoutId="activeIndicator"
                initial={false}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            )}
          </Link>
        ))}
      </div>
    </nav>
  );
}; 