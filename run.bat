@echo off
REM File Merger Application Launcher (Windows)
REM This script launches the File Merger application

echo.
echo ================================================================
echo                     FILE MERGER v1.0
echo ================================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo Using system Python...
    set PYTHON_CMD=python
)

REM Check command line arguments
if "%1"=="--cli" (
    echo Starting CLI mode...
    %PYTHON_CMD% main.py --cli
) else if "%1"=="--help" (
    echo Showing help...
    %PYTHON_CMD% main.py --help
) else (
    echo Starting GUI mode...
    %PYTHON_CMD% main.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Failed to start the application
    echo.
    echo Troubleshooting:
    echo 1. Make sure Python is installed
    echo 2. Run: python setup.py
    echo 3. Check: python test_installation.py
    echo.
    pause
)
