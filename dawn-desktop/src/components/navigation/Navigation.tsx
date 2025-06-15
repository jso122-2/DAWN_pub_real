import React from 'react'
import { motion } from 'framer-motion'
import { NavLink } from 'react-router-dom'

interface NavItem {
  path: string
  label: string
  icon?: string
}

export const Navigation: React.FC = () => {
  const navItems: NavItem[] = [
    { path: '/', label: 'Home', icon: '🏠' },
    { path: '/consciousness', label: 'Consciousness', icon: '🧠' },
    { path: '/talk', label: 'Talk to DAWN', icon: '💬' },
    { path: '/subprocess', label: 'Subprocess Manager', icon: '🌊' },
    { path: '/quantum', label: 'Quantum State', icon: '⚡' },
    { path: '/neural', label: 'Neural Network', icon: '🕸️' },
    { path: '/modules', label: 'Modules', icon: '📦' },
    { path: '/demo', label: 'Demo', icon: '🎨' },
    { path: '/glass', label: 'Glass Demo', icon: '🔮' },
  ]

  return (
    <motion.nav
      className="navigation"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="nav-items">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `nav-item ${isActive ? 'active' : ''}`
            }
          >
            {item.icon && <span className="nav-icon">{item.icon}</span>}
            <span className="nav-label">{item.label}</span>
          </NavLink>
        ))}
      </div>
    </motion.nav>
  )
} 