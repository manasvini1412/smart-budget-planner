@echo off
REM ###########################################################################
REM Smart Budget Planner - STOP SCRIPT (Windows)
REM This script handles:
REM - Finding the Flask process running on port 5000
REM - Gracefully shutting down the application
REM ###########################################################################

setlocal enabledelayedexpansion

cls
echo.
echo ===============================================================
echo     ^>^> Smart Budget Planner - Shutdown Script
echo ===============================================================
echo.

REM =========================================================================
REM STEP 1: Check if anything is running on port 5000
REM =========================================================================
echo [1/2] Checking for running processes on port 5000...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    set PID=%%a
)

if not defined PID (
    echo ! No process found running on port 5000
    echo Application may not be running, or running on a different port
    echo.
    echo To find processes on other ports:
    echo   netstat -ano | findstr LISTENING
    echo.
    pause
    exit /b 0
)

echo OK Found process (PID: %PID%) on port 5000
echo.

REM =========================================================================
REM STEP 2: Stop the process
REM =========================================================================
echo [2/2] Stopping the application...
echo.

taskkill /PID %PID% /F >nul 2>&1

timeout /t 2 /nobreak >nul

REM Verify process is stopped
tasklist /FI "PID eq %PID%" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo OK Process stopped successfully
    echo.
    echo ===============================================================
    echo     ^>^> Smart Budget Planner has been shut down
    echo ===============================================================
    echo.
    echo To start again, run: start.bat
    echo.
) else (
    echo X Failed to stop process (PID: %PID%)
    echo Try manual shutdown: taskkill /PID %PID% /F
    pause
    exit /b 1
)

pause
