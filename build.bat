@echo off
REM OctaveLights build script for Windows
REM Builds: pip install -> PyInstaller -> Inno Setup -> output OctaveLightsSetup.exe

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   OctaveLights Build Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Step 1: Install dependencies
echo [1/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)
echo.

REM Step 2: Build with PyInstaller
echo [2/3] Building with PyInstaller...
pyinstaller octavelights.spec --clean
if errorlevel 1 (
    echo Error: PyInstaller build failed
    exit /b 1
)
echo.

REM Step 3: Build installer with Inno Setup
echo [3/3] Building installer with Inno Setup...
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if not exist "!INNO_PATH!" (
    echo Error: Inno Setup 6 not found at "!INNO_PATH!"
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    exit /b 1
)

"!INNO_PATH!" installer.iss
if errorlevel 1 (
    echo Error: Inno Setup build failed
    exit /b 1
)
echo.

echo ========================================
echo   Build Complete
echo ========================================
echo Output: dist\OctaveLightsSetup.exe
echo.
pause
