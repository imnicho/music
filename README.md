# OctaveLights

A tiny Windows background app that lights every octave-sibling key on a Native Instruments Komplete Kontrol S61 MK1 while you play.

## What it does

- Press any C — every C on the keyboard lights up.
- Release the key — the lights clear.
- Works for chords and overlapping presses (per-pitch refcount).

## Requirements

- Windows 10 or 11
- Python 3.11 or newer, installed with **Add Python to PATH**
- Native Instruments Komplete Kontrol **S61 MK1** (MK2 and MK3 are not supported)
- Native Instruments drivers installed (device must appear in Device Manager as HID)

## Install

1. `git clone https://github.com/imnicho/music && cd music`
2. Plug in the S61 MK1. Quit the Komplete Kontrol desktop app if it is running (it holds the HID interface).
3. Double-click `install.bat`. A venv is created, dependencies are installed, and a Startup shortcut is written so the daemon runs at every login.

## Uninstall

Double-click `uninstall.bat`. The Startup shortcut, running process, and local `venv` are removed. The log is preserved.

## How it works

MIDI input is read via `mido` / `python-rtmidi` from the keyboard's MIDI port. A pitch-class refcount tracks currently-held notes so overlapping presses of the same key do not turn the light off early. On every change, a full HID frame is sent to the keyboard setting each of the 61 keys to white or off.

## Logs

`%LOCALAPPDATA%\OctaveLights\octavelights.log` (rotating, 1 MB × 3)

## Known limits

- S61 MK1 only. Other MKx models use a different HID protocol and product ID.
- Monochrome white — no color configuration.
- No tray icon or GUI by design.
- Conflicts with the Komplete Kontrol desktop app — whichever opens the HID interface first wins.

## Troubleshooting

- **Nothing lights up.** Quit the Komplete Kontrol app and any DAW that might hold the keyboard, then re-launch (reboot is easiest).
- **No MIDI detected.** Check `mido.get_input_names()` output in the log — the port name must contain "komplete kontrol" (case-insensitive).
- **Crashes at startup.** Check the log. HID open failures usually mean another process owns the device.

## License

MIT
