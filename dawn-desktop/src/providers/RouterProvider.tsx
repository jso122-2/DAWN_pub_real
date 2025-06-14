import React, { createContext, useContext, useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

interface RouterContextType {
  currentPath: string
  isTransitioning: boolean
  navigate: (path: string) => void
  goBack: () => void
  transitionState: 'idle' | 'entering' | 'exiting'
}

const RouterContext = createContext<RouterContextType | undefined>(undefined)

export const useRouter = () => {
  const context = useContext(RouterContext)
  if (!context) {
    throw new Error('useRouter must be used within RouterProvider')
  }
  return context
}

interface RouterProviderProps {
  children: React.ReactNode
}

export const RouterProvider: React.FC<RouterProviderProps> = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const [isTransitioning, setIsTransitioning] = useState(false)
  const [transitionState, setTransitionState] = useState<'idle' | 'entering' | 'exiting'>('idle')

  useEffect(() => {
    // Handle route transitions with consciousness awareness
    setIsTransitioning(true)
    setTransitionState('entering')
    
    const timer = setTimeout(() => {
      setIsTransitioning(false)
      setTransitionState('idle')
    }, 500)

    return () => clearTimeout(timer)
  }, [location.pathname])

  const handleNavigate = (path: string) => {
    setTransitionState('exiting')
    setIsTransitioning(true)
    
    setTimeout(() => {
      navigate(path)
    }, 250)
  }

  const goBack = () => {
    setTransitionState('exiting')
    setIsTransitioning(true)
    
    setTimeout(() => {
      navigate(-1)
    }, 250)
  }

  const contextValue: RouterContextType = {
    currentPath: location.pathname,
    isTransitioning,
    navigate: handleNavigate,
    goBack,
    transitionState
  }

  return (
    <RouterContext.Provider value={contextValue}>
      <AnimatePresence mode="wait">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.05 }}
          transition={{
            duration: 0.3,
            ease: [0.4, 0, 0.2, 1]
          }}
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </RouterContext.Provider>
  )
}

// Connection status component for WebSocket awareness
export const ConnectionStatus: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false)
  const [connectionState, setConnectionState] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('connecting')

  useEffect(() => {
    // Mock connection status - replace with actual WebSocket logic
    const timer = setTimeout(() => {
      setIsConnected(true)
      setConnectionState('connected')
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  const getStatusColor = () => {
    switch (connectionState) {
      case 'connected': return 'rgb(34, 197, 94)'
      case 'connecting': return 'rgb(234, 179, 8)'
      case 'disconnected': return 'rgb(239, 68, 68)'
      case 'error': return 'rgb(239, 68, 68)'
      default: return 'rgb(156, 163, 175)'
    }
  }

  return (
    <motion.div
      className="fixed top-4 right-4 z-50 glass-base p-2 rounded-lg"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.5 }}
    >
      <div className="flex items-center gap-2 text-xs">
        <motion.div
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: getStatusColor() }}
          animate={{
            scale: connectionState === 'connecting' ? [1, 1.2, 1] : 1,
            opacity: connectionState === 'connecting' ? [1, 0.5, 1] : 1
          }}
          transition={{
            duration: 1,
            repeat: connectionState === 'connecting' ? Infinity : 0
          }}
        />
        <span className="text-white/70 capitalize">{connectionState}</span>
      </div>
    </motion.div>
  )
} 