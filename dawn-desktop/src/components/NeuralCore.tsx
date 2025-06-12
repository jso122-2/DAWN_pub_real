import { motion } from 'framer-motion'
import { useCosmicStore } from '../store/cosmic.store'

export function NeuralCore() {
  const { neuralActivity, updateNeuralActivity } = useCosmicStore()

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="w-full max-w-4xl mx-auto p-8"
    >
      <div className="glass-heavy rounded-3xl p-8 glow">
        <h2 className="text-3xl font-bold mb-8 text-center text-purple-300">Neural Activity Monitor</h2>
        
        {/* Neural Visualization */}
        <div className="relative h-64 mb-8 rounded-2xl bg-black/50 overflow-hidden">
          <div className="absolute inset-0 flex items-end justify-around p-4">
            {Array.from({ length: 20 }).map((_, i) => (
              <motion.div
                key={i}
                className="w-4 bg-gradient-to-t from-purple-500 to-pink-500 rounded-t"
                animate={{
                  height: `${Math.random() * 100}%`,
                }}
                transition={{
                  duration: 0.5,
                  repeat: Infinity,
                  repeatType: "reverse",
                  delay: i * 0.1,
                }}
              />
            ))}
          </div>
          
          {/* Activity Level */}
          <div className="absolute top-4 right-4 glass rounded-full px-4 py-2">
            <span className="text-purple-300">{(neuralActivity * 100).toFixed(0)}%</span>
          </div>
        </div>

        {/* Controls */}
        <div className="space-y-4">
          <div>
            <label className="text-gray-400 text-sm">Neural Activity</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={neuralActivity}
              onChange={(e) => updateNeuralActivity(parseFloat(e.target.value))}
              className="w-full mt-2"
            />
          </div>
          
          <div className="grid grid-cols-3 gap-4">
            <button className="glass rounded-xl p-4 hover:bg-purple-500/20 transition-all">
              <div className="text-2xl mb-2">🧠</div>
              <div className="text-sm text-gray-400">Cortex</div>
            </button>
            <button className="glass rounded-xl p-4 hover:bg-purple-500/20 transition-all">
              <div className="text-2xl mb-2">⚡</div>
              <div className="text-sm text-gray-400">Synaptic</div>
            </button>
            <button className="glass rounded-xl p-4 hover:bg-purple-500/20 transition-all">
              <div className="text-2xl mb-2">🌊</div>
              <div className="text-sm text-gray-400">Waves</div>
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  )
}