/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        dawn: [
          'Iosevka Term',
          'JetBrains Mono',
          'Fantasque Sans Mono',
          'monospace',
        ],
        iosevka: ['Iosevka Term', 'monospace'],
        jetbrains: ['JetBrains Mono', 'monospace'],
        fantasque: ['Fantasque Sans Mono', 'monospace'],
      },
      colors: {
        black: '#000000',
        dawn: {
          black: '#0a0a0a',
          cyan: '#00ffff',
          magenta: '#ff00ff',
          amber: '#ffaa00',
        },
      },
      boxShadow: {
        'dawn-glow': '0 0 8px #00ffff, 0 0 16px #ff00ff',
        'holo-glow': '0 0 12px #00ffff, 0 0 24px #ff00ff, 0 0 32px #ffaa00',
      },
      textShadow: {
        glow: '0 0 4px #00ffff, 0 0 8px #ff00ff, 0 0 16px #ffaa00',
        holo: '0 0 8px #00ffff, 0 0 16px #ff00ff, 0 0 32px #ffaa00',
      },
    },
  },
  plugins: [
    require('tailwindcss-textshadow'),
  ],
};

