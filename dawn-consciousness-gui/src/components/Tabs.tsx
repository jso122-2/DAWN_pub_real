import React, { useState } from 'react';
import './Tabs.css';

export type TabId = 'dashboard' | 'voice' | 'visual';

interface Tab {
  id: TabId;
  label: string;
  icon: string;
  description: string;
}

interface TabsProps {
  activeTab: TabId;
  onTabChange: (tabId: TabId) => void;
  children: React.ReactNode;
}

const tabs: Tab[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: '⚡',
    description: 'System vitals, mood, entropy, SCUP monitoring'
  },
  {
    id: 'voice', 
    label: 'Voice',
    icon: '🎙️',
    description: 'Speech composition, playback history, mood-based generation'
  },
  {
    id: 'visual',
    label: 'Visual Processes', 
    icon: '🔮',
    description: 'Memory graphs, rebloom flows, symbolic glyphs'
  }
];

export const Tabs: React.FC<TabsProps> = ({ activeTab, onTabChange, children }) => {
  return (
    <div className="dawn-tabs">
      {/* Tab Navigation */}
      <div className="tab-navigation">
        <div className="tab-header">
          <div className="dawn-logo">
            <span className="logo-icon">🌅</span>
            <span className="logo-text">DAWN</span>
            <span className="logo-version">v1.3.0a</span>
          </div>
        </div>
        
        <div className="tab-buttons">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => onTabChange(tab.id)}
              title={tab.description}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
              {activeTab === tab.id && <div className="active-indicator" />}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {children}
      </div>
    </div>
  );
}; 