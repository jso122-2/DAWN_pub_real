import { motion } from 'framer-motion'
import { NeuralProcessMap } from './NeuralProcessMap'
import { useCosmicStore } from '../store/cosmicStore'

export function NeuralDashboard() {
  const { neuralActivity } = useCosmicStore()

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="w-full h-full p-8"
    >
      <div className="h-full flex flex-col gap-6">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-purple-300 mb-2">Neural Network Monitor</h2>
          <p className="text-gray-400">System Neural Activity: {(neuralActivity * 100).toFixed(0)}%</p>
        </div>
        
        <div className="flex-1 min-h-0">
          <NeuralProcessMap width={1200} height={600} />
        </div>
      </div>
    </motion.div>
  )
}

export default NeuralDashboard
