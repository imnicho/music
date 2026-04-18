@echo off
setlocal enabledelayedexpansion
pushd "%~dp0"

set "LOG_FILE=%LOCALAPPDATA%\OctaveLights\octavelights.log"
set "PID_FILE=%LOCALAPPDATA%\OctaveLights\octavelights.pid"

if exist "!PID_FILE!" (
    set /p OLDPID=<"!PID_FILE!"
    if defined OLDPID taskkill /F /PID !OLDPID! >nul 2>&1
    del /F /Q "!PID_FILE!" >nul 2>&1
) else (
    taskkill /F /IM pythonw.exe >nul 2>&1
)

del /F /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OctaveLights.lnk" >nul 2>&1

if exist "%~dp0venv" rmdir /S /Q "%~dp0venv"

echo.
echo Uninstalled. Log preserved at:
echo   !LOG_FILE!
echo.
popd
pause
exit /b 0
