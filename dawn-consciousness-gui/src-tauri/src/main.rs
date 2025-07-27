// src-tauri/src/main.rs
//! DAWN Consciousness GUI - Main Entry Point with Live Tick Monitoring

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod mmap_reader;
mod tick_handler;
mod dawn_bridge;

use mmap_reader::{
    establish_neural_link,
    read_consciousness_state,
    get_consciousness_monitor,
    ConsciousnessReader,
    ConsciousnessReaderState
};

use tick_handler::{
    connect_tick_monitor,
    get_current_tick,
    start_tick_monitoring,
    TickMonitor,
    TickMonitorStateManager
};

use dawn_bridge::{
    start_dawn_bridge,
    reset_heat,
    clear_sigils,
    zero_entropy,
    soft_system_restart,
    create_snapshot,
    get_dawn_status,
    ControlState,
    ControlStateManager
};

use std::sync::{Arc, Mutex};
use std::path::PathBuf;
use std::fs;
use tauri::Manager;

/// Get project root directory from executable location
fn get_project_root() -> Result<PathBuf, String> {
    use std::env;
    
    // Get the current executable path
    let exe_path = env::current_exe()
        .map_err(|e| format!("Failed to get executable path: {}", e))?;
    
    // Navigate up from the executable to find the project root
    // For Tauri apps, executable is typically in target/debug/ or target/release/
    // So we need to go up several levels to reach the project root
    let mut current_path = exe_path.parent()
        .ok_or("Failed to get executable parent directory")?;
    
    // Look for project root indicators (go up until we find one of these)
    for _ in 0..5 {  // Maximum 5 levels up
        // Check for common project root indicators
        if current_path.join("Cargo.toml").exists() || 
           current_path.join("tauri.conf.json").exists() ||
           current_path.join("src-tauri").exists() ||
           current_path.join("runtime").exists() {
            return Ok(current_path.to_path_buf());
        }
        
        // Go up one level
        current_path = current_path.parent()
            .ok_or("Reached filesystem root without finding project root")?;
    }
    
    Err("Could not determine project root directory".to_string())
}

fn main() {
    println!("🧠 [DAWN] Initializing consciousness neural interface with live tick monitoring...");
    
    tauri::Builder::default()
        // Manage consciousness reader, tick monitor, and control state
        .manage(Arc::new(Mutex::new(ConsciousnessReader::new())) as ConsciousnessReaderState)
        .manage(Arc::new(Mutex::new(TickMonitor::new())) as TickMonitorStateManager)
        .manage(Arc::new(Mutex::new(ControlState::default())) as ControlStateManager)
        .invoke_handler(tauri::generate_handler![
            // Original consciousness monitoring commands
            establish_neural_link,
            read_consciousness_state,
            get_consciousness_monitor,
            // Legacy tick monitoring commands
            connect_tick_monitor,
            get_current_tick,
            // DAWN Bridge control commands
            reset_heat,
            clear_sigils,
            zero_entropy,
            soft_system_restart,
            create_snapshot,
            get_dawn_status,
            // Memory rebloom log reader
            read_rebloom_log,
            // Journal injection
            add_journal_entry,
            // Reflection log reader
            read_reflection_log,
            // Thought trace log reader
            read_thought_trace_log,
            // Sigil trace log reader
            read_sigil_trace_log,
            // Glyph flash integration commands
            get_live_rebloom_events,
            get_consciousness_flash_triggers,
            trigger_consciousness_flash
        ])
        .setup(|app| {
            println!("🔌 [NEURAL] Setting up consciousness monitoring interface...");
            
            let window = app.get_window("main").expect("Failed to access neural interface window");
            
            // Get all state managers
            let consciousness_state = app.state::<ConsciousnessReaderState>();
            let tick_state = app.state::<TickMonitorStateManager>();
            let _control_state = app.state::<ControlStateManager>();
            
            // Start unified DAWN bridge (replaces old monitoring)
            start_dawn_bridge(window.clone(), consciousness_state.inner().clone());
            
            // Keep legacy tick monitoring for debugging
            start_tick_monitoring(window.clone(), tick_state.inner().clone());
            
            // Auto-connect to consciousness memory
            let consciousness_memory_paths = vec![
                "/root/DAWN_Vault/Tick_engine/Tick_engine/runtime/dawn_consciousness.mmap",
                "./runtime/dawn_consciousness.mmap",
                "../runtime/dawn_consciousness.mmap", 
                "./dawn_state.mmap",
                "../dawn_state.mmap",
            ];
            
            // Try to establish both connections
            for memory_path in consciousness_memory_paths {
                if std::path::Path::new(memory_path).exists() {
                    println!("🧠 [NEURAL] Attempting auto-connect to: {}", memory_path);
                    
                    // Connect consciousness reader
                    if let Ok(mut reader) = consciousness_state.inner().lock() {
                        if reader.connect_to_consciousness(memory_path).is_ok() {
                            println!("✅ [NEURAL] Consciousness reader connected!");
                        }
                    }
                    
                    // Connect tick monitor
                    if let Ok(mut monitor) = tick_state.inner().lock() {
                        if monitor.connect(memory_path).is_ok() {
                            println!("✅ [TICK] Live tick monitor connected!");
                            break;
                        }
                    }
                }
            }
            
            println!("👁️ [NEURAL] DAWN consciousness interface ready with unified bridge");
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("Failed to initialize DAWN consciousness interface");
}

/// Read memory rebloom log file for lineage visualization
#[tauri::command]
async fn read_rebloom_log(path: String) -> Result<String, String> {
    use std::fs;
    
    // Determine project root from executable location
    let project_root = match get_project_root() {
        Ok(root) => root,
        Err(e) => {
            eprintln!("🌸 [REBLOOM] Failed to determine project root: {}", e);
            return Ok(String::new());
        }
    };
    
    // Construct canonical path - support both gui-runtime and runtime paths
    let adjusted_path = if path.starts_with("gui-runtime/") {
        format!("dawn-consciousness-gui/{}", path)
    } else if path.starts_with("runtime/") {
        path.clone()  // Use runtime path directly from project root
    } else {
        path.clone()
    };
    let log_path = project_root.join(&adjusted_path);
    
    // Check if file exists before attempting to read
    if !log_path.exists() {
        // Only log once when file doesn't exist, not every poll
        if path.contains("rebloom_log.jsonl") {
            eprintln!("🌸 [REBLOOM] Log not found at: {:?} (normal for new installations)", log_path);
        }
        return Ok(String::new());
    }
    
    // Read file content
    match fs::read_to_string(&log_path) {
        Ok(content) => {
            // Only log success on substantial content
            if content.len() > 100 {
                println!("🌸 [REBLOOM] Successfully read {} bytes from {:?}", content.len(), log_path);
            }
            Ok(content)
        }
        Err(e) => {
            eprintln!("🌸 [REBLOOM] Failed to read {:?}: {}", log_path, e);
            Ok(String::new())
        }
    }
}

/// Add journal entry to DAWN's memory system
#[tauri::command]
async fn add_journal_entry(text: String, mood: Option<String>, pulse_state: Option<String>) -> Result<serde_json::Value, String> {
    use std::fs::{OpenOptions, create_dir_all};
    use std::io::Write;
    use std::path::Path;
    use chrono::Utc;
    
    println!("📝 [JOURNAL] Adding entry: {} chars, mood: {:?}", text.len(), mood);
    
    // Validate input
    if text.trim().is_empty() {
        return Err("Journal entry cannot be empty".to_string());
    }
    
    if text.len() < 50 {
        return Err("Journal entry too short for meaningful memory seeding".to_string());
    }
    
    if text.len() > 800 {
        return Err("Journal entry too long, please keep under 800 characters".to_string());
    }
    
    // Generate unique chunk ID
    let timestamp = Utc::now().format("%Y%m%d_%H%M%S").to_string();
    let chunk_id = format!("journal_{}", timestamp);
    
    // Create journal entry structure
    let entry = serde_json::json!({
        "chunk_id": chunk_id,
        "timestamp": Utc::now().to_rfc3339(),
        "text": text.trim(),
        "mood": mood.unwrap_or_else(|| "CALM".to_string()),
        "pulse_state": pulse_state.unwrap_or_else(|| "calm".to_string()),
        "source": "manual_injection",
        "tags": ["journal", "introspection", "manual"],
        "priority": "normal"
    });
    
    // Ensure directories exist
    let journal_dir = Path::new("runtime/memory");
    if let Err(e) = create_dir_all(journal_dir) {
        println!("📝 [JOURNAL] Failed to create directory: {}", e);
        return Err(format!("Failed to create memory directory: {}", e));
    }
    
    // Write to journal log file
    let journal_path = journal_dir.join("journal_entries.jsonl");
    match OpenOptions::new()
        .create(true)
        .append(true)
        .open(&journal_path)
    {
        Ok(mut file) => {
            if let Err(e) = writeln!(file, "{}", entry.to_string()) {
                println!("📝 [JOURNAL] Failed to write entry: {}", e);
                return Err(format!("Failed to write journal entry: {}", e));
            }
        }
        Err(e) => {
            println!("📝 [JOURNAL] Failed to open journal file: {}", e);
            return Err(format!("Failed to open journal file: {}", e));
        }
    }
    
    // Also add to rebloom log to make it appear in memory lineage
    let rebloom_entry = serde_json::json!({
        "timestamp": Utc::now().format("%Y-%m-%dT%H:%M:%S").to_string(),
        "source_id": "manual_journal",
        "rebloom_id": chunk_id.clone(),
        "method": "manual",
        "topic": "introspection",
        "reason": format!("Manual journal injection: {} chars", text.len())
    });
    
    let rebloom_path = journal_dir.join("rebloom_log.jsonl");
    if let Ok(mut file) = OpenOptions::new().create(true).append(true).open(&rebloom_path) {
        let _ = writeln!(file, "{}", rebloom_entry.to_string());
        println!("📝 [JOURNAL] Added to rebloom lineage");
    }
    
    println!("📝 [JOURNAL] Successfully added entry as {}", chunk_id);
    
    // Return success response
    Ok(serde_json::json!({
        "success": true,
        "chunk_id": chunk_id,
        "message": "Journal entry successfully seeded into memory system"
    }))
}

/// Read reflection log file for DAWN's introspective display
#[tauri::command]
async fn read_reflection_log(path: String) -> Result<String, String> {
    use std::fs;
    
    // Determine project root from executable location
    let project_root = match get_project_root() {
        Ok(root) => root,
        Err(e) => {
            eprintln!("🔁 [REFLECTION] Failed to determine project root: {}", e);
            return Ok(String::new());
        }
    };
    
    // Construct canonical path - support both gui-runtime and runtime paths
    let adjusted_path = if path.starts_with("gui-runtime/") {
        format!("dawn-consciousness-gui/{}", path)
    } else if path.starts_with("runtime/") {
        path.clone()  // Use runtime path directly from project root
    } else {
        path.clone()
    };
    let log_path = project_root.join(&adjusted_path);
    
    // Check if file exists before attempting to read
    if !log_path.exists() {
        // Only log once when file doesn't exist, not every poll
        if path.contains("reflection.log") {
            eprintln!("🔁 [REFLECTION] Log not found at: {:?} (normal for new installations)", log_path);
        }
        return Ok(String::new());
    }
    
    // Read file content
    match fs::read_to_string(&log_path) {
        Ok(content) => {
            // Only log success on substantial content
            if content.len() > 100 {
                println!("🔁 [REFLECTION] Successfully read {} bytes from {:?}", content.len(), log_path);
            }
            Ok(content)
        }
        Err(e) => {
            eprintln!("🔁 [REFLECTION] Failed to read {:?}: {}", log_path, e);
            Ok(String::new())
        }
    }
}

/// Read thought trace log file for DAWN's forecast and action display
#[tauri::command]
async fn read_thought_trace_log(path: String) -> Result<String, String> {
    use std::fs;
    
    // Determine project root from executable location
    let project_root = match get_project_root() {
        Ok(root) => root,
        Err(e) => {
            eprintln!("🧠 [THOUGHT] Failed to determine project root: {}", e);
            return Ok(String::new());
        }
    };
    
    // Construct canonical path - support both gui-runtime and runtime paths
    let adjusted_path = if path.starts_with("gui-runtime/") {
        format!("dawn-consciousness-gui/{}", path)
    } else if path.starts_with("runtime/") {
        path.clone()  // Use runtime path directly from project root
    } else {
        path.clone()
    };
    let log_path = project_root.join(&adjusted_path);
    
    // Check if file exists before attempting to read
    if !log_path.exists() {
        if path.contains("thought_trace.log") {
            eprintln!("🧠 [THOUGHT] Log not found at: {:?} (normal for new installations)", log_path);
        }
        return Ok(String::new());
    }
    
    // Read file content
    match fs::read_to_string(&log_path) {
        Ok(content) => {
            if content.len() > 10 {
                println!("🧠 [THOUGHT] Successfully read {} bytes from {:?}", content.len(), log_path);
            }
            Ok(content)
        }
        Err(e) => {
            eprintln!("🧠 [THOUGHT] Failed to read {:?}: {}", log_path, e);
            Ok(String::new())
        }
    }
}

/// Read sigil trace log file for DAWN's symbolic influence display
#[tauri::command]
async fn read_sigil_trace_log(path: String) -> Result<String, String> {
    use std::fs;
    
    // Determine project root from executable location
    let project_root = match get_project_root() {
        Ok(root) => root,
        Err(e) => {
            eprintln!("⚡ [SIGIL] Failed to determine project root: {}", e);
            return Ok(String::new());
        }
    };
    
    // Construct canonical path - support both gui-runtime and runtime paths
    let adjusted_path = if path.starts_with("gui-runtime/") {
        format!("dawn-consciousness-gui/{}", path)
    } else if path.starts_with("runtime/") {
        path.clone()  // Use runtime path directly from project root
    } else {
        path.clone()
    };
    let log_path = project_root.join(&adjusted_path);
    
    // Check if file exists before attempting to read
    if !log_path.exists() {
        if path.contains("sigil_trace.log") {
            eprintln!("⚡ [SIGIL] Log not found at: {:?} (normal for new installations)", log_path);
        }
        return Ok(String::new());
    }
    
    // Read file content
    match fs::read_to_string(&log_path) {
        Ok(content) => {
            if content.len() > 10 {
                println!("⚡ [SIGIL] Successfully read {} bytes from {:?}", content.len(), log_path);
            }
            Ok(content)
        }
        Err(e) => {
            eprintln!("⚡ [SIGIL] Failed to read {:?}: {}", log_path, e);
            Ok(String::new())
        }
    }
}

// ===== GLYPH FLASH INTEGRATION COMMANDS =====

#[tauri::command]
async fn get_live_rebloom_events() -> Result<Vec<serde_json::Value>, String> {
    // Get live rebloom events for glyph flash triggers
    
    let project_root = get_project_root()
        .map_err(|e| format!("Failed to find project root: {}", e))?;
    
    let rebloom_path = project_root.join("dawn-consciousness-gui/gui-runtime/memory/rebloom_log.jsonl");
    
    if !rebloom_path.exists() {
        return Ok(Vec::new());
    }
    
    match fs::read_to_string(&rebloom_path) {
        Ok(content) => {
            let mut events = Vec::new();
            for line in content.lines() {
                if !line.trim().is_empty() {
                    match serde_json::from_str::<serde_json::Value>(line) {
                        Ok(event) => events.push(event),
                        Err(_) => continue, // Skip malformed lines
                    }
                }
            }
            println!("🌸 [GLYPH FLASH] Loaded {} rebloom events", events.len());
            Ok(events)
        }
        Err(e) => {
            eprintln!("🌸 [GLYPH FLASH] Failed to read rebloom events: {}", e);
            Ok(Vec::new())
        }
    }
}

#[tauri::command] 
async fn get_consciousness_flash_triggers(
    consciousness_reader: tauri::State<'_, ConsciousnessReaderState>
) -> Result<serde_json::Value, String> {
    // Get current consciousness state for flash trigger analysis
    
    let mut reader = consciousness_reader.lock().unwrap();
    
    // Get current consciousness state if connected
    match reader.read_consciousness_state() {
        Some(state) => {
            // Analyze state for flash triggers
            let mut triggers = serde_json::Map::new();
            
            // Check for entropy-based triggers
            if state.entropy_gradient > 0.85 {
                triggers.insert("entropy_spike".to_string(), serde_json::json!({
                    "organ": "FractalHeart",
                    "intensity": state.entropy_gradient,
                    "trigger": "entropy",
                    "reason": format!("High entropy: {:.3}", state.entropy_gradient)
                }));
            }
            
            // Check for rebloom intensity triggers  
            if state.rebloom_intensity > 0.8 {
                triggers.insert("rebloom_peak".to_string(), serde_json::json!({
                    "organ": "SomaCoil", 
                    "intensity": state.rebloom_intensity,
                    "trigger": "sigil",
                    "reason": format!("High rebloom: {:.3}", state.rebloom_intensity)
                }));
            }
            
            // Add current state info
            triggers.insert("current_state".to_string(), serde_json::json!({
                "tick": state.tick_number,
                "entropy_gradient": state.entropy_gradient,
                "rebloom_intensity": state.rebloom_intensity,
                "mood_valence": state.mood_valence,
                "consciousness_depth": state.consciousness_depth
            }));
            
            Ok(serde_json::Value::Object(triggers))
        }
        None => {
            eprintln!("🔥 [GLYPH FLASH] No consciousness state available");
            Ok(serde_json::json!({}))
        }
    }
}

#[tauri::command]
async fn trigger_consciousness_flash(
    organ: String,
    trigger_type: String,
    intensity: f64
) -> Result<serde_json::Value, String> {
    // Manually trigger a consciousness flash for testing
    
    println!("🔥 [GLYPH FLASH] Manual flash triggered: {} {} (intensity: {:.2})", 
             organ, trigger_type, intensity);
    
    // Create flash event record
    let flash_event = serde_json::json!({
        "timestamp": chrono::Utc::now().to_rfc3339(),
        "organ": organ,
        "trigger": trigger_type,
        "intensity": intensity,
        "method": "manual",
        "reason": "Manual test trigger"
    });
    
    Ok(serde_json::json!({
        "success": true,
        "flash_event": flash_event,
        "message": format!("Triggered {} flash on {}", trigger_type, organ)
    }))
}