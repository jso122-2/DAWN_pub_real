const { contextBridge, ipcRenderer } = require('electron');
const path = require('path');
const fs = require('fs');

// Ensure log directory exists
const logDir = path.join(process.cwd(), 'logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const logPath = path.join(logDir, 'neuroshell.log');

contextBridge.exposeInMainWorld('shellAPI', {
  spawn: (shell) => ipcRenderer.invoke('shell:spawn', shell),
  write: (pid, data) => ipcRenderer.send('shell:write', pid, data),
  resize: (pid, cols, rows) => ipcRenderer.send('shell:resize', pid, cols, rows),
  kill: (pid) => ipcRenderer.send('shell:kill', pid),
  
  onData: (pid, callback) => {
    ipcRenderer.on(`shell:data:${pid}`, (event, data) => callback(data));
  },
  
  onExit: (pid, callback) => {
    ipcRenderer.on(`shell:exit:${pid}`, (event, code) => callback(code));
  },
  
  logToFile: (message) => {
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp} - ${message}\n`;
    fs.appendFileSync(logPath, logEntry);
  }
}); 