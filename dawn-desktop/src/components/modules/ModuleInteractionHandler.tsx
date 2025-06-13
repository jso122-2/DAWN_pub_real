import { motion } from 'framer-motion'
import { applyImpulse } from '../../hooks/useFloating'

interface ModuleInteractionHandlerProps {
  moduleId: string
  children: React.ReactNode
}

export function ModuleInteractionHandler({ moduleId, children }: ModuleInteractionHandlerProps) {
  const handleClick = () => {
    // Apply impulse on click
    applyImpulse(moduleId, 
      (Math.random() - 0.5) * 20, 
      (Math.random() - 0.5) * 20
    )
  }

  const handleDragEnd = (event: any, info: any) => {
    // Apply impulse based on drag velocity
    applyImpulse(moduleId, info.velocity.x / 10, info.velocity.y / 10)
  }

  return (
    <motion.div
      onClick={handleClick}
      onDragEnd={handleDragEnd}
      drag
      dragMomentum={false}
      whileDrag={{ scale: 1.1 }}
    >
      {children}
    </motion.div>
  )
} 