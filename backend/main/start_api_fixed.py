#!/usr/bin/env python3
"""
Fixed DAWN API Starter - Sets proper Python paths
"""
import os
import sys
import subprocess
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.demo_advanced_consciousness import run_demo
from main.restart_dawn_clean import restart_dawn
from main.start_dawn_api import start_api
from main.run_kan_server import run_kan
from main.integrate_kan_cairrn import integrate
from main.juliet_flower import run_juliet

# Get the project root directory (Tick_engine)
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
os.environ['PYTHONPATH'] = str(project_root) + ':' + os.environ.get('PYTHONPATH', '')

print(f"✅ Set PYTHONPATH to: {project_root}")
print(f"📁 Working directory: {os.getcwd()}")

# Change to interface directory for the API
interface_dir = project_root / "interface"
if interface_dir.exists():
    os.chdir(interface_dir)
    print(f"📂 Changed to interface directory: {interface_dir}")

# Run the API with uvicorn
cmd = [
    sys.executable,
    "-m", "uvicorn",
    "dawn_api:app",
    "--reload",
    "--host", "0.0.0.0",
    "--port", "8000"
]

print(f"🚀 Starting DAWN API with command: {' '.join(cmd)}")
subprocess.run(cmd)
