import { motion } from 'framer-motion'
import NeuralActivityVisualizer from './neural/NeuralActivityVisualizer'
import NeuralTimeline from './timeline/NeuralTimeline'
import PerformanceMetricsDashboard from './performance/PerformanceMetricsDashboard'

export function NeuralMonitoringDashboard() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="w-full h-full p-8 overflow-y-auto"
    >
      <div className="max-w-7xl mx-auto space-y-6">
        <h2 className="text-3xl font-bold text-center text-purple-300 mb-8">Neural Monitoring</h2>
        
        {/* Neural Activity Visualizer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <NeuralActivityVisualizer />
        </motion.div>
        
        {/* Neural Timeline */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <NeuralTimeline />
        </motion.div>
        
        {/* Performance Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <PerformanceMetricsDashboard />
        </motion.div>
      </div>
    </motion.div>
  )
}

export default NeuralMonitoringDashboard
