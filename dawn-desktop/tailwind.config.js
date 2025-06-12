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
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        }
      },
      animation: {
        'spin-slow': 'spin 20s linear infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
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