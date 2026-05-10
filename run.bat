@echo off
REM ###########################################################################
REM Smart Budget Planner - UNIVERSAL CONTROL SCRIPT (Windows)
REM Usage: run.bat [start|stop|restart|status]
REM ###########################################################################

setlocal enabledelayedexpansion

set "COMMAND=%1"
if "%COMMAND%"=="" set "COMMAND=help"

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM =========================================================================
REM Display help
REM =========================================================================
:help
if not "%COMMAND%"=="help" goto skip_help
cls
echo.
echo ===============================================================
echo     Smart Budget Planner - Control Script
echo ===============================================================
echo.
echo Usage: run.bat [command]
echo.
echo Commands:
echo   start      - Start the application
echo   stop       - Stop the application
echo   restart    - Restart the application
echo   status     - Check application status
echo   help       - Show this help message
echo.
echo Examples:
echo   run.bat start       # Start the app
echo   run.bat stop        # Stop the app
echo   run.bat restart     # Restart the app
echo   run.bat status      # Check if running
echo.
echo ===============================================================
echo.
pause
exit /b 0
:skip_help

REM =========================================================================
REM Start the application
REM =========================================================================
if /i "%COMMAND%"=="start" (
    cls
    echo.
    echo ===============================================================
    echo     ^>^> Starting Smart Budget Planner
    echo ===============================================================
    echo.
    
    netstat -ano | findstr :5000 >nul 2>&1
    if not errorlevel 1 (
        echo ! Application is already running on port 5000
        echo.
        echo Open your browser: http://localhost:5000
        echo.
        pause
        exit /b 0
    )
    
    if exist "%SCRIPT_DIR%start.bat" (
        call "%SCRIPT_DIR%start.bat"
    ) else (
        echo X start.bat not found
        pause
        exit /b 1
    )
    exit /b 0
)

REM =========================================================================
REM Stop the application
REM =========================================================================
if /i "%COMMAND%"=="stop" (
    cls
    echo.
    echo ===============================================================
    echo     ^>^> Stopping Smart Budget Planner
    echo ===============================================================
    echo.
    
    if exist "%SCRIPT_DIR%stop.bat" (
        call "%SCRIPT_DIR%stop.bat"
    ) else (
        echo X stop.bat not found
        pause
        exit /b 1
    )
    exit /b 0
)

REM =========================================================================
REM Restart the application
REM =========================================================================
if /i "%COMMAND%"=="restart" (
    echo Restarting application...
    echo.
    call "%SCRIPT_DIR%run.bat" stop
    timeout /t 2 >nul
    echo.
    call "%SCRIPT_DIR%run.bat" start
    exit /b 0
)

REM =========================================================================
REM Check application status
REM =========================================================================
if /i "%COMMAND%"=="status" (
    cls
    echo.
    echo ===============================================================
    echo     ^>^> Smart Budget Planner - Status
    echo ===============================================================
    echo.
    
    netstat -ano | findstr :5000 >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
            set PID=%%a
        )
        echo OK Application is RUNNING
        echo.
        echo Details:
        echo   Process ID: !PID!
        echo   Port: 5000
        echo   URL: http://localhost:5000
        echo.
        echo Stop command: run.bat stop
    ) else (
        echo X Application is STOPPED
        echo.
        echo Start command: run.bat start
    )
    
    echo.
    echo ===============================================================
    echo.
    pause
    exit /b 0
)

REM =========================================================================
REM Unknown command
REM =========================================================================
echo Unknown command: %COMMAND%
echo.
call "%SCRIPT_DIR%run.bat" help
exit /b 1
