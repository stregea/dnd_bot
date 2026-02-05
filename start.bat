@echo off
REM =============================================================================
REM DnD Roller Bot - Windows Startup Script
REM =============================================================================
REM This script automates the setup and startup of the DnD Roller Discord bot.
REM It handles virtual environment creation, dependency installation, and
REM launching the bot.
REM
REM Usage: start.bat (or double-click in File Explorer)
REM =============================================================================

setlocal EnableDelayedExpansion

REM -----------------------------------------------------------------------------
REM Configuration
REM -----------------------------------------------------------------------------
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"
set "REQUIREMENTS_FILE=%SCRIPT_DIR%requirements.txt"
set "MAIN_SCRIPT=%SCRIPT_DIR%dnd_roller.py"
set "PYTHON_CMD=python"

REM -----------------------------------------------------------------------------
REM Header
REM -----------------------------------------------------------------------------
echo.
echo ==============================================
echo    DnD Roller Bot - Setup ^& Startup Script
echo ==============================================
echo.

REM -----------------------------------------------------------------------------
REM Change to script directory
REM -----------------------------------------------------------------------------
cd /d "%SCRIPT_DIR%"

REM -----------------------------------------------------------------------------
REM Check Python Installation
REM -----------------------------------------------------------------------------
echo [INFO] Checking Python installation...

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo [ERROR] Please install Python 3.12 or later from https://python.org
    echo [ERROR] Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo [SUCCESS] Using: %PYTHON_VER%

REM -----------------------------------------------------------------------------
REM Create Virtual Environment
REM -----------------------------------------------------------------------------
if not exist "%VENV_DIR%" (
    echo [INFO] Creating virtual environment...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
) else (
    echo [INFO] Virtual environment already exists.
)

REM -----------------------------------------------------------------------------
REM Activate Virtual Environment
REM -----------------------------------------------------------------------------
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated.

REM -----------------------------------------------------------------------------
REM Install Dependencies
REM -----------------------------------------------------------------------------
echo [INFO] Checking and installing dependencies...

REM Upgrade pip first
python -m pip install --upgrade pip --quiet 2>nul

REM Check if requirements.txt exists
if exist "%REQUIREMENTS_FILE%" (
    python -m pip install -r "%REQUIREMENTS_FILE%" --quiet
    echo [SUCCESS] Dependencies installed from requirements.txt
) else (
    echo [WARNING] requirements.txt not found. Installing minimum dependencies...
    python -m pip install discord.py --quiet
    echo [SUCCESS] discord.py installed.
)

REM -----------------------------------------------------------------------------
REM Start the Bot
REM -----------------------------------------------------------------------------
echo.
echo ==============================================
echo    DnD Roller Bot Starting...
echo ==============================================
echo.

python "%MAIN_SCRIPT%"

REM -----------------------------------------------------------------------------
REM Keep window open if bot crashes
REM -----------------------------------------------------------------------------
echo.
echo [INFO] Bot has stopped. Press any key to exit...
pause >nul
