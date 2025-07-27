Write-Host "🧨 NUCLEAR RESET: Tauri Setup" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Remove all build artifacts and caches
Write-Host "🗑️ Removing build artifacts..." -ForegroundColor Yellow
if (Test-Path "src-tauri\target") { Remove-Item -Path "src-tauri\target" -Recurse -Force }
if (Test-Path "node_modules") { Remove-Item -Path "node_modules" -Recurse -Force }
if (Test-Path "package-lock.json") { Remove-Item -Path "package-lock.json" -Force }
if (Test-Path "src-tauri\Cargo.lock") { Remove-Item -Path "src-tauri\Cargo.lock" -Force }
if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }

Write-Host "✅ Build artifacts removed" -ForegroundColor Green

# Clean Cargo cache
Write-Host "🧹 Cleaning Cargo cache..." -ForegroundColor Yellow
Set-Location "src-tauri"
cargo clean
Set-Location ".."

Write-Host "✅ Cargo cache cleaned" -ForegroundColor Green

# Update Cargo.toml to use Tauri v2
Write-Host "⬆️ Updating to Tauri v2..." -ForegroundColor Yellow

$cargoToml = @"
[package]
name = "dawn-consciousness-gui"
version = "1.0.0"
description = "DAWN Consciousness GUI - Native consciousness monitoring interface"
authors = ["DAWN Team"]
license = ""
repository = ""
default-run = "dawn-consciousness-gui"
edition = "2021"
rust-version = "1.60"

[build-dependencies]
tauri-build = { version = "2.0", features = [] }

[dependencies]
serde_json = "1.0"
serde = { version = "1.0", features = ["derive"] }
tauri = { version = "2.0", features = ["shell-open"] }
tauri-plugin-shell = "2.0"
memmap2 = "0.7"
tokio = { version = "1.0", features = ["full"] }

[features]
# this feature is used for production builds or when `devPath` points to the filesystem and the built-in dev server is disabled.
# DO NOT REMOVE!!
custom-protocol = ["tauri/custom-protocol"]
"@

$cargoToml | Out-File -FilePath "src-tauri\Cargo.toml" -Encoding UTF8

Write-Host "✅ Cargo.toml updated to v2" -ForegroundColor Green

# Create proper Tauri v2 config
Write-Host "⚙️ Creating Tauri v2 configuration..." -ForegroundColor Yellow

$tauriConfig = @"
{
  "productName": "DAWN Consciousness Monitor",
  "version": "1.0.0",
  "identifier": "com.dawn.consciousness.gui",
  "build": {
    "frontendDist": "../dist"
  },
  "app": {
    "windows": [
      {
        "title": "DAWN Consciousness Monitor",
        "width": 1400,
        "height": 900,
        "resizable": true,
        "fullscreen": false,
        "center": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all"
  }
}
"@

$tauriConfig | Out-File -FilePath "src-tauri\tauri.conf.json" -Encoding UTF8

Write-Host "✅ Tauri v2 config created" -ForegroundColor Green

# Create dist directory and copy HTML
Write-Host "📁 Setting up frontend..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "dist" -Force | Out-Null
Copy-Item -Path "simple_gui.html" -Destination "dist\index.html" -Force

Write-Host "✅ Frontend prepared" -ForegroundColor Green

Write-Host ""
Write-Host "🎯 NUCLEAR RESET COMPLETE!" -ForegroundColor Green
Write-Host "Now run: cargo tauri dev" -ForegroundColor Cyan 