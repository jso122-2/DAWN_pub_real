# DAWN API Startup Guide

## Quick Start

### Windows (PowerShell or Command Prompt)
```bash
# Method 1: Using the batch script
start_dawn.bat

# Method 2: Using Python script
python start_dawn_api.py

# Method 3: Using Python script in debug mode
python start_debug_dawn.py
```

### Linux/WSL/macOS
```bash
# Make the script executable (first time only)
chmod +x start_dawn.sh

# Method 1: Using the shell script
./start_dawn.sh

# Method 2: Using Python script
python3 start_dawn_api.py

# Method 3: Using Python script in debug mode
python3 start_debug_dawn.py
```

## Manual Start (Any Platform)

If the scripts don't work, you can start the API manually:

```bash
# 1. Set PYTHONPATH to include the project root
# Windows:
set PYTHONPATH=C:\Users\Admin\Documents\DAWN_Vault\Tick_engine;%PYTHONPATH%

# Linux/WSL:
export PYTHONPATH=/mnt/c/Users/Admin/Documents/DAWN_vault/Tick_engine:$PYTHONPATH

# 2. Navigate to the interface directory
cd interface

# 3. Start the server
python -m uvicorn dawn_api:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'consciousness'"

This means Python can't find the DAWN modules. Make sure:
1. You're running from the correct directory
2. PYTHONPATH is set correctly (see Manual Start section)

### Port 8000 Already in Use

If port 8000 is occupied, you can use a different port:
```bash
python -m uvicorn dawn_api:app --reload --host 0.0.0.0 --port 8001
```

### WSL-Specific Issues

If running from WSL and imports fail:
1. Make sure you're using the Linux path format: `/mnt/c/Users/...`
2. Check case sensitivity - Linux is case-sensitive (`DAWN_vault` vs `DAWN_Vault`)

## API Endpoints

Once running, the API will be available at:
- Base URL: http://localhost:8000
- Health Check: http://localhost:8000/health
- API Documentation: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws

## Development Tips

- Use `start_debug_dawn.py` for verbose logging during development
- The `--reload` flag enables auto-reload when files change
- Check the console output for any import errors or warnings 