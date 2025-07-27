import React, { useState } from 'react';
import { Tabs, TabId } from './components/Tabs';
import { DashboardPanel } from './components/DashboardPanel';
import { VoicePanel } from './components/VoicePanel';
import { VisualProcessesPanel } from './components/VisualProcessesPanel';
import './App.css';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('dashboard');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPanel />;
      case 'voice':
        return <VoicePanel />;
      case 'visual':
        return <VisualProcessesPanel />;
      default:
        return <DashboardPanel />;
    }
  };

  return (
    <div className="dawn-app">
      <Tabs activeTab={activeTab} onTabChange={setActiveTab}>
        {renderTabContent()}
      </Tabs>
    </div>
  );
};

export default App;