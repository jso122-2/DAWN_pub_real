import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';

// Lazy load pages with error handling
const UnifiedHomePage = React.lazy(() => 
  import('../pages/UnifiedHomePage')
);

const OptimizedDashboardPage = React.lazy(() => 
  import('../components/OptimizedDashboard/OptimizedDashboard').then(module => ({
    default: () => <module.OptimizedDashboard />
  })).catch(err => {
    console.error('Failed to load OptimizedDashboard:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Optimized Dashboard: {err.message}</div> };
  })
);

const HomePage = React.lazy(() => 
  import('../pages/HomePage').catch(err => {
    console.error('Failed to load HomePage:', err);
    return { default: () => <div>Error loading HomePage</div> };
  })
);

const ConsciousnessPage = React.lazy(() => 
  import('../pages/ConsciousnessPage').catch(err => {
    console.error('Failed to load ConsciousnessPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Consciousness Page: {err.message}</div> };
  })
);

const NeuralPage = React.lazy(() => 
  import('../pages/NeuralPage').catch(err => {
    console.error('Failed to load NeuralPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Neural Page: {err.message}</div> };
  })
);

const RadarPage = React.lazy(() => 
  import('../pages/RadarPage').catch(err => {
    console.error('Failed to load RadarPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Radar Page: {err.message}</div> };
  })
);

const ModulesPage = React.lazy(() => 
  import('../pages/ModulesPage').catch(err => {
    console.error('Failed to load ModulesPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Modules Page: {err.message}</div> };
  })
);

const DemoPage = React.lazy(() => 
  import('../pages/DemoPage').catch(err => {
    console.error('Failed to load DemoPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Demo Page: {err.message}</div> };
  })
);

const ThreeTestPage = React.lazy(() => 
  import('../pages/ThreeTestPage').catch(err => {
    console.error('Failed to load ThreeTestPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Three Test Page: {err.message}</div> };
  })
);

const TalkToDawnPage = React.lazy(() => 
  import('../pages/TalkToDawnPage').catch(err => {
    console.error('Failed to load TalkToDawnPage:', err);
    return { default: () => <div style={{color: 'white', padding: '20px'}}>Error loading Talk to DAWN Page: {err.message}</div> };
  })
);

const LoadingSpinner = () => (
  <div className="loading-container" style={{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    background: '#000000',
    color: '#ffffff'
  }}>
    <motion.div
      style={{
        width: '50px',
        height: '50px',
        border: '3px solid rgba(0, 255, 136, 0.2)',
        borderTopColor: '#00ff88',
        borderRadius: '50%',
        marginBottom: '20px'
      }}
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    />
    <p>Initializing consciousness...</p>
  </div>
);

// Error Boundary Component
class ErrorBoundary extends React.Component<
  { children: React.ReactNode }, 
  { hasError: boolean; error?: Error }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Route Error Boundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          color: 'white',
          padding: '40px',
          textAlign: 'center',
          background: '#000000',
          minHeight: '100vh'
        }}>
          <h2 style={{ color: '#ff4444' }}>Something went wrong</h2>
          <p>Error: {this.state.error?.message}</p>
          <button 
            onClick={() => this.setState({ hasError: false })}
            style={{
              padding: '10px 20px',
              background: '#00ff88',
              color: '#000000',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export const AppRoutes: React.FC = () => {
  return (
    <ErrorBoundary>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<OptimizedDashboardPage />} />
          <Route path="/unified" element={<UnifiedHomePage />} />
          <Route path="/legacy" element={<HomePage />} />
          <Route path="/consciousness" element={<ConsciousnessPage />} />
          <Route path="/neural" element={<NeuralPage />} />
          <Route path="/radar" element={<RadarPage />} />
          <Route path="/modules" element={<ModulesPage />} />
          <Route path="/demo" element={<DemoPage />} />
          <Route path="/test-three" element={<ThreeTestPage />} />
          <Route path="/talk" element={<TalkToDawnPage />} />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}; 