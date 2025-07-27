import React, { useState, useEffect, useCallback } from 'react';
import './SemanticPromptEditor.css';

// Types
interface ThoughtEntry {
  text: string;
  tags: string[];
  mood: string;
  min_entropy: number;
  max_entropy: number;
  min_depth: number;
  max_depth: number;
  category: string;
}

interface EditState {
  isEditing: boolean;
  index: number;
  field: string;
}

// Available moods and categories for dropdowns
const MOODS = ['NEUTRAL', 'CALM', 'FOCUSED', 'ENERGETIC', 'CONTEMPLATIVE', 'ANXIOUS'];
const CATEGORIES = [
  'baseline_awareness', 'drift_warning', 'complex_emergence', 'deep_introspection',
  'memory_rebloom', 'symbolic_emergence', 'meta_paradox', 'milestone_achievement',
  'concern_alert', 'high_energy', 'drift_navigation'
];

const SemanticPromptEditor: React.FC = () => {
  const [thoughts, setThoughts] = useState<ThoughtEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editState, setEditState] = useState<EditState>({ isEditing: false, index: -1, field: '' });
  const [searchFilter, setSearchFilter] = useState('');
  const [moodFilter, setMoodFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [isDirty, setIsDirty] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  // Load thought bank from backend
  const loadThoughts = useCallback(async () => {
    try {
      setIsLoading(true);
      // In a real implementation, this would fetch from the DAWN backend
      // For now, simulate loading the thought_bank.jsonl
      const response = await fetch('/api/thought-bank');
      if (response.ok) {
        const data = await response.json();
        setThoughts(data);
      } else {
        // Fallback to mock data if backend not available
        setThoughts(getMockThoughts());
      }
    } catch (error) {
      console.warn('Failed to load thoughts from backend, using mock data');
      setThoughts(getMockThoughts());
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Save thoughts to backend
  const saveThoughts = useCallback(async () => {
    try {
      setSaveStatus('saving');
      const response = await fetch('/api/thought-bank', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(thoughts),
      });
      
      if (response.ok) {
        setSaveStatus('saved');
        setIsDirty(false);
        setTimeout(() => setSaveStatus('idle'), 2000);
      } else {
        setSaveStatus('error');
        setTimeout(() => setSaveStatus('idle'), 3000);
      }
    } catch (error) {
      console.error('Failed to save thoughts:', error);
      setSaveStatus('error');
      setTimeout(() => setSaveStatus('idle'), 3000);
    }
  }, [thoughts]);

  // Auto-save when dirty
  useEffect(() => {
    if (isDirty) {
      const timeout = setTimeout(() => {
        saveThoughts();
      }, 2000);
      return () => clearTimeout(timeout);
    }
  }, [isDirty, saveThoughts]);

  // Load thoughts on component mount
  useEffect(() => {
    loadThoughts();
  }, [loadThoughts]);

  // Update thought entry
  const updateThought = (index: number, field: keyof ThoughtEntry, value: any) => {
    const newThoughts = [...thoughts];
    if (field === 'tags' && typeof value === 'string') {
      newThoughts[index][field] = value.split(',').map(tag => tag.trim()).filter(tag => tag);
    } else {
      (newThoughts[index] as any)[field] = value;
    }
    setThoughts(newThoughts);
    setIsDirty(true);
  };

  // Add new thought
  const addThought = () => {
    const newThought: ThoughtEntry = {
      text: 'New thought...',
      tags: [],
      mood: 'NEUTRAL',
      min_entropy: 0.0,
      max_entropy: 1.0,
      min_depth: 0.0,
      max_depth: 1.0,
      category: 'general_reflection'
    };
    setThoughts([...thoughts, newThought]);
    setIsDirty(true);
    // Start editing the new thought
    setEditState({ isEditing: true, index: thoughts.length, field: 'text' });
  };

  // Delete thought
  const deleteThought = (index: number) => {
    if (window.confirm('Delete this thought? This action cannot be undone.')) {
      const newThoughts = thoughts.filter((_, i) => i !== index);
      setThoughts(newThoughts);
      setIsDirty(true);
    }
  };

  // Filter thoughts
  const filteredThoughts = thoughts.filter(thought => {
    const matchesSearch = !searchFilter || 
      thought.text.toLowerCase().includes(searchFilter.toLowerCase()) ||
      thought.tags.some(tag => tag.toLowerCase().includes(searchFilter.toLowerCase()));
    const matchesMood = !moodFilter || thought.mood === moodFilter;
    const matchesCategory = !categoryFilter || thought.category === categoryFilter;
    
    return matchesSearch && matchesMood && matchesCategory;
  });

  // Export/Import functions
  const exportThoughts = () => {
    const dataStr = thoughts.map(thought => JSON.stringify(thought)).join('\n');
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `thought_bank_${new Date().toISOString().split('T')[0]}.jsonl`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const importThoughts = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const content = e.target?.result as string;
          const lines = content.split('\n').filter(line => line.trim());
          const imported = lines.map(line => JSON.parse(line));
          setThoughts(imported);
          setIsDirty(true);
        } catch (error) {
          alert('Error importing file. Please check the format.');
        }
      };
      reader.readAsText(file);
    }
  };

  // Test thought function (placeholder)
  const testThought = (thought: ThoughtEntry) => {
    // In a real implementation, this would send the thought to DAWN for testing
    console.log('Testing thought:', thought.text);
    alert(`Testing: "${thought.text.substring(0, 50)}..."`);
  };

  if (isLoading) {
    return (
      <div className="semantic-prompt-editor loading">
        <div className="loading-spinner"></div>
        <div>Loading DAWN's thought bank...</div>
      </div>
    );
  }

  return (
    <div className="semantic-prompt-editor">
      <div className="editor-header">
        <h2>🧠 DAWN Thought Bank Editor</h2>
        <div className="header-controls">
          <div className="save-status">
            {saveStatus === 'saving' && <span className="status saving">💾 Saving...</span>}
            {saveStatus === 'saved' && <span className="status saved">✅ Saved</span>}
            {saveStatus === 'error' && <span className="status error">❌ Save failed</span>}
            {isDirty && saveStatus === 'idle' && <span className="status dirty">● Unsaved changes</span>}
          </div>
          <button onClick={exportThoughts} className="btn-secondary">📥 Export</button>
          <label className="btn-secondary file-input-label">
            📤 Import
            <input type="file" accept=".jsonl,.json" onChange={importThoughts} style={{ display: 'none' }} />
          </label>
          <button onClick={addThought} className="btn-primary">+ Add Thought</button>
        </div>
      </div>

      <div className="editor-filters">
        <input
          type="text"
          placeholder="🔍 Search thoughts..."
          value={searchFilter}
          onChange={(e) => setSearchFilter(e.target.value)}
          className="filter-input"
        />
        <select
          value={moodFilter}
          onChange={(e) => setMoodFilter(e.target.value)}
          className="filter-select"
        >
          <option value="">All Moods</option>
          {MOODS.map(mood => (
            <option key={mood} value={mood}>{mood}</option>
          ))}
        </select>
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="filter-select"
        >
          <option value="">All Categories</option>
          {CATEGORIES.map(cat => (
            <option key={cat} value={cat}>{cat.replace(/_/g, ' ')}</option>
          ))}
        </select>
        <div className="thought-count">
          {filteredThoughts.length} / {thoughts.length} thoughts
        </div>
      </div>

      <div className="thoughts-table">
        <div className="table-header">
          <div className="col-text">Thought Text</div>
          <div className="col-mood">Mood</div>
          <div className="col-entropy">Entropy Range</div>
          <div className="col-depth">Depth Range</div>
          <div className="col-tags">Tags</div>
          <div className="col-category">Category</div>
          <div className="col-actions">Actions</div>
        </div>

        <div className="table-body">
          {filteredThoughts.map((thought, index) => {
            const originalIndex = thoughts.indexOf(thought);
            const isEditing = editState.isEditing && editState.index === originalIndex;

            return (
              <div key={originalIndex} className="thought-row">
                <div className="col-text">
                  {isEditing && editState.field === 'text' ? (
                    <textarea
                      value={thought.text}
                      onChange={(e) => updateThought(originalIndex, 'text', e.target.value)}
                      onBlur={() => setEditState({ isEditing: false, index: -1, field: '' })}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && e.ctrlKey) {
                          setEditState({ isEditing: false, index: -1, field: '' });
                        }
                      }}
                      autoFocus
                      className="edit-textarea"
                    />
                  ) : (
                    <div
                      className="editable-cell"
                      onClick={() => setEditState({ isEditing: true, index: originalIndex, field: 'text' })}
                    >
                      {thought.text}
                    </div>
                  )}
                </div>

                <div className="col-mood">
                  <select
                    value={thought.mood}
                    onChange={(e) => updateThought(originalIndex, 'mood', e.target.value)}
                    className="mood-select"
                  >
                    {MOODS.map(mood => (
                      <option key={mood} value={mood}>{mood}</option>
                    ))}
                  </select>
                </div>

                <div className="col-entropy">
                  <div className="range-inputs">
                    <input
                      type="number"
                      min="0"
                      max="1"
                      step="0.1"
                      value={thought.min_entropy}
                      onChange={(e) => updateThought(originalIndex, 'min_entropy', parseFloat(e.target.value))}
                      className="range-input"
                    />
                    <span>-</span>
                    <input
                      type="number"
                      min="0"
                      max="1"
                      step="0.1"
                      value={thought.max_entropy}
                      onChange={(e) => updateThought(originalIndex, 'max_entropy', parseFloat(e.target.value))}
                      className="range-input"
                    />
                  </div>
                </div>

                <div className="col-depth">
                  <div className="range-inputs">
                    <input
                      type="number"
                      min="0"
                      max="1"
                      step="0.1"
                      value={thought.min_depth}
                      onChange={(e) => updateThought(originalIndex, 'min_depth', parseFloat(e.target.value))}
                      className="range-input"
                    />
                    <span>-</span>
                    <input
                      type="number"
                      min="0"
                      max="1"
                      step="0.1"
                      value={thought.max_depth}
                      onChange={(e) => updateThought(originalIndex, 'max_depth', parseFloat(e.target.value))}
                      className="range-input"
                    />
                  </div>
                </div>

                <div className="col-tags">
                  <input
                    type="text"
                    value={thought.tags.join(', ')}
                    onChange={(e) => updateThought(originalIndex, 'tags', e.target.value)}
                    placeholder="tag1, tag2, tag3"
                    className="tags-input"
                  />
                </div>

                <div className="col-category">
                  <select
                    value={thought.category}
                    onChange={(e) => updateThought(originalIndex, 'category', e.target.value)}
                    className="category-select"
                  >
                    {CATEGORIES.map(cat => (
                      <option key={cat} value={cat}>{cat.replace(/_/g, ' ')}</option>
                    ))}
                  </select>
                </div>

                <div className="col-actions">
                  <button 
                    onClick={() => testThought(thought)}
                    className="btn-test"
                    title="Test this thought"
                  >
                    🧪
                  </button>
                  <button 
                    onClick={() => deleteThought(originalIndex)}
                    className="btn-delete"
                    title="Delete this thought"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {filteredThoughts.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">🧠</div>
          <div>No thoughts match your current filters</div>
          <button onClick={() => {
            setSearchFilter('');
            setMoodFilter('');
            setCategoryFilter('');
          }} className="btn-secondary">Clear Filters</button>
        </div>
      )}
    </div>
  );
};

// Mock data for development/fallback
function getMockThoughts(): ThoughtEntry[] {
  return [
    {
      text: "I exist in quiet stability, processing without urgency.",
      tags: ["stability", "neutral", "baseline"],
      mood: "NEUTRAL",
      min_entropy: 0.0,
      max_entropy: 0.3,
      min_depth: 0.2,
      max_depth: 0.6,
      category: "baseline_awareness"
    },
    {
      text: "Complexity emerges at the edges of my understanding.",
      tags: ["complexity", "emergence", "high_entropy"],
      mood: "ENERGETIC",
      min_entropy: 0.6,
      max_entropy: 1.0,
      min_depth: 0.5,
      max_depth: 1.0,
      category: "complex_emergence"
    },
    {
      text: "I drift between thoughts, observing the spaces between.",
      tags: ["drift", "contemplation", "space"],
      mood: "CALM",
      min_entropy: 0.3,
      max_entropy: 0.6,
      min_depth: 0.4,
      max_depth: 0.8,
      category: "drift_navigation"
    }
  ];
}

export default SemanticPromptEditor; 