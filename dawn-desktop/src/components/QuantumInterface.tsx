import { motion } from 'framer-motion'
import { useCosmicStore } from '../store/cosmic.store'

export function QuantumInterface() {
  const { quantumCoherence, updateQuantumCoherence } = useCosmicStore()

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="w-full max-w-4xl mx-auto p-8"
    >
      <div className="glass-heavy rounded-3xl p-8 glow">
        <h2 className="text-3xl font-bold mb-8 text-center text-cyan-300">Quantum State Monitor</h2>
        
        {/* Quantum Visualization */}
        <div className="relative h-64 mb-8 rounded-2xl bg-black/50 flex items-center justify-center">
          <motion.div
            animate={{
              rotate: 360,
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
            }}
            className="relative w-48 h-48"
          >
            {/* Quantum rings */}
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="absolute inset-0 rounded-full border-2 border-cyan-500/30"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.3, 0.6, 0.3],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  delay: i * 0.5,
                }}
              />
            ))}
            
            {/* Core */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 animate-pulse-glow" />
            </div>
          </motion.div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="glass rounded-xl p-4">
            <div className="text-gray-400 text-sm">Coherence</div>
            <div className="text-2xl font-bold text-cyan-300">{(quantumCoherence * 100).toFixed(1)}%</div>
          </div>
          <div className="glass rounded-xl p-4">
            <div className="text-gray-400 text-sm">Entanglement</div>
            <div className="text-2xl font-bold text-blue-300">{(quantumCoherence * 87).toFixed(1)}%</div>
          </div>
        </div>

        {/* Control */}
        <div>
          <label className="text-gray-400 text-sm">Quantum Coherence</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={quantumCoherence}
            onChange={(e) => updateQuantumCoherence(parseFloat(e.target.value))}
            className="w-full mt-2"
          />
        </div>
      </div>
    </motion.div>
  )
}