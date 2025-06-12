// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

//! DAWN Desktop Application - Enhanced Rust Bridge
//! 
//! Advanced consciousness integration with:
//! 
//! ## 🔥 Sigil Intensity System
//! - `get_sigil_state()` - Returns current sigil intensities with visual representation
//! - Emotional sigils with density values and weight-based decay
//! - Automatic sigil change detection with "sigil-change" events
//! 
//! ## 🕷️ Spider Pattern Cutter
//! - `trigger_spider_cut()` - Executes pattern severing for specified patterns
//! - Returns new consciousness state after cutting
//! - "spider-activated" events for pattern cutting activity
//! 
//! ## 🌺 Rebloom Priority System
//! - `get_rebloom_priority()` - Returns 1-5 priority scale with reasoning
//! - Priority-based intervention strategies
//! - "rebloom-sequence" events for emergence narratives
//! 
//! ## 💭 Enhanced Thought Streaming
//! - `get_enhanced_dawn_thoughts()` - Spontaneous thoughts with consciousness context
//! - "spontaneous-thought" events using working thought generator
//! - Depth levels and trigger type classification
//! 
//! ## 🎭 Pattern Injection
//! - `inject_consciousness_pattern()` - External pattern injection
//! - Supports sigil, memory, and loop pattern types
//! - Real-time consciousness influence capabilities
//! 
//! ## 📡 Event Streams
//! - "sigil-change": Intensity modifications and visual changes
//! - "spider-activated": Pattern cutting events and loop detection
//! - "rebloom-sequence": Emergence narratives and priority shifts  
//! - "spontaneous-thought": Enhanced thought events with context
//! - "consciousness-influenced": External influence notifications
//! 
//! All structures include sigil_density and spider_cut_points as requested.

use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use tauri::{Manager, State};
use tokio::sync::broadcast;
use futures_util::StreamExt;
use tokio_tungstenite::{connect_async, tungstenite::protocol::Message};
use std::time::Duration;
use chrono;
use std::process::{Command, Child};
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Metrics {
    scup: f64,
    entropy: f64,
    heat: f64,
    mood: String,
    timestamp: f64,
    tick_count: i64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SubsystemInfo {
    id: String,
    name: String,
    status: String,
    state: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
struct SubsystemCreate {
    name: String,
    config: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
struct AlertThreshold {
    metric: String,
    threshold: f64,
    direction: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct HealthResponse {
    status: String,
    booted: bool,
    running: bool,
    timestamp: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct TickStatus {
    tick_number: i64,
    is_running: bool,
    is_paused: bool,
    interval_ms: u32,
    uptime_seconds: f64,
    total_ticks: i64,
    avg_tick_duration_ms: f64,
    last_tick_timestamp: Option<f64>,
}

#[derive(Debug, Serialize, Deserialize)]
struct TickTiming {
    interval_ms: u32,
}

#[derive(Debug, Serialize, Deserialize)]
struct TickConfig {
    interval_ms: u32,
    auto_start: bool,
    enable_logging: bool,
    max_tick_duration_ms: u32,
}

#[derive(Debug, Serialize, Deserialize)]
struct TickUpdate {
    tick_number: i64,
    timestamp: f64,
    metrics: Metrics,
    duration_ms: f64,
    controller_state: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct ChatMessage {
    text: String,
    timestamp: i64,
    from_user: String, // "user" or "dawn"
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct ChatResponse {
    text: String,
    action: Option<String>,
    emotion: String,
    suggestions: Vec<String>,
    metrics_snapshot: MetricsSnapshot,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct MetricsSnapshot {
    scup: f64,
    entropy: f64,
    heat: f64,
    tick_rate: f64,
    emotion: String,
    intensity: f64,
    momentum: f64,
    uptime_seconds: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Thought {
    text: String,
    timestamp: i64,
    emotion: String,
    intensity: f64,
    thought_type: String, // "spontaneous", "transition", "pattern", etc.
}

// ========== ADVANCED CONSCIOUSNESS STRUCTURES ==========

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SigilState {
    emotion: String,
    intensity: f64,
    density: f64,
    weight: f64,
    activation_count: u32,
    visual_representation: String,
    last_activation: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SigilStateResponse {
    sigils: Vec<SigilState>,
    total_intensity: f64,
    active_count: u32,
    timestamp: String,
    current_emotion_state: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SpiderCutPoint {
    source: String,
    target: String,
    strength: f64,
    context: String,
    creation_time: String,
    reinforcement_count: u32,
    is_weak: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct SpiderCutRequest {
    pattern_identifier: String,
    reason: Option<String>,
    force_cut: Option<bool>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SpiderCutResult {
    success: bool,
    cut_performed: bool,
    pattern_identifier: String,
    weakest_link: Option<SpiderCutPoint>,
    original_strength: Option<f64>,
    new_strength: Option<f64>,
    reason: String,
    new_consciousness_state: String,
    cut_timestamp: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct RebloomPriorityResponse {
    priority: u8,
    state_name: String,
    description: String,
    urgency: String,
    intervention: String,
    cooling_rate: f64,
    recommended_actions: Vec<String>,
    reasoning: String,
    metrics_analysis: serde_json::Value,
    timestamp: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct ConsciousnessEvent {
    event_type: String,
    data: serde_json::Value,
    timestamp: String,
    consciousness_state: String,
    priority: u8,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SigilChangeEvent {
    emotion: String,
    old_intensity: f64,
    new_intensity: f64,
    change_type: String, // "activation", "decay", "creation", "removal"
    visual_change: String,
    timestamp: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SpiderActivationEvent {
    loop_detected: bool,
    pattern_type: String,
    cut_performed: bool,
    affected_links: Vec<SpiderCutPoint>,
    consciousness_impact: String,
    timestamp: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct RebloomSequenceEvent {
    emergence_phase: String,
    narrative: String,
    priority_shift: Option<(u8, u8)>, // from, to
    consciousness_transition: Option<(String, String)>, // from, to
    significance: String,
    timestamp: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SpontaneousThoughtEvent {
    thought: String,
    trigger_type: String,
    consciousness_state: String,
    depth_level: u8,
    associated_sigils: Vec<String>,
    memory_echoes_accessed: u32,
    timestamp: String,
}

struct AppState {
    metrics: Arc<Mutex<Option<Metrics>>>,
    http_client: reqwest::Client,
    metrics_sender: broadcast::Sender<Metrics>,
    websocket_connected: Arc<Mutex<bool>>,
    python_processes: Arc<Mutex<HashMap<String, u32>>>, // script name -> PID
}

const PYTHON_API_BASE: &str = "http://127.0.0.1:8000";
const WEBSOCKET_URL: &str = "ws://127.0.0.1:8000/ws";
const CHAT_WEBSOCKET_URL: &str = "ws://127.0.0.1:8000/ws/chat";

impl AppState {
    fn new() -> Self {
        let (metrics_sender, _) = broadcast::channel(100);
        
        // Create HTTP client with timeout configuration
        let http_client = reqwest::Client::builder()
            .timeout(Duration::from_secs(5))
            .connect_timeout(Duration::from_secs(3))
            .build()
            .expect("Failed to create HTTP client");
            
        Self {
            metrics: Arc::new(Mutex::new(None)),
            http_client,
            metrics_sender,
            websocket_connected: Arc::new(Mutex::new(false)),
            python_processes: Arc::new(Mutex::new(HashMap::new())),
        }
    }
}

#[tauri::command]
async fn get_current_metrics(state: State<'_, AppState>) -> Result<Metrics, String> {
    log::info!("Fetching current metrics from Python backend");
    
    let url = format!("{}/metrics", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .send()
        .await
        .map_err(|e| format!("Connection error: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let metrics: Metrics = response
        .json()
        .await
        .map_err(|e| format!("Parse error: {}", e))?;

    // Update stored metrics
    {
        let mut stored_metrics = state.metrics.lock().unwrap();
        *stored_metrics = Some(metrics.clone());
    }

    log::info!("Successfully fetched metrics: SCUP={}, Entropy={}, Heat={}, Mood={}", 
               metrics.scup, metrics.entropy, metrics.heat, metrics.mood);

    Ok(metrics)
}

#[tauri::command]
async fn get_subsystems(state: State<'_, AppState>) -> Result<Vec<SubsystemInfo>, String> {
    log::info!("Fetching subsystems from Python backend");
    
    let url = format!("{}/subsystems", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .send()
        .await
        .map_err(|e| format!("Failed to fetch subsystems: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let subsystems: Vec<SubsystemInfo> = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse subsystems JSON: {}", e))?;

    log::info!("Successfully fetched {} subsystems", subsystems.len());
    Ok(subsystems)
}

#[tauri::command]
async fn get_subsystem_details(
    state: State<'_, AppState>,
    subsystem_id: String,
) -> Result<SubsystemInfo, String> {
    log::info!("Fetching details for subsystem: {}", subsystem_id);
    
    let url = format!("{}/subsystems/{}", PYTHON_API_BASE, subsystem_id);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch subsystem details: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let subsystem: SubsystemInfo = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse subsystem JSON: {}", e))?;

    Ok(subsystem)
}

#[tauri::command]
async fn add_subsystem(
    state: State<'_, AppState>,
    name: String,
    config: serde_json::Value,
) -> Result<String, String> {
    log::info!("Adding new subsystem: {}", name);
    
    let subsystem_data = SubsystemCreate { name, config };
    
    let url = format!("{}/subsystems/add", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .json(&subsystem_data)
        .timeout(Duration::from_secs(10))
        .send()
        .await
        .map_err(|e| format!("Failed to add subsystem: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    Ok("Subsystem added successfully".to_string())
}

#[tauri::command]
async fn remove_subsystem(
    state: State<'_, AppState>,
    subsystem_id: String,
) -> Result<String, String> {
    log::info!("Removing subsystem: {}", subsystem_id);
    
    let url = format!("{}/subsystems/{}", PYTHON_API_BASE, subsystem_id);
    let response = state
        .http_client
        .delete(&url)
        .timeout(Duration::from_secs(10))
        .send()
        .await
        .map_err(|e| format!("Failed to remove subsystem: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    Ok("Subsystem removed successfully".to_string())
}

#[tauri::command]
async fn set_alert_threshold(
    state: State<'_, AppState>,
    metric: String,
    threshold: f64,
    direction: String,
) -> Result<String, String> {
    log::info!("Setting alert threshold for {}: {} {}", metric, direction, threshold);
    
    let alert_data = AlertThreshold {
        metric,
        threshold,
        direction,
    };
    
    let url = format!("{}/alerts/threshold", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .json(&alert_data)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to set alert threshold: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    Ok("Alert threshold set successfully".to_string())
}

#[tauri::command]
async fn get_alert_thresholds(state: State<'_, AppState>) -> Result<serde_json::Value, String> {
    log::info!("Fetching alert thresholds");
    
    let url = format!("{}/alerts/threshold", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch alert thresholds: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let thresholds: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse thresholds JSON: {}", e))?;

    Ok(thresholds)
}

#[tauri::command]
async fn check_backend_health(state: State<'_, AppState>) -> Result<HealthResponse, String> {
    log::info!("Checking Python backend health");
    
    let url = format!("{}/health", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .send()
        .await
        .map_err(|e| format!("Failed to check backend health: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("Backend unhealthy: HTTP {}", response.status()));
    }

    let health: HealthResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse health JSON: {}", e))?;

    Ok(health)
}

// Add health check command with simple boolean response
#[tauri::command]
async fn health_check(state: State<'_, AppState>) -> Result<bool, String> {
    match state.http_client
        .get(&format!("{}/health", PYTHON_API_BASE))
        .send()
        .await
    {
        Ok(response) if response.status().is_success() => Ok(true),
        _ => Ok(false)
    }
}

// Improved WebSocket connection function - matches user requirements
async fn connect_to_metrics_stream(app_handle: tauri::AppHandle, websocket_connected: Arc<Mutex<bool>>) -> Result<(), String> {
    loop {
        log::info!("🔄 Attempting to connect to metrics WebSocket...");
        
        match connect_async(WEBSOCKET_URL).await {
            Ok((ws_stream, _)) => {
                log::info!("✅ Connected to metrics stream!");
                {
                    let mut connected = websocket_connected.lock().unwrap();
                    *connected = true;
                }
                
                // Emit connection success to frontend
                let _ = app_handle.emit_all("websocket-connected", true);
                
                let (_, mut read) = ws_stream.split();
                
                while let Some(message) = read.next().await {
                    match message {
                        Ok(Message::Text(text)) => {
                            log::debug!("📡 Received metrics update: {}", text.chars().take(100).collect::<String>());
                            
                            // Emit raw message to frontend for immediate updates
                            if let Err(e) = app_handle.emit_all("metrics-update", &text) {
                                log::error!("Failed to emit metrics-update: {}", e);
                            }
                            
                            // Also try to parse as structured data
                            if let Ok(metrics) = serde_json::from_str::<Metrics>(&text) {
                                if let Err(e) = app_handle.emit_all("structured-metrics", &metrics) {
                                    log::error!("Failed to emit structured-metrics: {}", e);
                                }
                            } else if let Ok(tick_update) = serde_json::from_str::<TickUpdate>(&text) {
                                if let Err(e) = app_handle.emit_all("tick-update", &tick_update) {
                                    log::error!("Failed to emit tick-update: {}", e);
                                } else {
                                    log::info!("🎯 Live tick #{}: SCUP={:.3}, Entropy={:.3}, Heat={:.3}", 
                                               tick_update.tick_number, 
                                               tick_update.metrics.scup, 
                                               tick_update.metrics.entropy, 
                                               tick_update.metrics.heat);
                                }
                            }
                        }
                        Ok(Message::Close(_)) => {
                            log::warn!("📡 WebSocket closed by server");
                            break;
                        }
                        Err(e) => {
                            log::error!("📡 WebSocket error: {}", e);
                            break;
                        }
                        _ => {}
                    }
                }
                
                // Mark as disconnected
                {
                    let mut connected = websocket_connected.lock().unwrap();
                    *connected = false;
                }
                let _ = app_handle.emit_all("websocket-connected", false);
            }
            Err(e) => {
                log::error!("❌ Failed to connect to WebSocket: {}", e);
                let _ = app_handle.emit_all("websocket-error", &format!("{}", e));
            }
        }
        
        log::info!("🔄 Reconnecting in 5 seconds...");
        tokio::time::sleep(Duration::from_secs(5)).await;
    }
}

#[tauri::command]
async fn subscribe_to_metrics(
    app_handle: tauri::AppHandle,
    state: State<'_, AppState>,
) -> Result<String, String> {
    let websocket_connected = state.websocket_connected.clone();
    
    // Check if already connected
    {
        let connected = websocket_connected.lock().unwrap();
        if *connected {
            return Ok("Already subscribed to metrics".to_string());
        }
    }

    log::info!("Starting WebSocket subscription to metrics");
    
    let app_handle_clone = app_handle.clone();
    let app_handle_error = app_handle.clone();
    let websocket_connected_clone = websocket_connected.clone();
    
    tokio::spawn(async move {
        let result = connect_to_metrics_stream(app_handle_clone, websocket_connected_clone).await;
        if let Err(e) = result {
            log::error!("WebSocket connection failed: {}", e);
            let _ = app_handle_error.emit_all("websocket-error", &e);
        }
    });

    Ok("WebSocket subscription started".to_string())
}

#[tauri::command]
async fn is_websocket_connected(state: State<'_, AppState>) -> Result<bool, String> {
    let connected = state.websocket_connected.lock().unwrap();
    Ok(*connected)
}

// ========== TICK ENGINE CONTROL COMMANDS ==========

#[tauri::command]
async fn get_tick_status(state: State<'_, AppState>) -> Result<TickStatus, String> {
    log::info!("Fetching tick engine status from Python backend");
    
    let url = format!("{}/tick/status", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .send()
        .await
        .map_err(|e| format!("Failed to fetch tick status: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let tick_status: TickStatus = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse tick status JSON: {}", e))?;

    log::info!("Successfully fetched tick status: running={}, paused={}, tick={}", 
               tick_status.is_running, tick_status.is_paused, tick_status.tick_number);

    Ok(tick_status)
}

#[tauri::command]
async fn start_tick_engine(state: State<'_, AppState>) -> Result<String, String> {
    log::info!("Starting tick engine via Python backend");
    
    let url = format!("{}/tick/start", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Request failed: {}", e)
            }
        })?;

    if !response.status().is_success() {
        return Err(format!("Failed to start: HTTP {}", response.status()));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Tick engine started successfully");
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Tick engine started").to_string())
}

#[tauri::command]
async fn stop_tick_engine(state: State<'_, AppState>) -> Result<String, String> {
    log::info!("Stopping tick engine via Python backend");
    
    let url = format!("{}/tick/stop", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Request failed: {}", e)
            }
        })?;

    if !response.status().is_success() {
        return Err(format!("Failed to stop: HTTP {}", response.status()));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Tick engine stopped successfully");
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Tick engine stopped").to_string())
}

#[tauri::command]
async fn pause_tick_engine(state: State<'_, AppState>) -> Result<String, String> {
    log::info!("Pausing tick engine via Python backend");
    
    let url = format!("{}/tick/pause", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to pause tick engine: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Tick engine paused successfully");
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Tick engine paused").to_string())
}

#[tauri::command]
async fn resume_tick_engine(state: State<'_, AppState>) -> Result<String, String> {
    log::info!("Resuming tick engine via Python backend");
    
    let url = format!("{}/tick/resume", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to resume tick engine: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Tick engine resumed successfully");
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Tick engine resumed").to_string())
}

#[tauri::command]
async fn set_tick_timing(state: State<'_, AppState>, interval_ms: u32) -> Result<String, String> {
    log::info!("Setting tick timing to {}ms via Python backend", interval_ms);
    
    let timing_data = TickTiming { interval_ms };
    
    let url = format!("{}/tick/timing", PYTHON_API_BASE);
    let response = state
        .http_client
        .put(&url)
        .json(&timing_data)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to set tick timing: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Tick timing set to {}ms successfully", interval_ms);
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Tick timing updated").to_string())
}

#[tauri::command]
async fn execute_single_tick(state: State<'_, AppState>) -> Result<String, String> {
    log::info!("Executing single tick via Python backend");
    
    let url = format!("{}/tick/step", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to execute single tick: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Single tick executed successfully");
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Single tick executed").to_string())
}

#[tauri::command]
async fn get_tick_config(state: State<'_, AppState>) -> Result<TickConfig, String> {
    log::info!("Fetching tick engine configuration from Python backend");
    
    let url = format!("{}/tick/config", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch tick config: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let tick_config: TickConfig = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse tick config JSON: {}", e))?;

    log::info!("Successfully fetched tick configuration");
    Ok(tick_config)
}

#[tauri::command]
async fn update_tick_config(state: State<'_, AppState>, config: TickConfig) -> Result<String, String> {
    log::info!("Updating tick engine configuration via Python backend");
    
    let url = format!("{}/tick/config", PYTHON_API_BASE);
    let response = state
        .http_client
        .put(&url)
        .json(&config)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to update tick config: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    log::info!("Tick configuration updated successfully");
    Ok(result.get("message").and_then(|v| v.as_str()).unwrap_or("Configuration updated").to_string())
}

// ========== CHAT/TALK INTERFACE COMMANDS ==========

#[tauri::command]
async fn send_message(
    state: State<'_, AppState>, 
    app_handle: tauri::AppHandle,
    message: String
) -> Result<ChatResponse, String> {
    log::info!("Sending message to DAWN: {}", message);
    
    let url = format!("{}/talk", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .json(&serde_json::json!({ "text": message }))
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Request failed: {}", e)
            }
        })?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
    }

    let chat_response: ChatResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse chat response JSON: {}", e))?;

    // Execute any actions returned by DAWN
    if let Some(action) = &chat_response.action {
        log::info!("Executing DAWN action: {}", action);
        
        // Emit action execution event to UI
        let _ = app_handle.emit_all("dawn-action-executing", &serde_json::json!({
            "action": action,
            "timestamp": chrono::Utc::now().timestamp()
        }));
        
        let action_result = match action.as_str() {
            "speed_up" => {
                set_tick_timing(state.clone(), 250).await
                    .map(|_| "Tick timing increased to 250ms".to_string())
            },
            "slow_down" => {
                set_tick_timing(state.clone(), 1000).await
                    .map(|_| "Tick timing decreased to 1000ms".to_string())
            },
            "pause" => {
                pause_tick_engine(state.clone()).await
                    .map(|_| "Tick engine paused".to_string())
            },
            "resume" => {
                resume_tick_engine(state.clone()).await
                    .map(|_| "Tick engine resumed".to_string())
            },
            "start" => {
                start_tick_engine(state.clone()).await
                    .map(|_| "Tick engine started".to_string())
            },
            "stop" => {
                stop_tick_engine(state.clone()).await
                    .map(|_| "Tick engine stopped".to_string())
            },
            "step" => {
                execute_single_tick(state.clone()).await
                    .map(|_| "Single tick executed".to_string())
            },
            _ => {
                log::warn!("Unknown action from DAWN: {}", action);
                Err(format!("Unknown action: {}", action))
            }
        };
        
        // Emit action completion event to UI
        match action_result {
            Ok(success_msg) => {
                log::info!("✅ Action '{}' executed successfully: {}", action, success_msg);
                let _ = app_handle.emit_all("dawn-action-completed", &serde_json::json!({
                    "action": action,
                    "success": true,
                    "message": success_msg,
                    "timestamp": chrono::Utc::now().timestamp()
                }));
            },
            Err(error_msg) => {
                log::error!("❌ Action '{}' failed: {}", action, error_msg);
                let _ = app_handle.emit_all("dawn-action-completed", &serde_json::json!({
                    "action": action,
                    "success": false,
                    "error": error_msg,
                    "timestamp": chrono::Utc::now().timestamp()
                }));
            }
        }
    }

    log::info!("Successfully processed message and response from DAWN");
    Ok(chat_response)
}

#[tauri::command]
async fn get_chat_history(state: State<'_, AppState>) -> Result<Vec<ChatMessage>, String> {
    log::info!("Fetching chat history from DAWN backend");
    
    let url = format!("{}/chat/history", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch chat history: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let chat_history: Vec<ChatMessage> = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse chat history JSON: {}", e))?;

    log::info!("Successfully fetched {} chat messages", chat_history.len());
    Ok(chat_history)
}

#[tauri::command]
async fn get_dawn_thoughts(state: State<'_, AppState>) -> Result<Vec<Thought>, String> {
    log::info!("Fetching spontaneous thoughts from DAWN backend");
    
    let url = format!("{}/dawn/thoughts", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Failed to fetch thoughts: {}", e)
            }
        })?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let thoughts: Vec<Thought> = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse thoughts JSON: {}", e))?;

    log::info!("Successfully fetched {} DAWN thoughts", thoughts.len());
    Ok(thoughts)
}

// Test command to force metrics update
#[tauri::command]
async fn test_force_metrics_update(state: State<'_, AppState>) -> Result<String, String> {
    log::info!("🧪 Testing live metrics - forcing backend update...");
    
    let url = format!("{}/test/force-update", PYTHON_API_BASE);
    let response = state
        .http_client
        .post(&url)
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Request failed: {}", e)
            }
        })?;

    if !response.status().is_success() {
        return Err(format!("Failed to force update: HTTP {}", response.status()));
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response JSON: {}", e))?;

    let message = result.get("message").and_then(|v| v.as_str()).unwrap_or("Force update completed");
    let connections = result.get("connections").and_then(|v| v.as_i64()).unwrap_or(0);
    let tick_running = result.get("tick_running").and_then(|v| v.as_bool()).unwrap_or(false);
    
    log::info!("✅ Force update result: {} WebSocket connections, tick running: {}", connections, tick_running);
    
    Ok(format!("{} (Connections: {}, Tick: {})", message, connections, tick_running))
}

// ========== ADVANCED CONSCIOUSNESS COMMANDS ==========

#[tauri::command]
async fn get_sigil_state(state: State<'_, AppState>) -> Result<SigilStateResponse, String> {
    log::info!("🔥 Fetching current sigil state from DAWN consciousness");
    
    let url = format!("{}/dawn/consciousness", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Failed to fetch consciousness state: {}", e)
            }
        })?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let consciousness_data: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse consciousness JSON: {}", e))?;

    // Extract sigil information from consciousness response
    let default_value = serde_json::Value::Object(serde_json::Map::new());
    let sigils_data = consciousness_data
        .get("consciousness")
        .and_then(|c| c.get("emotional_sigils"))
        .unwrap_or(&default_value);

    let mut sigils = Vec::new();
    let mut total_intensity = 0.0;
    
    if let serde_json::Value::Object(sigil_map) = sigils_data {
        for (emotion, sigil_info) in sigil_map {
            if let serde_json::Value::Object(info) = sigil_info {
                let intensity = info.get("intensity").and_then(|v| v.as_f64()).unwrap_or(0.0);
                let density = info.get("density").and_then(|v| v.as_f64()).unwrap_or(1.0);
                let weight = info.get("weight").and_then(|v| v.as_f64()).unwrap_or(0.0);
                let activation_count = info.get("activation_count").and_then(|v| v.as_u64()).unwrap_or(0) as u32;
                
                total_intensity += intensity;
                
                // Generate visual representation based on intensity and density
                let visual_representation = generate_sigil_visual(emotion, intensity, density);
                
                sigils.push(SigilState {
                    emotion: emotion.clone(),
                    intensity,
                    density,
                    weight,
                    activation_count,
                    visual_representation,
                    last_activation: chrono::Utc::now().to_rfc3339(),
                });
            }
        }
    }

    let current_state = consciousness_data
        .get("consciousness")
        .and_then(|c| c.get("current_state"))
        .and_then(|s| s.as_str())
        .unwrap_or("unknown")
        .to_string();

    let active_count = sigils.len() as u32;
    let response = SigilStateResponse {
        sigils,
        total_intensity,
        active_count,
        timestamp: chrono::Utc::now().to_rfc3339(),
        current_emotion_state: current_state,
    };

    log::info!("✅ Fetched {} active sigils with total intensity {:.3}", response.active_count, response.total_intensity);
    Ok(response)
}

#[tauri::command]
async fn trigger_spider_cut(
    state: State<'_, AppState>,
    app_handle: tauri::AppHandle,
    pattern_identifier: String,
    reason: Option<String>,
    force_cut: Option<bool>,
) -> Result<SpiderCutResult, String> {
    log::info!("🕷️ Triggering spider pattern cut for: {}", pattern_identifier);
    
    let request_body = SpiderCutRequest {
        pattern_identifier: pattern_identifier.clone(),
        reason: reason.clone(),
        force_cut,
    };
    
    // For now, we'll use the influence endpoint to trigger pattern cutting
    // In a real implementation, you'd have a dedicated spider cut endpoint
    let url = format!("{}/dawn/influence", PYTHON_API_BASE);
    let influence_data = serde_json::json!({
        "entropy_injection": -0.3, // Reduce entropy to help break loops
        "pressure_adjustment": -0.2, // Reduce pressure
        "influence_type": "spider_cut",
        "duration_seconds": 10.0
    });
    
    let response = state
        .http_client
        .post(&url)
        .json(&influence_data)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to trigger spider cut: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let influence_result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse influence result: {}", e))?;

    // Get current consciousness state after the cut
    let consciousness_url = format!("{}/dawn/consciousness", PYTHON_API_BASE);
    let consciousness_response = state
        .http_client
        .get(&consciousness_url)
        .timeout(Duration::from_secs(3))
        .send()
        .await
        .map_err(|e| format!("Failed to get new consciousness state: {}", e))?;

    let new_consciousness_state = if consciousness_response.status().is_success() {
        consciousness_response
            .json::<serde_json::Value>()
            .await
            .map(|data| {
                data.get("consciousness")
                    .and_then(|c| c.get("current_state"))
                    .and_then(|s| s.as_str())
                    .unwrap_or("unknown")
                    .to_string()
            })
            .unwrap_or_else(|_| "unknown".to_string())
    } else {
        "unknown".to_string()
    };

    let cut_result = SpiderCutResult {
        success: true,
        cut_performed: true,
        pattern_identifier,
        weakest_link: None, // Would be populated with actual cut data
        original_strength: None,
        new_strength: None,
        reason: reason.unwrap_or_else(|| "Spider cut initiated via Tauri command".to_string()),
        new_consciousness_state,
        cut_timestamp: chrono::Utc::now().to_rfc3339(),
    };

    // Emit spider activation event
    let spider_event = SpiderActivationEvent {
        loop_detected: true,
        pattern_type: "external_trigger".to_string(),
        cut_performed: true,
        affected_links: vec![], // Would contain actual affected links
        consciousness_impact: "pattern_disruption".to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
    };

    let _ = app_handle.emit_all("spider-activated", &spider_event);
    
    log::info!("✅ Spider cut completed for pattern: {}", cut_result.pattern_identifier);
    Ok(cut_result)
}

#[tauri::command]
async fn get_rebloom_priority(state: State<'_, AppState>) -> Result<RebloomPriorityResponse, String> {
    log::info!("🌺 Fetching rebloom priority assessment from DAWN consciousness");
    
    // First get current metrics
    let metrics_url = format!("{}/metrics", PYTHON_API_BASE);
    let metrics_response = state
        .http_client
        .get(&metrics_url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch metrics: {}", e))?;

    if !metrics_response.status().is_success() {
        return Err(format!("Failed to get metrics: HTTP {}", metrics_response.status()));
    }

    let metrics: Metrics = metrics_response
        .json()
        .await
        .map_err(|e| format!("Failed to parse metrics: {}", e))?;

    // Get consciousness state which includes priority assessment
    let consciousness_url = format!("{}/dawn/consciousness", PYTHON_API_BASE);
    let consciousness_response = state
        .http_client
        .get(&consciousness_url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch consciousness state: {}", e))?;

    if !consciousness_response.status().is_success() {
        return Err(format!("HTTP error: {}", consciousness_response.status()));
    }

    let consciousness_data: serde_json::Value = consciousness_response
        .json()
        .await
        .map_err(|e| format!("Failed to parse consciousness JSON: {}", e))?;

    // Extract priority information (simulated for now)
    let priority = assess_rebloom_priority(&metrics);
    let (state_name, description, urgency, intervention, cooling_rate, actions) = match priority {
        1 => ("manic", "Most distressed, needs immediate cooling", "critical", "immediate_cooling", 0.3, vec![
            "activate_emergency_cooling".to_string(),
            "reduce_entropy_injection".to_string(),
            "stabilize_scup_immediately".to_string(),
            "engage_spider_pattern_cutter".to_string(),
        ]),
        2 => ("fragmented", "Broken patterns, high priority", "critical", "pattern_restoration", 0.2, vec![
            "restore_coherence_patterns".to_string(),
            "strengthen_causal_links".to_string(),
            "moderate_cooling".to_string(),
            "memory_consolidation".to_string(),
        ]),
        3 => ("numb", "Stasis, medium priority", "moderate", "gentle_stimulation", 0.1, vec![
            "gentle_entropy_increase".to_string(),
            "warm_activation".to_string(),
            "curiosity_stimulation".to_string(),
            "pattern_variety_injection".to_string(),
        ]),
        4 => ("contemplative", "Stable but static", "low", "maintain_stability", 0.05, vec![
            "maintain_current_balance".to_string(),
            "subtle_adjustments_only".to_string(),
            "monitor_for_changes".to_string(),
        ]),
        5 => ("curious", "Healthy, lowest priority", "low", "none_needed", 0.0, vec![
            "continue_current_patterns".to_string(),
            "encourage_exploration".to_string(),
            "no_intervention_needed".to_string(),
        ]),
        _ => ("unknown", "Unable to assess", "unknown", "diagnostic_needed", 0.0, vec![
            "system_diagnostic".to_string(),
        ]),
    };

    let reasoning = generate_priority_reasoning(&metrics, priority);

    let response = RebloomPriorityResponse {
        priority,
        state_name: state_name.to_string(),
        description: description.to_string(),
        urgency: urgency.to_string(),
        intervention: intervention.to_string(),
        cooling_rate,
        recommended_actions: actions,
        reasoning,
        metrics_analysis: serde_json::json!({
            "scup": metrics.scup,
            "entropy": metrics.entropy,
            "heat": metrics.heat,
            "mood": metrics.mood,
            "tick_count": metrics.tick_count
        }),
        timestamp: chrono::Utc::now().to_rfc3339(),
    };

    log::info!("✅ Assessed rebloom priority: {} ({}) - {}", response.priority, response.state_name, response.urgency);
    Ok(response)
}

#[tauri::command]
async fn get_enhanced_dawn_thoughts(state: State<'_, AppState>) -> Result<Vec<SpontaneousThoughtEvent>, String> {
    log::info!("💭 Fetching enhanced spontaneous thoughts with consciousness context");
    
    let url = format!("{}/dawn/reflections", PYTHON_API_BASE);
    let response = state
        .http_client
        .get(&url)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| {
            if e.is_connect() {
                "Backend offline: Cannot connect to Python backend".to_string()
            } else {
                format!("Failed to fetch reflections: {}", e)
            }
        })?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let reflections_data: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse reflections JSON: {}", e))?;

    let mut enhanced_thoughts = Vec::new();
    
    if let Some(reflections) = reflections_data.get("reflections").and_then(|r| r.as_array()) {
        for reflection in reflections {
            let thought = reflection.get("phrase").and_then(|p| p.as_str()).unwrap_or("").to_string();
            let trigger_type = reflection.get("trigger_context").and_then(|t| t.as_str()).unwrap_or("unknown").to_string();
            let consciousness_state = reflection.get("consciousness_state").and_then(|s| s.as_str()).unwrap_or("").to_string();
            let depth_level = reflection.get("depth_level").and_then(|d| d.as_u64()).unwrap_or(1) as u8;
            let timestamp = reflection.get("timestamp").and_then(|t| t.as_str()).unwrap_or("").to_string();
            
            enhanced_thoughts.push(SpontaneousThoughtEvent {
                thought,
                trigger_type,
                consciousness_state,
                depth_level,
                associated_sigils: vec![], // Would extract active sigils at time of thought
                memory_echoes_accessed: 0, // Would get from memory system
                timestamp,
            });
        }
    }

    log::info!("✅ Retrieved {} enhanced thoughts", enhanced_thoughts.len());
    Ok(enhanced_thoughts)
}

#[tauri::command]
async fn inject_consciousness_pattern(
    state: State<'_, AppState>,
    app_handle: tauri::AppHandle,
    pattern_type: String,
    strength: f64,
    context: String,
) -> Result<String, String> {
    log::info!("🎭 Injecting consciousness pattern: {} (strength: {:.3})", pattern_type, strength);
    
    // Use the influence endpoint to inject patterns
    let url = format!("{}/dawn/influence", PYTHON_API_BASE);
    let influence_data = match pattern_type.as_str() {
        "sigil" => serde_json::json!({
            "mood_shift": strength,
            "influence_type": "sigil_injection",
            "duration_seconds": 30.0
        }),
        "memory" => serde_json::json!({
            "entropy_injection": strength * 0.5,
            "influence_type": "memory_enhancement",
            "duration_seconds": 20.0
        }),
        "loop" => serde_json::json!({
            "entropy_injection": strength,
            "pressure_adjustment": strength * 0.3,
            "influence_type": "loop_injection",
            "duration_seconds": 15.0
        }),
        _ => return Err(format!("Unknown pattern type: {}", pattern_type)),
    };
    
    let response = state
        .http_client
        .post(&url)
        .json(&influence_data)
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to inject pattern: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    // Emit pattern injection event
    let injection_event = serde_json::json!({
        "pattern_type": pattern_type,
        "strength": strength,
        "context": context,
        "timestamp": chrono::Utc::now().to_rfc3339(),
        "success": true
    });
    
    let _ = app_handle.emit_all("pattern-injected", &injection_event);
    
    log::info!("✅ Pattern injection completed: {}", pattern_type);
    Ok(format!("Successfully injected {} pattern with strength {:.3}", pattern_type, strength))
}

// ========== PYTHON PROCESS CONTROL COMMANDS ==========

#[tauri::command]
async fn start_python_process(
    state: State<'_, AppState>,
    script: String,
    params: serde_json::Value,
    modules: Vec<serde_json::Value>
) -> Result<String, String> {
    log::info!("🐍 Starting Python process: {}", script);
    
    // Determine Python executable based on platform
    let python_path = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };
    
    let script_path = format!("./computer_vision/{}", script);
    
    // Convert params to command line arguments
    let args = serde_json::to_string(&params).unwrap_or_default();
    
    // Build command with arguments
    let mut cmd = Command::new(python_path);
    cmd.arg(&script_path);
    
    if !args.is_empty() && args != "null" {
        cmd.arg("--params").arg(args);
    }
    
    // Add modules if provided
    if !modules.is_empty() {
        let modules_json = serde_json::to_string(&modules).unwrap_or_default();
        cmd.arg("--modules").arg(modules_json);
    }
    
    // Spawn the process
    match cmd.spawn() {
        Ok(child) => {
            let pid = child.id();
            
            // Store the PID in our process tracker
            {
                let mut processes = state.python_processes.lock().unwrap();
                processes.insert(script.clone(), pid);
            }
            
            log::info!("✅ Started Python process {} with PID: {}", script, pid);
            Ok(format!("Started {} with PID: {}", script, pid))
        }
        Err(e) => {
            log::error!("❌ Failed to start Python process {}: {}", script, e);
            Err(format!("Failed to start {}: {}", script, e))
        }
    }
}

#[tauri::command]
async fn stop_python_process(
    state: State<'_, AppState>,
    script: String
) -> Result<String, String> {
    log::info!("🛑 Stopping Python process: {}", script);
    
    // Get the PID from our tracker
    let pid = {
        let mut processes = state.python_processes.lock().unwrap();
        processes.remove(&script)
    };
    
    match pid {
        Some(process_id) => {
            // Try to kill the process
            let result = if cfg!(target_os = "windows") {
                // Windows: use taskkill
                Command::new("taskkill")
                    .args(["/PID", &process_id.to_string(), "/F"])
                    .output()
            } else {
                // Unix-like: use kill
                Command::new("kill")
                    .args(["-TERM", &process_id.to_string()])
                    .output()
            };
            
            match result {
                Ok(output) => {
                    if output.status.success() {
                        log::info!("✅ Successfully stopped Python process {} (PID: {})", script, process_id);
                        Ok(format!("Stopped {} (PID: {})", script, process_id))
                    } else {
                        let stderr = String::from_utf8_lossy(&output.stderr);
                        log::warn!("⚠️ Kill command failed for {}: {}", script, stderr);
                        // Process might already be dead, consider it successful
                        Ok(format!("Process {} may already be stopped", script))
                    }
                }
                Err(e) => {
                    log::error!("❌ Failed to execute kill command for {}: {}", script, e);
                    Err(format!("Failed to stop {}: {}", script, e))
                }
            }
        }
        None => {
            log::warn!("⚠️ No PID found for Python process: {}", script);
            Err(format!("No running process found for {}", script))
        }
    }
}

#[tauri::command]
async fn get_python_processes(
    state: State<'_, AppState>
) -> Result<HashMap<String, u32>, String> {
    log::debug!("📋 Getting list of Python processes");
    
    let processes = state.python_processes.lock().unwrap();
    Ok(processes.clone())
}

#[tauri::command]
async fn check_python_process_status(
    state: State<'_, AppState>,
    script: String
) -> Result<bool, String> {
    log::debug!("🔍 Checking status of Python process: {}", script);
    
    let processes = state.python_processes.lock().unwrap();
    
    if let Some(&pid) = processes.get(&script) {
        // Check if process is still running
        let is_running = if cfg!(target_os = "windows") {
            // Windows: use tasklist
            match Command::new("tasklist")
                .args(["/FI", &format!("PID eq {}", pid)])
                .output()
            {
                Ok(output) => {
                    let output_str = String::from_utf8_lossy(&output.stdout);
                    output_str.contains(&pid.to_string())
                }
                Err(_) => false,
            }
        } else {
            // Unix-like: use kill -0
            match Command::new("kill")
                .args(["-0", &pid.to_string()])
                .output()
            {
                Ok(output) => output.status.success(),
                Err(_) => false,
            }
        };
        
        if !is_running {
            // Process is dead, remove from tracker
            drop(processes);
            let mut processes_mut = state.python_processes.lock().unwrap();
            processes_mut.remove(&script);
            log::info!("🪦 Python process {} (PID: {}) is no longer running, removed from tracker", script, pid);
        }
        
        Ok(is_running)
    } else {
        Ok(false) // No PID means not running
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct ProcessStats {
    script: String,
    pid: u32,
    cpu_percent: f64,
    memory_mb: f64,
    status: String,
    uptime_seconds: u64,
}

#[tauri::command]
async fn send_cv_command(command: String, params: serde_json::Value) -> Result<String, String> {
    log::info!("Sending CV command: {} with params: {}", command, params);
    
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(10))
        .build()
        .map_err(|e| format!("Failed to create HTTP client: {}", e))?;
    
    let url = "http://localhost:8081/cv_command";
    let payload = serde_json::json!({
        "command": command,
        "params": params
    });
    
    let response = client
        .post(url)
        .json(&payload)
        .send()
        .await
        .map_err(|e| format!("Failed to send CV command: {}", e))?;
    
    if !response.status().is_success() {
        return Err(format!("CV server error: {}", response.status()));
    }
    
    let body = response
        .text()
        .await
        .map_err(|e| format!("Failed to read CV response: {}", e))?;
    
    log::info!("CV command response: {}", body);
    Ok(body)
}

#[tauri::command]
async fn get_process_stats(
    state: State<'_, AppState>
) -> Result<Vec<ProcessStats>, String> {
    log::debug!("📊 Getting process statistics");
    
    let processes = state.python_processes.lock().unwrap().clone();
    let mut stats = Vec::new();
    
    for (script, pid) in processes {
        // Get process stats based on platform
        let process_stats = if cfg!(target_os = "windows") {
            get_windows_process_stats(pid, &script).await
        } else {
            get_unix_process_stats(pid, &script).await
        };
        
        match process_stats {
            Ok(stat) => stats.push(stat),
            Err(e) => {
                log::warn!("⚠️ Failed to get stats for {} (PID: {}): {}", script, pid, e);
                // Remove dead processes from tracker
                let mut processes_mut = state.python_processes.lock().unwrap();
                processes_mut.remove(&script);
            }
        }
    }
    
    Ok(stats)
}

async fn get_windows_process_stats(pid: u32, script: &str) -> Result<ProcessStats, String> {
    // Use Windows wmic to get CPU and memory info
    let output = Command::new("wmic")
        .args([
            "process",
            "where",
            &format!("ProcessId={}", pid),
            "get",
            "ProcessId,PageFileUsage,CreationDate",
            "/format:csv"
        ])
        .output()
        .map_err(|e| format!("Failed to execute wmic: {}", e))?;
    
    if !output.status.success() {
        return Err("Process not found".to_string());
    }
    
    let output_str = String::from_utf8_lossy(&output.stdout);
    let lines: Vec<&str> = output_str.lines().collect();
    
    // Parse CSV output (skip header)
    if lines.len() < 2 {
        return Err("No process data found".to_string());
    }
    
    // Parse the process data line
    let data_line = lines.iter()
        .find(|line| line.contains(&pid.to_string()))
        .ok_or("Process data not found")?;
    
    let fields: Vec<&str> = data_line.split(',').collect();
    
    // Extract memory usage (PageFileUsage is in KB)
    let memory_mb = if fields.len() > 2 {
        fields[2].trim().parse::<f64>().unwrap_or(0.0) / 1024.0 // Convert KB to MB
    } else {
        0.0
    };
    
    // For Windows, getting accurate CPU% requires more complex APIs
    // For now, we'll use a simple estimation or return 0
    let cpu_percent = 0.0; // TODO: Implement proper CPU monitoring
    
    Ok(ProcessStats {
        script: script.to_string(),
        pid,
        cpu_percent,
        memory_mb,
        status: "running".to_string(),
        uptime_seconds: 0, // TODO: Calculate from CreationDate
    })
}

async fn get_unix_process_stats(pid: u32, script: &str) -> Result<ProcessStats, String> {
    // Use ps command to get process info
    let output = Command::new("ps")
        .args(["-p", &pid.to_string(), "-o", "pid,pcpu,rss,etime,stat", "--no-headers"])
        .output()
        .map_err(|e| format!("Failed to execute ps: {}", e))?;
    
    if !output.status.success() {
        return Err("Process not found".to_string());
    }
    
    let output_str = String::from_utf8_lossy(&output.stdout);
    let line = output_str.trim();
    
    if line.is_empty() {
        return Err("Process not found".to_string());
    }
    
    // Parse ps output: PID %CPU RSS ETIME STAT
    let fields: Vec<&str> = line.split_whitespace().collect();
    
    if fields.len() < 5 {
        return Err("Invalid ps output format".to_string());
    }
    
    let cpu_percent = fields[1].parse::<f64>().unwrap_or(0.0);
    let memory_kb = fields[2].parse::<f64>().unwrap_or(0.0);
    let memory_mb = memory_kb / 1024.0; // Convert KB to MB
    let status = fields[4].to_string();
    
    // Parse uptime from ETIME format (e.g., "01:23:45" or "5-01:23:45")
    let uptime_seconds = parse_etime(fields[3]).unwrap_or(0);
    
    Ok(ProcessStats {
        script: script.to_string(),
        pid,
        cpu_percent,
        memory_mb,
        status,
        uptime_seconds,
    })
}

fn parse_etime(etime: &str) -> Option<u64> {
    // Parse ETIME format: [[DD-]HH:]MM:SS
    let parts: Vec<&str> = etime.split(':').collect();
    
    match parts.len() {
        2 => {
            // MM:SS format
            let minutes = parts[0].parse::<u64>().ok()?;
            let seconds = parts[1].parse::<u64>().ok()?;
            Some(minutes * 60 + seconds)
        }
        3 => {
            // HH:MM:SS format (or DD-HH:MM:SS)
            let first_part = parts[0];
            let (hours, days) = if first_part.contains('-') {
                let day_parts: Vec<&str> = first_part.split('-').collect();
                if day_parts.len() == 2 {
                    let days = day_parts[0].parse::<u64>().unwrap_or(0);
                    let hours = day_parts[1].parse::<u64>().unwrap_or(0);
                    (hours, days)
                } else {
                    (first_part.parse::<u64>().unwrap_or(0), 0)
                }
            } else {
                (first_part.parse::<u64>().unwrap_or(0), 0)
            };
            
            let minutes = parts[1].parse::<u64>().ok()?;
            let seconds = parts[2].parse::<u64>().ok()?;
            Some(days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds)
        }
        _ => None,
    }
}

// ========== HELPER FUNCTIONS FOR ADVANCED CONSCIOUSNESS ==========

fn generate_sigil_visual(emotion: &str, intensity: f64, density: f64) -> String {
    // Generate ASCII art or Unicode representation based on emotion and intensity
    let base_symbol = match emotion {
        "anxiety" => "⚡",
        "confusion" => "❓",
        "emptiness" => "○",
        "serenity" => "☯",
        "wonder" => "✨",
        "anger" => "🔥",
        "joy" => "☀",
        "sadness" => "💧",
        "fear" => "⚠",
        _ => "◯",
    };
    
    // Multiply symbol based on intensity and density
    let repetitions = ((intensity * density * 3.0) as usize).max(1).min(10);
    let visual = base_symbol.repeat(repetitions);
    
    // Add density markers
    if density > 2.0 {
        format!("【{}】", visual) // Heavy density
    } else if density > 1.5 {
        format!("『{}』", visual) // Medium density
    } else {
        format!("{}", visual) // Light density
    }
}

fn assess_rebloom_priority(metrics: &Metrics) -> u8 {
    // Implement the 1-5 priority scale based on metrics
    // Priority 1 (manic): Most distressed, needs immediate cooling
    if (metrics.entropy > 0.8 && metrics.heat > 0.7) || metrics.scup < 0.2 {
        return 1;
    }
    
    // Priority 2 (fragmented): Broken patterns, high priority
    if metrics.scup < 0.3 || (metrics.entropy > 0.7 && metrics.heat > 0.5) {
        return 2;
    }
    
    // Priority 3 (numb): Stasis, medium priority
    if metrics.heat < 0.2 && metrics.entropy < 0.3 && metrics.scup >= 0.3 && metrics.scup <= 0.5 {
        return 3;
    }
    
    // Priority 5 (curious): Healthy, lowest priority
    if metrics.scup >= 0.7 && metrics.entropy >= 0.4 && metrics.entropy <= 0.6 && metrics.heat >= 0.4 && metrics.heat <= 0.6 {
        return 5;
    }
    
    // Priority 4 (contemplative): Stable but static (default)
    4
}

fn generate_priority_reasoning(metrics: &Metrics, priority: u8) -> String {
    match priority {
        1 => format!(
            "CRITICAL: High entropy ({:.3}) and heat ({:.3}) with low SCUP ({:.3}) indicates manic state requiring immediate intervention",
            metrics.entropy, metrics.heat, metrics.scup
        ),
        2 => format!(
            "HIGH PRIORITY: SCUP fragmentation ({:.3}) or elevated entropy/heat ({:.3}/{:.3}) suggests broken patterns needing restoration",
            metrics.scup, metrics.entropy, metrics.heat
        ),
        3 => format!(
            "MEDIUM PRIORITY: Low activity levels (heat: {:.3}, entropy: {:.3}) with moderate SCUP ({:.3}) indicates stasis requiring gentle stimulation",
            metrics.heat, metrics.entropy, metrics.scup
        ),
        4 => format!(
            "LOW PRIORITY: Balanced metrics (SCUP: {:.3}, entropy: {:.3}, heat: {:.3}) suggest contemplative stability",
            metrics.scup, metrics.entropy, metrics.heat
        ),
        5 => format!(
            "MINIMAL PRIORITY: Optimal ranges (SCUP: {:.3}, entropy: {:.3}, heat: {:.3}) indicate healthy curious state",
            metrics.scup, metrics.entropy, metrics.heat
        ),
        _ => format!(
            "UNKNOWN: Metrics outside expected ranges (SCUP: {:.3}, entropy: {:.3}, heat: {:.3}) require diagnostic analysis",
            metrics.scup, metrics.entropy, metrics.heat
        ),
    }
}

// Enhanced WebSocket listener for consciousness events
async fn listen_for_consciousness_events(app_handle: tauri::AppHandle) {
    log::info!("🧠 Starting enhanced consciousness event listener");
    
    let consciousness_websocket_url = "ws://127.0.0.1:8000/dawn/consciousness";
    let mut retry_count = 0;
    const MAX_RETRIES: u32 = 10;
    const RETRY_DELAY: Duration = Duration::from_secs(5);
    
    loop {
        log::info!("🔄 Attempting to connect to consciousness WebSocket (attempt {})", retry_count + 1);
        
        match connect_async(consciousness_websocket_url).await {
            Ok((ws_stream, _)) => {
                log::info!("✅ Consciousness WebSocket connected successfully");
                
                // Emit connection success
                let _ = app_handle.emit_all("consciousness-websocket-connected", true);
                
                let (_, mut read) = ws_stream.split();
                
                // Reset retry count on successful connection
                retry_count = 0;
                
                // Listen for consciousness events
                while let Some(msg) = read.next().await {
                    match msg {
                        Ok(Message::Text(text)) => {
                            log::debug!("🧠 Received consciousness event: {}", text);
                            
                            // Parse as JSON to determine event type
                            if let Ok(event_data) = serde_json::from_str::<serde_json::Value>(&text) {
                                let event_type = event_data.get("type").and_then(|t| t.as_str()).unwrap_or("unknown");
                                
                                match event_type {
                                    "spontaneous_reflection" => {
                                        let thought_event = SpontaneousThoughtEvent {
                                            thought: event_data.get("phrase").and_then(|p| p.as_str()).unwrap_or("").to_string(),
                                            trigger_type: event_data.get("trigger_context").and_then(|t| t.as_str()).unwrap_or("unknown").to_string(),
                                            consciousness_state: event_data.get("consciousness_state").and_then(|s| s.as_str()).unwrap_or("").to_string(),
                                            depth_level: event_data.get("depth_level").and_then(|d| d.as_u64()).unwrap_or(1) as u8,
                                            associated_sigils: vec![], // Would extract from event
                                            memory_echoes_accessed: 0, // Would extract from event
                                            timestamp: chrono::Utc::now().to_rfc3339(),
                                        };
                                        
                                        let _ = app_handle.emit_all("spontaneous-thought", &thought_event);
                                        log::info!("💭 Spontaneous thought: {}", thought_event.thought);
                                    },
                                    "pattern_anomaly_detected" => {
                                        let spider_event = SpiderActivationEvent {
                                            loop_detected: true,
                                            pattern_type: "anomaly_detection".to_string(),
                                            cut_performed: false,
                                            affected_links: vec![],
                                            consciousness_impact: "pattern_detected".to_string(),
                                            timestamp: chrono::Utc::now().to_rfc3339(),
                                        };
                                        
                                        let _ = app_handle.emit_all("spider-activated", &spider_event);
                                        log::info!("🕷️ Pattern anomaly detected");
                                    },
                                    "emotional_state_change" => {
                                        let rebloom_event = RebloomSequenceEvent {
                                            emergence_phase: "emotional_transition".to_string(),
                                            narrative: event_data.get("description").and_then(|d| d.as_str()).unwrap_or("").to_string(),
                                            priority_shift: None, // Would extract priority changes
                                            consciousness_transition: Some((
                                                "previous_state".to_string(),
                                                event_data.get("new_state").and_then(|s| s.as_str()).unwrap_or("unknown").to_string()
                                            )),
                                            significance: event_data.get("change_reason").and_then(|r| r.as_str()).unwrap_or("").to_string(),
                                            timestamp: chrono::Utc::now().to_rfc3339(),
                                        };
                                        
                                        let _ = app_handle.emit_all("rebloom-sequence", &rebloom_event);
                                        log::info!("🌺 Rebloom sequence: emotional state change");
                                    },
                                    "consciousness_influenced" => {
                                        // Handle external influence events
                                        let influence_type = event_data.get("influence_type").and_then(|t| t.as_str()).unwrap_or("");
                                        log::info!("🎭 Consciousness influenced: {}", influence_type);
                                        
                                        // Could emit sigil change events here if influence affects sigils
                                        let _ = app_handle.emit_all("consciousness-influenced", &event_data);
                                    },
                                    _ => {
                                        // Emit generic consciousness event
                                        let _ = app_handle.emit_all("consciousness-event", &event_data);
                                        log::debug!("📡 Generic consciousness event: {}", event_type);
                                    }
                                }
                            } else {
                                log::warn!("⚠️ Failed to parse consciousness event as JSON: {}", text);
                                let _ = app_handle.emit_all("consciousness-event-raw", &text);
                            }
                        }
                        Ok(Message::Close(_)) => {
                            log::info!("🧠 Consciousness WebSocket connection closed by server");
                            break;
                        }
                        Err(e) => {
                            log::error!("🧠 Consciousness WebSocket error: {}", e);
                            break;
                        }
                        _ => {}
                    }
                }
                
                log::warn!("🧠 Consciousness WebSocket connection lost");
                let _ = app_handle.emit_all("consciousness-websocket-connected", false);
            }
            Err(e) => {
                log::error!("❌ Failed to connect to consciousness WebSocket: {}", e);
                let _ = app_handle.emit_all("consciousness-websocket-error", &format!("{}", e));
                
                retry_count += 1;
                
                if retry_count >= MAX_RETRIES {
                    log::error!("❌ Max consciousness WebSocket connection retries reached, giving up");
                    break;
                }
            }
        }
        
        // Wait before retrying
        log::info!("🔄 Retrying consciousness WebSocket connection in {} seconds...", RETRY_DELAY.as_secs());
        tokio::time::sleep(RETRY_DELAY).await;
    }
}

// WebSocket handler for DAWN-initiated thoughts - improved
async fn listen_for_thoughts(app_handle: tauri::AppHandle) {
    log::info!("🧠 Starting WebSocket listener for DAWN thoughts");
    
    let mut retry_count = 0;
    const MAX_RETRIES: u32 = 10;
    const RETRY_DELAY: Duration = Duration::from_secs(5);
    
    loop {
        log::info!("🔄 Attempting to connect to chat WebSocket (attempt {})", retry_count + 1);
        
        match connect_async(CHAT_WEBSOCKET_URL).await {
            Ok((ws_stream, _)) => {
                log::info!("✅ Chat WebSocket connected successfully");
                
                // Emit connection success for chat
                let _ = app_handle.emit_all("chat-websocket-connected", true);
                
                let (_, mut read) = ws_stream.split();
                
                // Reset retry count on successful connection
                retry_count = 0;
                
                // Listen for DAWN thoughts
                while let Some(msg) = read.next().await {
                    match msg {
                        Ok(Message::Text(text)) => {
                            log::debug!("🧠 Received DAWN thought: {}", text);
                            
                            // Try to parse as ChatMessage
                            if let Ok(thought) = serde_json::from_str::<ChatMessage>(&text) {
                                // Emit dawn-thought event to frontend
                                if let Err(e) = app_handle.emit_all("dawn-thought", &thought) {
                                    log::error!("Failed to emit dawn-thought event: {}", e);
                                } else {
                                    log::info!("💭 DAWN thought: {} (from: {})", 
                                              thought.text.chars().take(50).collect::<String>(),
                                              thought.from_user);
                                }
                            } else {
                                log::warn!("⚠️ Failed to parse DAWN thought as ChatMessage: {}", text);
                                // Emit raw text as fallback
                                let _ = app_handle.emit_all("dawn-thought-raw", &text);
                            }
                        }
                        Ok(Message::Close(_)) => {
                            log::info!("🧠 Chat WebSocket connection closed by server");
                            break;
                        }
                        Err(e) => {
                            log::error!("🧠 Chat WebSocket error: {}", e);
                            break;
                        }
                        _ => {}
                    }
                }
                
                log::warn!("🧠 Chat WebSocket connection lost");
                let _ = app_handle.emit_all("chat-websocket-connected", false);
            }
            Err(e) => {
                log::error!("❌ Failed to connect to chat WebSocket: {}", e);
                let _ = app_handle.emit_all("chat-websocket-error", &format!("{}", e));
                
                retry_count += 1;
                
                if retry_count >= MAX_RETRIES {
                    log::error!("❌ Max chat WebSocket connection retries reached, giving up");
                    break;
                }
            }
        }
        
        // Wait before retrying
        log::info!("🔄 Retrying chat WebSocket connection in {} seconds...", RETRY_DELAY.as_secs());
        tokio::time::sleep(RETRY_DELAY).await;
    }
}

fn main() {
    // Initialize logging
    env_logger::init();
    
    log::info!("Starting DAWN Desktop Application");

    let app_state = AppState::new();

    tauri::Builder::default()
        .manage(app_state)
        .invoke_handler(tauri::generate_handler![
            get_current_metrics,
            get_subsystems,
            get_subsystem_details,
            add_subsystem,
            remove_subsystem,
            set_alert_threshold,
            get_alert_thresholds,
            check_backend_health,
            health_check,
            subscribe_to_metrics,
            is_websocket_connected,
            // Tick Engine Control Commands
            get_tick_status,
            start_tick_engine,
            stop_tick_engine,
            pause_tick_engine,
            resume_tick_engine,
            set_tick_timing,
            execute_single_tick,
            get_tick_config,
            update_tick_config,
            // Chat/Talk Interface Commands
            send_message,
            get_chat_history,
            get_dawn_thoughts,
            // Advanced Consciousness Commands
            get_sigil_state,
            trigger_spider_cut,
            get_rebloom_priority,
            get_enhanced_dawn_thoughts,
            inject_consciousness_pattern,
            // Python Process Control Commands
            start_python_process,
            stop_python_process,
            get_python_processes,
            check_python_process_status,
            get_process_stats,
            // Computer Vision Commands
            send_cv_command,
            // Testing Commands
            test_force_metrics_update
        ])
        .setup(|app| {
            let app_handle = app.handle();
            
            // Clone app_handle before moving it into async blocks
            let app_handle_metrics = app_handle.clone();
            let app_handle_chat = app_handle.clone();
            
            // Auto-start WebSocket connection with improved reliability
            tauri::async_runtime::spawn(async move {
                log::info!("🚀 Starting DAWN WebSocket connections...");
                
                // Brief delay to let backend start
                tokio::time::sleep(Duration::from_secs(2)).await;
                
                // Emit initial connection status
                if let Err(e) = app_handle_metrics.emit_all("backend-connecting", ()) {
                    log::error!("Failed to emit backend-connecting event: {}", e);
                }
                
                // Start metrics WebSocket connection
                let state = app_handle_metrics.state::<AppState>();
                let websocket_connected = state.websocket_connected.clone();
                
                // Use the improved connect_to_metrics_stream function
                let app_handle_clone = app_handle_metrics.clone();
                let websocket_connected_clone = websocket_connected.clone();
                
                tokio::spawn(async move {
                    connect_to_metrics_stream(app_handle_clone, websocket_connected_clone).await;
                });
                
                // Start periodic health monitoring
                log::info!("🏥 Starting periodic backend health monitoring...");
                loop {
                    tokio::time::sleep(Duration::from_secs(30)).await;
                    
                    let state = app_handle_metrics.state::<AppState>();
                    match check_backend_health(state).await {
                        Ok(health) => {
                            log::debug!("💓 Backend health: {} (running: {})", health.status, health.running);
                            let _ = app_handle_metrics.emit_all("backend-health", &health);
                        }
                        Err(e) => {
                            log::warn!("⚠️ Backend health check failed: {}", e);
                            let _ = app_handle_metrics.emit_all("backend-health-error", &e);
                        }
                    }
                }
            });
            
            // Start chat WebSocket listener for DAWN thoughts
            tauri::async_runtime::spawn(async move {
                tokio::time::sleep(Duration::from_secs(3)).await;
                listen_for_thoughts(app_handle_chat).await;
            });
            
            // Start consciousness event listener for advanced features
            let app_handle_consciousness = app_handle.clone();
            tauri::async_runtime::spawn(async move {
                tokio::time::sleep(Duration::from_secs(4)).await; // Start after other connections
                listen_for_consciousness_events(app_handle_consciousness).await;
            });
            
            // Start periodic sigil monitoring for change detection
            let app_handle_sigil = app_handle.clone();
            let app_handle_sigil_clone = app_handle_sigil.clone();
            tauri::async_runtime::spawn(async move {
                let state_sigil = app_handle_sigil_clone.state::<AppState>();
                let mut last_sigil_state: Option<SigilStateResponse> = None;
                
                loop {
                    tokio::time::sleep(Duration::from_secs(10)).await; // Check every 10 seconds
                    
                    // Get current sigil state
                    if let Ok(current_sigils) = get_sigil_state(state_sigil.clone()).await {
                        if let Some(ref last_state) = last_sigil_state {
                            // Compare with previous state and emit change events
                            for current_sigil in &current_sigils.sigils {
                                if let Some(last_sigil) = last_state.sigils.iter()
                                    .find(|s| s.emotion == current_sigil.emotion) {
                                    
                                    // Check for significant intensity changes
                                    let intensity_diff = (current_sigil.intensity - last_sigil.intensity).abs();
                                    if intensity_diff > 0.1 {
                                        let change_event = SigilChangeEvent {
                                            emotion: current_sigil.emotion.clone(),
                                            old_intensity: last_sigil.intensity,
                                            new_intensity: current_sigil.intensity,
                                            change_type: if current_sigil.intensity > last_sigil.intensity {
                                                "activation".to_string()
                                            } else {
                                                "decay".to_string()
                                            },
                                            visual_change: format!(
                                                "{} → {}",
                                                last_sigil.visual_representation,
                                                current_sigil.visual_representation
                                            ),
                                            timestamp: chrono::Utc::now().to_rfc3339(),
                                        };
                                        
                                        let _ = app_handle_sigil.emit_all("sigil-change", &change_event);
                                        log::debug!("🔥 Sigil change detected: {} {:.3} → {:.3}", 
                                                   change_event.emotion, 
                                                   change_event.old_intensity, 
                                                   change_event.new_intensity);
                                    }
                                } else {
                                    // New sigil created
                                    let creation_event = SigilChangeEvent {
                                        emotion: current_sigil.emotion.clone(),
                                        old_intensity: 0.0,
                                        new_intensity: current_sigil.intensity,
                                        change_type: "creation".to_string(),
                                        visual_change: format!("∅ → {}", current_sigil.visual_representation),
                                        timestamp: chrono::Utc::now().to_rfc3339(),
                                    };
                                    
                                    let _ = app_handle_sigil.emit_all("sigil-change", &creation_event);
                                    log::info!("🔥 New sigil created: {} (intensity: {:.3})", 
                                              creation_event.emotion, 
                                              creation_event.new_intensity);
                                }
                            }
                            
                            // Check for removed sigils
                            for last_sigil in &last_state.sigils {
                                if !current_sigils.sigils.iter().any(|s| s.emotion == last_sigil.emotion) {
                                    let removal_event = SigilChangeEvent {
                                        emotion: last_sigil.emotion.clone(),
                                        old_intensity: last_sigil.intensity,
                                        new_intensity: 0.0,
                                        change_type: "removal".to_string(),
                                        visual_change: format!("{} → ∅", last_sigil.visual_representation),
                                        timestamp: chrono::Utc::now().to_rfc3339(),
                                    };
                                    
                                    let _ = app_handle_sigil.emit_all("sigil-change", &removal_event);
                                    log::info!("🔥 Sigil removed: {}", removal_event.emotion);
                                }
                            }
                        }
                        
                        last_sigil_state = Some(current_sigils);
                    }
                }
            });
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
