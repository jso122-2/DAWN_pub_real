import React from 'react';
import { useTilingPanel, useTilingAwareUI } from './uiMode';

const ExamplePanel: React.FC = () => {
  const { isEnabled, isLocked, toggle, toggleLock, wmType, recommendations } = useTilingAwareUI();
  
  const panelProps = useTilingPanel('example-panel', {
    preferredWidth: 600,
    preferredHeight: 400,
    canResize: true,
    canFloat: true,
  });

  return (
    <div className={`panel ${panelProps.className}`} style={panelProps.style}>
      <div className="panel-header">
        <h3>Tiling-Aware Panel</h3>
        <div className="controls">
          <button onClick={toggle}>
            {isEnabled ? 'Disable' : 'Enable'} Tiling Mode
          </button>
          <button onClick={toggleLock} disabled={!isEnabled}>
            {isLocked ? 'Unlock' : 'Lock'} Panels
          </button>
        </div>
      </div>
      
      <div className="panel-content">
        <p>Window Manager: <strong>{wmType}</strong></p>
        <p>Tiling Mode: <strong>{isEnabled ? 'Enabled' : 'Disabled'}</strong></p>
        <p>Panels: <strong>{isLocked ? 'Locked' : 'Floating'}</strong></p>
        
        {wmType !== 'none' && recommendations.commands && (
          <div className="wm-tips">
            <h4>WM Configuration Tips:</h4>
            <pre>{recommendations.commands.join('\n')}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExamplePanel; 