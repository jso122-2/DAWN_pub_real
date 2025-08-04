import React from 'react';
import './Tabs.css';

export type TabId = 'overview' | 'consciousness' | 'conversation' | 'visualizations' | 'systems';

interface TabsProps {
  activeTab: TabId;
  onTabChange: (tabId: TabId) => void;
  children: React.ReactNode;
}

export const Tabs: React.FC<TabsProps> = ({ activeTab, onTabChange, children }) => {
  const tabs = [
    { id: 'overview' as TabId, label: 'Overview', icon: '🧠' },
    { id: 'consciousness' as TabId, label: 'Consciousness', icon: '🌌' },
    { id: 'conversation' as TabId, label: 'Conversation', icon: '💬' },
    { id: 'visualizations' as TabId, label: 'Visualizations', icon: '🎨' },
    { id: 'systems' as TabId, label: 'Systems', icon: '⚙️' }
  ];

  return (
    <div className="tabs-container">
      <div className="tabs-header">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>
      <div className="tab-content">
        {children}
      </div>
    </div>
  );
}; 