import create from 'zustand';
import { persist } from 'zustand/middleware';

export interface ModuleConfig {
  id: string;
  type: string;
  title: string;
  category: string;
  size: string;
  [key: string]: any;
}

export interface ModulePosition {
  x: number;
  y: number;
}

export interface Connection {
  from: string;
  to: string;
  type?: string;
}

interface ModuleStoreState {
  modules: Record<string, ModuleConfig>;
  positions: Record<string, ModulePosition>;
  connections: Connection[];
  spawnModule: (config: ModuleConfig, pos?: ModulePosition) => void;
  destroyModule: (id: string) => void;
  connectModules: (from: string, to: string, type?: string) => void;
  disconnectModules: (from: string, to: string) => void;
  setPosition: (id: string, pos: ModulePosition) => void;
  activeConnections: () => Record<string, string[]>;
}

export const useModuleStore = create<ModuleStoreState>()(
  persist(
    (set, get) => ({
      modules: {},
      positions: {},
      connections: [],
      spawnModule: (config, pos) => set(state => ({
        modules: { ...state.modules, [config.id]: config },
        positions: { ...state.positions, [config.id]: pos || { x: 100, y: 100 } },
      })),
      destroyModule: (id) => set(state => {
        const { [id]: _, ...restModules } = state.modules;
        const { [id]: __, ...restPositions } = state.positions;
        return {
          modules: restModules,
          positions: restPositions,
          connections: state.connections.filter(c => c.from !== id && c.to !== id),
        };
      }),
      connectModules: (from, to, type) => set(state => ({
        connections: [...state.connections, { from, to, type }],
      })),
      disconnectModules: (from, to) => set(state => ({
        connections: state.connections.filter(c => !(c.from === from && c.to === to)),
      })),
      setPosition: (id, pos) => set(state => ({
        positions: { ...state.positions, [id]: pos },
      })),
      activeConnections: () => {
        const map: Record<string, string[]> = {};
        get().connections.forEach(c => {
          if (!map[c.from]) map[c.from] = [];
          map[c.from].push(c.to);
        });
        return map;
      },
    }),
    {
      name: 'dawn-module-layout',
      partialize: (state) => ({
        modules: state.modules,
        positions: state.positions,
        connections: state.connections,
      }),
    }
  )
); 