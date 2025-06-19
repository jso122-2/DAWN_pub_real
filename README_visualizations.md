# DAWN Visualization Batch Runner

This script runs all DAWN cognitive visualization processes in parallel, providing a comprehensive real-time view of DAWN's cognitive state.

## Overview

The `run_visualizations.sh` script manages 11 different visualization processes:

1. **SCUP Zone Animator** - Real-time SCUP zone visualization with cognitive state mapping
2. **Tick Pulse** - Cognitive heartbeat and rhythm analysis
3. **Consciousness Constellation** - 4D SCUP trajectory visualization
4. **SCUP Pressure Grid** - Pressure distribution visualization
5. **Heat Monitor** - Cognitive intensity gauge
6. **Entropy Flow** - Information entropy visualization
7. **Semantic Flow Graph** - Semantic processing visualization
8. **Recursive Depth Explorer** - Recursive processing depth analysis
9. **Bloom Genealogy Network** - Bloom relationship visualization
10. **Sigil Command Stream** - Command processing visualization
11. **DAWN Mood State** - Emotional state visualization

## Prerequisites

- Python 3.7+
- Required Python packages (install via pip):
  ```bash
  pip install matplotlib numpy scipy
  ```
- Bash shell (Linux/WSL) or Git Bash (Windows)

## Usage

### Basic Usage

```bash
# Run all visualizations with default settings
./run_visualizations.sh

# Run in demo mode (simulated data)
./run_visualizations.sh --source demo

# Run with custom settings
./run_visualizations.sh --source stdin --interval 200 --buffer 150
```

### Command Line Options

- `--source SOURCE`: Data source ('stdin' or 'demo')
  - `stdin`: Read live DAWN JSON data from stdin (default)
  - `demo`: Use simulated data for testing
- `--interval MS`: Animation update interval in milliseconds (default: 100)
- `--buffer SIZE`: Buffer size for visualizations (default: 100)
- `--log-dir DIR`: Directory for log files (default: ./logs)
- `--kill-existing`: Kill any existing visualization processes before starting
- `--help`: Show help message

### Examples

```bash
# Start fresh (kill existing processes)
./run_visualizations.sh --kill-existing

# Run in demo mode with slower updates
./run_visualizations.sh --source demo --interval 200

# Custom log directory
./run_visualizations.sh --log-dir ./my_logs

# High-performance mode (faster updates, smaller buffers)
./run_visualizations.sh --interval 50 --buffer 50
```

## Data Source

### stdin Mode (Live Data)
When using `--source stdin`, the script expects DAWN to output JSON data to stdout. Each visualization reads this data and updates in real-time.

Example JSON format:
```json
{
  "tick": 1234,
  "heat": 0.7,
  "mood": {
    "vector": [0.6, 0.4, 0.8, 0.3]
  },
  "entropy": 0.5,
  "scup": {
    "schema": 0.6,
    "coherence": 0.7,
    "utility": 0.5,
    "pressure": 0.8
  }
}
```

### Demo Mode
When using `--source demo`, each visualization generates its own simulated data for testing and demonstration purposes.

## Process Management

### Starting Visualizations
The script starts each visualization as a background process and monitors their status. Each process gets its own log file in the specified log directory.

### Monitoring
The script continuously monitors all processes and reports any that stop unexpectedly. Press `Ctrl+C` to gracefully stop all visualizations.

### Log Files
Each visualization creates a log file in the format: `logs/script_name.log`

Example log files:
- `logs/scup_zone_animator.log`
- `logs/tick_pulse.log`
- `logs/consciousness_constellation.log`
- etc.

### Process IDs
The script maintains a `visualization_pids.txt` file containing the process IDs of all running visualizations for easy management.

## Troubleshooting

### Common Issues

1. **Script not found errors**
   - Ensure you're in the correct directory
   - Check that the `visual/` directory exists and contains the Python scripts

2. **Python import errors**
   - Install required packages: `pip install matplotlib numpy scipy`
   - Ensure Python 3.7+ is installed

3. **Permission denied**
   - Make script executable: `chmod +x run_visualizations.sh`
   - On Windows, use Git Bash or WSL

4. **Processes not starting**
   - Check log files for error messages
   - Verify Python environment and dependencies
   - Try running individual scripts manually to isolate issues

5. **High CPU usage**
   - Increase animation interval: `--interval 200`
   - Reduce buffer size: `--buffer 50`
   - Run fewer visualizations by modifying the script

### Individual Script Testing

To test individual visualizations:

```bash
# Test a single visualization
python3 visual/scup_zone_animator.py --source demo

# Test with live data
echo '{"tick": 1, "heat": 0.5}' | python3 visual/tick_pulse.py --source stdin
```

## Performance Considerations

- **CPU Usage**: Each visualization uses matplotlib animations which can be CPU-intensive
- **Memory Usage**: Buffer sizes affect memory consumption
- **Display**: Multiple matplotlib windows may impact system performance
- **Network**: If using remote data sources, network latency affects real-time updates

### Optimization Tips

- Use `--interval 200` for slower, less CPU-intensive updates
- Use `--buffer 50` for lower memory usage
- Run on a machine with good graphics capabilities
- Close unnecessary applications while running visualizations

## Integration with DAWN

To integrate with the DAWN system:

1. Ensure DAWN outputs JSON data to stdout
2. Pipe DAWN output to the visualization script
3. Use `--source stdin` mode

Example integration:
```bash
# Run DAWN and pipe to visualizations
python3 dawn_main.py | ./run_visualizations.sh --source stdin
```

## Customization

### Adding New Visualizations
To add a new visualization:

1. Add the script name to the `VISUALIZATIONS` array in the script
2. Ensure the script follows the same argument pattern as existing ones
3. Test individually before adding to the batch runner

### Modifying Default Settings
Edit the default configuration variables at the top of the script:
```bash
SOURCE="stdin"
INTERVAL=100
BUFFER_SIZE=100
LOG_DIR="./logs"
```

## Support

For issues or questions:
1. Check the log files for error messages
2. Test individual visualizations
3. Verify system requirements and dependencies
4. Check the DAWN documentation for data format requirements 