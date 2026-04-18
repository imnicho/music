# OctaveLights

A standalone Windows desktop application that illuminates all octave-siblings of any key pressed on a Native Instruments Komplete Kontrol S61 MK1 keyboard.

## Features

- **Octave highlighting**: Press G4 → G1, G2, G3, G4, G5, G6 all light up on the keyboard
- **Customizable colors**: Choose from the MK1's supported color palette
- **Optional dual-color mode**: Highlight pressed key differently from siblings
- **Launch at startup**: Optional registry integration with Windows startup
- **Native Windows appearance**: No visible Python — looks and feels like a native C++ application

## System Requirements

- **OS**: Windows 10 or Windows 11 (x64)
- **Hardware**: Komplete Kontrol S61 MK1 (device ID `0x1360`, 61 keys)
- **Dependencies**: Included in installer (no separate Python installation needed for end users)

## Installation

### Option 1: Pre-Built Installer (Easiest)

1. Download `OctaveLightsSetup.exe` from [releases](https://github.com/imnicho/music/releases)
2. Run the installer
3. Follow the on-screen prompts
4. Choose to create a desktop shortcut and launch at startup (optional)
5. App installs to `Program Files\OctaveLights\`

### Option 2: Build from Source (One-Click)

If you want to build the installer yourself:

1. **Clone the repository**
   ```bash
   git clone https://github.com/imnicho/music.git
   cd music
   ```

2. **Run the one-click setup script** (choose one):
   - **Command Prompt:** Double-click `setup.bat`
   - **PowerShell:** Right-click `setup.ps1`, select "Run with PowerShell"

3. The script will automatically:
   - Create a Python virtual environment
   - Install all dependencies (no additional tools required—we use pre-compiled dependencies)
   - Build the executable with PyInstaller
   - Create the Windows installer with Inno Setup

4. Your installer is ready at `dist\OctaveLightsSetup.exe`

### Prerequisites for Building

- Windows 10 or 11
- Python 3.11 or 3.12 (download from [python.org](https://www.python.org/downloads/))
- [Inno Setup 6](https://jrsoftware.org/isdl.php)

### Important

**Close the Native Instruments Komplete Kontrol software before using OctaveLights.** Both applications cannot control the keyboard's lights simultaneously.

## Usage

1. Launch OctaveLights from the Start Menu or desktop shortcut
2. Click the **Enable** button to activate octave highlighting
3. Press any key on your Komplete Kontrol S61 — all octave-siblings light up
4. Release the key — lights extinguish
5. Adjust color and other settings in the Settings panel as desired

### Settings

- **Color**: Select which color to use for highlighted octaves
- **Highlight pressed key differently**: When enabled, the key you press uses a secondary color; siblings use the primary color
- **Launch on Windows startup**: When checked, OctaveLights will start automatically when you log in to Windows

## Development Setup

### Requirements

- Python 3.11 or 3.12
- Windows (development and testing must occur on Windows; cross-compilation is not supported)
- Komplete Kontrol S61 MK1 hardware for functional testing

### Initial Setup

```bash
# Clone the repository
git clone <repo-url>
cd music

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Development Commands

```bash
# Run the app directly (for development/debugging)
python main.py

# Run tests
python -m pytest

# Build PyInstaller executable (single-folder mode, no console window)
pyinstaller octavelights.spec --clean

# Build full installer (one-click setup)
.\setup.bat
# or with PowerShell:
.\setup.ps1
```

## Project Structure

```
music/
├── main.py                 # App entry point, single-instance enforcement
├── gui.py                  # PySide6 GUI: settings window, status display
├── octave_engine.py        # Core logic: pitch tracking, octave computation
├── midi_listener.py        # MIDI input handler
├── hid_driver.py           # USB HID communication with S61 MK1
├── config.py               # Settings persistence
├── logger.py               # Logging with rotation
├── version.py              # Single source for version string
├── version_info.txt        # Windows executable metadata
├── octavelights.spec       # PyInstaller spec file
├── installer.iss           # Inno Setup script
├── setup.bat               # Windows one-click setup and build script
├── setup.ps1               # PowerShell one-click setup and build script
├── requirements.txt        # Python dependencies
├── assets/
│   ├── app.ico             # Multi-resolution icon (16×16, 32×32, 48×48, 256×256)
│   ├── app-16.png
│   ├── app-32.png
│   ├── app-48.png
│   └── app-256.png
└── README.md               # This file
```

## Building the Installer

### Prerequisites

- Windows 10 or 11
- Python 3.11 or 3.12 installed and in PATH
- Inno Setup 6 installed at `C:\Program Files (x86)\Inno Setup 6\`
- Dependencies installed: `pip install -r requirements.txt`

### Build Steps

**Using batch script (recommended on Windows cmd.exe):**
```bash
build.bat
```

**Using PowerShell:**
```powershell
.\build.ps1
```

The build script will:
1. Install Python dependencies
2. Run PyInstaller to create `OctaveLights.exe` in single-folder mode
3. Run Inno Setup to create the installer
4. Output `OctaveLightsSetup.exe` to the `dist/` directory

Build time: ~2–3 minutes on typical hardware.

## Testing Checklist

Before releasing, verify:

- [ ] Fresh install on clean Windows VM — installer runs without errors
- [ ] App launches and finds the Komplete Kontrol S61 MK1
- [ ] Octave highlighting works: press G4 → G1–G6 light up, release → all lights off
- [ ] Task Manager shows `OctaveLights.exe`, not `python.exe`
- [ ] Right-click exe → Properties → Details shows all metadata correctly:
  - FileDescription: "OctaveLights"
  - ProductName: "OctaveLights"
  - CompanyName: "Nicho"
  - FileVersion: "1.0.0.0"
- [ ] Start Menu, taskbar, Add/Remove Programs, and window all show correct icon
- [ ] Color picker works: change color, see lights update
- [ ] "Highlight pressed key differently" toggle works
- [ ] NI Komplete Kontrol running → app shows conflict message with Retry button
- [ ] Close NI Komplete Kontrol, click Retry → app connects
- [ ] Hold G4, press G5, release G4 → G's stay lit (pitch-class reference counting)
- [ ] Close app → lights clear immediately, NI software can open device
- [ ] Launch at startup: enable, restart Windows, app launches automatically
- [ ] Uninstaller removes all files and registry entries
- [ ] Cold start from click to visible window: <2 seconds
- [ ] No console window flashes at any point during launch or operation

## Known Issues & Troubleshooting

### "Keyboard not found" message

**Problem**: App can't connect to the Komplete Kontrol S61 MK1.

**Solutions**:
- Check that the keyboard is powered on and connected via USB
- Close the Native Instruments Komplete Kontrol software (both control and listen to the same device)
- Unplug the keyboard, wait 5 seconds, plug it back in
- In Device Manager, right-click the keyboard and select "Update driver"
- Restart your computer

### "Conflict: close Komplete Kontrol software"

**Problem**: Native Instruments Komplete Kontrol is running and holding the HID device.

**Solution**: Close the Komplete Kontrol app, then click the **Retry** button in OctaveLights.

### Windows Defender / SmartScreen warning on first launch

**Problem**: Installer or executable is flagged as unsigned by Windows Defender or SmartScreen.

**Explanation**: OctaveLights is unsigned. This is expected and safe. PyInstaller-built executables can occasionally trigger false positives.

**Solution**: 
1. Click "More info" on the SmartScreen dialog
2. Click "Run anyway"
3. The warning will not appear again after the first launch

If you want to avoid this warning, code signing is possible but requires a certificate and is outside the scope of v1.

### Lights stay on after crash

**Problem**: App crashes while holding keys, and the lights don't turn off.

**Explanation**: Windows holds the USB HID device open, so NI's Komplete Kontrol software must be restarted or the keyboard must be replugged to reclaim the lights.

**Prevention**: Check logs at `%APPDATA%\OctaveLights\logs\app.log` for error details. Report to developer.

### Installer is very large (~60–100 MB)

**Expected behavior**: The installer includes the full Qt6 runtime, Python runtime, and all dependencies. This is typical for PyInstaller-based Windows apps.

**If size is a blocker**, an alternative packager (Nuitka, compiling to C) could reduce this to ~30–40 MB but would increase build time. This is out of scope for v1.

### Performance: Slow to start or UI lag

**Troubleshooting**:
- First launch is slower (~2–3 seconds) as Windows Defender scans the executable
- Subsequent launches should be <1 second
- Check logs for any errors: `%APPDATA%\OctaveLights\logs\app.log`
- Ensure antivirus is not aggressively scanning the app folder

## Architecture Overview

### Core Modules

**`hid_driver.py`**
- Opens S61 MK1 via USB HID (vendor ID `0x17cc`, product ID `0x1360`)
- Implements MK1 Light Guide protocol (reference: [SynthesiaKontrol](https://github.com/ojacques/SynthesiaKontrol))
- All HID I/O serialized through a single worker thread (thread-safe)
- Public methods: `set_keys_lit()`, `set_keys_with_colors()`, `clear_all()`, `close()`

**`midi_listener.py`**
- Listens for MIDI note-on/note-off events from the S61
- Uses `mido` + `python-rtmidi`
- Substring-matches port name ("Komplete Kontrol") to be robust across driver versions
- Emits Qt signals for GUI updates

**`octave_engine.py`**
- Maintains the set of currently-held pitches
- Computes octave-siblings and tracks reference counts (so releasing one G doesn't dark the G's if another G is held)
- On note-on: lights all pitches in 36–96 with same pitch class
- On note-off: decrements reference count

**`gui.py`** (PySide6)
- Main window with native Windows 11 theme
- Enable/Disable toggle
- Color picker and settings
- Status indicator (connected / not found / conflict)
- "Launch at startup" checkbox (writes to Windows registry)

**`main.py`**
- Single-instance enforcement via named mutex
- Global exception handler with user-facing error dialogs
- Graceful shutdown via Qt `aboutToQuit` signal

**`config.py`**
- Settings persistence to `%APPDATA%\OctaveLights\config.json`

**`logger.py`**
- Rotating file logger to `%APPDATA%\OctaveLights\logs\app.log`

## References

- [SynthesiaKontrol MK1 Protocol Reference](https://github.com/ojacques/SynthesiaKontrol)
- [hidapi Windows Binaries](https://github.com/libusb/hidapi/releases)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Inno Setup Documentation](https://jrsoftware.org/isinfo.php)

## License

See LICENSE file in repository.

## Support

For bugs, feature requests, or questions, open an issue on the project repository.
