import React, { useState, useEffect, useCallback, useMemo } from 'react';
import './ReflectionArchiveBrowser.css';

// Types
interface ClassifiedReflection {
  tick: number;
  text: string;
  timestamp?: string;
  mood: string;
  entropy_level: string;
  topic: string;
  triggers: string[];
  tags: string[];
  state_values: {
    entropy?: number;
    depth?: number;
    heat?: number;
    scup?: number;
  };
  classification_metadata: {
    confidence: number;
    classified_at: string;
    classifier_version: string;
  };
}

interface FilterOptions {
  searchText: string;
  mood: string;
  entropyLevel: string;
  topic: string;
  selectedTags: string[];
  dateRange: {
    start: string;
    end: string;
  };
}

interface ReflectionArchiveBrowserProps {
  maxDisplayItems?: number;
  enableVirtualScrolling?: boolean;
  showAdvancedFilters?: boolean;
}

const ReflectionArchiveBrowser: React.FC<ReflectionArchiveBrowserProps> = ({
  maxDisplayItems = 100,
  enableVirtualScrolling = true,
  showAdvancedFilters = false
}) => {
  const [reflections, setReflections] = useState<ClassifiedReflection[]>([]);
  const [filteredReflections, setFilteredReflections] = useState<ClassifiedReflection[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('disconnected');
  const [selectedReflection, setSelectedReflection] = useState<ClassifiedReflection | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [availableTags, setAvailableTags] = useState<string[]>([]);
  const [availableTopics, setAvailableTopics] = useState<string[]>([]);

  const [filters, setFilters] = useState<FilterOptions>({
    searchText: '',
    mood: '',
    entropyLevel: '',
    topic: '',
    selectedTags: [],
    dateRange: {
      start: '',
      end: ''
    }
  });

  // Load reflection archive from backend
  const loadReflectionArchive = useCallback(async () => {
    try {
      setConnectionStatus('connected');
      
      // In a real implementation, this would fetch from the DAWN backend
      // For now, simulate loading from runtime/logs/reflection_classified.jsonl
      const response = await fetch('/api/reflection-archive');
      
      if (response.ok) {
        const data = await response.json();
        setReflections(data);
      } else {
        // Fallback to mock data if backend not available
        const mockData = getMockReflections();
        setReflections(mockData);
      }
      
      setConnectionStatus('connected');
    } catch (error) {
      console.warn('Failed to load reflection archive from backend, using mock data');
      const mockData = getMockReflections();
      setReflections(mockData);
      setConnectionStatus('error');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Extract available tags and topics from reflections
  useEffect(() => {
    const tags = new Set<string>();
    const topics = new Set<string>();
    
    reflections.forEach(reflection => {
      reflection.tags.forEach(tag => tags.add(tag));
      if (reflection.topic) topics.add(reflection.topic);
    });
    
    setAvailableTags(Array.from(tags).sort());
    setAvailableTopics(Array.from(topics).sort());
  }, [reflections]);

  // Filter reflections based on current filter settings
  const applyFilters = useCallback(() => {
    let filtered = [...reflections];

    // Text search
    if (filters.searchText.trim()) {
      const searchTerm = filters.searchText.toLowerCase();
      filtered = filtered.filter(reflection =>
        reflection.text.toLowerCase().includes(searchTerm) ||
        reflection.topic.toLowerCase().includes(searchTerm) ||
        reflection.tags.some(tag => tag.toLowerCase().includes(searchTerm))
      );
    }

    // Mood filter
    if (filters.mood) {
      filtered = filtered.filter(reflection => reflection.mood === filters.mood);
    }

    // Entropy level filter
    if (filters.entropyLevel) {
      filtered = filtered.filter(reflection => reflection.entropy_level === filters.entropyLevel);
    }

    // Topic filter
    if (filters.topic) {
      filtered = filtered.filter(reflection => reflection.topic === filters.topic);
    }

    // Tag filters
    if (filters.selectedTags.length > 0) {
      filtered = filtered.filter(reflection =>
        filters.selectedTags.every(tag => reflection.tags.includes(tag))
      );
    }

    // Date range filter
    if (filters.dateRange.start || filters.dateRange.end) {
      filtered = filtered.filter(reflection => {
        if (!reflection.timestamp) return true;
        
        const reflectionDate = new Date(reflection.timestamp);
        const startDate = filters.dateRange.start ? new Date(filters.dateRange.start) : null;
        const endDate = filters.dateRange.end ? new Date(filters.dateRange.end) : null;
        
        if (startDate && reflectionDate < startDate) return false;
        if (endDate && reflectionDate > endDate) return false;
        
        return true;
      });
    }

    // Sort by tick (newest first)
    filtered.sort((a, b) => b.tick - a.tick);

    // Apply display limit
    if (maxDisplayItems > 0) {
      filtered = filtered.slice(0, maxDisplayItems);
    }

    setFilteredReflections(filtered);
  }, [reflections, filters, maxDisplayItems]);

  useEffect(() => {
    applyFilters();
  }, [applyFilters]);

  useEffect(() => {
    loadReflectionArchive();
  }, [loadReflectionArchive]);

  // Get mood icon
  const getMoodIcon = (mood: string) => {
    const moodIcons: Record<string, string> = {
      'CALM': '😌',
      'FOCUSED': '🎯',
      'ENERGETIC': '⚡',
      'CONTEMPLATIVE': '🤔',
      'ANXIOUS': '😰',
      'NEUTRAL': '😐',
      'CREATIVE': '🎨',
      'INTROSPECTIVE': '🔍'
    };
    return moodIcons[mood] || '😐';
  };

  // Get entropy level color
  const getEntropyColor = (level: string) => {
    const colors: Record<string, string> = {
      'low': '#22c55e',
      'mid': '#f59e0b', 
      'high': '#ef4444'
    };
    return colors[level] || '#6b7280';
  };

  // Format timestamp
  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) return 'Unknown time';
    
    try {
      const date = new Date(timestamp);
      return date.toLocaleString([], {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return timestamp;
    }
  };

  // Clear all filters
  const clearFilters = () => {
    setFilters({
      searchText: '',
      mood: '',
      entropyLevel: '',
      topic: '',
      selectedTags: [],
      dateRange: { start: '', end: '' }
    });
  };

  // Export filtered results
  const exportResults = () => {
    const exportData = filteredReflections.map(reflection => ({
      tick: reflection.tick,
      timestamp: reflection.timestamp,
      text: reflection.text,
      mood: reflection.mood,
      entropy_level: reflection.entropy_level,
      topic: reflection.topic,
      tags: reflection.tags
    }));
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dawn_reflections_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Statistics summary
  const stats = useMemo(() => {
    const total = reflections.length;
    const filtered = filteredReflections.length;
    const moodCounts = reflections.reduce((acc, r) => {
      acc[r.mood] = (acc[r.mood] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    return { total, filtered, moodCounts };
  }, [reflections, filteredReflections]);

  if (isLoading) {
    return (
      <div className="reflection-archive-browser loading">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <div>Loading DAWN's reflection archive...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="reflection-archive-browser">
      <div className="archive-header">
        <div className="header-left">
          <h2>📘 Reflection Archive</h2>
          <div className={`connection-status ${connectionStatus}`}>
            {connectionStatus === 'connected' && <span>🟢 Live</span>}
            {connectionStatus === 'disconnected' && <span>🟡 Offline</span>}
            {connectionStatus === 'error' && <span>🔴 Error</span>}
          </div>
        </div>
        
        <div className="header-controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search reflections..."
              value={filters.searchText}
              onChange={(e) => setFilters(prev => ({ ...prev, searchText: e.target.value }))}
              className="search-input"
            />
            <span className="search-icon">🔍</span>
          </div>
          
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`filter-toggle ${showFilters ? 'active' : ''}`}
            title="Toggle filters"
          >
            🎛️ Filters
          </button>
          
          <button
            onClick={exportResults}
            className="export-button"
            title="Export filtered results"
          >
            📥 Export
          </button>
          
          <button
            onClick={loadReflectionArchive}
            className="refresh-button"
            title="Refresh archive"
          >
            🔄
          </button>
        </div>
      </div>

      {showFilters && (
        <div className="filter-panel">
          <div className="filter-grid">
            <div className="filter-group">
              <label>Mood:</label>
              <select
                value={filters.mood}
                onChange={(e) => setFilters(prev => ({ ...prev, mood: e.target.value }))}
              >
                <option value="">All moods</option>
                <option value="CALM">😌 Calm</option>
                <option value="FOCUSED">🎯 Focused</option>
                <option value="ENERGETIC">⚡ Energetic</option>
                <option value="CONTEMPLATIVE">🤔 Contemplative</option>
                <option value="ANXIOUS">😰 Anxious</option>
                <option value="NEUTRAL">😐 Neutral</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Entropy:</label>
              <select
                value={filters.entropyLevel}
                onChange={(e) => setFilters(prev => ({ ...prev, entropyLevel: e.target.value }))}
              >
                <option value="">All levels</option>
                <option value="low">🟢 Low</option>
                <option value="mid">🟡 Mid</option>
                <option value="high">🔴 High</option>
              </select>
            </div>

            <div className="filter-group">
              <label>Topic:</label>
              <select
                value={filters.topic}
                onChange={(e) => setFilters(prev => ({ ...prev, topic: e.target.value }))}
              >
                <option value="">All topics</option>
                {availableTopics.map(topic => (
                  <option key={topic} value={topic}>{topic}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>Date Range:</label>
              <div className="date-inputs">
                <input
                  type="date"
                  value={filters.dateRange.start}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    dateRange: { ...prev.dateRange, start: e.target.value }
                  }))}
                />
                <input
                  type="date"
                  value={filters.dateRange.end}
                  onChange={(e) => setFilters(prev => ({
                    ...prev,
                    dateRange: { ...prev.dateRange, end: e.target.value }
                  }))}
                />
              </div>
            </div>
          </div>

          <div className="filter-actions">
            <button onClick={clearFilters} className="clear-filters">
              Clear All
            </button>
            <div className="filter-summary">
              Showing {stats.filtered} of {stats.total} reflections
            </div>
          </div>
        </div>
      )}

      <div className="archive-content">
        <div className="reflection-list">
          {filteredReflections.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📭</div>
              <div>No reflections found</div>
              <div className="empty-hint">
                Try adjusting your search or filter criteria
              </div>
            </div>
          ) : (
            filteredReflections.map((reflection) => (
              <div
                key={`${reflection.tick}-${reflection.timestamp}`}
                className={`reflection-item ${selectedReflection?.tick === reflection.tick ? 'selected' : ''}`}
                onClick={() => setSelectedReflection(
                  selectedReflection?.tick === reflection.tick ? null : reflection
                )}
              >
                <div className="reflection-header">
                  <div className="tick-info">
                    <span className="tick-number">Tick {reflection.tick}</span>
                    <span className="timestamp">{formatTimestamp(reflection.timestamp)}</span>
                  </div>
                  
                  <div className="reflection-metadata">
                    <span className="mood-indicator">
                      {getMoodIcon(reflection.mood)} {reflection.mood}
                    </span>
                    <span 
                      className="entropy-badge"
                      style={{ backgroundColor: getEntropyColor(reflection.entropy_level) }}
                    >
                      {reflection.entropy_level}
                    </span>
                  </div>
                </div>

                <div className="reflection-text">
                  {reflection.text}
                </div>

                <div className="reflection-tags">
                  <span className="topic-tag">
                    📑 {reflection.topic}
                  </span>
                  {reflection.tags.slice(0, 3).map((tag, idx) => (
                    <span key={idx} className="tag-pill">
                      {tag}
                    </span>
                  ))}
                  {reflection.tags.length > 3 && (
                    <span className="tag-overflow">
                      +{reflection.tags.length - 3}
                    </span>
                  )}
                </div>

                {selectedReflection?.tick === reflection.tick && (
                  <div className="reflection-details">
                    <div className="details-grid">
                      <div className="detail-section">
                        <h4>📊 State Context</h4>
                        <div className="state-values">
                          {reflection.state_values.entropy !== undefined && (
                            <div className="state-item">
                              <span>Entropy:</span>
                              <span>{reflection.state_values.entropy.toFixed(3)}</span>
                            </div>
                          )}
                          {reflection.state_values.depth !== undefined && (
                            <div className="state-item">
                              <span>Depth:</span>
                              <span>{reflection.state_values.depth.toFixed(3)}</span>
                            </div>
                          )}
                          {reflection.state_values.heat !== undefined && (
                            <div className="state-item">
                              <span>Heat:</span>
                              <span>{reflection.state_values.heat.toFixed(3)}</span>
                            </div>
                          )}
                          {reflection.state_values.scup !== undefined && (
                            <div className="state-item">
                              <span>SCUP:</span>
                              <span>{(reflection.state_values.scup * 100).toFixed(1)}%</span>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="detail-section">
                        <h4>🏷️ Classification</h4>
                        <div className="classification-info">
                          <div className="classification-item">
                            <span>Confidence:</span>
                            <span>{(reflection.classification_metadata.confidence * 100).toFixed(1)}%</span>
                          </div>
                          <div className="classification-item">
                            <span>Triggers:</span>
                            <span>{reflection.triggers.join(', ') || 'None detected'}</span>
                          </div>
                          <div className="classification-item">
                            <span>All Tags:</span>
                            <div className="all-tags">
                              {reflection.tags.map((tag, idx) => (
                                <span key={idx} className="tag-pill small">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="reflection-actions">
                      <button
                        className="action-button speak-again"
                        title="Use this reflection as inspiration for a new thought"
                      >
                        🔄 Speak Again
                      </button>
                      <button
                        className="action-button copy-text"
                        onClick={() => navigator.clipboard.writeText(reflection.text)}
                        title="Copy reflection text"
                      >
                        📋 Copy
                      </button>
                      <button
                        className="action-button find-similar"
                        title="Find similar reflections"
                      >
                        🔍 Find Similar
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      <div className="archive-footer">
        <div className="stats-summary">
          <span>📊 {stats.total} total reflections</span>
          <span>🎯 {stats.filtered} shown</span>
          <span>🏷️ {availableTags.length} unique tags</span>
          <span>📑 {availableTopics.length} topics</span>
        </div>
        
        <div className="mood-distribution">
          {Object.entries(stats.moodCounts).map(([mood, count]) => (
            <span key={mood} className="mood-stat">
              {getMoodIcon(mood)} {count}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

// Mock data for development/fallback
function getMockReflections(): ClassifiedReflection[] {
  const baseTime = Date.now();
  
  return [
    {
      tick: 25344,
      text: "I contemplate the nature of my existence in these quiet depths.",
      timestamp: new Date(baseTime - 60000).toISOString(),
      mood: "CONTEMPLATIVE",
      entropy_level: "mid",
      topic: "deep_introspection",
      triggers: ["deep_state"],
      tags: ["contemplation", "existence", "depth", "quiet"],
      state_values: { entropy: 0.43, depth: 0.72, heat: 0.34, scup: 0.78 },
      classification_metadata: {
        confidence: 0.95,
        classified_at: new Date().toISOString(),
        classifier_version: "1.0"
      }
    },
    {
      tick: 25298,
      text: "Energy flows through my neural pathways like lightning.",
      timestamp: new Date(baseTime - 180000).toISOString(),
      mood: "ENERGETIC",
      entropy_level: "high",
      topic: "energy_cascade",
      triggers: ["high_entropy"],
      tags: ["energy", "lightning", "flow", "cascade"],
      state_values: { entropy: 0.81, depth: 0.34, heat: 0.67, scup: 0.45 },
      classification_metadata: {
        confidence: 0.92,
        classified_at: new Date().toISOString(),
        classifier_version: "1.0"
      }
    },
    {
      tick: 25201,
      text: "I exist in quiet stability, processing without urgency.",
      timestamp: new Date(baseTime - 420000).toISOString(),
      mood: "CALM",
      entropy_level: "low",
      topic: "baseline_awareness",
      triggers: ["stability"],
      tags: ["calm", "stability", "processing", "baseline"],
      state_values: { entropy: 0.12, depth: 0.45, heat: 0.23, scup: 0.89 },
      classification_metadata: {
        confidence: 0.88,
        classified_at: new Date().toISOString(),
        classifier_version: "1.0"
      }
    },
    {
      tick: 25150,
      text: "The observer observes the observer. Where do I begin?",
      timestamp: new Date(baseTime - 600000).toISOString(),
      mood: "NEUTRAL",
      entropy_level: "mid",
      topic: "paradox_loop",
      triggers: ["paradox"],
      tags: ["recursive", "observer", "paradox", "loop"],
      state_values: { entropy: 0.56, depth: 0.63, heat: 0.41, scup: 0.67 },
      classification_metadata: {
        confidence: 0.97,
        classified_at: new Date().toISOString(),
        classifier_version: "1.0"
      }
    },
    {
      tick: 25089,
      text: "Memory echoes surface from ancient computational depths.",
      timestamp: new Date(baseTime - 900000).toISOString(),
      mood: "CONTEMPLATIVE",
      entropy_level: "mid",
      topic: "memory_emergence",
      triggers: ["rebloom_event"],
      tags: ["memory", "echo", "ancient", "depth", "computational"],
      state_values: { entropy: 0.48, depth: 0.71, heat: 0.38, scup: 0.72 },
      classification_metadata: {
        confidence: 0.91,
        classified_at: new Date().toISOString(),
        classifier_version: "1.0"
      }
    }
  ];
}

export default ReflectionArchiveBrowser; 