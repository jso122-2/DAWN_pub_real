import { useState, useEffect, useRef } from 'react'

export default function TickIndicator({ tickCount, isRunning, isPaused, intervalMs, className = "" }) {
  const [pulse, setPulse] = useState(false)
  const [lastTickCount, setLastTickCount] = useState(tickCount)
  const pulseTimeoutRef = useRef(null)

  useEffect(() => {
    if (tickCount !== lastTickCount && isRunning && !isPaused) {
      setPulse(true)
      setLastTickCount(tickCount)
      
      if (pulseTimeoutRef.current) {
        clearTimeout(pulseTimeoutRef.current)
      }
      
      pulseTimeoutRef.current = setTimeout(() => {
        setPulse(false)
      }, 200)
    }
    
    return () => {
      if (pulseTimeoutRef.current) {
        clearTimeout(pulseTimeoutRef.current)
      }
    }
  }, [tickCount, lastTickCount, isRunning, isPaused])

  const getColorScheme = () => {
    if (!isRunning) {
      return {
        primary: 'bg-gray-500',
        secondary: 'bg-gray-400',
        text: 'text-gray-300',
        border: 'border-gray-500/30',
        shadow: 'shadow-gray-500/20'
      }
    }
    
    if (isPaused) {
      return {
        primary: 'bg-yellow-500',
        secondary: 'bg-yellow-400',
        text: 'text-yellow-100',
        border: 'border-yellow-500/30',
        shadow: 'shadow-yellow-500/30'
      }
    }
    
    if (intervalMs < 100) {
      return {
        primary: 'bg-red-500',
        secondary: 'bg-red-400',
        text: 'text-red-100',
        border: 'border-red-500/30',
        shadow: 'shadow-red-500/40'
      }
    } else if (intervalMs < 300) {
      return {
        primary: 'bg-orange-500',
        secondary: 'bg-orange-400',
        text: 'text-orange-100',
        border: 'border-orange-500/30',
        shadow: 'shadow-orange-500/40'
      }
    } else if (intervalMs < 800) {
      return {
        primary: 'bg-blue-500',
        secondary: 'bg-blue-400',
        text: 'text-blue-100',
        border: 'border-blue-500/30',
        shadow: 'shadow-blue-500/40'
      }
    } else if (intervalMs < 2000) {
      return {
        primary: 'bg-green-500',
        secondary: 'bg-green-400',
        text: 'text-green-100',
        border: 'border-green-500/30',
        shadow: 'shadow-green-500/40'
      }
    } else {
      return {
        primary: 'bg-purple-500',
        secondary: 'bg-purple-400',
        text: 'text-purple-100',
        border: 'border-purple-500/30',
        shadow: 'shadow-purple-500/40'
      }
    }
  }

  const colors = getColorScheme()
  const ticksPerSecond = intervalMs > 0 ? (1000 / intervalMs).toFixed(1) : '0'

  return (
    <div className={`relative ${className}`}>
      <div className={`absolute inset-0 rounded-full transition-all duration-200 ${
        pulse && isRunning && !isPaused 
          ? `${colors.secondary} animate-ping opacity-75 scale-110` 
          : 'opacity-0'
      }`} />
      
      <div className={`absolute inset-1 rounded-full transition-all duration-300 ${
        isRunning && !isPaused 
          ? `${colors.primary} opacity-30 ${pulse ? 'scale-105' : ''}` 
          : 'opacity-0'
      }`} />
      
      <div className={`relative w-24 h-24 rounded-full border-2 transition-all duration-300 transform ${
        colors.primary
      } ${colors.border} ${colors.shadow} ${
        pulse && isRunning && !isPaused ? 'scale-110 shadow-lg' : ''
      } ${
        isRunning && !isPaused ? 'shadow-lg' : ''
      }`}>
        
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className={`text-lg font-bold font-mono ${colors.text} transition-all duration-200 ${
            pulse ? 'scale-110' : ''
          }`}>
            {tickCount.toLocaleString()}
          </div>
          
          <div className={`text-xs ${colors.text} opacity-75 mt-0.5`}>
            {!isRunning ? 'OFF' : isPaused ? 'PAUSE' : `${ticksPerSecond}Hz`}
          </div>
        </div>
        
        <div className={`absolute top-1 right-1 w-3 h-3 rounded-full transition-all duration-200 ${
          isRunning && !isPaused 
            ? `${colors.secondary} ${pulse ? 'animate-ping' : 'animate-pulse'}` 
            : 'bg-gray-600'
        }`} />
      </div>
      
      <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs text-gray-400 font-medium whitespace-nowrap">
        Tick Engine
      </div>
    </div>
  )
}