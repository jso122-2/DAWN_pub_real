# DAWN Visualization Batch Runner (PowerShell)
# Runs all DAWN cognitive visualization processes in parallel

param(
    [string]$Source = "stdin",
    [int]$Interval = 100,
    [int]$BufferSize = 100,
    [string]$LogDir = "logs",
    [switch]$KillExisting,
    [switch]$Help
)

# Help function
function Show-Help {
    Write-Host "DAWN Visualization Batch Runner (PowerShell)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run_visualizations.ps1 [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -Source SOURCE    Data source: 'stdin' (default) or 'demo'" -ForegroundColor Gray
    Write-Host "  -Interval MS      Animation interval in milliseconds (default: 100)" -ForegroundColor Gray
    Write-Host "  -BufferSize SIZE  Buffer size for visualizations (default: 100)" -ForegroundColor Gray
    Write-Host "  -LogDir DIR       Directory for log files (default: logs)" -ForegroundColor Gray
    Write-Host "  -KillExisting     Kill any existing visualization processes" -ForegroundColor Gray
    Write-Host "  -Help             Show this help message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\run_visualizations.ps1                                    # Run with defaults" -ForegroundColor Gray
    Write-Host "  .\run_visualizations.ps1 -Source demo -Interval 200        # Run in demo mode" -ForegroundColor Gray
    Write-Host "  .\run_visualizations.ps1 -KillExisting                     # Kill existing processes" -ForegroundColor Gray
}

# Show help if requested
if ($Help) {
    Show-Help
    exit 0
}

# Configuration
$VisualDir = "visual"
$PidFile = "visualization_pids.txt"

# Visualization scripts to run
$Visualizations = @(
    "scup_zone_animator.py",
    "tick_pulse.py", 
    "consciousness_constellation.py",
    "SCUP_pressure_grid.py",
    "heat_monitor.py",
    "entropy_flow.py",
    "semantic_flow_graph.py",
    "recursive_depth_explorer.py",
    "bloom_genealogy_network.py",
    "sigil_command_stream.py",
    "dawn_mood_state.py"
)

# Process storage
$Processes = @()

# Function to write colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
}

# Function to check if process is running
function Test-ProcessRunning {
    param([int]$ProcessId)
    try {
        $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
        return $process -ne $null
    }
    catch {
        return $false
    }
}

# Function to kill existing processes
function Stop-ExistingProcesses {
    Write-Status "Checking for existing visualization processes..."
    
    # Kill processes from PID file if it exists
    if (Test-Path $PidFile) {
        $pids = Get-Content $PidFile
        foreach ($pid in $pids) {
            if ($pid -and (Test-ProcessRunning $pid)) {
                Write-Warning "Killing existing process PID $pid"
                try {
                    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
                }
                catch {
                    # Process might already be dead
                }
            }
        }
    }
    
    # Remove PID file
    if (Test-Path $PidFile) {
        Remove-Item $PidFile -Force
    }
    
    # Kill any remaining python processes that might be our visualizations
    try {
        Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -eq "python" } | Stop-Process -Force
    }
    catch {
        # No python processes running
    }
    
    Write-Status "Existing processes cleaned up"
}

# Function to start a visualization
function Start-Visualization {
    param([string]$Script)
    
    $logFile = Join-Path $LogDir ($Script -replace '\.py$', '.log')
    
    Write-Status "Starting $Script..."
    
    # Check if script exists
    $scriptPath = Join-Path $VisualDir $Script
    if (-not (Test-Path $scriptPath)) {
        Write-Error "Script not found: $scriptPath"
        return $null
    }
    
    # Create log directory if it doesn't exist
    if (-not (Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    }
    
    # Start the visualization
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "python"
    $startInfo.Arguments = "`"$scriptPath`" --source $Source --interval $Interval --buffer $BufferSize"
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $false
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    
    try {
        $process.Start() | Out-Null
        
        # Save PID to file
        $process.Id | Out-File -FilePath $PidFile -Append
        
        Write-Status "$Script started with PID $($process.Id) (log: $logFile)"
        
        # Give it a moment to start up
        Start-Sleep -Milliseconds 500
        
        # Check if process is still running
        if (-not $process.HasExited) {
            Write-Status "$Script is running successfully"
            return $process
        } else {
            Write-Error "$Script failed to start (check $logFile for details)"
            return $null
        }
    }
    catch {
        Write-Error "Failed to start $Script : $($_.Exception.Message)"
        return $null
    }
}

# Function to cleanup on exit
function Stop-AllProcesses {
    Write-Status "Shutting down all visualization processes..."
    
    foreach ($process in $Processes) {
        if ($process -and -not $process.HasExited) {
            Write-Status "Killing process $($process.Id)"
            try {
                $process.Kill()
            }
            catch {
                # Process might already be dead
            }
        }
    }
    
    # Clean up PID file
    if (Test-Path $PidFile) {
        Remove-Item $PidFile -Force
    }
    
    Write-Status "All processes stopped"
}

# Set up cleanup on script exit
trap {
    Stop-AllProcesses
    exit 1
}

# Main execution
Write-Header "DAWN Visualization Batch Runner"
Write-Status "Configuration:"
Write-Status "  Data source: $Source"
Write-Status "  Animation interval: ${Interval}ms"
Write-Status "  Buffer size: $BufferSize"
Write-Status "  Log directory: $LogDir"
Write-Status "  Visualizations to start: $($Visualizations.Count)"
Write-Host ""

# Check if visual directory exists
if (-not (Test-Path $VisualDir)) {
    Write-Error "Visualization directory '$VisualDir' not found!"
    exit 1
}

# Kill existing processes if requested
if ($KillExisting) {
    Stop-ExistingProcesses
}

# Check for existing processes
if (Test-Path $PidFile) {
    Write-Warning "Found existing PID file. Use -KillExisting to clean up first."
    exit 1
}

# Validate source parameter
if ($Source -ne "stdin" -and $Source -ne "demo") {
    Write-Error "Invalid source: $Source. Must be 'stdin' or 'demo'"
    exit 1
}

# Start each visualization
Write-Header "Starting Visualizations"

$successCount = 0
$failedCount = 0

foreach ($script in $Visualizations) {
    $process = Start-Visualization $script
    if ($process) {
        $Processes += $process
        $successCount++
    } else {
        $failedCount++
    }
    
    # Small delay between starts
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Status "Started $successCount visualizations successfully"
if ($failedCount -gt 0) {
    Write-Warning "$failedCount visualizations failed to start"
}

Write-Host ""
Write-Status "Visualization processes:"
for ($i = 0; $i -lt $Visualizations.Count; $i++) {
    $script = $Visualizations[$i]
    $process = $Processes[$i]
    if ($process) {
        Write-Host "  $script : PID $($process.Id)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Status "Log files are in: $LogDir"
Write-Status "PID file: $PidFile"
Write-Host ""

# Monitor processes
Write-Status "Monitoring visualization processes..."
Write-Status "Press Ctrl+C to stop all visualizations"
Write-Host ""

try {
    while ($true) {
        $allRunning = $true
        
        foreach ($process in $Processes) {
            if ($process -and $process.HasExited) {
                Write-Warning "Process $($process.Id) has stopped"
                $allRunning = $false
            }
        }
        
        if (-not $allRunning) {
            Write-Warning "Some processes have stopped. Check logs for details."
        }
        
        Start-Sleep -Seconds 5
    }
}
catch {
    # Ctrl+C or other interruption
    Write-Host ""
    Stop-AllProcesses
} 