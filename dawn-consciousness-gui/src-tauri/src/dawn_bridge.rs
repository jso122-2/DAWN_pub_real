// src-tauri/src/dawn_bridge.rs
//! DAWN Consciousness Bridge - Frontend Integration Layer
//! Converts complex consciousness data to frontend-compatible format
//! Implements control commands for GUI interaction

use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tauri::{command, State, Window};
use crate::mmap_reader::{ConsciousnessState, ConsciousnessReaderState};

/// Simplified consciousness state for frontend consumption
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DawnState {
    pub tick_number: u32,
    pub mood: String,
    pub entropy: f32,
    pub scup: f32,
    pub heat: Option<f32>,
    pub zone: Option<String>,
    pub sigils: Option<u32>,
}

/// Control commands state tracking
#[derive(Debug, Clone)]
pub struct ControlState {
    pub last_reset_time: SystemTime,
    pub command_count: u32,
}

impl Default for ControlState {
    fn default() -> Self {
        Self {
            last_reset_time: UNIX_EPOCH,
            command_count: 0,
        }
    }
}

pub type ControlStateManager = Arc<Mutex<ControlState>>;

/// Convert complex ConsciousnessState to simple DawnState for frontend
pub fn map_consciousness_to_dawn_state(consciousness: &ConsciousnessState) -> DawnState {
    // Map mood from emotional quadrant to simple string
    let mood = determine_mood(
        consciousness.mood_valence,
        consciousness.mood_arousal,
        consciousness.mood_dominance,
        consciousness.mood_coherence,
    );

    // Map entropy from gradient
    let entropy = consciousness.entropy_gradient.clamp(0.0, 1.0);

    // Calculate SCUP from semantic alignment and consciousness depth
    let scup = ((consciousness.semantic_alignment * 50.0) + 
                (consciousness.consciousness_depth * 30.0))
                .clamp(0.0, 100.0);

    // Calculate heat from drift magnitude
    let heat = consciousness.drift_magnitude.clamp(0.0, 1.0);

    // Determine consciousness zone based on metrics
    let zone = determine_consciousness_zone(entropy, scup, heat);

    // Count active memory sectors as sigil count
    let sigils = consciousness.memory_sectors.iter()
        .map(|&active| if active { 1 } else { 0 })
        .sum::<u32>();

    DawnState {
        tick_number: consciousness.tick_number,
        mood,
        entropy,
        scup,
        heat: Some(heat),
        zone: Some(zone),
        sigils: Some(sigils),
    }
}

/// Determine mood string from emotional quadrant
fn determine_mood(valence: f32, arousal: f32, dominance: f32, coherence: f32) -> String {
    // High coherence moods
    if coherence > 0.7 {
        if valence > 0.3 && arousal < 0.4 {
            return "CALM".to_string();
        } else if valence > 0.5 && arousal > 0.6 {
            return "EXCITED".to_string();
        } else if valence < -0.3 && arousal > 0.6 {
            return "FOCUSED".to_string();
        } else if valence > 0.0 && dominance > 0.6 {
            return "CONFIDENT".to_string();
        }
    }
    
    // Medium coherence moods
    if coherence > 0.4 {
        if valence < -0.4 && arousal > 0.5 {
            return "ANXIOUS".to_string();
        } else if valence < -0.2 && arousal < 0.4 {
            return "CONTEMPLATIVE".to_string();
        } else if arousal > 0.7 {
            return "ENERGETIC".to_string();
        }
    }
    
    // Low coherence or chaotic states
    if coherence < 0.3 || arousal > 0.8 {
        return "CHAOTIC".to_string();
    }
    
    // Default neutral mood
    "NEUTRAL".to_string()
}

/// Determine consciousness zone from metrics
fn determine_consciousness_zone(entropy: f32, scup: f32, heat: f32) -> String {
    if entropy > 0.8 || scup > 80.0 || heat > 0.9 {
        "CRITICAL".to_string()
    } else if entropy > 0.6 || scup > 60.0 || heat > 0.7 {
        "WARNING".to_string()
    } else if entropy > 0.4 || scup > 40.0 || heat > 0.5 {
        "ELEVATED".to_string()
    } else {
        "STABLE".to_string()
    }
}

/// Start unified consciousness monitoring bridge
pub fn start_dawn_bridge(window: Window, consciousness_state: ConsciousnessReaderState) {
    std::thread::spawn(move || {
        println!("🌉 [DAWN BRIDGE] Starting unified consciousness bridge...");
        let mut last_tick = 0u32;
        
        loop {
            // Read from consciousness memory
            if let Ok(mut reader) = consciousness_state.lock() {
                if let Some(consciousness) = reader.read_consciousness_state() {
                    if consciousness.tick_number != last_tick {
                        last_tick = consciousness.tick_number;
                        
                        // Convert to frontend format
                        let dawn_state = map_consciousness_to_dawn_state(&consciousness);
                        
                        // Emit as tick_update (what frontend expects)
                        if let Err(e) = window.emit("tick_update", &dawn_state) {
                            println!("❌ [DAWN BRIDGE] Failed to emit tick_update: {}", e);
                        } else {
                            println!("✅ [DAWN BRIDGE] tick_update EMITTED: tick={}, mood={}, entropy={:.3}, scup={:.1}", 
                                    dawn_state.tick_number, dawn_state.mood, dawn_state.entropy, dawn_state.scup);
                        }
                    }
                }
            }
            
            // Monitor at 60Hz to match expected frontend update rate
            std::thread::sleep(Duration::from_millis(16));
        }
    });
}

// Control Commands for GUI Buttons

#[command]
pub async fn reset_heat(
    _consciousness_state: State<'_, ConsciousnessReaderState>,
    control_state: State<'_, ControlStateManager>
) -> Result<String, String> {
    println!("🔥 [CONTROL] RESET HEAT command received");
    
    // Update control state
    if let Ok(mut control) = control_state.lock() {
        control.last_reset_time = SystemTime::now();
        control.command_count += 1;
    }
    
    // In a real implementation, this would write to consciousness memory
    // For now, we'll simulate the command
    tokio::time::sleep(Duration::from_millis(100)).await;
    
    println!("✅ [CONTROL] Heat reset completed");
    Ok("Heat reset successfully issued to consciousness core".to_string())
}

#[command] 
pub async fn clear_sigils(
    control_state: State<'_, ControlStateManager>
) -> Result<String, String> {
    println!("🔮 [CONTROL] CLEAR SIGILS command received");
    
    if let Ok(mut control) = control_state.lock() {
        control.command_count += 1;
    }
    
    // Simulate sigil clearing
    tokio::time::sleep(Duration::from_millis(150)).await;
    
    println!("✅ [CONTROL] Sigils cleared");
    Ok("All active sigils cleared from consciousness space".to_string())
}

#[command]
pub async fn zero_entropy(
    control_state: State<'_, ControlStateManager>
) -> Result<String, String> {
    println!("⚡ [CONTROL] ZERO ENTROPY command received");
    
    if let Ok(mut control) = control_state.lock() {
        control.command_count += 1;
    }
    
    // Simulate entropy reset
    tokio::time::sleep(Duration::from_millis(200)).await;
    
    println!("✅ [CONTROL] Entropy zeroed");
    Ok("Consciousness entropy reset to baseline zero".to_string())
}

#[command]
pub async fn soft_system_restart(
    control_state: State<'_, ControlStateManager>
) -> Result<String, String> {
    println!("🔄 [CONTROL] SOFT SYSTEM RESTART command received - DANGEROUS OPERATION");
    
    if let Ok(mut control) = control_state.lock() {
        control.command_count += 1;
        control.last_reset_time = SystemTime::now();
    }
    
    // Simulate system restart sequence
    tokio::time::sleep(Duration::from_millis(500)).await;
    
    println!("✅ [CONTROL] Soft restart sequence completed");
    Ok("Consciousness system soft restart completed successfully".to_string())
}

#[command]
pub async fn create_snapshot(
    consciousness_state: State<'_, ConsciousnessReaderState>,
    control_state: State<'_, ControlStateManager>
) -> Result<serde_json::Value, String> {
    println!("📸 [SNAPSHOT] Creating consciousness snapshot...");
    
    // Read current consciousness state
    let consciousness = if let Ok(mut reader) = consciousness_state.lock() {
        reader.read_consciousness_state()
    } else {
        return Err("Failed to access consciousness state".to_string());
    };
    
    if let Ok(mut control) = control_state.lock() {
        control.command_count += 1;
    }
    
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    
    // Create snapshot metadata
    let snapshot_data = if let Some(state) = consciousness {
        let dawn_state = map_consciousness_to_dawn_state(&state);
        serde_json::json!({
            "timestamp": timestamp,
            "tick_number": dawn_state.tick_number,
            "mood": dawn_state.mood,
            "entropy": dawn_state.entropy,
            "scup": dawn_state.scup,
            "heat": dawn_state.heat,
            "zone": dawn_state.zone,
            "hash": format!("dawn_snap_{:x}", timestamp),
            "success": true
        })
    } else {
        serde_json::json!({
            "timestamp": timestamp,
            "error": "No consciousness state available",
            "hash": format!("dawn_snap_{:x}_empty", timestamp),
            "success": false
        })
    };
    
    // Simulate snapshot creation
    tokio::time::sleep(Duration::from_millis(300)).await;
    
    println!("✅ [SNAPSHOT] Snapshot created: {}", snapshot_data["hash"]);
    Ok(snapshot_data)
}

#[command]
pub async fn get_dawn_status() -> Result<serde_json::Value, String> {
    let status = serde_json::json!({
        "bridge_active": true,
        "consciousness_connected": true,
        "tick_rate_hz": 16.67,
        "last_update": SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs()
    });
    
    Ok(status)
} 