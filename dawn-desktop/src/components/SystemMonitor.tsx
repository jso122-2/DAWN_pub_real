import { motion } from 'framer-motion'
import { useCosmicStore } from '../store/cosmic.store'

export function SystemMonitor() {
  const store = useCosmicStore()

  const metrics = [
    { label: 'Neural Activity', value: store.neuralActivity, color: 'purple' },
    { label: 'Quantum Coherence', value: store.quantumCoherence, color: 'cyan' },
    { label: 'Entropy Level', value: store.entropy, color: 'pink' },
    { label: 'System Load', value: store.systemLoad, color: 'green' },
  ]

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="w-full max-w-4xl mx-auto p-8"
    >
      <div className="glass-heavy rounded-3xl p-8 glow">
        <h2 className="text-3xl font-bold mb-8 text-center text-green-300">System Monitor</h2>
        
        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-6">
          {metrics.map((metric) => (
            <div key={metric.label} className="glass rounded-xl p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="text-gray-400 text-sm">{metric.label}</div>
                  <div className={`text-3xl font-bold text-${metric.color}-300`}>
                    {(metric.value * 100).toFixed(0)}%
                  </div>
                </div>
                <div className={`w-12 h-12 rounded-full bg-${metric.color}-500/20 flex items-center justify-center`}>
                  <div className={`w-6 h-6 rounded-full bg-${metric.color}-500 animate-pulse`} />
                </div>
              </div>
              
              {/* Progress bar */}
              <div className="h-2 bg-black/50 rounded-full overflow-hidden">
                <motion.div
                  className={`h-full bg-gradient-to-r from-${metric.color}-500 to-${metric.color}-400`}
                  initial={{ width: 0 }}
                  animate={{ width: `${metric.value * 100}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-3 gap-4 mt-8">
          <button className="glass rounded-xl p-4 hover:bg-green-500/20 transition-all">
            <div className="text-sm text-gray-400">Optimize</div>
          </button>
          <button className="glass rounded-xl p-4 hover:bg-yellow-500/20 transition-all">
            <div className="text-sm text-gray-400">Analyze</div>
          </button>
          <button className="glass rounded-xl p-4 hover:bg-red-500/20 transition-all">
            <div className="text-sm text-gray-400">Reset</div>
          </button>
        </div>
      </div>
    </motion.div>
  )
}