// Example of how to integrate EntropyRingHUD into your main layout

import React from 'react';
import EntropyRingHUD from './EntropyRingHUD';

const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="relative min-h-screen">
      {/* Main content */}
      {children}
      
      {/* Entropy HUD overlay */}
      <EntropyRingHUD />
    </div>
  );
};

export default AppLayout; 