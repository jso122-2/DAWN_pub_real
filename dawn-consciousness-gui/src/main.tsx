import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { init } from './hooks/useTickState'

console.log('🚀 [MAIN] Starting DAWN Consciousness GUI')

// Initialize DAWN tick state listener
console.log('🔧 [MAIN] Initializing tick state listener...')
init()
  .then(() => {
    console.log('✅ [MAIN] Tick state listener initialized successfully')
  })
  .catch((error) => {
    console.error('❌ [MAIN] Failed to initialize tick state listener:', error)
  })

console.log('⚛️ [MAIN] Rendering React app')
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
) 