import { StateCreator, StoreMutatorIdentifier } from 'zustand';

// Types for state persistence system
interface PersistenceConfig {
  name: string;
  version?: number;
  serialize?: (state: any) => string;
  deserialize?: (str: string) => any;
  partialize?: (state: any) => any;
  onRehydrateStorage?: (state: any) => ((state?: any, error?: Error) => void) | void;
  skipHydration?: boolean;
  merge?: (persistedState: any, currentState: any) => any;
}

interface StateHistory<T = any> {
  state: T;
  timestamp: number;
  action?: string;
}

interface PersistedStore {
  state: any;
  version: number;
  history: StateHistory[];
  lastSaved: number;
}

interface CrossTabMessage {
  type: 'STATE_UPDATE' | 'HISTORY_CHANGE' | 'EXPORT_REQUEST' | 'IMPORT_COMPLETE';
  storeName: string;
  data: any;
  timestamp: number;
}

// Encryption utilities using Web Crypto API
class StateEncryption {
  private static async getKey(password: string): Promise<CryptoKey> {
    const encoder = new TextEncoder();
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      encoder.encode(password),
      { name: 'PBKDF2' },
      false,
      ['deriveKey']
    );

    return crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: encoder.encode('dawn-state-salt-2024'),
        iterations: 100000,
        hash: 'SHA-256',
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt']
    );
  }

  static async encrypt(data: string, password: string): Promise<string> {
    const key = await this.getKey(password);
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(data);
    const iv = crypto.getRandomValues(new Uint8Array(12));

    const encrypted = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      dataBuffer
    );

    const result = new Uint8Array(iv.length + encrypted.byteLength);
    result.set(iv);
    result.set(new Uint8Array(encrypted), iv.length);

    return btoa(String.fromCharCode(...result));
  }

  static async decrypt(encryptedData: string, password: string): Promise<string> {
    const key = await this.getKey(password);
    const data = new Uint8Array(
      atob(encryptedData)
        .split('')
        .map(char => char.charCodeAt(0))
    );

    const iv = data.slice(0, 12);
    const encrypted = data.slice(12);

    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      key,
      encrypted
    );

    return new TextDecoder().decode(decrypted);
  }
}

// IndexedDB wrapper
class IndexedDBStorage {
  private dbName = 'dawn-state-persistence';
  private version = 1;
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        // Create stores object store
        if (!db.objectStoreNames.contains('stores')) {
          db.createObjectStore('stores', { keyPath: 'name' });
        }
        
        // Create exports object store
        if (!db.objectStoreNames.contains('exports')) {
          const exportStore = db.createObjectStore('exports', { 
            keyPath: 'id',
            autoIncrement: true 
          });
          exportStore.createIndex('timestamp', 'timestamp');
        }
      };
    });
  }

  async get(storeName: string): Promise<PersistedStore | null> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['stores'], 'readonly');
      const store = transaction.objectStore('stores');
      const request = store.get(storeName);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result || null);
    });
  }

  async set(storeName: string, data: PersistedStore): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['stores'], 'readwrite');
      const store = transaction.objectStore('stores');
      const request = store.put({ name: storeName, ...data });

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async delete(storeName: string): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['stores'], 'readwrite');
      const store = transaction.objectStore('stores');
      const request = store.delete(storeName);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async saveExport(data: any): Promise<number> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['exports'], 'readwrite');
      const store = transaction.objectStore('exports');
      const request = store.add({
        ...data,
        timestamp: Date.now()
      });

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result as number);
    });
  }

  async getExports(limit = 50): Promise<any[]> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['exports'], 'readonly');
      const store = transaction.objectStore('exports');
      const index = store.index('timestamp');
      const request = index.openCursor(null, 'prev');
      
      const results: any[] = [];
      let count = 0;

      request.onerror = () => reject(request.error);
      request.onsuccess = (event) => {
        const cursor = (event.target as IDBRequest).result;
        if (cursor && count < limit) {
          results.push(cursor.value);
          count++;
          cursor.continue();
        } else {
          resolve(results);
        }
      };
    });
  }
}

// Main state persistence manager
class StatePersistenceManager {
  private storage = new IndexedDBStorage();
  private broadcastChannel: BroadcastChannel;
  private registeredStores = new Map<string, any>();
  private saveTimers = new Map<string, NodeJS.Timeout>();
  private historyLimit = 50;
  private saveDelay = 2000; // 2 seconds

  constructor() {
    this.broadcastChannel = new BroadcastChannel('dawn-state-sync');
    this.broadcastChannel.addEventListener('message', this.handleCrossTabMessage.bind(this));
    this.storage.init();
  }

  // Register a Zustand store for persistence
  registerStore<T>(
    storeName: string,
    store: any,
    config: Partial<PersistenceConfig> = {}
  ): void {
    const fullConfig: PersistenceConfig = {
      name: storeName,
      version: 1,
      serialize: JSON.stringify,
      deserialize: JSON.parse,
      partialize: (state) => state,
      merge: (persisted, current) => ({ ...current, ...persisted }),
      ...config
    };

    this.registeredStores.set(storeName, { store, config: fullConfig });

    // Subscribe to store changes
    store.subscribe((state: T, prevState: T) => {
      this.debouncedSave(storeName, state, prevState);
    });

    // Load initial state
    this.loadState(storeName);
  }

  // Debounced save to prevent excessive writes
  private debouncedSave<T>(storeName: string, state: T, prevState: T): void {
    const existingTimer = this.saveTimers.get(storeName);
    if (existingTimer) {
      clearTimeout(existingTimer);
    }

    const timer = setTimeout(async () => {
      await this.saveState(storeName, state, prevState);
      this.saveTimers.delete(storeName);
    }, this.saveDelay);

    this.saveTimers.set(storeName, timer);
  }

  // Save state to IndexedDB
  private async saveState<T>(storeName: string, state: T, prevState: T): Promise<void> {
    try {
      const storeInfo = this.registeredStores.get(storeName);
      if (!storeInfo) return;

      const { config } = storeInfo;
      const partializedState = config.partialize ? config.partialize(state) : state;
      const serializedState = config.serialize!(partializedState);

      // Get existing data or create new
      let persistedData = await this.storage.get(storeName);
      if (!persistedData) {
        persistedData = {
          state: serializedState,
          version: config.version!,
          history: [],
          lastSaved: Date.now()
        };
      }

      // Add to history
      const historyEntry: StateHistory = {
        state: serializedState,
        timestamp: Date.now(),
        action: this.detectAction(state, prevState)
      };

      persistedData.history.push(historyEntry);
      
      // Limit history size
      if (persistedData.history.length > this.historyLimit) {
        persistedData.history = persistedData.history.slice(-this.historyLimit);
      }

      // Update current state
      persistedData.state = serializedState;
      persistedData.lastSaved = Date.now();

      await this.storage.set(storeName, persistedData);

      // Broadcast to other tabs
      this.broadcastChange(storeName, partializedState);

    } catch (error) {
      console.error(`Failed to save state for ${storeName}:`, error);
    }
  }

  // Load state from IndexedDB
  private async loadState(storeName: string): Promise<void> {
    try {
      const storeInfo = this.registeredStores.get(storeName);
      if (!storeInfo) return;

      const { store, config } = storeInfo;
      const persistedData = await this.storage.get(storeName);

      if (!persistedData) return;

      // Version migration check
      if (persistedData.version !== config.version) {
        console.warn(`Version mismatch for ${storeName}. Expected ${config.version}, got ${persistedData.version}`);
        return;
      }

      const deserializedState = config.deserialize!(persistedData.state);
      const currentState = store.getState();
      const mergedState = config.merge!(deserializedState, currentState);

      // Apply state
      store.setState(mergedState, false);

      // Call rehydration callback
      if (config.onRehydrateStorage) {
        const callback = config.onRehydrateStorage(deserializedState);
        if (callback) {
          callback(mergedState);
        }
      }

    } catch (error) {
      console.error(`Failed to load state for ${storeName}:`, error);
      if (this.registeredStores.get(storeName)?.config.onRehydrateStorage) {
        const callback = this.registeredStores.get(storeName)!.config.onRehydrateStorage!(null);
        if (callback) callback(null, error as Error);
      }
    }
  }

  // Detect what action caused the state change
  private detectAction<T>(newState: T, prevState: T): string {
    // Simple heuristic to detect action type
    const newKeys = Object.keys(newState as any);
    const changedKeys = newKeys.filter(key => 
      (newState as any)[key] !== (prevState as any)[key]
    );

    if (changedKeys.length === 0) return 'unknown';
    if (changedKeys.length === 1) return `update_${changedKeys[0]}`;
    return `batch_update_${changedKeys.length}_fields`;
  }

  // Cross-tab synchronization
  private broadcastChange(storeName: string, state: any): void {
    const message: CrossTabMessage = {
      type: 'STATE_UPDATE',
      storeName,
      data: state,
      timestamp: Date.now()
    };

    this.broadcastChannel.postMessage(message);
  }

  private handleCrossTabMessage(event: MessageEvent<CrossTabMessage>): void {
    const { type, storeName, data, timestamp } = event.data;

    switch (type) {
      case 'STATE_UPDATE':
        this.handleRemoteStateUpdate(storeName, data, timestamp);
        break;
      case 'HISTORY_CHANGE':
        // Handle history synchronization if needed
        break;
      case 'EXPORT_REQUEST':
        // Handle export requests from other tabs
        break;
      case 'IMPORT_COMPLETE':
        // Reload state after import
        this.loadState(storeName);
        break;
    }
  }

  private handleRemoteStateUpdate(storeName: string, state: any, timestamp: number): void {
    const storeInfo = this.registeredStores.get(storeName);
    if (!storeInfo) return;

    const { store, config } = storeInfo;
    const currentState = store.getState();
    const mergedState = config.merge!(state, currentState);

    // Only apply if the remote state is newer
    const lastSave = this.saveTimers.get(storeName);
    if (!lastSave && timestamp > Date.now() - 5000) { // Within 5 seconds
      store.setState(mergedState, false);
    }
  }

  // Undo/Redo functionality
  async undo(storeName: string): Promise<boolean> {
    try {
      const persistedData = await this.storage.get(storeName);
      if (!persistedData || persistedData.history.length < 2) {
        return false;
      }

      // Get previous state (second to last)
      const prevStateEntry = persistedData.history[persistedData.history.length - 2];
      const storeInfo = this.registeredStores.get(storeName);
      
      if (!storeInfo) return false;

      const { store, config } = storeInfo;
      const deserializedState = config.deserialize!(prevStateEntry.state);
      const currentState = store.getState();
      const mergedState = config.merge!(deserializedState, currentState);

      store.setState(mergedState, false);

      // Remove last entry from history
      persistedData.history.pop();
      await this.storage.set(storeName, persistedData);

      return true;
    } catch (error) {
      console.error(`Failed to undo ${storeName}:`, error);
      return false;
    }
  }

  async redo(storeName: string): Promise<boolean> {
    // Redo functionality would require additional state tracking
    // For now, return false as it's complex to implement without forward history
    return false;
  }

  // Get state history
  async getHistory(storeName: string): Promise<StateHistory[]> {
    try {
      const persistedData = await this.storage.get(storeName);
      return persistedData?.history || [];
    } catch (error) {
      console.error(`Failed to get history for ${storeName}:`, error);
      return [];
    }
  }

  // Export functionality
  async exportState(
    storeNames?: string[], 
    password?: string, 
    includeHistory = false
  ): Promise<string> {
    try {
      const stores = storeNames || Array.from(this.registeredStores.keys());
      const exportData: Record<string, any> = {};

      for (const storeName of stores) {
        const persistedData = await this.storage.get(storeName);
        if (persistedData) {
          exportData[storeName] = {
            state: persistedData.state,
            version: persistedData.version,
            lastSaved: persistedData.lastSaved,
            ...(includeHistory && { history: persistedData.history })
          };
        }
      }

      const exportString = JSON.stringify({
        timestamp: Date.now(),
        version: 1,
        stores: exportData
      }, null, 2);

      // Save export to IndexedDB
      await this.storage.saveExport({
        data: exportString,
        encrypted: !!password,
        storeNames: stores
      });

      if (password) {
        return StateEncryption.encrypt(exportString, password);
      }

      return exportString;
    } catch (error) {
      console.error('Failed to export state:', error);
      throw error;
    }
  }

  // Import functionality
  async importState(
    importData: string, 
    password?: string, 
    merge = true
  ): Promise<void> {
    try {
      let dataString = importData;
      
      if (password) {
        dataString = await StateEncryption.decrypt(importData, password);
      }

      const parsed = JSON.parse(dataString);
      
      if (parsed.version !== 1) {
        throw new Error(`Unsupported export version: ${parsed.version}`);
      }

      for (const [storeName, storeData] of Object.entries(parsed.stores)) {
        const storeInfo = this.registeredStores.get(storeName);
        if (!storeInfo) {
          console.warn(`Store ${storeName} not registered, skipping import`);
          continue;
        }

        const { store, config } = storeInfo;
        const data = storeData as any;

        // Version check
        if (data.version !== config.version) {
          console.warn(`Version mismatch for ${storeName} during import`);
          continue;
        }

        const deserializedState = config.deserialize!(data.state);
        
        if (merge) {
          const currentState = store.getState();
          const mergedState = config.merge!(deserializedState, currentState);
          store.setState(mergedState, false);
        } else {
          store.setState(deserializedState, false);
        }

        // Update persisted data
        const persistedData: PersistedStore = {
          state: data.state,
          version: data.version,
          history: data.history || [],
          lastSaved: Date.now()
        };

        await this.storage.set(storeName, persistedData);
      }

      // Broadcast import completion
      this.broadcastChannel.postMessage({
        type: 'IMPORT_COMPLETE',
        storeName: 'all',
        data: null,
        timestamp: Date.now()
      });

    } catch (error) {
      console.error('Failed to import state:', error);
      throw error;
    }
  }

  // Clear all persisted data
  async clearAll(): Promise<void> {
    try {
      for (const storeName of this.registeredStores.keys()) {
        await this.storage.delete(storeName);
      }
    } catch (error) {
      console.error('Failed to clear all state:', error);
      throw error;
    }
  }

  // Get recent exports
  async getRecentExports(limit = 10): Promise<any[]> {
    return this.storage.getExports(limit);
  }

  // Cleanup resources
  destroy(): void {
    this.broadcastChannel.close();
    for (const timer of this.saveTimers.values()) {
      clearTimeout(timer);
    }
    this.saveTimers.clear();
    this.registeredStores.clear();
  }
}

// Global persistence manager instance
export const persistenceManager = new StatePersistenceManager();

// Utility function to create persistent store
export function createPersistentStore<T>(
  storeName: string,
  createState: StateCreator<T, [], [], T>,
  config?: Partial<PersistenceConfig>
) {
  const store = createState;
  persistenceManager.registerStore(storeName, store, config);
  return store;
}

// Hooks for React components
export function usePersistenceActions() {
  return {
    undo: (storeName: string) => persistenceManager.undo(storeName),
    redo: (storeName: string) => persistenceManager.redo(storeName),
    getHistory: (storeName: string) => persistenceManager.getHistory(storeName),
    exportState: (storeNames?: string[], password?: string) => 
      persistenceManager.exportState(storeNames, password),
    importState: (data: string, password?: string, merge?: boolean) =>
      persistenceManager.importState(data, password, merge),
    clearAll: () => persistenceManager.clearAll(),
    getRecentExports: () => persistenceManager.getRecentExports()
  };
}

// Middleware for existing stores
export function withPersistence<T>(
  storeName: string,
  config?: Partial<PersistenceConfig>
) {
  return (createState: StateCreator<T, [], [], T>) => {
    const store = createState;
    persistenceManager.registerStore(storeName, store, config);
    return store;
  };
}

// Auto-register existing stores (call this in your app initialization)
export function initializePersistence() {
  // This would be called with your existing stores
  // Example usage shown in comments:
  
  // Register modulation store
  // persistenceManager.registerStore('modulation', useModulationStore);
  
  // Register memory store  
  // persistenceManager.registerStore('memory', useMemoryStore);
  
  // Register dashboard store
  // persistenceManager.registerStore('dashboard', useDashboardStore, {
  //   partialize: (state) => ({
  //     metrics: state.metrics,
  //     emotion: state.emotion,
  //     intensity: state.intensity
  //   })
  // });
  
  // Register metrics store
  // persistenceManager.registerStore('metrics', useMetricsStore);
  
  // Register UI mode store
  // persistenceManager.registerStore('uiMode', useUIModeStore);
  
  console.log('State persistence initialized');
}

export default persistenceManager;