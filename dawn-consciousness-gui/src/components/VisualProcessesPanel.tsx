import React, { useState } from 'react';
import { RebloomMapPanel } from './RebloomMapPanel';
import { SigilTracePanel } from './SigilTracePanel';
import { SymbolicGlyphPanel } from './SymbolicGlyphPanel';
import { ConsciousnessConstellation } from './ConsciousnessConstellation';
import GlyphFlashOverlay from './GlyphFlashOverlay';
import './VisualProcessesPanel.css';

// Tabbed Section Component for organizing visual processes
interface TabbedSectionProps {
  title: string;
  icon: string;
  tabs: Array<{
    id: string;
    label: string;
    content: React.ReactNode;
    icon?: string;
  }>;
}

const TabbedSection: React.FC<TabbedSectionProps> = ({ title, icon, tabs }) => {
  const [activeTab, setActiveTab] = useState(tabs[0]?.id || '');

  return (
    <div className="visual-tabbed-section">
      <div className="section-header">
        <div className="section-title">
          <span className="section-icon">{icon}</span>
          {title}
        </div>
        <div className="tab-switcher">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-switch ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.icon && <span className="tab-icon">{tab.icon}</span>}
              {tab.label}
            </button>
          ))}
        </div>
      </div>
      
      <div className="section-content">
        {tabs.find(tab => tab.id === activeTab)?.content}
      </div>
    </div>
  );
};

// Visual Process Panel Component
interface VisualPanelProps {
  title: string;
  children: React.ReactNode;
  icon?: string;
  className?: string;
  overlay?: React.ReactNode;
}

const VisualPanel: React.FC<VisualPanelProps> = ({ 
  title, 
  children, 
  icon, 
  className = '',
  overlay 
}) => {
  return (
    <div className={`visual-panel ${className}`}>
      <div className="panel-header">
        <div className="panel-title">
          {icon && <span className="panel-icon">{icon}</span>}
          {title}
        </div>
        <div className="live-indicator" title="Live visual processing active"></div>
      </div>
      <div className="panel-content">
        {children}
        {overlay}
      </div>
    </div>
  );
};

// Memory Flow Visualization Component
const MemoryFlowViz: React.FC = () => {
  const [flowMode, setFlowMode] = useState<'rebloom' | 'consolidation' | 'retrieval'>('rebloom');

  const flowModes = [
    { id: 'rebloom', label: 'Rebloom Flow', description: 'Memory reactivation patterns' },
    { id: 'consolidation', label: 'Consolidation', description: 'Memory strengthening processes' },
    { id: 'retrieval', label: 'Retrieval', description: 'Active memory recall patterns' }
  ];

  return (
    <div className="memory-flow-viz">
      <div className="flow-controls">
        <label>Flow Mode:</label>
        <div className="mode-selector">
          {flowModes.map(mode => (
            <button
              key={mode.id}
              className={`flow-mode-btn ${flowMode === mode.id ? 'active' : ''}`}
              onClick={() => setFlowMode(mode.id as any)}
              title={mode.description}
            >
              {mode.label}
            </button>
          ))}
        </div>
      </div>
      
      <div className="flow-display">
        <RebloomMapPanel />
      </div>
    </div>
  );
};

// Symbolic Processing Visualizer
const SymbolicProcessor: React.FC = () => {
  const [processingMode, setProcessingMode] = useState<'generation' | 'recognition' | 'evolution'>('generation');

  return (
    <div className="symbolic-processor">
      <div className="processor-controls">
        <div className="mode-tabs">
          <button 
            className={`mode-tab ${processingMode === 'generation' ? 'active' : ''}`}
            onClick={() => setProcessingMode('generation')}
          >
            🌱 Generation
          </button>
          <button 
            className={`mode-tab ${processingMode === 'recognition' ? 'active' : ''}`}
            onClick={() => setProcessingMode('recognition')}
          >
            🔍 Recognition
          </button>
          <button 
            className={`mode-tab ${processingMode === 'evolution' ? 'active' : ''}`}
            onClick={() => setProcessingMode('evolution')}
          >
            🧬 Evolution
          </button>
        </div>
      </div>

      <div className="processor-display">
        {processingMode === 'generation' && (
          <div style={{ position: 'relative' }}>
            <SymbolicGlyphPanel />
            <GlyphFlashOverlay />
          </div>
        )}
        {processingMode === 'recognition' && <SigilTracePanel />}
        {processingMode === 'evolution' && <ConsciousnessConstellation />}
      </div>
    </div>
  );
};

// Network Topology Visualizer
const NetworkTopology: React.FC = () => {
  const [viewMode, setViewMode] = useState<'constellation' | 'flows' | 'clusters'>('constellation');

  return (
    <div className="network-topology">
      <div className="topology-controls">
        <label>Network View:</label>
        <select 
          value={viewMode}
          onChange={(e) => setViewMode(e.target.value as any)}
          className="view-selector"
        >
          <option value="constellation">Consciousness Constellation</option>
          <option value="flows">Information Flows</option>
          <option value="clusters">Memory Clusters</option>
        </select>
      </div>
      
      <div className="topology-display">
        <ConsciousnessConstellation />
      </div>
    </div>
  );
};

export const VisualProcessesPanel: React.FC = () => {
  return (
    <div className="visual-container">
      <div className="visual-header">
        <h2>Visual Processes</h2>
        <p>Memory graphs, symbolic flows, rebloom patterns, and consciousness network visualization</p>
      </div>

      <div className="visual-grid">
        {/* Primary Row: Memory and Symbolic Processing */}
        <div className="visual-row primary-row">
          <TabbedSection
            title="Memory Dynamics"
            icon="🌸"
            tabs={[
              {
                id: 'rebloom',
                label: 'Rebloom Map',
                icon: '🌺',
                content: <MemoryFlowViz />
              },
              {
                id: 'topology',
                label: 'Network',
                icon: '🕸️',
                content: <NetworkTopology />
              }
            ]}
          />
          
          <TabbedSection
            title="Symbolic Processing"
            icon="✨"
            tabs={[
              {
                id: 'processor',
                label: 'Symbol Engine',
                icon: '⚡',
                content: <SymbolicProcessor />
              },
              {
                id: 'patterns',
                label: 'Pattern Flow',
                icon: '🌀',
                content: <SigilTracePanel />
              }
            ]}
          />
        </div>

        {/* Secondary Row: Individual Visualizers */}
        <div className="visual-row secondary-row">
          <VisualPanel 
            title="Consciousness Constellation" 
            icon="🌌"
            className="constellation-panel"
          >
            <ConsciousnessConstellation />
          </VisualPanel>
          
          <VisualPanel 
            title="Symbolic Glyphs" 
            icon="🔮"
            className="glyph-panel"
            overlay={<GlyphFlashOverlay />}
          >
            <SymbolicGlyphPanel />
          </VisualPanel>
          
          <VisualPanel 
            title="Sigil Traces" 
            icon="📜"
            className="sigil-panel"
          >
            <SigilTracePanel />
          </VisualPanel>
        </div>
      </div>
    </div>
  );
}; 