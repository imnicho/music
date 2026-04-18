# OctaveLights One-Click Setup and Build Script (PowerShell)
# Usage: .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "================================================"
Write-Host "   OctaveLights - One-Click Setup and Build"
Write-Host "================================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Detected Python: $pythonVersion"
} catch {
    Write-Host "Error: Python 3.11+ is required but not found in PATH"
    Write-Host "Please install Python from: https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Inno Setup is installed
$innoPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
$skipInno = $false

if (-not (Test-Path $innoPath)) {
    Write-Host "Warning: Inno Setup 6 not found"
    Write-Host "  Expected at: $innoPath"
    Write-Host "  Download from: https://jrsoftware.org/isdl.php"
    Write-Host "  Or update `$innoPath in this script"
    Write-Host ""
    $skipInno = $true
} else {
    Write-Host "Detected Inno Setup 6: Ready"
}

Write-Host ""

# Check if we're in the repo directory
if (-not (Test-Path "requirements.txt")) {
    Write-Host "Error: requirements.txt not found"
    Write-Host "This script must be run from the OctaveLights repository root"
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "[Step 1/4] Creating Python virtual environment..."
    & python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment"
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "  Virtual environment created: venv\"
} else {
    Write-Host "[Step 1/4] Using existing virtual environment"
}
Write-Host ""

# Step 2: Activate venv and install dependencies
Write-Host "[Step 2/4] Installing dependencies..."
& ".\venv\Scripts\Activate.ps1"

& python -m pip install --upgrade pip setuptools wheel | Out-Null
& pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies"
    Write-Host "This may be due to network issues or an incompatible Python version"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "  Dependencies installed"
Write-Host ""

# Step 3: Build with PyInstaller
Write-Host "[Step 3/4] Building executable with PyInstaller..."
& pyinstaller octavelights.spec --clean
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: PyInstaller build failed"
    Write-Host "Check the console output above for details"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "  Executable built: dist\OctaveLights\OctaveLights.exe"
Write-Host ""

# Step 4: Build installer with Inno Setup (optional)
if ($skipInno) {
    Write-Host "[Step 4/4] Skipping Inno Setup (not installed)"
    Write-Host "  Windows installer could not be created"
    Write-Host "  To create the installer, install Inno Setup 6 from:"
    Write-Host "  https://jrsoftware.org/isdl.php"
    Write-Host ""
    Write-Host "  Then run: & '$innoPath' installer.iss"
} else {
    Write-Host "[Step 4/4] Building Windows installer with Inno Setup..."
    & "$innoPath" installer.iss
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Inno Setup build failed"
        Write-Host "Check the console output above for details"
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "  Installer created: dist\OctaveLightsSetup.exe"
}
Write-Host ""

Write-Host "================================================"
Write-Host "   Build Complete!"
Write-Host "================================================"
Write-Host ""

if ($skipInno) {
    Write-Host "Executable: dist\OctaveLights\OctaveLights.exe"
    Write-Host ""
    Write-Host "To create the Windows installer:"
    Write-Host "1. Install Inno Setup 6 from https://jrsoftware.org/isdl.php"
    Write-Host "2. Run: & '$innoPath' installer.iss"
} else {
    Write-Host "Installer: dist\OctaveLightsSetup.exe"
    Write-Host ""
    Write-Host "Ready to install! You can now run OctaveLightsSetup.exe"
    Write-Host "or distribute it to other Windows 10/11 machines"
}
Write-Host ""

Read-Host "Press Enter to exit"
