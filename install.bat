@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

where python >nul 2>&1 || goto :no_python

if not exist "venv\Scripts\python.exe" (
    python -m venv venv || goto :err
)

"venv\Scripts\python.exe" -m pip install --upgrade pip || goto :err
"venv\Scripts\python.exe" -m pip install mido==1.3.2 python-rtmidi==1.5.8 hid==1.0.8 || goto :err

set "INSTALL_DIR=%~dp0"
if "!INSTALL_DIR:~-1!"=="\" set "INSTALL_DIR=!INSTALL_DIR:~0,-1!"

set "PS1=%TEMP%\octavelights_shortcut.ps1"
> "!PS1!" echo param([string]$InstallDir)
>>"!PS1!" echo $d = $InstallDir.TrimEnd('\')
>>"!PS1!" echo $target = Join-Path $d 'venv\Scripts\pythonw.exe'
>>"!PS1!" echo if (-not (Test-Path $target)) { $target = Join-Path $d 'venv\Scripts\python.exe' }
>>"!PS1!" echo $ws = New-Object -ComObject WScript.Shell
>>"!PS1!" echo $lnkPath = [IO.Path]::Combine([Environment]::GetFolderPath('Startup'),'OctaveLights.lnk')
>>"!PS1!" echo $lnk = $ws.CreateShortcut($lnkPath)
>>"!PS1!" echo $lnk.TargetPath = $target
>>"!PS1!" echo $lnk.Arguments = '"' + (Join-Path $d 'octavelights.py') + '"'
>>"!PS1!" echo $lnk.WorkingDirectory = $d
>>"!PS1!" echo $lnk.WindowStyle = 7
>>"!PS1!" echo $lnk.Save()

powershell -NoProfile -ExecutionPolicy Bypass -File "!PS1!" -InstallDir "!INSTALL_DIR!"

set "LNK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OctaveLights.lnk"
if not exist "!LNK!" (
    echo ERROR: Startup shortcut was not created.
    del "!PS1!" 2>nul
    goto :err
)
del "!PS1!" 2>nul

set "PID_FILE=%LOCALAPPDATA%\OctaveLights\octavelights.pid"
if exist "!PID_FILE!" (
    set /p OLDPID=<"!PID_FILE!"
    if defined OLDPID taskkill /F /PID !OLDPID! >nul 2>&1
) else (
    taskkill /F /IM pythonw.exe >nul 2>&1
)

if exist "venv\Scripts\pythonw.exe" (
    start "" "venv\Scripts\pythonw.exe" "%~dp0octavelights.py"
) else (
    echo WARNING: pythonw.exe not found, launching via python.exe minimized.
    start /min "" "venv\Scripts\python.exe" "%~dp0octavelights.py"
)

echo.
echo Installed. OctaveLights auto-starts at login.
echo Log: %LOCALAPPDATA%\OctaveLights\octavelights.log
echo.
popd
pause
exit /b 0

:no_python
echo Python not found on PATH.
echo Install Python 3.11+ from https://www.python.org/downloads/ and tick "Add to PATH".
popd
pause
exit /b 1

:err
echo.
echo FAILED. See output above.
popd
pause
exit /b 1
