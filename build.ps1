# OctaveLights build script for Windows (PowerShell)
# Builds: pip install -> PyInstaller -> Inno Setup -> output OctaveLightsSetup.exe

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================"
Write-Host "   OctaveLights Build Script"
Write-Host "========================================"
Write-Host ""

# Check if Python is available
try {
    python --version | Out-Null
} catch {
    Write-Error "Python is not installed or not in PATH"
    exit 1
}

# Step 1: Install dependencies
Write-Host "[1/3] Installing dependencies..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies"
    exit 1
}
Write-Host ""

# Step 2: Build with PyInstaller
Write-Host "[2/3] Building with PyInstaller..."
pyinstaller octavelights.spec --clean
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller build failed"
    exit 1
}
Write-Host ""

# Step 3: Build installer with Inno Setup
Write-Host "[3/3] Building installer with Inno Setup..."
$InnoPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if (-not (Test-Path $InnoPath)) {
    Write-Error "Inno Setup 6 not found at '$InnoPath'. Please install from: https://jrsoftware.org/isdl.php"
    exit 1
}

& $InnoPath installer.iss
if ($LASTEXITCODE -ne 0) {
    Write-Error "Inno Setup build failed"
    exit 1
}
Write-Host ""

Write-Host "========================================"
Write-Host "   Build Complete"
Write-Host "========================================"
Write-Host "Output: dist\OctaveLightsSetup.exe"
Write-Host ""
