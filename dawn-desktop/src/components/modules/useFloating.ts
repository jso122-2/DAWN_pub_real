import { useEffect, useRef, useState, useMemo, useCallback } from 'react'
import { useAnimationFrame, useMotionValue, useSpring } from 'framer-motion'
import type { MotionProps } from 'framer-motion'

interface FloatingConfig {
  amplitude: { x: number; y: number }
  frequency: number
  rotationAmount: number
  magneticStrength: number
  orbitalRadius: number
  mouseInfluence: number
  dampening: number
}

interface UseFloatingOptions {
  preset?: 'gentle' | 'active' | 'orbital' | 'magnetic'
  disabled?: boolean
  boundaryRef?: React.RefObject<HTMLElement>
  moduleId?: string
  groupId?: string // For orbital movements
  customConfig?: Partial<FloatingConfig>
  enableMouse?: boolean
}

interface ModulePosition {
  x: number
  y: number
  vx: number
  vy: number
  element: HTMLElement | null
}

// Global registry for module positions (for magnetic repulsion)
const moduleRegistry = new Map<string, ModulePosition>()
const orbitalGroups = new Map<string, { center: { x: number; y: number }; modules: string[] }>()

const FLOATING_PRESETS: Record<string, FloatingConfig> = {
  gentle: {
    amplitude: { x: 10, y: 15 },
    frequency: 0.0005,
    rotationAmount: 2,
    magneticStrength: 50,
    orbitalRadius: 0,
    mouseInfluence: 0.1,
    dampening: 0.95
  },
  active: {
    amplitude: { x: 20, y: 25 },
    frequency: 0.001,
    rotationAmount: 5,
    magneticStrength: 80,
    orbitalRadius: 0,
    mouseInfluence: 0.2,
    dampening: 0.9
  },
  orbital: {
    amplitude: { x: 5, y: 5 },
    frequency: 0.0003,
    rotationAmount: 360,
    magneticStrength: 30,
    orbitalRadius: 150,
    mouseInfluence: 0.05,
    dampening: 0.98
  },
  magnetic: {
    amplitude: { x: 15, y: 20 },
    frequency: 0.0008,
    rotationAmount: 3,
    magneticStrength: 120,
    orbitalRadius: 0,
    mouseInfluence: 0.3,
    dampening: 0.85
  }
}

export function useFloating(options: UseFloatingOptions = {}): MotionProps & { 
  setPosition?: (x: number, y: number) => void 
} {
  const {
    preset = 'gentle',
    disabled = false,
    boundaryRef,
    moduleId = `module-${Math.random().toString(36).substr(2, 9)}`,
    groupId,
    customConfig,
    enableMouse = true
  } = options

  const config = useMemo(() => ({
    ...FLOATING_PRESETS[preset],
    ...customConfig
  }), [preset, customConfig])

  // Motion values for smooth animations
  const x = useMotionValue(0)
  const y = useMotionValue(0)

  // Spring configuration for smooth movements
  const springConfig = { stiffness: 50, damping: 20 }
  const springX = useSpring(x, springConfig)
  const springY = useSpring(y, springConfig)

  // State
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const elementRef = useRef<HTMLElement | null>(null)
  const timeRef = useRef(0)
  const velocityRef = useRef({ x: 0, y: 0 })
  const positionRef = useRef({ x: 0, y: 0 })
  const lastTimeRef = useRef(0)
  const animationRef = useRef<number>()

  // Register module in global registry
  useEffect(() => {
    if (!disabled && moduleId) {
      moduleRegistry.set(moduleId, {
        x: positionRef.current.x,
        y: positionRef.current.y,
        vx: velocityRef.current.x,
        vy: velocityRef.current.y,
        element: elementRef.current
      })

      // Register in orbital group if specified
      if (groupId) {
        const group = orbitalGroups.get(groupId) || { 
          center: { x: window.innerWidth / 2, y: window.innerHeight / 2 }, 
          modules: [] 
        }
        if (!group.modules.includes(moduleId)) {
          group.modules.push(moduleId)
        }
        orbitalGroups.set(groupId, group)
      }

      return () => {
        moduleRegistry.delete(moduleId)
        if (groupId) {
          const group = orbitalGroups.get(groupId)
          if (group) {
            group.modules = group.modules.filter(id => id !== moduleId)
            if (group.modules.length === 0) {
              orbitalGroups.delete(groupId)
            }
          }
        }
      }
    }
  }, [disabled, moduleId, groupId])

  // Mouse tracking
  useEffect(() => {
    if (!enableMouse || disabled) return

    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ x: e.clientX, y: e.clientY })
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [enableMouse, disabled])

  // Calculate forces
  const calculateForces = useCallback((timestamp: number) => {
    const deltaTime = timestamp - timeRef.current
    timeRef.current = timestamp

    let forceX = 0
    let forceY = 0

    // 1. Base floating motion
    const floatX = Math.sin(timestamp * config.frequency) * config.amplitude.x
    const floatY = Math.cos(timestamp * config.frequency * 0.7) * config.amplitude.y
    
    forceX += floatX - positionRef.current.x
    forceY += floatY - positionRef.current.y

    // 2. Orbital motion
    if (config.orbitalRadius > 0 && groupId) {
      const group = orbitalGroups.get(groupId)
      if (group) {
        const moduleIndex = group.modules.indexOf(moduleId)
        const angleOffset = (moduleIndex / group.modules.length) * Math.PI * 2
        const orbitAngle = timestamp * config.frequency + angleOffset
        
        const targetX = group.center.x + Math.cos(orbitAngle) * config.orbitalRadius
        const targetY = group.center.y + Math.sin(orbitAngle) * config.orbitalRadius
        
        forceX += (targetX - positionRef.current.x) * 0.1
        forceY += (targetY - positionRef.current.y) * 0.1
      }
    }

    // 3. Magnetic repulsion from other modules
    if (config.magneticStrength > 0) {
      moduleRegistry.forEach((otherModule, otherId) => {
        if (otherId === moduleId) return

        const dx = positionRef.current.x - otherModule.x
        const dy = positionRef.current.y - otherModule.y
        const distance = Math.sqrt(dx * dx + dy * dy)

        if (distance < 200 && distance > 0) {
          const force = config.magneticStrength / (distance * distance)
          forceX += (dx / distance) * force
          forceY += (dy / distance) * force
        }
      })
    }

    // 4. Mouse influence
    if (enableMouse && config.mouseInfluence > 0) {
      const mouseDx = mousePos.x - positionRef.current.x
      const mouseDy = mousePos.y - positionRef.current.y
      const mouseDistance = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy)

      if (mouseDistance < 300 && mouseDistance > 0) {
        const mouseForce = config.mouseInfluence * (300 - mouseDistance) / 300
        forceX += (mouseDx / mouseDistance) * mouseForce
        forceY += (mouseDy / mouseDistance) * mouseForce
      }
    }

    // 5. Boundary constraints
    if (boundaryRef?.current) {
      const bounds = boundaryRef.current.getBoundingClientRect()
      const padding = 50

      if (positionRef.current.x < padding) {
        forceX += (padding - positionRef.current.x) * 0.2
      } else if (positionRef.current.x > bounds.width - padding) {
        forceX += (bounds.width - padding - positionRef.current.x) * 0.2
      }

      if (positionRef.current.y < padding) {
        forceY += (padding - positionRef.current.y) * 0.2
      } else if (positionRef.current.y > bounds.height - padding) {
        forceY += (bounds.height - padding - positionRef.current.y) * 0.2
      }
    }

    // Apply forces with dampening
    velocityRef.current.x = velocityRef.current.x * config.dampening + forceX * 0.01
    velocityRef.current.y = velocityRef.current.y * config.dampening + forceY * 0.01

    // Update position
    positionRef.current.x += velocityRef.current.x
    positionRef.current.y += velocityRef.current.y

    return {
      x: positionRef.current.x,
      y: positionRef.current.y
    }
  }, [config, groupId, moduleId, mousePos, enableMouse, boundaryRef])

  // Animation loop
  useAnimationFrame((timestamp) => {
    if (disabled) return

    const { x: newX, y: newY } = calculateForces(timestamp)
    
    x.set(newX)
    y.set(newY)

    // Update global registry
    if (moduleId) {
      const moduleData = moduleRegistry.get(moduleId)
      if (moduleData) {
        moduleData.x = newX
        moduleData.y = newY
        moduleData.vx = velocityRef.current.x
        moduleData.vy = velocityRef.current.y
      }
    }
  })

  // Manual position setter
  const setPosition = useCallback((newX: number, newY: number) => {
    positionRef.current = { x: newX, y: newY }
    x.set(newX)
    y.set(newY)
  }, [x, y])

  // Generate motion props
  const motionProps: MotionProps = useMemo(() => {
    if (disabled) {
      return {}
    }

    return {
      style: {
        x: springX,
        y: springY,
      },
      ref: (el: HTMLElement | null) => {
        elementRef.current = el
        if (moduleId) {
          const moduleData = moduleRegistry.get(moduleId)
          if (moduleData) {
            moduleData.element = el
          }
        }
      },
      initial: false,
      transition: {
        type: 'spring',
        ...springConfig
      }
    }
  }, [disabled, springX, springY, moduleId])

  return { ...motionProps, setPosition }
}

// Utility hook to create orbital group center
export function useOrbitalCenter(groupId: string) {
  const setCenter = useCallback((x: number, y: number) => {
    const group = orbitalGroups.get(groupId) || { center: { x, y }, modules: [] }
    group.center = { x, y }
    orbitalGroups.set(groupId, group)
  }, [groupId])

  return { setCenter }
}

// Get all module positions for visualization
export function getModulePositions(): Map<string, ModulePosition> {
  return new Map(moduleRegistry)
}

// Force recalculation for specific module
export function applyImpulse(moduleId: string, impulseX: number, impulseY: number) {
  const module = moduleRegistry.get(moduleId)
  if (module) {
    module.vx += impulseX
    module.vy += impulseY
  }
}