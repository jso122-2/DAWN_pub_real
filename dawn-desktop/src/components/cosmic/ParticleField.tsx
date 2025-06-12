import { motion } from 'framer-motion';

export function ParticleField() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass rounded-xl p-8 backdrop-blur-xl"
    >
      <h2 className="text-2xl font-bold text-purple-300">ParticleField</h2>
      <p className="text-gray-400 mt-4">Component implementation coming soon...</p>
    </motion.div>
  )
} 