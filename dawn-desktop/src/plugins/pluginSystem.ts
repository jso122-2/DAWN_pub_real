export interface PluginManifest {
  name: string;
  version: string;
  description: string;
  permissions?: string[];
}

export interface Plugin {
  manifest: PluginManifest;
  iframe: HTMLIFrameElement;
}

export const plugins: Plugin[] = [];

export const loadPlugin = (manifest: PluginManifest, callback: (plugin: Plugin) => void) => {
  const iframe = document.createElement('iframe');
  iframe.src = manifest.name; // You'll need to implement actual plugin loading
  document.body.appendChild(iframe);
  
  const plugin: Plugin = { manifest, iframe };
  plugins.push(plugin);
  callback(plugin);
};

export const unloadPlugin = (name: string) => {
  const index = plugins.findIndex(p => p.manifest.name === name);
  if (index !== -1) {
    const plugin = plugins[index];
    plugin.iframe.remove();
    plugins.splice(index, 1);
  }
};

export const examplePluginManifest: PluginManifest = {
  name: 'Example Plugin',
  version: '1.0.0',
  description: 'A sample plugin',
  permissions: ['panel']
};
