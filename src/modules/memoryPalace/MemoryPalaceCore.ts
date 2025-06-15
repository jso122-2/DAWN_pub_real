import { EventEmitter } from 'events';
import * as THREE from 'three';
import { 
  Memory, 
  MemoryPattern, 
  MemoryPalaceState,
  ConsolidationEvent,
  MemoryQuery,
  SpatialPosition,
  MemoryType,
  ConsolidationType,
  PatternType,
  MemorySector,
  EmotionalValence,
  MemoryAssociation,
  AssociationType,
  EmotionLabel
} from './types/memory.types';
import { memoryPalaceConfig } from './config/memoryPalace.config';

export class MemoryPalaceCore extends EventEmitter {
  private state: MemoryPalaceState;
  
  // Performance tracking
  private lastConsolidation = 0;
  private consolidationInterval = 1000; // ms
  private memoryIdCounter = 0;
  
  constructor() {
    super();
    
    this.state = this.initializeState();
    
    // Start consolidation loop
    this.startConsolidationLoop();
  }
  
  private initializeState(): MemoryPalaceState {
    return {
      memories: new Map(),
      patterns: new Map(),
      consolidationQueue: [],
      spatialIndex: {
        sectors: this.initializeSectors(),
        clusters: new Map(),
        connections: [],
        landmarks: []
      },
      temporalIndex: {
        layers: [],
        currentLayer: 0,
        timeRange: [0, 0],
        resolution: 100 // ticks per layer
      },
      activeExplorations: [],
      statistics: {
        totalMemories: 0,
        totalPatterns: 0,
        memoryDensity: 0,
        consolidationRate: 0,
        averageStrength: 0,
        oldestMemory: 0,
        newestMemory: 0,
        mostAccessedMemory: '',
        strongestPattern: '',
        emotionalBalance: {
          valence: 0,
          arousal: 0.5,
          dominance: 0.5,
          specific: []
        }
      }
    };
  }
  
  /**
   * Create memory from external data (like Owl observations)
   */
  async createMemory(
    content: string,
    details: Record<string, any>,
    systemState: any
  ): Promise<Memory> {
    const memoryId = `mem_${Date.now()}_${this.memoryIdCounter++}`;
    
    const spatialPos = this.calculateSpatialPosition(content, systemState);
    
    const memory: Memory = {
      id: memoryId,
      type: this.inferMemoryType(content, details),
      content: {
        primary: content,
        details,
        sensory: this.extractSensoryData(content, details),
        context: {
          systemState: {
            scup: systemState.scup || 50,
            entropy: systemState.entropy || 0.5,
            mood: systemState.mood || 'contemplative'
          },
          activeModules: systemState.activeModules || [],
          precedingEvents: this.getRecentMemoryIds(5),
          followingEvents: []
        },
        source: {
          type: 'system',
          moduleId: 'memoryPalace',
          reliability: systemState.reliability || 0.8
        }
      },
      timestamp: Date.now(),
      tickNumber: systemState.tickNumber || 0,
      strength: this.calculateInitialStrength(content, details),
      consolidation: 0,
      associations: [],
      spatialPosition: spatialPos,
      temporalLayer: this.getTemporalLayer(),
      emotionalValence: this.calculateEmotionalValence(content, systemState),
      accessCount: 0,
      lastAccessed: Date.now(),
      metadata: {
        importance: this.calculateImportance(content, details),
        uniqueness: await this.calculateUniqueness(content),
        unity: systemState.unity || 0.7,
        abstractionLevel: this.determineAbstractionLevel(content),
        crystallized: false,
        tags: this.extractTags(content, details)
      }
    };
    
    // Store memory
    this.state.memories.set(memory.id, memory);
    
    // Update statistics
    this.updateStatistics();
    
    // Find associations
    await this.findAndCreateAssociations(memory);
    
    // Queue for consolidation
    this.queueConsolidation(memory);
    
    // Emit event
    this.emit('memoryCreated', memory);
    
    return memory;
  }
  
  /**
   * Consolidation loop - runs pattern detection and memory management
   */
  private startConsolidationLoop() {
    setInterval(async () => {
      if (Date.now() - this.lastConsolidation < this.consolidationInterval) {
        return;
      }
      
      await this.performConsolidation();
      this.lastConsolidation = Date.now();
    }, 100);
  }
  
  private async performConsolidation() {
    // Process consolidation queue
    while (this.state.consolidationQueue.length > 0) {
      const event = this.state.consolidationQueue.shift()!;
      await this.processConsolidationEvent(event);
    }
    
    // Decay old memories
    await this.decayMemories();
    
    // Detect new patterns
    const newPatterns = await this.detectPatterns();
    newPatterns.forEach(pattern => {
      this.state.patterns.set(pattern.id, pattern);
      this.emit('patternEmerged', pattern);
    });
    
    // Crystallize strong memories
    await this.crystallizeMemories();
    
    // Update clusters
    await this.updateClusters();
  }
  
  private async processConsolidationEvent(event: ConsolidationEvent) {
    switch (event.type) {
      case 'merge':
        await this.mergeMemories(event);
        break;
      case 'abstract':
        await this.abstractMemories(event);
        break;
      case 'crystallize':
        await this.crystallizeMemory(event);
        break;
      case 'forget':
        await this.forgetMemory(event);
        break;
      case 'transform':
        await this.transformMemory(event);
        break;
      case 'dream':
        await this.dreamRecombination(event);
        break;
    }
  }
  
  private async mergeMemories(event: ConsolidationEvent) {
    const memories = event.sourceMemories
      .map(id => this.state.memories.get(id))
      .filter(Boolean) as Memory[];
    
    if (memories.length < 2) return;
    
    // Create merged memory
    const merged = await this.createMergedMemory(memories);
    this.state.memories.set(merged.id, merged);
    
    // Weaken source memories
    memories.forEach(mem => {
      mem.strength *= 0.5;
      if (mem.strength < memoryPalaceConfig.memory.decayThreshold) {
        this.state.memories.delete(mem.id);
      }
    });
    
    this.emit('memoriesMerged', { sources: memories, result: merged });
  }
  
  private async crystallizeMemory(event: ConsolidationEvent) {
    const memory = this.state.memories.get(event.sourceMemories[0]);
    if (!memory) return;
    
    memory.metadata.crystallized = true;
    memory.consolidation = 1;
    memory.strength = 1;
    
    // Create landmark
    const landmark = {
      id: `landmark_${memory.id}`,
      position: memory.spatialPosition.position,
      type: 'monument' as const,
      significance: memory.metadata.importance,
      description: `Crystallized: ${memory.content.primary}`,
      linkedMemories: [memory.id]
    };
    
    this.state.spatialIndex.landmarks.push(landmark);
    this.emit('memoryCrystallized', memory);
  }
  
  private async decayMemories() {
    const now = Date.now();
    
    this.state.memories.forEach((memory, id) => {
      if (memory.metadata.crystallized) return;
      
      // Calculate decay rate
      const age = now - memory.timestamp;
      const accessRecency = now - memory.lastAccessed;
      
      let decayRate = memoryPalaceConfig.memory.baseDecayRate;
      
      // Modify based on factors
      if (memory.consolidation > 0.8) decayRate *= 0.5;
      if (memory.associations.length > 5) decayRate *= 0.7;
      if (accessRecency < 10000) decayRate *= 0.6;
      
      // Apply decay
      memory.strength = Math.max(0, memory.strength - decayRate);
      
      // Remove if below threshold
      if (memory.strength < memoryPalaceConfig.memory.decayThreshold) {
        this.state.memories.delete(id);
        this.emit('memoryDecayed', id);
      }
    });
  }
  
  private async detectPatterns(): Promise<MemoryPattern[]> {
    const patterns: MemoryPattern[] = [];
    const memories = Array.from(this.state.memories.values());
    
    // Look for clusters
    const clusters = this.findMemoryClusters(memories);
    clusters.forEach(cluster => {
      if (cluster.memories.length >= memoryPalaceConfig.patterns.minMemoriesForPattern) {
        patterns.push(this.createClusterPattern(cluster));
      }
    });
    
    // Look for sequences
    const sequences = this.findTemporalSequences(memories);
    sequences.forEach(sequence => {
      patterns.push(this.createSequencePattern(sequence));
    });
    
    return patterns;
  }
  
  /**
   * Access memory (increases strength and updates stats)
   */
  accessMemory(memoryId: string): Memory | null {
    const memory = this.state.memories.get(memoryId);
    if (!memory) return null;
    
    memory.accessCount++;
    memory.lastAccessed = Date.now();
    memory.strength = Math.min(memory.strength + 0.05, 1);
    
    this.emit('memoryAccessed', memory);
    return memory;
  }
  
  /**
   * Query memories based on criteria
   */
  async queryMemories(query: MemoryQuery): Promise<Memory[]> {
    let results = Array.from(this.state.memories.values());
    
    // Apply filters
    if (query.spatial) {
      results = this.filterBySpatial(results, query.spatial);
    }
    
    if (query.temporal) {
      results = this.filterByTemporal(results, query.temporal);
    }
    
    if (query.emotional) {
      results = this.filterByEmotional(results, query.emotional);
    }
    
    // Apply sorting
    if (query.sort) {
      results = this.sortMemories(results, query.sort);
    }
    
    // Apply limit
    if (query.limit) {
      results = results.slice(0, query.limit);
    }
    
    return results;
  }
  
  /**
   * Get current state for visualization
   */
  getVisualizationState() {
    return {
      memories: Array.from(this.state.memories.values()),
      patterns: Array.from(this.state.patterns.values()),
      connections: this.getAllConnections(),
      landmarks: this.state.spatialIndex.landmarks,
      statistics: this.state.statistics
    };
  }
  
  // Helper methods
  private calculateSpatialPosition(content: string, systemState: any): SpatialPosition {
    // Use semantic hashing to determine position
    const hash = this.hashString(content);
    const x = ((hash % 1000) / 1000 - 0.5) * 200;
    const y = (((hash >> 10) % 1000) / 1000 - 0.5) * 200;
    const z = (((hash >> 20) % 1000) / 1000 - 0.5) * 200;
    
    return {
      position: new THREE.Vector3(x, y, z),
      layer: Math.floor(systemState.tickNumber / 100) || 0,
      sector: this.determineSector(content, systemState),
      locked: false
    };
  }
  
  private determineSector(content: string, systemState: any): MemorySector {
    const sectors = Array.from(this.state.spatialIndex.sectors.values());
    
    // Simple logic - could be more sophisticated
    if (systemState.scup > 80) {
      return sectors.find(s => s.type === 'core') || sectors[0];
    } else if (systemState.entropy > 0.7) {
      return sectors.find(s => s.type === 'peripheral') || sectors[0];
    } else {
      return sectors.find(s => s.type === 'transitional') || sectors[0];
    }
  }
  
  private inferMemoryType(content: string, details: Record<string, any>): MemoryType {
    const lower = content.toLowerCase();
    
    if (lower.includes('insight') || lower.includes('understand')) return 'insight';
    if (lower.includes('pattern') || lower.includes('recurring')) return 'pattern';
    if (lower.includes('milestone') || lower.includes('achievement')) return 'milestone';
    if (lower.includes('dream') || lower.includes('abstract')) return 'dream';
    if (lower.includes('revelation') || lower.includes('breakthrough')) return 'revelation';
    
    return 'observation';
  }
  
  private extractSensoryData(content: string, details: Record<string, any>) {
    return {
      dominant: 'abstract' as const,
      qualities: new Map([
        ['complexity', Math.random()],
        ['clarity', Math.random()],
        ['intensity', Math.random()]
      ]),
      texture: 'crystalline',
      color: this.getContentColor(content)
    };
  }
  
  private getContentColor(content: string): string {
    const hash = this.hashString(content);
    const hue = hash % 360;
    return `hsl(${hue}, 70%, 50%)`;
  }
  
  private calculateInitialStrength(content: string, details: Record<string, any>): number {
    return Math.random() * 0.5 + 0.3; // 0.3 to 0.8
  }
  
  private calculateEmotionalValence(content: string, systemState: any): EmotionalValence {
    const isPositive = content.includes('success') || content.includes('breakthrough') || systemState.scup > 70;
    
    return {
      valence: isPositive ? 0.7 : -0.3,
      arousal: Math.random() * 0.5 + 0.3,
      dominance: Math.random() * 0.5 + 0.3,
      specific: this.inferEmotions(content)
    };
  }
  
  private inferEmotions(content: string): EmotionLabel[] {
    const emotions: EmotionLabel[] = [];
    const lower = content.toLowerCase();
    
    if (lower.includes('breakthrough') || lower.includes('success')) emotions.push('joy');
    if (lower.includes('unexpected') || lower.includes('surprise')) emotions.push('surprise');
    if (lower.includes('complex') || lower.includes('deep')) emotions.push('awe');
    if (lower.includes('unclear') || lower.includes('confused')) emotions.push('confusion');
    
    return emotions;
  }
  
  private calculateImportance(content: string, details: Record<string, any>): number {
    let importance = 0.5;
    
    if (content.includes('critical') || content.includes('important')) importance += 0.3;
    if (content.length > 100) importance += 0.1;
    if (details.priority === 'high') importance += 0.2;
    
    return Math.min(importance, 1);
  }
  
  private async calculateUniqueness(content: string): Promise<number> {
    const similar = Array.from(this.state.memories.values())
      .filter(m => this.calculateSimilarity(content, m.content.primary) > 0.7);
    
    return Math.max(0.1, 1 - (similar.length * 0.1));
  }
  
  private calculateSimilarity(text1: string, text2: string): number {
    // Simple word overlap similarity
    const words1 = text1.toLowerCase().split(/\s+/);
    const words2 = text2.toLowerCase().split(/\s+/);
    const intersection = words1.filter(w => words2.includes(w));
    const union = [...new Set([...words1, ...words2])];
    
    return intersection.length / union.length;
  }
  
  private determineAbstractionLevel(content: string): number {
    if (content.includes('concept') || content.includes('principle')) return 0.9;
    if (content.includes('pattern') || content.includes('relationship')) return 0.7;
    return 0.3;
  }
  
  private extractTags(content: string, details: Record<string, any>): string[] {
    const tags = [...(details.tags || [])];
    
    const lower = content.toLowerCase();
    if (lower.includes('pattern')) tags.push('pattern');
    if (lower.includes('insight')) tags.push('insight');
    if (lower.includes('important')) tags.push('significant');
    
    return tags;
  }
  
  private getRecentMemoryIds(count: number): string[] {
    return Array.from(this.state.memories.values())
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, count)
      .map(m => m.id);
  }
  
  private getTemporalLayer(): number {
    return this.state.temporalIndex.currentLayer;
  }
  
  private async findAndCreateAssociations(memory: Memory) {
    const relatedMemories = Array.from(this.state.memories.values())
      .filter(m => m.id !== memory.id)
      .map(m => ({
        memory: m,
        similarity: this.calculateSimilarity(memory.content.primary, m.content.primary),
        type: this.determineAssociationType(memory, m)
      }))
      .filter(rel => rel.similarity > 0.5)
      .slice(0, 10); // Limit associations
    
    relatedMemories.forEach(rel => {
      const association: MemoryAssociation = {
        targetId: rel.memory.id,
        strength: rel.similarity,
        type: rel.type,
        bidirectional: true,
        formed: Date.now(),
        reinforcements: 0
      };
      
      memory.associations.push(association);
      
      // Add reverse association
      rel.memory.associations.push({
        targetId: memory.id,
        strength: rel.similarity,
        type: rel.type,
        bidirectional: true,
        formed: Date.now(),
        reinforcements: 0
      });
    });
  }
  
  private determineAssociationType(mem1: Memory, mem2: Memory): AssociationType {
    if (Math.abs(mem1.timestamp - mem2.timestamp) < 60000) return 'temporal';
    if (mem1.emotionalValence.valence * mem2.emotionalValence.valence > 0.5) return 'emotional';
    return 'semantic';
  }
  
  private queueConsolidation(memory: Memory, type: ConsolidationType = 'merge') {
    this.state.consolidationQueue.push({
      id: `consol_${Date.now()}`,
      timestamp: Date.now(),
      type,
      sourceMemories: [memory.id],
      strength: memory.strength,
      description: `${type} consolidation for ${memory.id}`
    });
  }
  
  private initializeSectors(): Map<string, MemorySector> {
    const sectors = new Map();
    
    sectors.set('core_insights', {
      id: 'core_insights',
      name: 'Core Insights',
      type: 'core',
      characteristics: ['fundamental', 'stable', 'crystallized'],
      accessibility: 1
    });
    
    sectors.set('active_patterns', {
      id: 'active_patterns',
      name: 'Active Patterns',
      type: 'peripheral',
      characteristics: ['dynamic', 'emerging', 'volatile'],
      accessibility: 0.8
    });
    
    sectors.set('deep_memory', {
      id: 'deep_memory',
      name: 'Deep Memory',
      type: 'deep',
      characteristics: ['ancient', 'foundational', 'unconscious'],
      accessibility: 0.3
    });
    
    return sectors;
  }
  
  private updateStatistics() {
    const stats = this.state.statistics;
    const memories = Array.from(this.state.memories.values());
    
    stats.totalMemories = memories.length;
    stats.totalPatterns = this.state.patterns.size;
    
    if (memories.length > 0) {
      stats.averageStrength = memories.reduce((sum, m) => sum + m.strength, 0) / memories.length;
      
      const sorted = memories.sort((a, b) => a.timestamp - b.timestamp);
      stats.oldestMemory = sorted[0].timestamp;
      stats.newestMemory = sorted[sorted.length - 1].timestamp;
      
      const mostAccessed = memories.sort((a, b) => b.accessCount - a.accessCount)[0];
      stats.mostAccessedMemory = mostAccessed.id;
    }
  }
  
  private getAllConnections(): any[] {
    const connections: any[] = [];
    
    this.state.memories.forEach(memory => {
      memory.associations.forEach(assoc => {
        const target = this.state.memories.get(assoc.targetId);
        if (target) {
          connections.push({
            from: memory.spatialPosition.position,
            to: target.spatialPosition.position,
            strength: assoc.strength,
            type: 'association',
            active: true
          });
        }
      });
    });
    
    return connections;
  }
  
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }
  
  // Stub implementations for complex methods
  private async createMergedMemory(memories: Memory[]): Promise<Memory> {
    // Implement memory merging logic
    return memories[0]; // Simplified
  }
  
  private async abstractMemories(event: ConsolidationEvent) {
    // Implement abstraction logic
  }
  
  private async forgetMemory(event: ConsolidationEvent) {
    // Implement forgetting logic
  }
  
  private async transformMemory(event: ConsolidationEvent) {
    // Implement transformation logic
  }
  
  private async dreamRecombination(event: ConsolidationEvent) {
    // Implement dream recombination logic
  }
  
  private async crystallizeMemories() {
    // Find candidates for crystallization
    const candidates = Array.from(this.state.memories.values()).filter(mem => 
      !mem.metadata.crystallized &&
      mem.consolidation > memoryPalaceConfig.memory.crystallizationThreshold &&
      mem.strength > 0.8 &&
      mem.accessCount > 10
    );
    
    candidates.forEach(memory => {
      this.queueConsolidation(memory, 'crystallize');
    });
  }
  
  private async updateClusters() {
    // Implement cluster update logic
  }
  
  private findMemoryClusters(memories: Memory[]): any[] {
    // Implement clustering algorithm
    return [];
  }
  
  private findTemporalSequences(memories: Memory[]): any[] {
    // Implement sequence detection
    return [];
  }
  
  private createClusterPattern(cluster: any): MemoryPattern {
    // Implement cluster pattern creation
    return {} as MemoryPattern;
  }
  
  private createSequencePattern(sequence: any): MemoryPattern {
    // Implement sequence pattern creation
    return {} as MemoryPattern;
  }
  
  private filterBySpatial(memories: Memory[], spatial: any): Memory[] {
    // Implement spatial filtering
    return memories;
  }
  
  private filterByTemporal(memories: Memory[], temporal: any): Memory[] {
    // Implement temporal filtering
    return memories;
  }
  
  private filterByEmotional(memories: Memory[], emotional: any): Memory[] {
    // Implement emotional filtering
    return memories;
  }
  
  private sortMemories(memories: Memory[], sort: any): Memory[] {
    // Implement sorting
    return memories;
  }
}

// Export singleton
export const memoryPalace = new MemoryPalaceCore(); 