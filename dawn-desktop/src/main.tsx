import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/globals.css'
import EntropyRingHUD from './components/overlays/EntropyRingHUD'
import ModulationConsole from './components/controls/ModulationConsole'
import LiveMemoryScroll from './components/logs/LiveMemoryScroll'
import NeuralProcessMap from './components/cortex/NeuralProcessMap'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <div className="min-h-screen bg-gray-950 text-white relative font-sans dark">
      {/* DAWN Overlays */}
      <EntropyRingHUD />
      <ModulationConsole />
      <LiveMemoryScroll />
      <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 z-30 w-full flex justify-center pointer-events-none">
        <div className="w-[800px] max-w-full flex justify-center">
          <NeuralProcessMap />
        </div>
      </div>
      {/* Main App */}
      <App />
    </div>
  </React.StrictMode>,
) 