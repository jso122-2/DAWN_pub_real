@echo off
echo.
echo 🌅 Starting DAWN Interactive Environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Run DAWN
python run_dawn.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo ❌ DAWN exited with an error
    pause
)