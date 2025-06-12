import { ModuleContainer } from './ModuleContainer';
import PerformanceMetricsDashboard from '../performance/PerformanceMetricsDashboard';

export default function ModuleContainerExample() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-purple-950 to-black relative overflow-hidden">
      <ModuleContainer
        config={{
          id: 'system-metrics',
          title: 'System Metrics',
          category: 'neural', // purple glow
          size: 'md',
          breathingSpeed: 4,
          draggable: true,
          minimizable: true,
        }}
      >
        <PerformanceMetricsDashboard />
      </ModuleContainer>
      {/* Optional: cosmic particles or stars for extra space feel */}
      <div className="absolute inset-0 pointer-events-none z-0" style={{background: 'radial-gradient(ellipse at 60% 40%, #a78bfa33 0%, #f472b622 40%, #22d3ee11 100%)', filter: 'blur(2px)'}} />
    </div>
  );
} 