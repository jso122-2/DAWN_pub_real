import React from 'react'
import { motion } from 'framer-motion'
import { useRouter } from '../../providers/RouterProvider'
import { CheckCircle, AlertCircle, Clock, Navigation } from 'lucide-react'

export const RouterTest: React.FC = () => {
  const { currentPath, isTransitioning, navigate, goBack, transitionState } = useRouter()

  const testRoutes = [
    { path: '/', name: 'Home', description: 'Main module orchestra' },
    { path: '/demo', name: 'Demo', description: 'DAWN demonstration' },
    { path: '/quantum', name: 'Quantum', description: 'Quantum interface' },
    { path: '/neural', name: 'Neural', description: 'Neural dashboard' },
    { path: '/system', name: 'System', description: 'System dashboard' },
    { path: '/modules', name: 'Modules', description: 'Module demo page' },
  ]

  return (
    <motion.div
      className="fixed bottom-4 left-4 z-50 glass-base p-4 rounded-lg max-w-md"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 1.5 }}
    >
      <div className="flex items-center gap-2 mb-3">
        <CheckCircle className="w-5 h-5 text-green-400" />
        <h3 className="text-white font-semibold">Router Status</h3>
      </div>

      <div className="space-y-3">
        {/* Current Status */}
        <div className="glass-base p-3 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="text-white/70 text-sm">Current Route:</span>
            <span className="text-cyan-400 font-mono text-sm">{currentPath}</span>
          </div>
          
          <div className="flex items-center justify-between mb-2">
            <span className="text-white/70 text-sm">Transition State:</span>
            <div className="flex items-center gap-1">
              {isTransitioning && <Clock className="w-3 h-3 text-yellow-400" />}
              <span className={`font-mono text-sm ${
                transitionState === 'idle' ? 'text-green-400' :
                transitionState === 'entering' ? 'text-yellow-400' :
                'text-orange-400'
              }`}>
                {transitionState}
              </span>
            </div>
          </div>
        </div>

        {/* Quick Navigation */}
        <div className="glass-base p-3 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <Navigation className="w-4 h-4 text-purple-400" />
            <span className="text-white/70 text-sm">Quick Test:</span>
          </div>
          
          <div className="grid grid-cols-2 gap-2">
            {testRoutes.map((route) => (
              <motion.button
                key={route.path}
                onClick={() => navigate(route.path)}
                disabled={isTransitioning || currentPath === route.path}
                className={`
                  p-2 rounded text-xs transition-all duration-200
                  ${currentPath === route.path
                    ? 'bg-cyan-500/20 text-cyan-400 cursor-default'
                    : isTransitioning
                      ? 'bg-white/5 text-white/30 cursor-not-allowed'
                      : 'bg-white/10 text-white/70 hover:bg-white/20 hover:text-white'
                  }
                `}
                whileHover={!isTransitioning && currentPath !== route.path ? { scale: 1.02 } : {}}
                whileTap={!isTransitioning && currentPath !== route.path ? { scale: 0.98 } : {}}
              >
                {route.name}
              </motion.button>
            ))}
          </div>
        </div>

        {/* Route Information */}
        <div className="glass-base p-3 rounded-lg">
          <span className="text-white/70 text-sm">Route Info:</span>
          <div className="mt-1">
            {testRoutes.find(r => r.path === currentPath)?.description || 'Unknown route'}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <motion.button
            onClick={goBack}
            disabled={isTransitioning}
            className="flex-1 p-2 bg-white/10 text-white/70 rounded text-sm hover:bg-white/20 hover:text-white transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={!isTransitioning ? { scale: 1.02 } : {}}
            whileTap={!isTransitioning ? { scale: 0.98 } : {}}
          >
            ← Back
          </motion.button>
          
          <motion.button
            onClick={() => navigate('/')}
            disabled={isTransitioning || currentPath === '/'}
            className="flex-1 p-2 bg-purple-500/20 text-purple-400 rounded text-sm hover:bg-purple-500/30 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={!isTransitioning && currentPath !== '/' ? { scale: 1.02 } : {}}
            whileTap={!isTransitioning && currentPath !== '/' ? { scale: 0.98 } : {}}
          >
            🏠 Home
          </motion.button>
        </div>

        {/* Status Indicator */}
        <div className="flex items-center justify-center pt-2">
          <motion.div
            className="flex items-center gap-2 text-xs text-green-400"
            animate={{
              opacity: [1, 0.7, 1]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <CheckCircle className="w-3 h-3" />
            Router Working ✨
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
} 