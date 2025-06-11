// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use tauri::{Manager, State};
use tokio::sync::broadcast;
use futures_util::StreamExt;
use tokio_tungstenite::{connect_async, tungstenite::protocol::Message};
use std::time::Duration;

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

struct AppState {
    metrics: Arc<Mutex<Option<Metrics>>>,
    http_client: reqwest::Client,
    metrics_sender: broadcast::Sender<Metrics>,
    websocket_connected: Arc<Mutex<bool>>,
}

const PYTHON_API_BASE: &str = "http://localhost:8000";
const WEBSOCKET_URL: &str = "ws://localhost:8000/ws";

impl AppState {
    fn new() -> Self {
        let (metrics_sender, _) = broadcast::channel(100);
        Self {
            metrics: Arc::new(Mutex::new(None)),
            http_client: reqwest::Client::new(),
            metrics_sender,
            websocket_connected: Arc::new(Mutex::new(false)),
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
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to fetch metrics: {}", e))?;

    if !response.status().is_success() {
        return Err(format!("HTTP error: {}", response.status()));
    }

    let metrics: Metrics = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse metrics JSON: {}", e))?;

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
        .timeout(Duration::from_secs(10))
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
        .timeout(Duration::from_secs(3))
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
    let websocket_connected_clone = websocket_connected.clone();
    
    tokio::spawn(async move {
        let mut retry_count = 0;
        const MAX_RETRIES: u32 = 10;
        const RETRY_DELAY: Duration = Duration::from_secs(5);
        
        loop {
            log::info!("Attempting to connect to WebSocket (attempt {})", retry_count + 1);
            
            match connect_async(WEBSOCKET_URL).await {
                Ok((ws_stream, _)) => {
                    log::info!("WebSocket connected successfully");
                    {
                        let mut connected = websocket_connected_clone.lock().unwrap();
                        *connected = true;
                    }
                    
                    let (mut _write, mut read) = ws_stream.split();
                    
                    // Reset retry count on successful connection
                    retry_count = 0;
                    
                    // Listen for messages
                    while let Some(msg) = read.next().await {
                        match msg {
                            Ok(Message::Text(text)) => {
                                log::debug!("Received WebSocket message: {}", text);
                                
                                // Try parsing as TickUpdate first (new format), then fall back to Metrics (legacy)
                                if let Ok(tick_update) = serde_json::from_str::<TickUpdate>(&text) {
                                    // Emit enhanced tick update event
                                    if let Err(e) = app_handle_clone.emit_all("tick-update", &tick_update) {
                                        log::error!("Failed to emit tick-update event: {}", e);
                                    } else {
                                        log::debug!("Emitted tick update: tick={}, state={}, SCUP={}", 
                                                   tick_update.tick_number, tick_update.controller_state, tick_update.metrics.scup);
                                    }
                                    
                                    // Also emit metrics-update for backward compatibility
                                    if let Err(e) = app_handle_clone.emit_all("metrics-update", &tick_update.metrics) {
                                        log::error!("Failed to emit metrics-update event: {}", e);
                                    }
                                } else if let Ok(metrics) = serde_json::from_str::<Metrics>(&text) {
                                    // Handle legacy metrics format
                                    if let Err(e) = app_handle_clone.emit_all("metrics-update", &metrics) {
                                        log::error!("Failed to emit metrics-update event: {}", e);
                                    } else {
                                        log::debug!("Emitted metrics update: SCUP={}, Entropy={}, Heat={}", 
                                                   metrics.scup, metrics.entropy, metrics.heat);
                                    }
                                } else {
                                    log::error!("Failed to parse WebSocket message as TickUpdate or Metrics: {}", text);
                                }
                            }
                            Ok(Message::Close(_)) => {
                                log::info!("WebSocket connection closed by server");
                                break;
                            }
                            Err(e) => {
                                log::error!("WebSocket error: {}", e);
                                break;
                            }
                            _ => {}
                        }
                    }
                    
                    log::warn!("WebSocket connection lost");
                    {
                        let mut connected = websocket_connected_clone.lock().unwrap();
                        *connected = false;
                    }
                }
                Err(e) => {
                    log::error!("Failed to connect to WebSocket: {}", e);
                    retry_count += 1;
                    
                    if retry_count >= MAX_RETRIES {
                        log::error!("Max WebSocket connection retries reached, giving up");
                        break;
                    }
                }
            }
            
            // Wait before retrying
            log::info!("Retrying WebSocket connection in {} seconds...", RETRY_DELAY.as_secs());
            tokio::time::sleep(RETRY_DELAY).await;
        }
        
        {
            let mut connected = websocket_connected_clone.lock().unwrap();
            *connected = false;
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
        .timeout(Duration::from_secs(5))
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
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to start tick engine: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
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
        .timeout(Duration::from_secs(5))
        .send()
        .await
        .map_err(|e| format!("Failed to stop tick engine: {}", e))?;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("HTTP error {}: {}", status, error_text));
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
            update_tick_config
        ])
        .setup(|app| {
            let app_handle = app.handle();
            
            // Auto-start WebSocket subscription
            tauri::async_runtime::spawn(async move {
                tokio::time::sleep(Duration::from_secs(2)).await;
                
                if let Err(e) = app_handle.emit_all("backend-connecting", ()) {
                    log::error!("Failed to emit backend-connecting event: {}", e);
                }
                
                // Try to connect to WebSocket
                let state = app_handle.state::<AppState>();
                if let Err(e) = subscribe_to_metrics(app_handle.clone(), state).await {
                    log::error!("Failed to start WebSocket subscription: {}", e);
                    
                    if let Err(e) = app_handle.emit_all("backend-error", &e) {
                        log::error!("Failed to emit backend-error event: {}", e);
                    }
                } else {
                    if let Err(e) = app_handle.emit_all("backend-connected", ()) {
                        log::error!("Failed to emit backend-connected event: {}", e);
                    }
                }
            });
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
