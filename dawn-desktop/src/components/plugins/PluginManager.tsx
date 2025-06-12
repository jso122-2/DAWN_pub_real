import React, { useEffect, useState } from 'react';
import {
  plugins,
  loadPlugin,
  unloadPlugin,
  examplePluginManifest,
  PluginManifest,
  Plugin
} from '../plugins/pluginSystem';
import { motion, AnimatePresence } from 'framer-motion';

const PluginManager: React.FC = () => {
  const [pluginList, setPluginList] = useState<Plugin[]>([]);
  const [panels, setPanels] = useState<{ name: string; iframe: HTMLIFrameElement }[]>([]);

  useEffect(() => {
    setPluginList([...plugins]);
    // Load example plugin on mount (for demo)
    if (!plugins.find((p: Plugin) => p.manifest.name === examplePluginManifest.name)) {
      loadPlugin(examplePluginManifest, (plugin: Plugin) => {
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
      pluginList.forEach((p: Plugin) => unloadPlugin(p.manifest.name));
    };
    // eslint-disable-next-line
  }, []);

  return (
    <div
      className="glass fixed bottom-6 left-6 z-50 border border-purple-500/30 rounded-2xl shadow-glow-md p-6 min-w-[260px] min-h-[80px] max-w-xs w-full md:w-[340px] flex flex-col space-y-4 backdrop-blur-xl"
    >
      <h3 className="text-lg font-bold text-purple-300 mb-2">🔌 Plugin Manager</h3>
      <ul className="space-y-3">
        <AnimatePresence>
          {pluginList.map((plugin: Plugin) => (
            <motion.li
              key={plugin.manifest.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="bg-black/30 glass rounded-lg p-3 border border-purple-500/10 flex flex-col gap-1"
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-cyan-300">{plugin.manifest.name}</span>
                <span className="text-xs text-purple-400">v{plugin.manifest.version}</span>
              </div>
              <div className="text-xs text-gray-400 mb-1">{plugin.manifest.description}</div>
              <div className="text-xs text-cyan-400">Permissions: {plugin.manifest.permissions?.join(', ') || 'none'}</div>
              <button
                className="mt-2 px-3 py-1 rounded-lg bg-gradient-to-r from-purple-600 to-cyan-500 text-white font-semibold text-xs shadow-glow-sm hover:from-cyan-500 hover:to-purple-600 transition-colors"
                onClick={() => {
                  unloadPlugin(plugin.manifest.name);
                  setPluginList([...plugins]);
                }}
              >Unload</button>
            </motion.li>
          ))}
        </AnimatePresence>
      </ul>
      {/* UI injection: plugin panels (iframes) are already injected in the DOM if permission is granted */}
      {panels.length > 0 && (
        <div className="mt-2 text-xs text-purple-300">
          <b>Custom Panels:</b> {panels.map((p) => p.name).join(', ')}
        </div>
      )}
    </div>
  );
};

export default PluginManager; 