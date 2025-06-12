# NeuroShell Setup Instructions

## For Electron:

1. Install dependencies:
```bash
npm install xterm xterm-addon-fit xterm-addon-web-links xterm-addon-search node-pty
```

2. Add the preload script to your Electron main process:
```javascript
// In your main.js
const { setupShellHandlers } = require('./components/shell/electron-shell-handler');

// Setup shell handlers
setupShellHandlers();

// Create window with preload
new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, 'components/shell/electron-preload.js'),
    nodeIntegration: false,
    contextIsolation: true
  }
});
```

3. For production Claude integration, replace the mock API in `claude-api-mock.ts` with actual Claude API calls.

## For Tauri:

1. Install dependencies:
```bash
npm install xterm xterm-addon-fit xterm-addon-web-links xterm-addon-search
```

2. Add shell commands to `tauri.conf.json`:
```json
{
  "tauri": {
    "allowlist": {
      "shell": {
        "all": true,
        "open": true
      }
    }
  }
}
```

3. Create a Tauri command for shell operations in your Rust backend.

## Integration:

1. Import the component:
```tsx
import NeuroShellOverlay from './components/shell/NeuroShellOverlay';
```

2. Add to your app layout:
```tsx
function App() {
  return (
    <div>
      {/* Your app content */}
      <NeuroShellOverlay />
    </div>
  );
}
```

## Keyboard Shortcuts:

- `Ctrl + \`` (backtick): Toggle shell visibility
- `Esc`: Hide shell
- Standard terminal shortcuts work within the shell

## Security Notes:

- The shell runs with full system privileges
- Commands from Claude are marked with risk levels
- All commands are logged to `logs/neuroshell.log`
- Consider sandboxing for production environments

## Customization:

- Modify the terminal theme in `NeuroShellOverlay.tsx`
- Add custom commands to the Claude mock API
- Adjust positioning and sizing in the component styles
- Configure logging preferences in the preload script 