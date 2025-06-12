const { ipcMain, BrowserWindow } = require('electron');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// X11 utilities for window management
let x11;
try {
  x11 = require('x11');
} catch (e) {
  console.log('x11 module not available, using fallback detection');
}

async function detectWindowManager() {
  try {
    // Method 1: Check running processes
    const { stdout } = await execAsync('ps aux | grep -E "i3|sway|bspwm|awesome|dwm|xmonad|qtile" | grep -v grep');
    const processes = stdout.toLowerCase();
    
    if (processes.includes('i3') && !processes.includes('sway')) return 'i3';
    if (processes.includes('sway')) return 'sway';
    if (processes.includes('bspwm')) return 'bspwm';
    if (processes.includes('awesome')) return 'awesome';
    if (processes.includes('dwm')) return 'dwm';
    if (processes.includes('xmonad')) return 'xmonad';
    if (processes.includes('qtile')) return 'qtile';
    
    // Method 2: Check X11 window properties
    if (x11) {
      // Implementation would query _NET_WM_NAME on root window
    }
    
    // Method 3: Check environment variables
    const wmEnv = process.env.XDG_CURRENT_DESKTOP || process.env.DESKTOP_SESSION || '';
    if (wmEnv.includes('i3')) return 'i3';
    if (wmEnv.includes('sway')) return 'sway';
    if (wmEnv.includes('bspwm')) return 'bspwm';
    
    return 'none';
  } catch (error) {
    console.error('Error detecting WM:', error);
    return 'none';
  }
}

function setupWMHandlers() {
  ipcMain.handle('wm:detect', detectWindowManager);
  
  ipcMain.handle('wm:checkProcess', async () => {
    try {
      const { stdout } = await execAsync('ps aux');
      return stdout;
    } catch (error) {
      return '';
    }
  });
  
  ipcMain.handle('wm:applyConstraints', (event, windowId, constraints) => {
    const window = BrowserWindow.fromId(windowId);
    if (!window) return;
    
    const { wmType, lockPanels, respectHints, constraints: sizeConstraints } = constraints;
    
    // Apply size constraints
    if (sizeConstraints) {
      window.setMinimumSize(sizeConstraints.minWidth, sizeConstraints.minHeight);
    }
    
    // WM-specific window properties
    switch (wmType) {
      case 'i3':
      case 'sway':
        // Set window class and instance for i3/sway rules
        if (process.platform === 'linux') {
          window.setTitle(`DAWN Panel - ${windowId}`);
        }
        break;
        
      case 'bspwm':
        // bspwm uses different window properties
        break;
    }
    
    // Lock/unlock window
    window.setMovable(!lockPanels);
    window.setResizable(!lockPanels);
  });
  
  ipcMain.handle('wm:registerPanel', (event, panelId, options) => {
    // Store panel registration for WM hints
    // This would integrate with your window creation logic
  });
}

module.exports = { setupWMHandlers }; 