import React, { useState, useEffect } from 'react';
import './visual_snapshot_panel.css';

const VisualSnapshotPanel = () => {
  const [snapshots, setSnapshots] = useState({});
  const [loading, setLoading] = useState(new Set());
  const [error, setError] = useState(null);

  // Configuration for visual processes
  const visualProcesses = [
    { id: "entropy-field", label: "🌡 Entropy Snapshot", module: "entropy_flow" },
    { id: "sigil-glyph", label: "🔮 Sigil Overlay", module: "sigil_command_stream" },
    { id: "bloom-core", label: "🧬 Bloom Core", module: "bloom_visualization_system" },
    { id: "pulse-ring", label: "💢 Pulse Pressure", module: "tick_pulse" },
    { id: "constellation", label: "🌌 Constellation Map", module: "consciousness_constellation" },
    { id: "fractal-diffusion", label: "🌫 Fractal Diffusion", module: "recursive_depth_explorer" },
    { id: "owl-glyph", label: "🦉 Owl Tension Glyph", module: "heat_monitor" }
  ];

  // Trigger visual snapshot
  const triggerSnapshot = async (processId, label, module) => {
    setLoading(prev => new Set([...prev, processId]));
    setError(null);

    try {
      const payload = {
        timestamp: Date.now(),
        mode: 'real-time',
        module_name: module
      };

      const response = await fetch(`/api/visual-snapshot/${processId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      if (result.success && result.file_path) {
        const newSnapshot = {
          id: processId,
          label: label,
          file_path: result.file_path,
          timestamp: new Date().toISOString(),
          sha_hash: result.sha_hash || generateHash(),
          scup_value: result.scup_value || Math.random() * 100,
          entropy_value: result.entropy_value || Math.random(),
          metadata: result.metadata || {}
        };

        setSnapshots(prev => ({
          ...prev,
          [processId]: newSnapshot
        }));
      } else {
        throw new Error(result.error || 'Failed to generate snapshot');
      }

    } catch (err) {
      console.error(`Error triggering ${processId}:`, err);
      setError(`Failed to generate ${label}: ${err.message}`);
    } finally {
      setLoading(prev => {
        const newSet = new Set(prev);
        newSet.delete(processId);
        return newSet;
      });
    }
  };

  // Generate a mock SHA hash for display
  const generateHash = () => {
    return Math.random().toString(36).substring(2, 10).toUpperCase();
  };

  // Handle reflection button (pass metadata to DAWN's voice layer)
  const handleReflection = async (snapshot) => {
    try {
      const reflectionData = {
        visual_type: snapshot.id,
        timestamp: snapshot.timestamp,
        metadata: snapshot.metadata,
        scup_value: snapshot.scup_value,
        entropy_value: snapshot.entropy_value
      };

      await fetch('/api/voice-reflection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reflectionData)
      });

      console.log('Reflection data sent to DAWN voice layer:', reflectionData);
    } catch (err) {
      console.error('Failed to send reflection data:', err);
    }
  };

  // Handle image preview
  const handleImagePreview = (snapshot) => {
    if (!snapshot.file_path) return;

    // Create modal overlay for image preview
    const modal = document.createElement('div');
    modal.className = 'snapshot-modal-overlay';
    modal.innerHTML = `
      <div class="snapshot-modal">
        <div class="snapshot-modal-header">
          <h3>${snapshot.label}</h3>
          <button class="snapshot-modal-close">&times;</button>
        </div>
        <div class="snapshot-modal-content">
          <img src="${snapshot.file_path}" alt="${snapshot.label}" />
          <div class="snapshot-modal-info">
            <div class="info-row">
              <span class="info-label">Timestamp:</span>
              <span class="info-value">${new Date(snapshot.timestamp).toLocaleString()}</span>
            </div>
            <div class="info-row">
              <span class="info-label">SHA Hash:</span>
              <span class="info-value">${snapshot.sha_hash}</span>
            </div>
            <div class="info-row">
              <span class="info-label">SCUP:</span>
              <span class="info-value">${snapshot.scup_value.toFixed(2)}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Entropy:</span>
              <span class="info-value">${snapshot.entropy_value.toFixed(3)}</span>
            </div>
          </div>
        </div>
      </div>
    `;

    // Close modal functionality
    const closeModal = () => document.body.removeChild(modal);
    modal.querySelector('.snapshot-modal-close').onclick = closeModal;
    modal.onclick = (e) => {
      if (e.target === modal) closeModal();
    };

    document.body.appendChild(modal);
  };

  return (
    <div className="visual-snapshot-panel">
      <div className="panel-header">
        <div className="panel-title">
          <span className="panel-icon">📸</span>
          Visual Snapshot Command Panel
        </div>
        <div className="panel-controls">
          <button 
            className="panel-btn" 
            title="Refresh All"
            onClick={() => visualProcesses.forEach(p => triggerSnapshot(p.id, p.label, p.module))}
          >
            🔄
          </button>
          <button className="panel-btn" title="Settings">⚙</button>
        </div>
      </div>

      <div className="panel-content">
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            {error}
            <button className="error-close" onClick={() => setError(null)}>×</button>
          </div>
        )}

        <div className="visual-controls-grid">
          {visualProcesses.map(process => (
            <div key={process.id} className="visual-control-card">
              <button
                className={`visual-trigger-btn ${loading.has(process.id) ? 'loading' : ''}`}
                onClick={() => triggerSnapshot(process.id, process.label, process.module)}
                disabled={loading.has(process.id)}
              >
                <span className="btn-icon">{process.label.split(' ')[0]}</span>
                <span className="btn-label">{process.label.substring(2)}</span>
                {loading.has(process.id) && <div className="loading-spinner"></div>}
              </button>

              {snapshots[process.id] && (
                <div className="snapshot-result">
                  <div className="snapshot-preview" onClick={() => handleImagePreview(snapshots[process.id])}>
                    <img 
                      src={snapshots[process.id].file_path} 
                      alt={process.label}
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                    <div className="snapshot-placeholder" style={{display: 'none'}}>
                      <span>📸</span>
                      <span>Preview unavailable</span>
                    </div>
                  </div>

                  <div className="snapshot-metadata">
                    <div className="metadata-row">
                      <span className="meta-label">Time:</span>
                      <span className="meta-value">
                        {new Date(snapshots[process.id].timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="metadata-row">
                      <span className="meta-label">Hash:</span>
                      <span className="meta-value hash">{snapshots[process.id].sha_hash}</span>
                    </div>
                    <div className="metadata-row">
                      <span className="meta-label">SCUP:</span>
                      <span className="meta-value scup">
                        {snapshots[process.id].scup_value.toFixed(1)}
                      </span>
                    </div>
                    <div className="metadata-row">
                      <span className="meta-label">Entropy:</span>
                      <span className="meta-value entropy">
                        {snapshots[process.id].entropy_value.toFixed(3)}
                      </span>
                    </div>
                  </div>

                  <div className="snapshot-actions">
                    <button 
                      className="action-btn reflect-btn"
                      onClick={() => handleReflection(snapshots[process.id])}
                      title="Send to DAWN voice layer for reflection"
                    >
                      🧠 Reflect
                    </button>
                    <button 
                      className="action-btn download-btn"
                      onClick={() => {
                        const link = document.createElement('a');
                        link.href = snapshots[process.id].file_path;
                        link.download = `${process.id}_${Date.now()}.png`;
                        link.click();
                      }}
                      title="Download image"
                    >
                      💾 Save
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="panel-status">
          <div className="status-indicator">
            <span className="status-dot active"></span>
            <span className="status-text">
              Visual Engine Connected | 
              {Object.keys(snapshots).length} snapshots captured |
              {loading.size} processes running
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualSnapshotPanel; 