// Example integration with window manager awareness for Linux

import React, { useEffect } from 'react';
import ModulationConsole from './ModulationConsole';

// Window manager integration for Linux
declare global {
  interface Window {
    wmAPI?: {
      setAlwaysOnTop: (value: boolean) => void;
      setSkipTaskbar: (value: boolean) => void;
    };
  }
}

const ModulationConsoleWithWM: React.FC = () => {
  useEffect(() => {
    // If running in Electron or similar with WM API
    if (window.wmAPI) {
      window.wmAPI.setAlwaysOnTop(true);
      window.wmAPI.setSkipTaskbar(true);
    }
  }, []);

  return <ModulationConsole />;
};

export default ModulationConsoleWithWM; 