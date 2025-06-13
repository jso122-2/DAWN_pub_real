/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cosmic: {
          void: '#0A0A0F',
          deep: '#0F0F1F',
          dark: '#151525',
          surface: '#1A1A2E',
        },
        neural: {
          50: 'var(--neural-50)',
          100: 'var(--neural-100)',
          200: 'var(--neural-200)',
          300: 'var(--neural-300)',
          400: 'var(--neural-400)',
          500: 'var(--neural-500)',
          600: 'var(--neural-600)',
          700: 'var(--neural-700)',
          800: 'var(--neural-800)',
          900: 'var(--neural-900)',
          950: 'var(--neural-950)',
        },
        quantum: {
          50: 'var(--quantum-50)',
          100: 'var(--quantum-100)',
          200: 'var(--quantum-200)',
          300: 'var(--quantum-300)',
          400: 'var(--quantum-400)',
          500: 'var(--quantum-500)',
          600: 'var(--quantum-600)',
          700: 'var(--quantum-700)',
          800: 'var(--quantum-800)',
          900: 'var(--quantum-900)',
          950: 'var(--quantum-950)',
        },
        chaos: {
          50: 'var(--chaos-50)',
          100: 'var(--chaos-100)',
          200: 'var(--chaos-200)',
          300: 'var(--chaos-300)',
          400: 'var(--chaos-400)',
          500: 'var(--chaos-500)',
          600: 'var(--chaos-600)',
          700: 'var(--chaos-700)',
          800: 'var(--chaos-800)',
          900: 'var(--chaos-900)',
          950: 'var(--chaos-950)',
        },
        process: {
          50: 'var(--process-50)',
          100: 'var(--process-100)',
          200: 'var(--process-200)',
          300: 'var(--process-300)',
          400: 'var(--process-400)',
          500: 'var(--process-500)',
          600: 'var(--process-600)',
          700: 'var(--process-700)',
          800: 'var(--process-800)',
          900: 'var(--process-900)',
          950: 'var(--process-950)',
        },
        alert: {
          50: 'var(--alert-50)',
          100: 'var(--alert-100)',
          200: 'var(--alert-200)',
          300: 'var(--alert-300)',
          400: 'var(--alert-400)',
          500: 'var(--alert-500)',
          600: 'var(--alert-600)',
          700: 'var(--alert-700)',
          800: 'var(--alert-800)',
          900: 'var(--alert-900)',
          950: 'var(--alert-950)',
        },
      },
      spacing: {
        quantum: 'var(--space-quantum)',
        atom: 'var(--space-atom)',
        molecule: 'var(--space-molecule)',
        cell: 'var(--space-cell)',
        tissue: 'var(--space-tissue)',
        organ: 'var(--space-organ)',
        system: 'var(--space-system)',
        entity: 'var(--space-entity)',
        cosmos: 'var(--space-cosmos)',
      },
      animation: {
        'spin-slow': 'spin 20s linear infinite',
        'breathe-fast': 'breathe var(--breathe-fast) var(--ease-breathe-in) infinite',
        'breathe-normal': 'breathe var(--breathe-normal) var(--ease-breathe-in) infinite',
        'breathe-slow': 'breathe var(--breathe-slow) var(--ease-breathe-in) infinite',
        'breathe-cosmic': 'breathe var(--breathe-cosmic) var(--ease-breathe-in) infinite',
        'pulse-glow': 'pulse-glow var(--breathe-fast) ease-in-out infinite',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { 
            opacity: '1',
            filter: 'drop-shadow(0 0 20px rgba(139, 92, 246, 0.8))'
          },
          '50%': { 
            opacity: '0.8',
            filter: 'drop-shadow(0 0 40px rgba(139, 92, 246, 1))'
          }
        }
      }
    },
  },
  plugins: [],
}