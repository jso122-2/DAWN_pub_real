import React from 'react'
import { motion } from 'framer-motion'
import { useRouter } from '../../providers/RouterProvider'
import { Home, Brain, Zap, Settings, Monitor, Layers, Activity } from 'lucide-react'

interface NavItem {
  path: string
  label: string
  icon: React.ReactNode
  category: 'neural' | 'quantum' | 'system' | 'home'
}

const navItems: NavItem[] = [
  { path: '/', label: 'Home', icon: <Home className="w-4 h-4" />, category: 'home' },
  { path: '/demo', label: 'Demo', icon: <Brain className="w-4 h-4" />, category: 'neural' },
  { path: '/consciousness', label: 'Consciousness', icon: <Activity className="w-4 h-4" />, category: 'neural' },
  { path: '/quantum', label: 'Quantum', icon: <Zap className="w-4 h-4" />, category: 'quantum' },
  { path: '/neural', label: 'Neural', icon: <Brain className="w-4 h-4" />, category: 'neural' },
  { path: '/system', label: 'System', icon: <Monitor className="w-4 h-4" />, category: 'system' },
  { path: '/modules', label: 'Modules', icon: <Layers className="w-4 h-4" />, category: 'system' },
]

export const Navigation: React.FC = () => {
  const { currentPath, navigate, isTransitioning } = useRouter()

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'neural': return 'rgb(168, 85, 247)'
      case 'quantum': return 'rgb(34, 211, 238)'
      case 'system': return 'rgb(34, 197, 94)'
      case 'home': return 'rgb(251, 191, 36)'
      default: return 'rgb(156, 163, 175)'
    }
  }

  return (
    <motion.nav
      className="fixed left-4 top-1/2 transform -translate-y-1/2 z-40 glass-base p-2 rounded-xl"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 1 }}
    >
      <div className="flex flex-col gap-2">
        {navItems.map((item) => {
          const isActive = currentPath === item.path
          
          return (
            <motion.button
              key={item.path}
              onClick={() => navigate(item.path)}
              disabled={isTransitioning}
              className={`
                relative p-3 rounded-lg transition-all duration-300 group
                ${isActive 
                  ? 'bg-white/20 text-white shadow-lg' 
                  : 'bg-white/5 text-white/70 hover:bg-white/10 hover:text-white'
                }
              `}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {/* Active indicator */}
              {isActive && (
                <motion.div
                  className="absolute inset-0 rounded-lg border-2 opacity-50"
                  style={{ borderColor: getCategoryColor(item.category) }}
                  layoutId="activeNavItem"
                  transition={{
                    type: "spring",
                    stiffness: 300,
                    damping: 30
                  }}
                />
              )}
              
              {/* Glow effect */}
              <motion.div
                className="absolute inset-0 rounded-lg"
                style={{
                  boxShadow: isActive 
                    ? `0 0 20px ${getCategoryColor(item.category)}40`
                    : 'none'
                }}
                animate={{
                  opacity: isActive ? [0.6, 1, 0.6] : 0
                }}
                transition={{
                  duration: 2,
                  repeat: isActive ? Infinity : 0,
                  ease: "easeInOut"
                }}
              />
              
              {/* Icon */}
              <motion.div
                style={{ color: isActive ? getCategoryColor(item.category) : undefined }}
                animate={{
                  scale: isActive ? [1, 1.1, 1] : 1
                }}
                transition={{
                  duration: 1.5,
                  repeat: isActive ? Infinity : 0,
                  ease: "easeInOut"
                }}
              >
                {item.icon}
              </motion.div>
              
              {/* Tooltip */}
              <motion.div
                className="absolute left-full ml-3 px-2 py-1 bg-black/80 text-white text-xs rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none"
                style={{ borderColor: getCategoryColor(item.category) }}
              >
                {item.label}
                <div
                  className="absolute left-0 top-1/2 transform -translate-x-1 -translate-y-1/2 w-2 h-2 rotate-45 bg-black/80"
                />
              </motion.div>
            </motion.button>
          )
        })}
      </div>
      
      {/* Connection status indicator */}
      <motion.div
        className="mt-4 pt-2 border-t border-white/10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2 }}
      >
        <div className="flex items-center justify-center">
          <motion.div
            className="w-2 h-2 rounded-full bg-green-400"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [1, 0.7, 1]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        </div>
      </motion.div>
    </motion.nav>
  )
} 