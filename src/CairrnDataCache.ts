/**
 * CairrnDataCache.ts
 * 
 * A symbolic state caching layer inspired by Cairrn architecture.
 * Stores consciousness states as "memory stones" that can be 
 * efficiently retrieved and pattern-matched.
 */

interface ConsciousnessState {
    tick: number;
    scup: number;
    entropy: number;
    mood: string;
    heat: number;
    timestamp: number;
  }
  
  interface CachedGlyph {
    state: ConsciousnessState;
    symbol: string; // Compressed symbolic representation
    patterns: string[]; // Detected patterns at this state
    edges: Map<string, number>; // Connections to other states
    weight: number; // Importance/frequency weight
  }
  
  interface CacheMetrics {
    hits: number;
    misses: number;
    evictions: number;
    compressionRatio: number;
  }
  
  // Simple data cache for CAIRRN system
  interface CacheEntry {
    data: any;
    timestamp: number;
    ttl: number;
  }
  
  class CairrnDataCache {
    private cache = new Map<string, CacheEntry>();
    private defaultTTL = 5000; // 5 seconds
  
    set(key: string, data: any, ttl?: number): void {
      this.cache.set(key, {
        data,
        timestamp: Date.now(),
        ttl: ttl || this.defaultTTL
      });
    }
  
    get(key: string): any {
      const entry = this.cache.get(key);
      if (!entry) return null;
  
      const now = Date.now();
      if (now - entry.timestamp > entry.ttl) {
        this.cache.delete(key);
        return null;
      }
  
      return entry.data;
    }
  
    has(key: string): boolean {
      return this.get(key) !== null;
    }
  
    clear(): void {
      this.cache.clear();
    }
  
      size(): number {
    return this.cache.size;
  }

  // Legacy method for compatibility
  store(data: any, key?: string): string {
    const cacheKey = key || `state_${Date.now()}`;
    this.set(cacheKey, data);
    return cacheKey;
  }
}

export const cairrnCache = new CairrnDataCache();