/**
 * DAWN GUI Fix Script
 * Comprehensive solution for non-functional buttons and tab loading issues
 * Addresses all 12+ missing button handlers identified by diagnostic
 */

// =====================================
// MISSING BUTTON HANDLERS - CORE FIXES
// =====================================

// 1. Entropy Panel Controls
function toggleEntropyPanel() {
    const panel = document.querySelector('[data-panel="entropy"]');
    if (panel) {
        panel.classList.toggle('minimized');
        console.log('🔍 Entropy panel toggled');
    }
}

function exportEntropyData() {
    const entropyData = {
        current_entropy: parseFloat(document.getElementById('entropy-value')?.textContent || '0'),
        timestamp: new Date().toISOString(),
        zone: document.getElementById('zone-indicator')?.textContent || 'UNKNOWN'
    };
    
    const blob = new Blob([JSON.stringify(entropyData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dawn_entropy_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('📤 Entropy data exported');
}

function openEntropySettings() {
    showModal('Entropy Settings', `
        <div class="settings-panel">
            <h3>🌀 Entropy Configuration</h3>
            <label>Update Frequency (ms):</label>
            <input type="number" id="entropy-freq" value="1000" min="100" max="5000">
            
            <label>Alert Threshold:</label>
            <input type="range" id="entropy-threshold" min="0" max="1" step="0.1" value="0.8">
            
            <button onclick="applyEntropySettings()">Apply</button>
        </div>
    `);
}

// 2. Neural Activity Panel Controls  
function pauseNeuralActivity() {
    window.neuralActivityPaused = !window.neuralActivityPaused;
    const btn = event.target;
    btn.textContent = window.neuralActivityPaused ? '▶' : '⏸';
    btn.title = window.neuralActivityPaused ? 'Resume' : 'Pause';
    console.log(`🧠 Neural activity ${window.neuralActivityPaused ? 'paused' : 'resumed'}`);
}

function resetNeuralActivity() {
    // Reset neural activity visualization
    const canvas = document.querySelector('#neural-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    console.log('🔄 Neural activity reset');
}

function openNeuralSettings() {
    showModal('Neural Activity Settings', `
        <div class="settings-panel">
            <h3>🧠 Neural Configuration</h3>
            <label>Node Count:</label>
            <input type="range" id="neural-nodes" min="10" max="100" value="50">
            
            <label>Connection Density:</label>
            <input type="range" id="neural-density" min="0.1" max="1" step="0.1" value="0.3">
            
            <button onclick="applyNeuralSettings()">Apply</button>
        </div>
    `);
}

// 3. Consciousness Constellation Controls
function toggle3DView() {
    const constellation = document.querySelector('#constellation-container');
    if (constellation) {
        constellation.classList.toggle('view-3d');
        const btn = event.target;
        btn.textContent = constellation.classList.contains('view-3d') ? '🔮' : '⚬';
        console.log('🔮 3D view toggled');
    }
}

function exportConstellation() {
    // Export constellation data
    const constellationData = {
        nodes: window.constellationNodes || [],
        connections: window.constellationConnections || [],
        timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(constellationData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dawn_constellation_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('📤 Constellation data exported');
}

// 4. Sigil Command Panel Controls
function executeSigilCommand() {
    const input = document.querySelector('#sigil-input');
    if (input && input.value.trim()) {
        const command = input.value.trim();
        
        // Send to backend
        fetch('/api/execute-sigil', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => {
            console.log('⚡ Sigil executed:', command);
            input.value = '';
            updateSigilLog(command, data);
        })
        .catch(error => {
            console.error('❌ Sigil execution failed:', error);
        });
    }
}

function clearSigilInput() {
    const input = document.querySelector('#sigil-input');
    if (input) {
        input.value = '';
        console.log('🗑 Sigil input cleared');
    }
}

// 5. Memory Rebloom Controls
function toggleAutoRebloom() {
    window.autoRebloomEnabled = !window.autoRebloomEnabled;
    const btn = event.target;
    btn.classList.toggle('active');
    btn.title = window.autoRebloomEnabled ? 'Disable Auto-Rebloom' : 'Enable Auto-Rebloom';
    console.log(`🔄 Auto-rebloom ${window.autoRebloomEnabled ? 'enabled' : 'disabled'}`);
}

function exportMemoryData() {
    const memoryData = {
        reblooms: window.rebloomHistory || [],
        current_memory_state: window.currentMemoryState || {},
        timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(memoryData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dawn_memory_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('📤 Memory data exported');
}

// 6. Visualization Panel Controls
function toggleFullscreenVisualization() {
    const panel = document.querySelector('#visualization-container');
    if (panel) {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            panel.requestFullscreen();
        }
        console.log('⛶ Visualization fullscreen toggled');
    }
}

// 7. Voice Commentary Controls
function toggleVoiceMode() {
    window.voiceModeEnabled = !window.voiceModeEnabled;
    const btn = event.target;
    btn.classList.toggle('active');
    btn.textContent = window.voiceModeEnabled ? '🎤' : '🔇';
    btn.title = window.voiceModeEnabled ? 'Disable Voice' : 'Enable Voice';
    console.log(`🎤 Voice mode ${window.voiceModeEnabled ? 'enabled' : 'disabled'}`);
}

function clearCommentary() {
    const container = document.querySelector('#commentary-container');
    if (container) {
        container.innerHTML = '<div class="commentary-empty">Commentary cleared</div>';
        console.log('🗑 Commentary cleared');
    }
}

// 8. Thought Trace Controls
function toggleAutoFollow() {
    window.autoFollowEnabled = !window.autoFollowEnabled;
    const btn = event.target;
    btn.classList.toggle('active');
    btn.textContent = window.autoFollowEnabled ? '👁' : '👁‍🗨';
    btn.title = window.autoFollowEnabled ? 'Disable Auto-Follow' : 'Enable Auto-Follow';
    console.log(`👁 Auto-follow ${window.autoFollowEnabled ? 'enabled' : 'disabled'}`);
}

function clearThoughtTrace() {
    const container = document.querySelector('#thought-trace-container');
    if (container) {
        container.innerHTML = '<div class="trace-empty">Thought trace cleared</div>';
        console.log('🗑 Thought trace cleared');
    }
}

// 9. System Log Controls
function toggleLogFilter() {
    const panel = document.querySelector('#log-filter-panel');
    if (panel) {
        panel.classList.toggle('expanded');
        console.log('🔍 Log filter toggled');
    }
}

function clearSystemLogs() {
    const container = document.querySelector('#system-logs');
    if (container) {
        container.innerHTML = '<div class="log-empty">System logs cleared</div>';
        console.log('🗑 System logs cleared');
    }
}

// 10. Advanced Controls
function openAdvancedPanel() {
    showModal('Advanced Controls', `
        <div class="advanced-panel">
            <h3>🔧 Advanced System Controls</h3>
            
            <div class="control-section">
                <h4>Debug Mode</h4>
                <button onclick="toggleDebugMode()">Toggle Debug</button>
                <button onclick="exportDebugInfo()">Export Debug Info</button>
            </div>
            
            <div class="control-section">
                <h4>Performance</h4>
                <button onclick="optimizePerformance()">Optimize Performance</button>
                <button onclick="clearCache()">Clear Cache</button>
            </div>
            
            <div class="control-section">
                <h4>Data Management</h4>
                <button onclick="exportAllData()">Export All Data</button>
                <button onclick="importData()">Import Data</button>
            </div>
        </div>
    `);
}

// =====================================
// TAB SYSTEM FIXES
// =====================================

function switchTab(tabName) {
    // Hide all tab content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
        tab.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const targetTab = document.getElementById(tabName) || document.querySelector(`[data-tab="${tabName}"]`);
    if (targetTab) {
        targetTab.style.display = 'block';
        targetTab.classList.add('active');
    }
    
    // Activate tab button
    const tabButton = document.querySelector(`[data-tab-target="${tabName}"]`) || 
                      document.querySelector(`[onclick*="${tabName}"]`);
    if (tabButton) {
        tabButton.classList.add('active');
    }
    
    // Load tab data from backend
    fetch(`/api/tab/${tabName}`)
        .then(response => response.json())
        .then(data => {
            console.log(`📑 Tab ${tabName} loaded:`, data);
            updateTabContent(tabName, data);
        })
        .catch(error => {
            console.warn(`⚠️ Could not load tab data for ${tabName}:`, error);
            // Continue with static content
        });
    
    console.log(`📑 Switched to tab: ${tabName}`);
}

function updateTabContent(tabName, data) {
    const tabElement = document.getElementById(tabName) || document.querySelector(`[data-tab="${tabName}"]`);
    if (!tabElement || !data) return;
    
    // Update content based on tab type
    switch(tabName) {
        case 'CONVERSATION':
            updateConversationTab(tabElement, data);
            break;
        case 'SYSTEMS':
            updateSystemsTab(tabElement, data);
            break;
        case 'VISUALIZATION':
            updateVisualizationTab(tabElement, data);
            break;
        default:
            console.log(`Tab ${tabName} loaded with data:`, data);
    }
}

// =====================================
// UTILITY FUNCTIONS
// =====================================

function showModal(title, content) {
    // Remove existing modal
    const existingModal = document.querySelector('.dawn-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'dawn-modal';
    modal.innerHTML = `
        <div class="modal-backdrop" onclick="closeModal()"></div>
        <div class="modal-content">
            <div class="modal-header">
                <h2>${title}</h2>
                <button class="modal-close" onclick="closeModal()">✕</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function closeModal() {
    const modal = document.querySelector('.dawn-modal');
    if (modal) {
        modal.remove();
    }
}

function handleButtonClick(action, data = {}) {
    console.log(`🔘 Button clicked: ${action}`, data);
    
    // Send to backend
    fetch(`/api/action/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log(`✅ Action ${action} completed:`, result);
        updateUI(result);
    })
    .catch(error => {
        console.error(`❌ Action ${action} failed:`, error);
        showNotification(`Action failed: ${action}`, 'error');
    });
}

function updateUI(data) {
    // Update consciousness state
    if (data.consciousness_state) {
        updateConsciousnessDisplay(data.consciousness_state);
    }
    
    // Update entropy
    if (data.entropy !== undefined) {
        const entropyElement = document.getElementById('entropy-value');
        if (entropyElement) {
            entropyElement.textContent = data.entropy.toFixed(3);
        }
    }
    
    // Update zone
    if (data.zone) {
        const zoneElement = document.getElementById('zone-indicator');
        if (zoneElement) {
            zoneElement.textContent = data.zone;
            zoneElement.className = `zone zone-${data.zone.toLowerCase()}`;
        }
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// =====================================
// INITIALIZATION
// =====================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DAWN GUI Fix Script Loaded');
    
    // Apply button handlers to elements that were missing them
    const unhandledButtons = [
        { selector: 'button[title="Toggle"]:not([onclick])', handler: 'toggleEntropyPanel()' },
        { selector: 'button[title="Export"]:not([onclick])', handler: 'exportEntropyData()' },
        { selector: 'button[title="Settings"]:not([onclick])', handler: 'openEntropySettings()' },
        { selector: 'button[title="Pause"]:not([onclick])', handler: 'pauseNeuralActivity()' },
        { selector: 'button[title="Reset"]:not([onclick])', handler: 'resetNeuralActivity()' },
        { selector: 'button[title="3D View"]:not([onclick])', handler: 'toggle3DView()' },
        { selector: 'button[title="Execute"]:not([onclick])', handler: 'executeSigilCommand()' },
        { selector: 'button[title="Clear"]:not([onclick])', handler: 'clearSigilInput()' },
        { selector: 'button[title="Auto-Rebloom"]:not([onclick])', handler: 'toggleAutoRebloom()' },
        { selector: 'button[title="Fullscreen"]:not([onclick])', handler: 'toggleFullscreenVisualization()' },
        { selector: 'button[title="Voice Mode"]:not([onclick])', handler: 'toggleVoiceMode()' },
        { selector: 'button[title="Auto-Follow"]:not([onclick])', handler: 'toggleAutoFollow()' },
        { selector: 'button[title="Filter"]:not([onclick])', handler: 'toggleLogFilter()' },
        { selector: 'button[title="Advanced"]:not([onclick])', handler: 'openAdvancedPanel()' }
    ];
    
    // Apply handlers
    unhandledButtons.forEach(buttonConfig => {
        const buttons = document.querySelectorAll(buttonConfig.selector);
        buttons.forEach(button => {
            button.setAttribute('onclick', buttonConfig.handler);
        });
    });
    
    console.log(`✅ Applied handlers to ${unhandledButtons.length} button types`);
    
    // Initialize tab system
    initializeTabSystem();
    
    console.log('🎉 DAWN GUI Fix Complete - All buttons should now be functional!');
});

function initializeTabSystem() {
    // Add click handlers to tab buttons
    document.querySelectorAll('[data-tab-target]').forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab-target');
            switchTab(tabName);
        });
    });
    
    // Initialize first tab
    const firstTab = document.querySelector('[data-tab-target]');
    if (firstTab) {
        const firstTabName = firstTab.getAttribute('data-tab-target');
        switchTab(firstTabName);
    }
} 