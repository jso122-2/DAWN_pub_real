import { motion } from 'framer-motion'
import { useCosmicStore } from '../store/cosmic.store'

export function EntropyVisualizer() {
  const { entropy, updateEntropy } = useCosmicStore()

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      className="w-full max-w-4xl mx-auto p-8"
    >
      <div className="glass-heavy rounded-3xl p-8 glow">
        <h2 className="text-3xl font-bold mb-8 text-center text-pink-300">Entropy Visualizer</h2>
        
        {/* Entropy Ring */}
        <div className="relative h-64 mb-8 rounded-2xl bg-black/50 flex items-center justify-center">
          <svg className="w-48 h-48">
            <circle
              cx="96"
              cy="96"
              r="88"
              fill="none"
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="8"
            />
            <motion.circle
              cx="96"
              cy="96"
              r="88"
              fill="none"
              stroke="url(#gradient)"
              strokeWidth="8"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: entropy }}
              transition={{ duration: 0.5 }}
              style={{
                transform: 'rotate(-90deg)',
                transformOrigin: 'center',
              }}
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#f472b6" />
                <stop offset="100%" stopColor="#ec4899" />
              </linearGradient>
            </defs>
          </svg>
          
          <div className="absolute text-center">
            <div className="text-4xl font-bold text-pink-300">{(entropy * 100).toFixed(0)}%</div>
            <div className="text-sm text-gray-400">Entropy Level</div>
          </div>
        </div>

        {/* Chaos Particles */}
        <div className="relative h-32 mb-6 rounded-xl bg-black/30 overflow-hidden">
          {Array.from({ length: 20 }).map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-pink-400 rounded-full"
              animate={{
                x: [0, Math.random() * 400 - 200],
                y: [0, Math.random() * 100 - 50],
                opacity: [0, 1, 0],
              }}
              transition={{
                duration: 3 + Math.random() * 2,
                repeat: Infinity,
                delay: i * 0.1,
              }}
              style={{
                left: '50%',
                top: '50%',
              }}
            />
          ))}
        </div>

        {/* Control */}
        <div>
          <label className="text-gray-400 text-sm">Entropy Level</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={entropy}
            onChange={(e) => updateEntropy(parseFloat(e.target.value))}
            className="w-full mt-2"
          />
        </div>
      </div>
    </motion.div>
  )
}