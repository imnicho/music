@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

where python >nul 2>&1 || goto :no_python

if not exist "venv\Scripts\python.exe" (
    python -m venv venv || goto :err
)

"venv\Scripts\python.exe" -m pip install --upgrade pip || goto :err
"venv\Scripts\python.exe" -m pip install mido==1.3.2 python-rtmidi==1.5.8 hid==1.0.8 || goto :err

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$d='%~dp0'.TrimEnd('\'); ^
   $target = Join-Path $d 'venv\Scripts\pythonw.exe'; ^
   if (-not (Test-Path $target)) { $target = Join-Path $d 'venv\Scripts\python.exe' }; ^
   $ws = New-Object -ComObject WScript.Shell; ^
   $lnkPath = [IO.Path]::Combine([Environment]::GetFolderPath('Startup'),'OctaveLights.lnk'); ^
   $lnk = $ws.CreateShortcut($lnkPath); ^
   $lnk.TargetPath = $target; ^
   $lnk.Arguments = '\"' + (Join-Path $d 'octavelights.py') + '\"'; ^
   $lnk.WorkingDirectory = $d; ^
   $lnk.WindowStyle = 7; ^
   $lnk.Save()" || goto :err

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
