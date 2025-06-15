import React, { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import '../styles/loader.css';

// Lazy load components to avoid circular dependencies
const HomePage = lazy(() => import('../pages/HomePage'));
const ConsciousnessPage = lazy(() => import('../pages/ConsciousnessPage'));
const NeuralPage = lazy(() => import('../pages/NeuralPage'));
const ModulesPage = lazy(() => import('../pages/ModulesPage'));
const DemoPage = lazy(() => import('../pages/DemoPage'));

// Loading component
const PageLoader = () => (
  <div className="page-loader">
    <div className="loader-spinner">
      <div className="quantum-loader">
        <div className="quantum-particle"></div>
        <div className="quantum-particle"></div>
        <div className="quantum-particle"></div>
      </div>
      <p>Initializing consciousness...</p>
    </div>
  </div>
);

export const AppRoutes: React.FC = () => {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/consciousness" element={<ConsciousnessPage />} />
        <Route path="/neural" element={<NeuralPage />} />
        <Route path="/modules" element={<ModulesPage />} />
        <Route path="/demo" element={<DemoPage />} />
        <Route path="*" element={<HomePage />} /> {/* Fallback */}
      </Routes>
    </Suspense>
  );
}; 