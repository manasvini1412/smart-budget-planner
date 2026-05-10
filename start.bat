@echo off
REM ###########################################################################
REM Smart Budget Planner - START SCRIPT (Windows)
REM This script handles:
REM - Checking dependencies
REM - Initializing database
REM - Starting the Flask application
REM ###########################################################################

setlocal enabledelayedexpansion

cls
echo.
echo ===============================================================
echo     ^>^> Smart Budget Planner - Startup Script
echo ===============================================================
echo.

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM =========================================================================
REM STEP 1: Check if Python is installed
REM =========================================================================
echo [1/4] Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo OK Python found: %PYTHON_VERSION%
echo.

REM =========================================================================
REM STEP 2: Check and install dependencies
REM =========================================================================
echo [2/4] Checking Python dependencies...

if not exist "%SCRIPT_DIR%requirements.txt" (
    echo X requirements.txt not found!
    pause
    exit /b 1
)

python -c "import flask, pandas, numpy" >nul 2>&1
if errorlevel 1 (
    echo ! Installing required packages...
    python -m pip install -r "%SCRIPT_DIR%requirements.txt" >nul 2>&1
    if errorlevel 1 (
        echo X Failed to install dependencies
        echo Try running manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo OK Dependencies installed successfully
) else (
    echo OK All dependencies are installed
)
echo.

REM =========================================================================
REM STEP 3: Initialize database
REM =========================================================================
echo [3/4] Initializing database...

if not exist "%SCRIPT_DIR%database.db" (
    echo ! Database not found. Creating...
    python "%SCRIPT_DIR%database.py" >nul 2>&1
    if errorlevel 1 (
        echo X Failed to initialize database
        echo Try running manually: python database.py
        pause
        exit /b 1
    )
    echo OK Database initialized successfully
) else (
    echo OK Database already exists
)
echo.

REM =========================================================================
REM STEP 4: Check if port 5000 is in use
REM =========================================================================
netstat -ano | findstr :5000 >nul 2>&1
if not errorlevel 1 (
    echo X Port 5000 is already in use!
    echo.
    echo To find and kill the process:
    echo   netstat -ano | findstr :5000
    echo   taskkill /PID [PID] /F
    pause
    exit /b 1
)

REM =========================================================================
REM STEP 5: Start the Flask application
REM =========================================================================
echo [4/4] Starting Flask application...
echo.
echo ===============================================================
echo     ^>^> Smart Budget Planner is running!
echo ===============================================================
echo.
echo Open your browser and navigate to:
echo    http://localhost:5000
echo.
echo To stop the application, press: Ctrl + C
echo ===============================================================
echo.

cd /d "%SCRIPT_DIR%"
python app.py

pause
