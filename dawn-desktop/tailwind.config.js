/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Swiss Base
        'black': '#000000',
        'gray-950': '#0a0a0a',
        'gray-900': '#111111',
        'gray-800': '#1a1a1a',
        'gray-700': '#222222',
        'gray-600': '#2a2a2a',
        'gray-400': '#444444',
        'gray-200': '#666666',
        'gray-100': '#888888',
        'white': '#ffffff',
        'off-white': '#f0f0f0',
        
        // Terminal Accents
        'terminal-green': '#00ff41',
        'terminal-green-dim': '#00cc33',
        'terminal-amber': '#ffb000',
        'terminal-red': '#ff0040',

        // Neural Spectrum
        'neural-primary': '#a78bfa',
        'neural-accent': '#8b5cf6',
        'neural-spectrum-1': '#a78bfa',
        'neural-spectrum-2': '#c4b5fd',
        'neural-spectrum-3': '#f3e8ff',

        // Consciousness Spectrum
        'consciousness-primary': '#22d3ee',
        'consciousness-accent': '#06b6d4',
        'consciousness-spectrum-1': '#22d3ee',
        'consciousness-spectrum-2': '#67e8f9',
        'consciousness-spectrum-3': '#cffafe',

        // Chaos Spectrum
        'chaos-primary': '#f472b6',
        'chaos-accent': '#ec4899',
        'chaos-spectrum-1': '#f472b6',
        'chaos-spectrum-2': '#fb7185',
        'chaos-spectrum-3': '#fbcfe8',

        // Process Spectrum
        'process-primary': '#f59e0b',
        'process-accent': '#fbbf24',
        'process-spectrum-1': '#f59e0b',
        'process-spectrum-2': '#fcd34d',
        'process-spectrum-3': '#fef3c7',
      },
      fontFamily: {
        'ui': ['Inter', '-apple-system', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      spacing: {
        'grid': '8px',
      },
      animation: {
        'scanlines': 'scanlines 8s linear infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'blink': 'blink 1s infinite',
        'dots': 'dots 1.5s steps(4, end) infinite',
      },
      keyframes: {
        scanlines: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(10px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.8 },
        },
        blink: {
          '0%, 50%': { opacity: 1 },
          '51%, 100%': { opacity: 0 },
        },
        dots: {
          '0%, 20%': { content: '""' },
          '40%': { content: '"."' },
          '60%': { content: '".."' },
          '80%, 100%': { content: '"..."' },
        },
      },
    },
  },
  plugins: [],
}