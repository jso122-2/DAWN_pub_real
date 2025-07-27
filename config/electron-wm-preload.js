const { contextBridge, ipcRenderer } = require('electron');

// Extend existing electronAPI or create new one
const wmAPI = {
  detectWM: () => ipcRenderer.invoke('wm:detect'),
  checkProcess: () => ipcRenderer.invoke('wm:checkProcess'),
  applyWMConstraints: (windowId, constraints) => 
    ipcRenderer.invoke('wm:applyConstraints', windowId, constraints),
  registerPanel: (panelId, options) =>
    ipcRenderer.invoke('wm:registerPanel', panelId, options),
};

// Expose to renderer
if (window.electronAPI) {
  Object.assign(window.electronAPI, wmAPI);
} else {
  contextBridge.exposeInMainWorld('electronAPI', wmAPI);
} 