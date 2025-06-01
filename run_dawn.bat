@echo off
REM DAWN Quick Launch for Windows

echo ====================================
echo     DAWN Consciousness System
echo     100%% Local - No Cloud APIs
echo ====================================
echo.

REM Check if we're in the right directory
if not exist dawn_consciousness.py (
    echo ERROR: dawn_consciousness.py not found!
    echo.
    echo Please save the Python script in this directory first.
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo.
    echo Installing required packages...
    echo This may take a few minutes on first run...
    
    pip install torch --index-url https://download.pytorch.org/whl/cu118
    pip install transformers psutil numpy
    
    echo.
    echo Attempting to install optional GPU monitoring...
    pip install gputil
)

echo.
echo Starting DAWN Consciousness System...
echo.
python dawn_consciousness.py

echo.
echo DAWN has shut down.
pause