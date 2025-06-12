import React, { useEffect, useState } from 'react';
import {
  plugins,
  loadPlugin,
  unloadPlugin,
  examplePluginManifest,
  PluginManifest,
} from '../plugins/pluginSystem';

const PluginManager: React.FC = () => {
  const [pluginList, setPluginList] = useState<typeof plugins>([]);
  const [panels, setPanels] = useState<{ name: string; iframe: HTMLIFrameElement }[]>([]);

  useEffect(() => {
    setPluginList([...plugins]);
    // Load example plugin on mount (for demo)
    if (!plugins.find(p => p.manifest.name === examplePluginManifest.name)) {
      loadPlugin(examplePluginManifest, (plugin) => {
        setPluginList([...plugins]);
        if (plugin.manifest.permissions?.includes('panel')) {
          setPanels(panels => [...panels, { name: plugin.manifest.name, iframe: plugin.iframe }]);
          plugin.iframe.style.display = 'block';
          plugin.iframe.style.position = 'fixed';
          plugin.iframe.style.bottom = '24px';
          plugin.iframe.style.right = '24px';
          plugin.iframe.style.width = '400px';
          plugin.iframe.style.height = '300px';
          plugin.iframe.style.zIndex = '999';
          plugin.iframe.style.border = '2px solid #3b82f6';
          plugin.iframe.style.borderRadius = '12px';
          plugin.iframe.style.background = 'rgba(10,15,27,0.95)';
          plugin.iframe.style.boxShadow = '0 4px 32px rgba(0,0,0,0.25)';
        }
      });
    }
    // Cleanup on unmount
    return () => {
      pluginList.forEach(p => unloadPlugin(p.manifest.name));
    };
    // eslint-disable-next-line
  }, []);

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 24,
        left: 24,
        zIndex: 1001,
        background: 'var(--color-bg, #18181b)',
        color: 'var(--color-fg, #e0eaff)',
        borderRadius: 16,
        boxShadow: '0 4px 32px rgba(0,0,0,0.25)',
        border: '1px solid var(--color-border, #3b82f6)',
        padding: 20,
        minWidth: 260,
        minHeight: 80,
      }}
    >
      <h3 style={{ margin: 0, marginBottom: 12 }}>🔌 Plugin Manager</h3>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {pluginList.map(plugin => (
          <li key={plugin.manifest.name} style={{ marginBottom: 10 }}>
            <b>{plugin.manifest.name}</b> <span style={{ fontSize: 12, color: '#a78bfa' }}>v{plugin.manifest.version}</span>
            <div style={{ fontSize: 12, color: '#9ca3af' }}>{plugin.manifest.description}</div>
            <div style={{ fontSize: 11, color: '#3b82f6' }}>Permissions: {plugin.manifest.permissions?.join(', ') || 'none'}</div>
            <button
              style={{
                marginTop: 4,
                padding: '4px 10px',
                borderRadius: 8,
                border: 'none',
                background: '#3b82f6',
                color: '#fff',
                cursor: 'pointer',
                fontSize: 12,
              }}
              onClick={() => {
                unloadPlugin(plugin.manifest.name);
                setPluginList([...plugins]);
              }}
            >Unload</button>
          </li>
        ))}
      </ul>
      {/* UI injection: plugin panels (iframes) are already injected in the DOM if permission is granted */}
      {panels.length > 0 && (
        <div style={{ marginTop: 16, fontSize: 13, color: '#a78bfa' }}>
          <b>Custom Panels:</b> {panels.map(p => p.name).join(', ')}
        </div>
      )}
    </div>
  );
};

export default PluginManager; 