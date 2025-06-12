// Plugin Manifest Type
export interface PluginManifest {
  name: string;
  version: string;
  description?: string;
  permissions?: string[];
  entry: string; // URL or relative path to plugin iframe
}

export interface Plugin {
  manifest: PluginManifest;
  iframe: HTMLIFrameElement;
  loaded: boolean;
  hooks: Partial<PluginHooks>;
}

export interface PluginHooks {
  onSystemStart?: () => void;
  onEntropyChange?: (entropy: number) => void;
  onMemoryEvent?: (event: any) => void;
}

// Shared API (read-only state)
import { eventBus } from '../utils/eventBus';
import { getTheme } from '../theme/themeSystem';

const sharedAPI = {
  eventBus: {
    emit: eventBus.emit.bind(eventBus),
    on: eventBus.on.bind(eventBus),
    off: eventBus.off.bind(eventBus),
  },
  getTheme,
  getState: () => window.__DAWN_STATE__ || {}, // Expose global state if available
};

// Plugin registry
const plugins: Plugin[] = [];

// Load plugin
export function loadPlugin(manifest: PluginManifest, onReady?: (plugin: Plugin) => void) {
  const iframe = document.createElement('iframe');
  iframe.src = manifest.entry;
  iframe.sandbox.add('allow-scripts');
  iframe.style.display = 'none';
  iframe.onload = () => {
    // Send shared API to plugin
    iframe.contentWindow?.postMessage({ type: 'dawn:sharedAPI', api: sharedAPI }, '*');
    if (onReady) onReady(plugin);
    plugin.loaded = true;
    // Call onSystemStart if present
    plugin.hooks.onSystemStart?.();
  };
  document.body.appendChild(iframe);
  const plugin: Plugin = {
    manifest,
    iframe,
    loaded: false,
    hooks: {},
  };
  plugins.push(plugin);
  return plugin;
}

// Unload plugin
export function unloadPlugin(name: string) {
  const idx = plugins.findIndex(p => p.manifest.name === name);
  if (idx !== -1) {
    const plugin = plugins[idx];
    plugin.iframe.remove();
    plugins.splice(idx, 1);
  }
}

// Broadcast hook events
export function triggerHook<K extends keyof PluginHooks>(hook: K, ...args: Parameters<NonNullable<PluginHooks[K]>>) {
  plugins.forEach(plugin => {
    if (plugin.hooks[hook]) {
      try {
        (plugin.hooks[hook] as any)(...args);
      } catch (e) {
        console.warn(`Plugin ${plugin.manifest.name} hook error:`, e);
      }
    } else {
      // Forward to iframe
      plugin.iframe.contentWindow?.postMessage({ type: 'dawn:hook', hook, args }, '*');
    }
  });
}

// Hot-reload support (dev only)
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    plugins.forEach(plugin => {
      plugin.iframe.contentWindow?.postMessage({ type: 'dawn:hotReload' }, '*');
    });
  });
}

// Example plugin manifest
export const examplePluginManifest: PluginManifest = {
  name: 'EntropyVisualizer',
  version: '1.0.0',
  description: 'Custom entropy visualization panel',
  permissions: ['panel', 'entropy'],
  entry: '/plugins/entropy-visualizer/index.html',
};

export { plugins };

declare global {
  interface Window {
    __DAWN_STATE__?: any;
  }
} 