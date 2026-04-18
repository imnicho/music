@echo off
REM OctaveLights One-Click Setup and Build Script
REM This script handles everything: clone, venv, dependencies, build
REM Usage: Double-click this file or run from cmd

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   OctaveLights - One-Click Setup and Build
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.11+ is required but not found in PATH
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Detected Python: %PYTHON_VERSION%
echo.

REM Check if Inno Setup is installed
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "!INNO_PATH!" (
    echo Warning: Inno Setup 6 not found
    echo   Expected at: !INNO_PATH!
    echo   Download from: https://jrsoftware.org/isdl.php
    echo   Or update INNO_PATH in this script
    echo.
    set SKIP_INNO=1
) else (
    echo Detected Inno Setup 6: Ready
    set SKIP_INNO=0
)
echo.

REM Check if we're in the repo directory
if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    echo This script must be run from the OctaveLights repository root
    pause
    exit /b 1
)

REM Step 1: Create virtual environment
if not exist "venv\" (
    echo [Step 1/4] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo   Virtual environment created: venv\
) else (
    echo [Step 1/4] Using existing virtual environment
)
echo.

REM Step 2: Activate virtual environment and install dependencies
echo [Step 2/4] Installing dependencies...
call venv\Scripts\activate.bat

pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    echo This may be due to network issues or an incompatible Python version
    pause
    exit /b 1
)
echo   Dependencies installed
echo.

REM Step 3: Build with PyInstaller
echo [Step 3/4] Building executable with PyInstaller...
pyinstaller octavelights.spec --clean
if errorlevel 1 (
    echo Error: PyInstaller build failed
    echo Check the console output above for details
    pause
    exit /b 1
)
echo   Executable built: dist\OctaveLights\OctaveLights.exe
echo.

REM Step 4: Build installer with Inno Setup (optional)
if %SKIP_INNO%==1 (
    echo [Step 4/4] Skipping Inno Setup (not installed)
    echo   Windows installer could not be created
    echo   To create the installer, install Inno Setup 6 from:
    echo   https://jrsoftware.org/isdl.php
    echo.
    echo   Then run: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
) else (
    echo [Step 4/4] Building Windows installer with Inno Setup...
    "!INNO_PATH!" installer.iss
    if errorlevel 1 (
        echo Error: Inno Setup build failed
        echo Check the console output above for details
        pause
        exit /b 1
    )
    echo   Installer created: dist\OctaveLightsSetup.exe
)
echo.

echo ================================================
echo   Build Complete!
echo ================================================
echo.

if %SKIP_INNO%==1 (
    echo Executable: dist\OctaveLights\OctaveLights.exe
    echo.
    echo To create the Windows installer:
    echo 1. Install Inno Setup 6 from https://jrsoftware.org/isdl.php
    echo 2. Run: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
) else (
    echo Installer: dist\OctaveLightsSetup.exe
    echo.
    echo Ready to install! You can now run OctaveLightsSetup.exe
    echo or distribute it to other Windows 10/11 machines
)
echo.

pause
