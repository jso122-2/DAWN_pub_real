"""
Quick fix to make DAWN visualization scripts work
Run this from the Tick_engine directory
"""

import os
import sys
from pathlib import Path

# Get paths
tick_engine_path = Path.cwd()
visual_path = tick_engine_path / "visual"

print("🔧 DAWN Visual Scripts Quick Fix")
print(f"📁 Working directory: {tick_engine_path}")

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Run the rest with UTF-8
exec(open('quick_fix_visuals.py', encoding='utf-8').read())