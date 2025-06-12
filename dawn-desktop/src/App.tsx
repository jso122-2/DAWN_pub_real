import { ModuleContainer } from './components/system/ModuleContainer';
import PerformanceMetricsDashboard from './components/performance/PerformanceMetricsDashboard';
import { CosmicBackground } from './components/CosmicBackground';

export default function App() {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden" style={{ background: '#000' }}>
      {/* Subtle Stars Background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <CosmicBackground />
      </div>
      {/* Minimal DAWN Header */}
      <header className="relative z-10 mt-12 mb-8 flex flex-col items-center">
        <h1
          className="text-5xl font-extrabold tracking-widest text-center animate-pulse"
          style={{
            background: 'linear-gradient(90deg, #a78bfa 0%, #f472b6 50%, #22d3ee 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            textShadow: '0 0 32px #a78bfa88, 0 0 16px #f472b688, 0 0 8px #22d3ee88',
            letterSpacing: '0.2em',
          }}
        >
          D.A.W.N
        </h1>
        <span className="text-purple-200 text-xs mt-2 tracking-widest" style={{ textShadow: '0 0 8px #a78bfa55' }}>
          Deep Adaptive Wisdom Network
        </span>
      </header>
      {/* System Metrics in ModuleContainer */}
      <main className="relative z-10 flex-1 flex items-center justify-center w-full">
        <ModuleContainer
          config={{
            id: 'system-metrics',
            title: 'System Metrics',
            category: 'neural',
            size: 'md',
            breathingSpeed: 4,
            draggable: false,
            minimizable: false,
          }}
        >
          <PerformanceMetricsDashboard />
        </ModuleContainer>
      </main>
    </div>
  );
}
