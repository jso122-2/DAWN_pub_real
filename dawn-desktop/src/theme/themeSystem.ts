// Theme definitions
export type ThemeName = 'neural' | 'void' | 'plasma' | 'entropy';

export interface Theme {
  name: ThemeName;
  displayName: string;
  variables: Record<string, string>;
  dynamic?: (context: { entropy?: number }) => Record<string, string>;
}

const themes: Record<ThemeName, Theme> = {
  neural: {
    name: 'neural',
    displayName: 'Neural',
    variables: {
      '--color-bg': '#0a0f1b',
      '--color-fg': '#e0eaff',
      '--color-accent': '#a78bfa',
      '--color-cyan': '#06b6d4',
      '--color-purple': '#a78bfa',
      '--color-glow': 'rgba(39, 246, 255, 0.4)',
      '--color-border': '#3b82f6',
    },
  },
  void: {
    name: 'void',
    displayName: 'Void',
    variables: {
      '--color-bg': '#000000',
      '--color-fg': '#ffffff',
      '--color-accent': '#ffffff',
      '--color-cyan': '#ffffff',
      '--color-purple': '#ffffff',
      '--color-glow': 'rgba(255,255,255,0.1)',
      '--color-border': '#ffffff',
    },
  },
  plasma: {
    name: 'plasma',
    displayName: 'Plasma',
    variables: {
      '--color-bg': '#0f0026',
      '--color-fg': '#fff600',
      '--color-accent': '#ff00ea',
      '--color-cyan': '#00fff7',
      '--color-purple': '#ff00ea',
      '--color-glow': 'rgba(255, 0, 234, 0.4)',
      '--color-border': '#fff600',
    },
  },
  entropy: {
    name: 'entropy',
    displayName: 'Entropy',
    variables: {
      '--color-bg': '#1a1a1a',
      '--color-fg': '#e0eaff',
      '--color-accent': '#ff9800',
      '--color-cyan': '#06b6d4',
      '--color-purple': '#a78bfa',
      '--color-glow': 'rgba(255, 152, 0, 0.3)',
      '--color-border': '#ff9800',
    },
    dynamic: ({ entropy = 0 }) => {
      // Shift accent color from blue (low) to red (high)
      const hue = 200 - (entropy * 2); // 200 (blue) to 0 (red)
      return {
        '--color-accent': `hsl(${hue}, 100%, 50%)`,
        '--color-glow': `hsla(${hue}, 100%, 60%, 0.4)`
      };
    },
  },
};

let currentTheme: ThemeName = 'neural';
let entropyValue = 0;
const componentOverrides = new Map<string, ThemeName>();

function setTheme(theme: ThemeName, options?: { smooth?: boolean }) {
  currentTheme = theme;
  applyTheme(theme, { entropy: entropyValue, smooth: options?.smooth });
}

function getTheme(): ThemeName {
  return currentTheme;
}

function setEntropy(entropy: number) {
  entropyValue = entropy;
  if (currentTheme === 'entropy') {
    applyTheme('entropy', { entropy });
  }
}

function applyTheme(theme: ThemeName, opts?: { entropy?: number; smooth?: boolean }) {
  const themeObj = themes[theme];
  const root = document.documentElement;
  if (opts?.smooth) {
    root.style.transition = 'background 0.5s, color 0.5s, border-color 0.5s, box-shadow 0.5s';
  } else {
    root.style.transition = '';
  }
  // Set static variables
  Object.entries(themeObj.variables).forEach(([key, value]) => {
    root.style.setProperty(key, value);
  });
  // Set dynamic variables
  if (themeObj.dynamic) {
    const dynamicVars = themeObj.dynamic({ entropy: opts?.entropy });
    Object.entries(dynamicVars).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
  }
}

function registerComponentOverride(componentId: string, theme: ThemeName) {
  componentOverrides.set(componentId, theme);
}

function unregisterComponentOverride(componentId: string) {
  componentOverrides.delete(componentId);
}

function getComponentTheme(componentId: string): ThemeName {
  return componentOverrides.get(componentId) || currentTheme;
}

// Time-based auto-switching
let autoSwitchInterval: any = null;
function startAutoSwitch(intervalMs: number = 60000) {
  if (autoSwitchInterval) clearInterval(autoSwitchInterval);
  autoSwitchInterval = setInterval(() => {
    const hour = new Date().getHours();
    if (hour >= 22 || hour < 6) setTheme('void', { smooth: true });
    else if (hour >= 6 && hour < 12) setTheme('neural', { smooth: true });
    else if (hour >= 12 && hour < 18) setTheme('plasma', { smooth: true });
    else setTheme('entropy', { smooth: true });
  }, intervalMs);
}
function stopAutoSwitch() {
  if (autoSwitchInterval) clearInterval(autoSwitchInterval);
}

export {
  themes,
  setTheme,
  getTheme,
  setEntropy,
  registerComponentOverride,
  unregisterComponentOverride,
  getComponentTheme,
  startAutoSwitch,
  stopAutoSwitch,
}; 