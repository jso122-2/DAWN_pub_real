/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Neural Astral Palette
        dawn: {
          void: '#0a0a0f',
          deep: '#0d0d1a',
          surface: '#12131f',
          panel: '#1a1b2e',
          glow: {
            teal: '#00ffcc',
            purple: '#9945ff',
            amber: '#ffaa00',
            pink: '#ff0080',
          },
          neural: {
            100: '#1e3a8a',
            200: '#3730a3',
            300: '#6d28d9',
            400: '#8b5cf6',
            500: '#a78bfa',
          }
        },
        entropy: {
          stable: '#14b8a6',
          flux: '#f59e0b',
          critical: '#ef4444',
        }
      },
      fontFamily: {
        dawn: ['Iosevka', 'JetBrains Mono', 'Fantasque Sans Mono', 'monospace'],
      },
      animation: {
        'breathe': 'breathe 4s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'neural-flow': 'neuralFlow 3s linear infinite',
        'entropy-spin': 'entropySpin 20s linear infinite',
      },
      keyframes: {
        breathe: {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.8' },
          '50%': { transform: 'scale(1.05)', opacity: '1' },
        },
        pulseGlow: {
          '0%, 100%': { 
            boxShadow: '0 0 20px rgba(0, 255, 204, 0.5), inset 0 0 20px rgba(0, 255, 204, 0.1)',
          },
          '50%': { 
            boxShadow: '0 0 40px rgba(0, 255, 204, 0.8), inset 0 0 30px rgba(0, 255, 204, 0.2)',
          },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        neuralFlow: {
          '0%': { strokeDashoffset: '0' },
          '100%': { strokeDashoffset: '-100' },
        },
        entropySpin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        }
      },
      backdropFilter: {
        'blur-xl': 'blur(24px)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-neural': 'linear-gradient(135deg, #0d0d1a 0%, #1a1b2e 50%, #0a0a0f 100%)',
        'gradient-astral': 'radial-gradient(ellipse at top, #1e3a8a 0%, #0a0a0f 100%)',
      },
      boxShadow: {
        'glow-sm': '0 0 10px rgba(0, 255, 204, 0.5)',
        'glow-md': '0 0 20px rgba(0, 255, 204, 0.5)',
        'glow-lg': '0 0 30px rgba(0, 255, 204, 0.5)',
        'glow-xl': '0 0 40px rgba(0, 255, 204, 0.5)',
        'inner-glow': 'inset 0 0 20px rgba(0, 255, 204, 0.1)',
      },
    },
  },
  plugins: [
    // Custom plugin for glassmorphism utilities
    function({ addUtilities }) {
      const newUtilities = {
        '.glass': {
          background: 'rgba(26, 27, 46, 0.4)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
        '.glass-dark': {
          background: 'rgba(10, 10, 15, 0.6)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
        },
        '.neural-glow': {
          filter: 'drop-shadow(0 0 10px rgba(0, 255, 204, 0.5))',
        },
        '.text-glow': {
          textShadow: '0 0 10px currentColor, 0 0 20px currentColor',
        },
      }
      addUtilities(newUtilities)
    },
  ],
}